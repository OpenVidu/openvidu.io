# Testing, the export preprocessor, and `verify`

## Testing

```bash
pip install -e "./publish-tool[dev]"
cd publish-tool
pytest
ruff check . && ruff format --check .
```

The tests concentrate on the pure layer, with hand-written minimal fixtures rather than captured
pages: a real built page is ~100 KB of theme chrome, and the substitutions only ever look at a
few characters around a link.

Three of them are worth knowing about, because they are what keeps the rest honest:

- **The synthetic tree is derived from the configuration, not listed.**
  [`test_postprocess.py`](../tests/unit/test_postprocess.py) builds it from the real `ovweb.yaml`
  layout and materialises every redirect rule's target from the rules themselves, so a page or a
  rule added to the config is covered without touching the fixture.
- **A tree that has just been post-processed must `verify` clean**
  ([`test_verify.py`](../tests/unit/test_verify.py)). That makes `verify` a real post-publish signal:
  anything it reports right after a publish is something the pipeline failed to do.
- **The printed plan must match the steps that run.** `--dry-run` is only useful if it is the
  truth, so the pipeline is run against a recording reporter and compared to `plan.py`, in order.

## The export preprocessor

[`llmstxt_preprocess.py`](../llmstxt_preprocess.py) replaces the `mkdocs-llmstxt` plugin's own
`autoclean`, which `mkdocs.yml` turns off. It has to be a replacement rather than an addition,
because the plugin runs `autoclean` **before** the `preprocess` hook and `autoclean` deletes every
`twemoji` and the tab label bar — so by the time a hook sees the page, the comparison-table icons
and the tab labels are already gone.

Everything `autoclean` did is reimplemented, and the things below deliberately differ. They serve
one reader, an assistant that cannot see the page: what it gets must read as the page does, and
nothing it cannot use may pass for prose.

| Deviation | Why |
| --- | --- |
| A comparison-table icon becomes `Yes` / `No` / `In progress`, and the product logos heading the table become their `alt` text | The markup already says which — `class="twemoji compare-table-icon-yes"` — so the table exports as data with no change to the content. Every other image is removed as `autoclean` does: the site's alt texts are caption-length labels, which on a line of their own read as sentences of the page. |
| A link whose only content is an image or video is dropped whole; one with words of its own keeps them and its URL | `autoclean` removes an `<a>` around an `<img>` but not around a `<video>`, so markdownify writes an empty link — and it drops a link with real text in it along with the image. |
| Tab labels are kept, as a bold line before each tab's block | Without them a tabbed block is a run of code blocks with nothing saying which is Linux, Windows or macOS — silently ambiguous rather than visibly missing. |
| A code block keeps its linked filename | Pygments 2.20.0 escapes the `<a>` our fences put in `title=`, so the export would print raw HTML; `pygments_fence_title_hook.py` does the same for the page's HTML. A line-numbered block's filename header is kept too, where `autoclean` drops it with the numbers. |
| An admonition or a collapsible block becomes a blockquote, its title a bold first line | As plain paragraphs the title reads as a stray word and nothing marks where the callout ends and the page resumes — and 3.8 has 668 of them. |

Two layers of checking, because "identical to `autoclean` except on purpose" is the whole promise:

- [`tests/unit/test_llmstxt_preprocess.py`](../tests/unit/test_llmstxt_preprocess.py) runs the module
  and the plugin's real `autoclean` over the same markup and requires **byte-identical** output for
  every rule that is not a deviation, individually and all at once.
- A **differential build** proves it over the real site. Build once as configured, once with
  `autoclean: true` and the `preprocess` line removed, then diff the exports: every difference must
  be one of those above.

  ```bash
  mkdocs build --strict -d /tmp/withhook
  # then flip autoclean to true, drop the preprocess line, and:
  mkdocs build --strict -d /tmp/baseline
  diff -r /tmp/baseline /tmp/withhook
  ```

  Run this after a plugin upgrade, or after changing any rule in the module.

## `verify`

`ovweb verify` asserts the invariants of a published tree: every version folder has a redirect at
its root with a relative target, no promoted page claims a versioned URL as its own, every version
folder carries a correctly pruned and stub-synced sitemap, every search location is absolute,
nothing served from the root pins the version `latest` points at, no versioned export links to a
root-served page under its version, no export links to another export that does not exist, every
`<lastmod>` in the root sitemap is a real date that is not in the future, the root sitemap lists
no URL a redirect stub serves, the unversioned mirror and every alias folder are exactly the sets
their rules generate, no generated redirect points at a page that does not exist or at another
redirect, and `versions.json` agrees with the folders on disk.

The redirect-target check earns its place: a redirect into a 404 costs the visitor a second hop to
reach nothing and tells a crawler the content moved somewhere it did not. The chain half matters
because the expansions collapse chains at generation time, so one surviving to a published tree
means a `files` rule was pointed at another rule's stub.

The sitemap check is the one worth understanding, because it guards a feature that fails silently.
It asserts five things about `<X.Y>/sitemap.xml` — that it exists, that it has the version-root
entry, that it lists no root-served page, that it lists every generated redirect in the folder,
and that it lists no URL nothing serves — each of which degrades the version selector's
"keep the reader on the same page" behaviour on its own.
[sitemaps-and-search.md](sitemaps-and-search.md) explains why. A publish only fixes its own
version, so findings for the others are the to-do list; the fix for an unlisted stub is
`ovweb redirects apply`, which the finding names.
