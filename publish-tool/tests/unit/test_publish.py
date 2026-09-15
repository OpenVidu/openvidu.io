"""The publish state machine against fakes: what a failure leaves behind, and what a delete needs.

`publish()` is driven end to end with a recording stand-in for `Git` and `Mike`; the
post-processing and the published-versions lookup are stubbed, so these tests cover the branch
bookkeeping and the rollback paths, which no other test reaches.
"""

from __future__ import annotations

import importlib
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace
from typing import ClassVar

import pytest

from ovweb.mikewrap import MikeError
from ovweb.model import PublishPlan
from ovweb.pipeline.publish import PublishError, publish
from ovweb.report import Reporter

# The package re-exports the `publish` function under the module's name, so the module itself
# has to come from the import system.
publish_module = importlib.import_module("ovweb.pipeline.publish")


class FakeGit:
    dry_run = False
    remote = "origin"

    def __init__(self, *, remote_branches=("gh-pages",), held=None):
        self.root = Path("/repo")
        self.remote_branches = set(remote_branches)
        self.current = "main"
        self.branches = {"main": "aaa", "gh-pages": "bbb", **dict.fromkeys(remote_branches, "bbb")}
        self.held = held or {}
        self.calls: list[tuple[str, ...]] = []

    # -- reads
    def current_branch(self):
        return self.current

    def status_porcelain(self):
        return ""

    def remote_branch_exists(self, branch):
        return branch in self.remote_branches

    def branch_sha(self, branch):
        return self.branches.get(branch)

    def worktree_holding(self, branch):
        return self.held.get(branch)

    # -- writes, all recorded
    def do(self, *args, cwd=None):
        self.calls.append(args)

    def set_branch(self, branch, sha):
        self.calls.append(("set-branch", branch, sha))
        self.branches[branch] = sha

    def delete_local_branch(self, branch):
        self.calls.append(("delete-branch", branch))
        self.branches.pop(branch, None)

    def prune_worktrees(self):
        self.calls.append(("worktree-prune",))

    def switch(self, branch):
        self.calls.append(("switch", branch))
        self.current = branch

    def create_branch(self, branch):
        self.calls.append(("create-branch", branch))
        self.branches[branch] = self.branches[self.current]
        self.current = branch

    @contextmanager
    def worktree(self, branch, *, keep=False):
        yield Path("/tmp/fake-worktree")

    def add_all(self, *, cwd):
        self.calls.append(("add-all",))

    def commit(self, message, *, cwd):
        self.calls.append(("commit", message))
        self.branches["gh-pages"] = "ccc"
        return True

    def push(self, branch, *, set_upstream=False, cwd=None):
        self.calls.append(("push", branch))

    def push_force_with_lease(self, branch, *, cwd=None):
        self.calls.append(("push-force", branch))

    def rebase(self, onto, *, cwd=None):
        self.calls.append(("rebase", onto))

    def pull_ff_only(self, branch, *, cwd=None):
        self.calls.append(("pull", branch))


class FakeMike:
    fail_on: ClassVar[set[str]] = set()
    calls: ClassVar[list[tuple]] = []

    def __init__(self, root, *, dry_run=False, log=None):
        pass

    @staticmethod
    def is_available():
        return True

    @staticmethod
    def require():
        return None

    def delete(self, version):
        FakeMike.calls.append(("delete", version))
        if "delete" in FakeMike.fail_on:
            raise MikeError("mike delete failed")

    def deploy(self, version, *, alias=None):
        FakeMike.calls.append(("deploy", version, alias))
        if "deploy" in FakeMike.fail_on:
            raise MikeError("mike deploy failed")


@pytest.fixture
def harness(monkeypatch, config):
    """Wire the fakes in and hand back a way to run a publish."""
    state = SimpleNamespace(published=[], mike_fails=set())
    monkeypatch.setattr(FakeMike, "calls", [])
    monkeypatch.setattr(FakeMike, "fail_on", state.mike_fails)
    monkeypatch.setattr(publish_module, "Mike", FakeMike)
    monkeypatch.setattr(
        publish_module, "postprocess", lambda tree, **kwargs: SimpleNamespace(warnings=[])
    )
    monkeypatch.setattr(
        publish_module, "published_versions", lambda repo, gh_branch="gh-pages": state.published
    )

    def run(repo, plan):
        publish(repo=repo, config=config, plan=plan, report=Reporter(color=False))

    state.run = run
    return state


def new_plan(version="3.9", **overrides):
    fields = {
        "version": version,
        "update_latest": True,
        "source_branch": "main",
        "delete_first": False,
        "create_branch": True,
        "sync_branch": False,
        "push": True,
    }
    fields.update(overrides)
    return PublishPlan(**fields)


def test_a_failed_new_publish_deletes_the_branch_it_created(harness):
    harness.mike_fails.add("deploy")
    repo = FakeGit()

    with pytest.raises(MikeError):
        harness.run(repo, new_plan())

    assert ("create-branch", "3.9") in repo.calls
    assert ("delete-branch", "3.9") in repo.calls, "the retry must be able to create it again"
    assert ("set-branch", "gh-pages", "bbb") in repo.calls, "gh-pages is rolled back"
    assert repo.current == "main"
    assert ("push", "3.9") not in repo.calls


def test_a_successful_new_publish_pushes_the_branch_it_created(harness):
    repo = FakeGit()

    harness.run(repo, new_plan())

    assert ("push", "gh-pages") in repo.calls
    assert ("push", "3.9") in repo.calls
    assert ("delete-branch", "3.9") not in repo.calls


def test_delete_runs_only_when_the_version_is_published(harness):
    plan = new_plan("3.8", create_branch=False, delete_first=True)

    harness.published = []
    harness.run(FakeGit(remote_branches=("gh-pages", "3.8")), plan)
    assert [call for call in FakeMike.calls if call[0] == "delete"] == []

    harness.published = ["3.8"]
    FakeMike.calls.clear()
    harness.run(FakeGit(remote_branches=("gh-pages", "3.8")), plan)
    assert FakeMike.calls[0] == ("delete", "3.8")
    assert FakeMike.calls[1][0] == "deploy"


def test_a_failed_delete_stops_the_publish_before_deploying(harness):
    harness.published = ["3.8"]
    harness.mike_fails.add("delete")
    repo = FakeGit(remote_branches=("gh-pages", "3.8"))

    with pytest.raises(MikeError):
        harness.run(repo, new_plan("3.8", create_branch=False, delete_first=True))

    assert [call[0] for call in FakeMike.calls] == ["delete"]
    assert ("push", "gh-pages") not in repo.calls


def test_a_branch_held_by_another_worktree_is_refused_with_its_path(harness):
    kept = Path("/tmp/ovweb-gh-pages-kept")
    repo = FakeGit(held={"gh-pages": kept})

    with pytest.raises(PublishError, match=str(kept)):
        harness.run(repo, new_plan())

    assert FakeMike.calls == []
    assert ("create-branch", "3.9") not in repo.calls
