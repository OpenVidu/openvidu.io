"""The pin-agreement check: every place naming a build input must name the same version."""

from __future__ import annotations

from ovweb.doctor import PINNED_DISTRIBUTIONS, check_pins

PYPROJECT = """
build = [
    "mike==2.2.0",
    "mkdocs==1.6.1",
    "pymdown-extensions==11.0.1",
    "mkdocs-material[imaging]==9.7.6",
    "pygments==2.19.2",
    "mkdocs-glightbox==0.5.2",
    "mkdocs-llmstxt==0.5.0",
    "mkdocs-rss-plugin==1.19.0",
    "gitpython==3.1.59",
]
validate = [
    "mkdocs==1.6.1",
    "pymdown-extensions==11.0.1",
    "mkdocs-material==9.7.6",
    "pygments==2.19.2",
    "mkdocs-glightbox==0.5.2",
    "mkdocs-llmstxt==0.5.0",
    "mkdocs-rss-plugin==1.19.0",
    "gitpython==3.1.59",
]
"""

DOCKERFILE = (
    "FROM squidfunk/mkdocs-material:9.7.6\n"
    "RUN pip install mkdocs==1.6.1 pymdown-extensions==11.0.1 "
    "mkdocs-glightbox==0.5.2 mkdocs-llmstxt==0.5.0 "
    "mkdocs-rss-plugin==1.19.0 pygments==2.19.2 gitpython==3.1.59\n"
)


def write_repo(root, *, pyproject=PYPROJECT, dockerfile=DOCKERFILE, mike_dockerfile=None):
    (root / "publish-tool").mkdir()
    (root / "publish-tool" / "pyproject.toml").write_text(pyproject, encoding="utf-8")
    (root / "Dockerfile").write_text(dockerfile, encoding="utf-8")
    if mike_dockerfile is None:
        mike_dockerfile = dockerfile + "RUN pip install mike==2.2.0\n"
    (root / "Dockerfile.mike").write_text(mike_dockerfile, encoding="utf-8")


#: Deterministic stand-in for the running environment, matching the fixture's declared pins.
#: The real lookup would make the tests depend on whatever this environment has installed.
INSTALLED = {
    "mkdocs": "1.6.1",
    "pymdown-extensions": "11.0.1",
    "mkdocs-material": "9.7.6",
    "mike": "2.2.0",
    "mkdocs-glightbox": "0.5.2",
    "mkdocs-llmstxt": "0.5.0",
    "mkdocs-rss-plugin": "1.19.0",
    "pygments": "2.19.2",
    "gitpython": "3.1.59",
}


def pins_of(root, installed=INSTALLED):
    return check_pins(root, installed_version=installed.get)


def by_distribution(checks):
    return {check.detail.split(" ")[0]: check for check in checks}


def test_agreeing_pins_pass_for_every_distribution(tmp_path):
    write_repo(tmp_path)

    checks = pins_of(tmp_path)

    assert len(checks) == len(PINNED_DISTRIBUTIONS)
    assert [check.detail for check in checks if not check.ok] == []


def test_a_drifted_installed_distribution_fails(tmp_path):
    write_repo(tmp_path)

    result = by_distribution(pins_of(tmp_path, {**INSTALLED, "pygments": "2.21.0"}))

    assert not result["pygments"].ok
    assert "installed=2.21.0" in result["pygments"].detail


def test_a_drifted_dockerfile_pin_fails_that_distribution_only(tmp_path):
    drifted = DOCKERFILE.replace("mkdocs-glightbox==0.5.2", "mkdocs-glightbox==0.6.0")
    write_repo(tmp_path, dockerfile=drifted)

    result = by_distribution(pins_of(tmp_path))

    assert not result["mkdocs-glightbox"].ok
    assert "disagree" in result["mkdocs-glightbox"].detail
    assert result["mkdocs-llmstxt"].ok


def test_a_drifted_base_image_tag_fails_mkdocs_material(tmp_path):
    write_repo(tmp_path, dockerfile=DOCKERFILE.replace(":9.7.6", ":9.9.9"))

    result = by_distribution(pins_of(tmp_path))

    assert not result["mkdocs-material"].ok


def test_pyproject_disagreeing_with_itself_fails(tmp_path):
    write_repo(
        tmp_path,
        pyproject=PYPROJECT.replace('"pygments==2.19.2",', '"pygments==2.18.0",', 1),
    )

    result = by_distribution(pins_of(tmp_path))

    assert not result["pygments"].ok


def test_a_distribution_missing_from_pyproject_fails(tmp_path):
    write_repo(
        tmp_path,
        pyproject=PYPROJECT.replace("mike==2.2.0", "requests==1.0"),
        mike_dockerfile=DOCKERFILE,
    )

    result = by_distribution(pins_of(tmp_path))

    assert not result["mike"].ok
    assert "not pinned" in result["mike"].detail


def test_a_digest_pinned_base_image_still_names_its_tag(tmp_path):
    digest = "@sha256:" + "0" * 64
    write_repo(tmp_path, dockerfile=DOCKERFILE.replace(":9.7.6\n", f":9.7.6{digest}\n"))

    result = by_distribution(pins_of(tmp_path))

    assert result["mkdocs-material"].ok


def test_run_checks_outside_a_repository_is_fatal():
    from ovweb.doctor import run_checks

    checks = run_checks(repo=None, repo_root=None, pins_only=True)

    assert [check.ok for check in checks] == [False]
    assert checks[0].fatal
    assert "not inside a git repository" in checks[0].detail


def test_site_url_agreement_reads_mkdocs_yml_from_the_checkout(tmp_path, config):
    from ovweb.doctor import _check_site_url_agreement

    (tmp_path / "mkdocs.yml").write_text("site_url: https://example.invalid\n", encoding="utf-8")
    drifted = _check_site_url_agreement(config, repo_root=tmp_path)
    assert drifted is not None and not drifted.ok

    (tmp_path / "mkdocs.yml").write_text(f"site_url: {config.layout.site_url}\n", encoding="utf-8")
    agreeing = _check_site_url_agreement(config, repo_root=tmp_path)
    assert agreeing is not None and agreeing.ok

    missing = _check_site_url_agreement(config, repo_root=tmp_path / "elsewhere")
    assert missing is not None and not missing.ok
