"""The command line surface.

Mostly one thing: the global options may be written after the subcommand. click does not allow
that — a group's options must precede the command — and the publish workflow broke on
`ovweb publish latest 3.8 --verbose` the first time it ran. `hoist_global_options` rewrites argv
instead of failing, and the tests below keep that rewriting honest by checking it against the
real app rather than against a hardcoded list.
"""

from __future__ import annotations

import pytest
from typer.main import get_command

from ovweb.cli import GLOBAL_OPTIONS_WITH_VALUE, GLOBAL_SWITCHES, app, hoist_global_options


def _group():
    return get_command(app)


def _walk(command, path=()):
    """Yield `(path, click_command)` for every leaf command in the app."""
    subcommands = getattr(command, "commands", None)
    if not subcommands:
        yield path, command
        return
    for name, child in subcommands.items():
        yield from _walk(child, (*path, name))


def _option_names(command) -> set[str]:
    """Every spelling of every option, including the off switch of a boolean flag.

    A `--color/--no-color` pair is one click param: `--color` is in `opts` and `--no-color` in
    `secondary_opts`. Reading only `opts` would miss half the names, and so would miss a command
    shadowing one of them.
    """
    return {name for param in command.params for name in (*param.opts, *param.secondary_opts)}


# -- the invariant that makes the rewriting safe ------------------------------------------


def test_no_command_declares_a_global_option_name():
    """If a command ever declared `--verbose`, hoisting would steal it. Fail here instead."""
    reserved = GLOBAL_SWITCHES | GLOBAL_OPTIONS_WITH_VALUE
    for path, command in _walk(_group()):
        clash = _option_names(command) & reserved
        assert not clash, f"`ovweb {' '.join(path)}` declares global option(s) {sorted(clash)}"


def test_the_declared_globals_match_the_app():
    """Keeps the two frozensets from drifting away from the callback they describe."""
    declared = _option_names(_group()) - {"--help", "--version"}
    assert declared == GLOBAL_SWITCHES | GLOBAL_OPTIONS_WITH_VALUE


def test_value_taking_globals_are_classified_correctly():
    """A switch hoisted as if it took a value would swallow the next argument."""
    for param in _group().params:
        names = set(param.opts)
        if names & GLOBAL_OPTIONS_WITH_VALUE:
            assert not param.is_flag, f"{sorted(names)} is a flag but listed as taking a value"
        elif names & GLOBAL_SWITCHES:
            assert param.is_flag or param.count, f"{sorted(names)} takes a value but is a switch"


# -- the rewriting itself ----------------------------------------------------------------


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        # The exact invocation that broke the workflow.
        (
            ["--dry-run", "publish", "latest", "3.8", "--verbose"],
            ["--dry-run", "--verbose", "publish", "latest", "3.8"],
        ),
        (["publish", "latest", "3.8", "-v"], ["-v", "publish", "latest", "3.8"]),
        # Already in front: unchanged, so hoisting is idempotent.
        (
            ["--dry-run", "--verbose", "publish", "latest", "3.8"],
            ["--dry-run", "--verbose", "publish", "latest", "3.8"],
        ),
        # A value-taking option drags its value along.
        (
            ["publish", "past", "3.7", "--repo", "/tmp/x"],
            ["--repo", "/tmp/x", "publish", "past", "3.7"],
        ),
        (["publish", "past", "3.7", "--repo=/tmp/x"], ["--repo=/tmp/x", "publish", "past", "3.7"]),
        # Per-command options stay exactly where they are.
        (
            ["publish", "latest", "3.8", "--no-push", "--json"],
            ["--json", "publish", "latest", "3.8", "--no-push"],
        ),
        (
            ["postprocess", "3.8", "--tree", "/tmp/t", "--force", "-v"],
            ["-v", "postprocess", "3.8", "--tree", "/tmp/t", "--force"],
        ),
        # Nothing to do.
        (["verify"], ["verify"]),
        ([], []),
    ],
)
def test_hoisting(argv, expected):
    assert hoist_global_options(argv) == expected


def test_everything_after_a_double_dash_is_left_alone():
    """`--` ends option parsing, so a literal `--verbose` past it is data, not a flag."""
    argv = ["publish", "latest", "3.8", "--", "--verbose", "--repo", "x"]
    assert hoist_global_options(argv) == argv


def test_a_trailing_value_taking_option_does_not_run_off_the_end():
    assert hoist_global_options(["verify", "--repo"]) == ["--repo", "verify"]
