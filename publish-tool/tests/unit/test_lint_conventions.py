"""The lint SEO and page-composition checks."""

from __future__ import annotations

from ovweb.lint import run_lint
from ovweb.model import SiteLayout

LAYOUT = SiteLayout(
    site_url="https://openvidu.io",
    versioned_pages=("docs", "meet"),
    non_versioned_pages=("pricing", "blog"),
    assets=("assets", "javascripts", "stylesheets", "search"),
    pinned_assets=("assets",),
    root_files=("index.html",),
    feeds=(),
)


def write(root, relpath, text=""):
    path = root / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def findings_of(root, check):
    return [f for f in run_lint(root, layout=LAYOUT) if f.check == check]


def page(title="A page", description="A fine description of the page."):
    return f'---\ntitle: "{title}"\ndescription: "{description}"\n---\nBody.\n'


# -- SEO fields ------------------------------------------------------------------------------


def test_a_long_docs_title_warns_but_a_blog_title_gets_more_room(tmp_path):
    long_title = "A title that runs well past the fifty-seven character budget"
    write(tmp_path, "docs/docs/guide.md", page(title=long_title))
    write(tmp_path, "docs/blog/posts/2026/08/post.md", page(title=long_title))

    (finding,) = findings_of(tmp_path, "title-length")
    assert finding.file == "docs/docs/guide.md"
    assert finding.severity == "warn"


def test_a_description_without_a_full_stop_warns(tmp_path):
    write(tmp_path, "docs/docs/guide.md", page(description="No stop at the end"))

    (finding,) = findings_of(tmp_path, "description-format")
    assert finding.severity == "warn"


def test_an_overlong_description_warns(tmp_path):
    write(tmp_path, "docs/docs/guide.md", page(description="x" * 170 + "."))

    (finding,) = findings_of(tmp_path, "description-length")
    assert finding.severity == "warn"


def test_duplicate_titles_warn_on_every_holder(tmp_path):
    write(tmp_path, "docs/a.md", page(title="Same", description="One description here."))
    write(tmp_path, "docs/b.md", page(title="Same", description="Another description here."))

    findings = findings_of(tmp_path, "duplicate-title")
    assert sorted(finding.file for finding in findings) == ["docs/a.md", "docs/b.md"]


def test_unique_fields_stay_silent(tmp_path):
    write(tmp_path, "docs/a.md", page(title="One", description="First description here."))
    write(tmp_path, "docs/b.md", page(title="Two", description="Second description here."))

    assert findings_of(tmp_path, "duplicate-title") == []
    assert findings_of(tmp_path, "duplicate-description") == []


# -- admonitions -----------------------------------------------------------------------------


def test_an_admonition_without_a_space_is_an_error(tmp_path):
    write(tmp_path, "docs/guide.md", '!!!warning "Careful"\n    Body.\n')

    (finding,) = findings_of(tmp_path, "admonition-spacing")
    assert finding.severity == "error"
    assert finding.line == 1


def test_wellformed_admonitions_are_silent(tmp_path):
    write(tmp_path, "docs/guide.md", '!!! warning "Careful"\n    Body.\n\n??? details\n    x\n')

    assert findings_of(tmp_path, "admonition-spacing") == []


def test_a_collapsed_admonition_without_a_space_is_an_error(tmp_path):
    write(tmp_path, "docs/guide.md", "???details\n    Body.\n")

    (finding,) = findings_of(tmp_path, "admonition-spacing")
    assert finding.severity == "error"


# -- the tags contract -----------------------------------------------------------------------


def test_glightbox_html_pulled_in_by_a_snippet_needs_the_tag_on_the_page(tmp_path):
    write(tmp_path, "shared/tutorials/gallery.md", '<a class="glightbox" href="/x.png">i</a>')
    write(tmp_path, "docs/docs/tutorial.md", '--8<-- "shared/tutorials/gallery.md"\n')

    (finding,) = findings_of(tmp_path, "tag-contract")
    assert finding.file == "docs/docs/tutorial.md"
    assert "setupcustomgallery" in finding.message
    assert finding.severity == "error"


def test_the_tag_on_the_page_satisfies_the_contract(tmp_path):
    write(tmp_path, "shared/tutorials/gallery.md", '<a class="glightbox" href="/x.png">i</a>')
    write(
        tmp_path,
        "docs/docs/tutorial.md",
        '---\ntags:\n  - setupcustomgallery\n---\n--8<-- "shared/tutorials/gallery.md"\n',
    )

    assert findings_of(tmp_path, "tag-contract") == []


def test_feature_cards_need_setupcardglow(tmp_path):
    cards = '<div class="feature-cards"><div class="grid cards"></div></div>'
    write(tmp_path, "docs/index.md", cards)

    (finding,) = findings_of(tmp_path, "tag-contract")
    assert "setupcardglow" in finding.message


def test_the_class_token_must_match_whole_not_substring(tmp_path):
    """`ov-meet-commercial-feature-cards` is a custom class, not the glow wrapper."""
    write(
        tmp_path,
        "docs/index.md",
        '<div class="cards no-border ov-meet-commercial-feature-cards">x</div>',
    )

    assert findings_of(tmp_path, "tag-contract") == []


def test_the_class_token_matches_among_other_classes(tmp_path):
    write(tmp_path, "docs/index.md", '<a class="dark-img glightbox" href="/x.png">i</a>')

    (finding,) = findings_of(tmp_path, "tag-contract")
    assert "setupcustomgallery" in finding.message


# -- assets ----------------------------------------------------------------------------------


def test_a_file_at_the_images_root_warns(tmp_path):
    write(tmp_path, "docs/assets/images/loose.png")
    write(tmp_path, "docs/assets/images/home/placed.png")

    (finding,) = findings_of(tmp_path, "asset-placement")
    assert finding.file == "docs/assets/images/loose.png"


def test_unpaired_theme_images_warn(tmp_path):
    write(
        tmp_path,
        "docs/docs/guide.md",
        "![a](../assets/a-light.png#only-light)\n![a](../assets/a-dark.png#only-dark)\n"
        "![b](../assets/b-light.png#only-light)\n",
    )

    (finding,) = findings_of(tmp_path, "light-dark-pair")
    assert "2 #only-light vs 1 #only-dark" in finding.message


def test_a_blog_post_referencing_another_posts_assets_warns(tmp_path):
    write(
        tmp_path,
        "docs/blog/posts/2026/08/mine.md",
        "![x](/assets/images/blog/2026/07/other-post/x.png)",
    )

    (finding,) = findings_of(tmp_path, "blog-asset-mirror")
    assert "2026/07/other-post" in finding.message


def test_a_blog_post_using_its_own_asset_folder_is_silent(tmp_path):
    write(
        tmp_path,
        "docs/blog/posts/2026/08/mine.md",
        "![x](/assets/images/blog/2026/08/mine/x.png)",
    )

    assert findings_of(tmp_path, "blog-asset-mirror") == []


# -- snippet naming --------------------------------------------------------------------------


def test_a_snippet_repeating_its_folder_name_warns(tmp_path):
    write(tmp_path, "shared/aws/aws-troubleshooting.md", "x")
    write(tmp_path, "shared/aws/troubleshooting.md", "x")

    (finding,) = findings_of(tmp_path, "snippet-name")
    assert finding.file == "shared/aws/aws-troubleshooting.md"
