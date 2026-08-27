"""The rules behind each page's `<lastmod>`: git-log walking and snippet resolution.

All pure, so none of this needs a repository or a filesystem — `read` is injected. The end-to-end
check that the values actually reach the sitemap is in the README's verification steps; what is
pinned here is the arithmetic: newest-first wins, an include pushes a page's date forward, and no
shape of input makes the resolver loop or raise.
"""

from __future__ import annotations

from ovweb.sources import MARKER, newest_dates, parse_git_log, sources_of


def log(*commits: tuple[str, list[str]]) -> str:
    """`git log --format=@@%cs --name-only` output, newest commit first."""
    return "\n".join(f"{MARKER}{date}\n" + "\n".join(paths) + "\n" for date, paths in commits)


# -- parsing the log ---------------------------------------------------------------------


def test_the_most_recent_commit_touching_a_path_wins():
    text = log(
        ("2026-07-22", ["docs/pricing.md", "docs/support.md"]),
        ("2026-01-04", ["docs/pricing.md"]),
    )
    assert parse_git_log(text) == {"docs/pricing.md": "2026-07-22", "docs/support.md": "2026-07-22"}


def test_each_commit_claims_only_its_own_paths():
    text = log(("2026-07-22", ["a.md"]), ("2025-03-01", ["b.md"]))
    assert parse_git_log(text) == {"a.md": "2026-07-22", "b.md": "2025-03-01"}


def test_a_commit_that_touched_nothing_under_the_paths_is_harmless():
    """`git log -- docs shared` still prints the commit, with no file list under it."""
    text = f"{MARKER}2026-07-22\n\n{MARKER}2026-07-21\ndocs/a.md\n"
    assert parse_git_log(text) == {"docs/a.md": "2026-07-21"}


def test_paths_of_deleted_files_are_kept_and_simply_never_looked_up():
    text = log(("2026-07-22", ["docs/gone.md"]))
    assert parse_git_log(text) == {"docs/gone.md": "2026-07-22"}


def test_an_empty_log_is_an_empty_map():
    assert parse_git_log("") == {}


def test_a_path_before_any_date_is_ignored():
    """Defensive: without a date there is nothing to record, and guessing would be worse."""
    assert parse_git_log("docs/orphan.md\n") == {}


# -- resolving what a page is made of ----------------------------------------------------


def reader(files: dict[str, str]):
    return lambda path: files.get(path)


def test_a_page_with_no_includes_is_its_own_only_source():
    assert sources_of("docs/a.md", reader({"docs/a.md": "# Title"})) == {"docs/a.md"}


def test_an_include_is_followed():
    files = {"docs/a.md": '--8<-- "x.md"', "shared/x.md": "text"}
    assert sources_of("docs/a.md", reader(files)) == {"docs/a.md", "shared/x.md"}


def test_includes_are_followed_to_any_depth():
    files = {
        "docs/a.md": '--8<-- "x.md"',
        "shared/x.md": '--8<-- "y.md"',
        "shared/y.md": '--8<-- "z.md"',
        "shared/z.md": "text",
    }
    assert sources_of("docs/a.md", reader(files)) == {
        "docs/a.md",
        "shared/x.md",
        "shared/y.md",
        "shared/z.md",
    }


def test_an_indented_include_counts():
    """Many of them sit inside admonitions, so the marker is not at column zero."""
    files = {"docs/a.md": '!!! note\n    --8<-- "x.md"\n', "shared/x.md": "t"}
    assert sources_of("docs/a.md", reader(files)) == {"docs/a.md", "shared/x.md"}


def test_a_missing_include_is_not_an_error():
    """`shared/README.md` documents the syntax with a placeholder path inside a code fence."""
    files = {"docs/a.md": '--8<-- "<folder>/<snippet>.md"'}
    assert sources_of("docs/a.md", reader(files)) == {"docs/a.md", "shared/<folder>/<snippet>.md"}


def test_a_snippet_included_twice_is_visited_once():
    files = {
        "docs/a.md": '--8<-- "x.md"\n--8<-- "y.md"',
        "shared/x.md": '--8<-- "shared.md"',
        "shared/y.md": '--8<-- "shared.md"',
        "shared/shared.md": "t",
    }
    assert sources_of("docs/a.md", reader(files)) == {
        "docs/a.md",
        "shared/x.md",
        "shared/y.md",
        "shared/shared.md",
    }


def test_a_cycle_terminates():
    files = {"shared/a.md": '--8<-- "b.md"', "shared/b.md": '--8<-- "a.md"'}
    assert sources_of("shared/a.md", reader(files)) == {"shared/a.md", "shared/b.md"}


def test_a_snippet_that_includes_itself_terminates():
    assert sources_of("shared/a.md", reader({"shared/a.md": '--8<-- "a.md"'})) == {"shared/a.md"}


# -- choosing the date to publish --------------------------------------------------------


def test_a_page_without_includes_takes_its_own_date():
    dates = {"docs/a.md": "2026-01-05"}
    assert newest_dates(["docs/a.md"], dates=dates, read=reader({})) == {"docs/a.md": "2026-01-05"}


def test_a_newer_snippet_moves_the_page_forward():
    """The reason this module exists: one shared snippet is shown by up to 34 pages."""
    files = {"docs/install.md": '--8<-- "version.md"', "shared/version.md": "3.8.0"}
    dates = {"docs/install.md": "2026-06-25", "shared/version.md": "2026-07-22"}
    assert newest_dates(["docs/install.md"], dates=dates, read=reader(files)) == {
        "docs/install.md": "2026-07-22"
    }


def test_an_older_snippet_does_not_drag_the_page_back():
    files = {"docs/install.md": '--8<-- "version.md"', "shared/version.md": "3.8.0"}
    dates = {"docs/install.md": "2026-07-22", "shared/version.md": "2026-01-01"}
    resolved = newest_dates(["docs/install.md"], dates=dates, read=reader(files))
    assert resolved == {"docs/install.md": "2026-07-22"}


def test_a_page_git_has_never_seen_can_still_be_dated_by_its_snippet():
    files = {"docs/new.md": '--8<-- "x.md"', "shared/x.md": "t"}
    dates = {"shared/x.md": "2026-07-22"}
    assert newest_dates(["docs/new.md"], dates=dates, read=reader(files)) == {
        "docs/new.md": "2026-07-22"
    }


def test_a_page_with_nothing_dated_is_left_out_rather_than_invented():
    """The caller omits `<lastmod>` for it; the spec makes the field optional per URL."""
    assert newest_dates(["docs/untracked.md"], dates={}, read=reader({})) == {}


def test_each_file_is_read_once_however_many_pages_include_it():
    files = {
        "docs/a.md": '--8<-- "x.md"',
        "docs/b.md": '--8<-- "x.md"',
        "shared/x.md": "t",
    }
    reads: list[str] = []

    def counting(path: str) -> str | None:
        reads.append(path)
        return files.get(path)

    newest_dates(["docs/a.md", "docs/b.md"], dates={"shared/x.md": "2026-07-22"}, read=counting)
    assert sorted(reads) == ["docs/a.md", "docs/b.md", "shared/x.md"]
