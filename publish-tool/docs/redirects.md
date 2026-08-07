# Redirects

GitHub Pages has no server-side redirects, and it serves `404.html` with a **404 status** — the
thing a crawler acts on before it runs any JavaScript. So every redirect on this site is a real,
generated HTML page answering 200 with a zero-delay meta refresh, declared as data in
[`ovweb.yaml`](../ovweb.yaml). There is no client-side router.

Two families of rules exist, separated by what has to be written by hand:

- **`redirects.files`** — one rule, one page: a known path and where it goes.
- **`redirects.expand`** — one rule, many pages, enumerated from the published tree.

## `redirects.files` — a known path

A rule says where the page goes (`at`) and where it sends the visitor (`to`):

```yaml
- id: version-root
  at: version-root              # the named location for "<X.Y>/index.html"
  to: "docs/"
  canonical: "{site_url}/latest/docs/"
  body: "Redirecting to the OpenVidu Platform documentation…"
  when:
    # Versions 3.0–3.3 predate the /docs/ landing page: back then the getting started guide
    # *was* the Platform documentation index.
    - versions: "<3.4"
      to: "docs/getting-started/"
      body: "Redirecting to the OpenVidu getting started guide…"
```

`to` may carry a fragment (`../how-to-guides/#backup-and-restore`), which is how several pages
converging into one land on the section that absorbed them. The `canonical` should not repeat
the fragment: search engines normalise it away.

`versions` (and `when[].versions`) are [PEP 440](https://peps.python.org/pep-0440/) specifiers
evaluated with `packaging`, so `3.10` correctly sorts above `3.9` and legacy folders like
`3.0.0-beta1` fall in the range written for them. **At most one `when` entry may match a given
version** — an overlap is an error, not a silent first-match-wins, because that would make the
published redirect depend on the order of the file.

**A rule's `versions` gate must not be wider than its target's.** Gate a rule at the first version
that stopped shipping the old page, then check that the *successor* exists in every version from
there on — those are not always the same release. When they differ, the older band needs a `when`
override pointing at a page that version really has; without one the stub redirects into a 404,
which is worse than the 404 it replaced. `ovweb verify` rejects that — see the redirect-target
check in [testing-and-verify.md](testing-and-verify.md).

**Not every dead URL earns a redirect.** A page that was never part of a release should not have
its URL preserved, and neither should a generated API page for a class that has been deleted. The
exclusions are pinned in [`test_redirects.py`](../tests/unit/test_redirects.py) as
`DELIBERATELY_UNCOVERED`, which fails both ways — if a listed URL gains a rule, and if an
unlisted dead URL loses one.

## `redirects.expand` — one rule, many pages

Every kind enumerates its pages from the **published tree** rather than from a list, under three
filters that make a bulk expansion safe to materialise as files:

- **Never shadow a real page.** A candidate path already holding a page ovweb did not generate is
  skipped, so an expansion cannot overwrite content — `ha/on-premises/` survives the
  provider-index rule with no exclusion list to maintain.
- **Never redirect into a 404.** A candidate whose target does not exist in that tree is skipped.
- **Never chain.** A target that is itself a generated redirect is followed to its final
  destination, so every stub answers in one hop.

Five kinds ship:

**`kind: cross-product`** — many single-page moves that differ only by path segments. `at`, `to`,
`canonical` and `body` may use `{version}` and any `values` key; one candidate per combination:

```yaml
- id: removed-provider-index
  kind: cross-product
  at: "{version}/docs/self-hosting/{edition}/{provider}/index.html"
  to: "install/"
  canonical: "{site_url}/latest/docs/self-hosting/{edition}/{provider}/install/"
  versions: ">=3.8"           # the release the consolidation belongs to
  values:
    edition:  [single-node, single-node-pro, elastic, ha]
    provider: [on-premises, aws, azure, gcp, digitalocean, oracle]
```

Gate it at the release the change belongs to — the filters keep the rule honest *inside* the
gate, they do not replace it.

**`kind: tree-rename`** — a directory moved. The pages are enumerated from the tree under `to`,
so every stub has a live target by construction; a page removed in the same release as the rename
gets no stub and needs its own `files` rule, which is right — its successor is a judgement call,
not a path substitution:

```yaml
- id: self-hosting-becomes-deployment
  kind: tree-rename
  from: "{version}/docs/self-hosting"
  to: "{version}/docs/deployment"
  versions: ">=3.9"
```

**`kind: section-fallback`** — a section absent from some versions: every URL it answers in the
versions that have it redirects to a single page in the versions that do not. Sources are
enumerated from the versions **outside** the `versions` gate (which is required — it is what
separates the versions lacking the section from the ones donating its URLs), so a page added to
the section in any release gets its fallback everywhere. This exists for the version selector:
a reader on a `/meet/…` page picking 3.2 lands on the Call docs instead of the version root.
Targets and canonicals are version-pinned — the fallback page has no counterpart under
`latest`, which is the whole reason the rule exists:

```yaml
- id: meet-was-openvidu-call
  kind: section-fallback
  dir: "{version}/meet"
  to: "{version}/docs/openvidu-call/"
  versions: "<3.4"
```

**`kind: version-alias`** — a retired version folder rebuilt as a full mirror of its minor.
`3.4.1/docs/x/` answers with a redirect to `/3.4/docs/x/`, one stub per page of the minor's tree,
targets absolute and version-pinned (the folder is not behind the `latest` symlink, and the
reader asked for that version). A folder is rebuilt whenever its minor is published; creating the
folders in the first place is `ovweb redirects apply`'s job, since no publish creates them from
nothing.

**`kind: unversioned-mirror`** — every page of the newest version answering at its unversioned
URL: `/docs/ai/live-captions/` → `/latest/docs/ai/live-captions/`. Enumerated from the newest
version's section folders, so it covers the exported `reference-docs/*.html` file URLs too, and a
versioned page that is itself a redirect is mirrored as its final destination.

## Ownership, and why the bulk scopes are wiped

Everything an expansion writes is **ovweb-owned**: the root section mirrors (`/docs/`, `/meet/`)
and the alias folders are deleted outright and rebuilt on every publish that touches them, never
reconciled page by page — a renamed or removed page would otherwise leave a stub redirecting into
a 404, and rebuilding makes that state unrepresentable. The wipe refuses to delete any file that
does not carry the generated marker, so it can never reach content. Inside version folders, where
stubs live next to real pages, `redirects apply` reconciles instead: it deletes generated stubs
no rule produces any more and rewrites the rest.

`ovweb verify` asserts the wholly-owned scopes as **set equality** against the same functions
that generate them: a missing stub means a URL 404s for crawlers again, an extra one means it may
redirect into a 404.

## Why a `files` target is relative

`latest` is a **symlink** to the newest version folder, so one file answers at both `/3.9/` and
`/latest/`. An absolute target would have to name a version, and would leak `/3.9/` to visitors
of the stable `/latest/` URL. A relative target is resolved by the browser against the document
URL, so the same bytes send `/latest/` to `/latest/docs/` and `/3.9/` to `/3.9/docs/` — with no
JavaScript involved. `ovweb` rejects an absolute target on a rule marked `relative` (the
default), and `ovweb verify` asserts it on the published bytes. The mirror and alias stubs are
the exception: each is served from exactly one URL, so their targets are absolute.

## What the generated page contains

Every element earns its place; see
[`redirect.html.j2`](../src/ovweb/data/templates/redirect.html.j2).

| Element                                         | Why                                                                                                                                 |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `<meta http-equiv="refresh" content="0; url=…">` | The no-JavaScript path. Search engines treat a zero-delay meta refresh as a redirect and pass ranking signals through.                              |
| `<meta name="robots" content="noindex, follow">` | Keeps the stub out of search results while still letting link equity flow to the target.                                                             |
| `<link rel="canonical" href="…">`                | Consolidates every version's copy on one evergreen URL. Belt and braces — a `noindex` page's canonical is ignored — so `canonical: null` omits it.  |
| `location.replace(…)` forwarding query and hash  | No history entry, so Back still works, and `?a=1#b` survives the redirect.                                                                          |
| A real `<a>` in the body                         | Works when the refresh is blocked, and gives crawlers an edge to follow.                                                                            |

## Inspecting and applying them

```bash
ovweb redirects render 3.2      # print the `files` pages that would be installed for a version
ovweb redirects check           # every version resolves every rule to exactly one target
ovweb redirects apply --tree T  # reconcile EVERY generated redirect in a tree with the config
```

`redirects apply` is the maintenance entry point: it writes the `files` and expansion stubs of
every version folder (deleting stubs no rule produces any more), lists the stubs in each
version's sitemap for the version selector, rebuilds the unversioned mirror and the alias
folders, and is how a rule reaches versions that are not being republished. With the global
`--dry-run` it reports what would change and writes nothing.
