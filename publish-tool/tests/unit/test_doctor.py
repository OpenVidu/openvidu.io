"""The pin-agreement check: every place naming a build input must name the same version."""

from __future__ import annotations

from ovweb.doctor import PINNED_DISTRIBUTIONS, check_pins

PYPROJECT = """
build = [
    "mike==2.2.0",
    "mkdocs-material[imaging]==9.7.6",
    "pygments==2.19.2",
    "mkdocs-glightbox==0.5.2",
    "mkdocs-llmstxt==0.5.0",
    "mkdocs-rss-plugin==1.19.0",
]
validate = [
    "mkdocs-material==9.7.6",
    "pygments==2.19.2",
    "mkdocs-glightbox==0.5.2",
    "mkdocs-llmstxt==0.5.0",
    "mkdocs-rss-plugin==1.19.0",
]
"""

DOCKERFILE = (
    "FROM squidfunk/mkdocs-material:9.7.6\n"
    "RUN pip install mkdocs-glightbox==0.5.2 mkdocs-llmstxt==0.5.0 "
    "mkdocs-rss-plugin==1.19.0 pygments==2.19.2\n"
)


def write_repo(root, *, pyproject=PYPROJECT, dockerfile=DOCKERFILE, mike_dockerfile=None):
    (root / "publish-tool").mkdir()
    (root / "publish-tool" / "pyproject.toml").write_text(pyproject, encoding="utf-8")
    (root / "Dockerfile").write_text(dockerfile, encoding="utf-8")
    if mike_dockerfile is None:
        mike_dockerfile = dockerfile + "RUN pip install mike==2.2.0\n"
    (root / "Dockerfile.mike").write_text(mike_dockerfile, encoding="utf-8")


def by_distribution(checks):
    return {check.detail.split(" ")[0]: check for check in checks}


def test_agreeing_pins_pass_for_every_distribution(tmp_path):
    write_repo(tmp_path)

    checks = check_pins(tmp_path)

    assert len(checks) == len(PINNED_DISTRIBUTIONS)
    # The installed environment may add its own version to each set; declared places agree, and
    # the installed versions come from the same pins, so everything must hold.
    failures = [check.detail for check in checks if not check.ok]
    assert failures == []


def test_a_drifted_dockerfile_pin_fails_that_distribution_only(tmp_path):
    drifted = DOCKERFILE.replace("mkdocs-glightbox==0.5.2", "mkdocs-glightbox==0.6.0")
    write_repo(tmp_path, dockerfile=drifted)

    result = by_distribution(check_pins(tmp_path))

    assert not result["mkdocs-glightbox"].ok
    assert "disagree" in result["mkdocs-glightbox"].detail
    assert result["mkdocs-llmstxt"].ok


def test_a_drifted_base_image_tag_fails_mkdocs_material(tmp_path):
    write_repo(tmp_path, dockerfile=DOCKERFILE.replace(":9.7.6", ":9.9.9"))

    result = by_distribution(check_pins(tmp_path))

    assert not result["mkdocs-material"].ok


def test_pyproject_disagreeing_with_itself_fails(tmp_path):
    write_repo(
        tmp_path,
        pyproject=PYPROJECT.replace('"pygments==2.19.2",', '"pygments==2.18.0",', 1),
    )

    result = by_distribution(check_pins(tmp_path))

    assert not result["pygments"].ok


def test_a_distribution_missing_from_pyproject_fails(tmp_path):
    write_repo(
        tmp_path,
        pyproject=PYPROJECT.replace("mike==2.2.0", "requests==1.0"),
        mike_dockerfile=DOCKERFILE,
    )

    result = by_distribution(check_pins(tmp_path))

    assert not result["mike"].ok
    assert "not pinned" in result["mike"].detail
