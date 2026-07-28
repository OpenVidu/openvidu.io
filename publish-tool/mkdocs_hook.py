"""MkDocs hook that exposes ovweb.yaml to the templates.

Wired up through `hooks:` in mkdocs.yml. It exists so that the 404 router
(docs/overrides/404.html) compiles its redirect patterns from the same configuration ovweb
publishes with, instead of hardcoding a list that has to be kept in sync by hand.

The import shim below keeps a plain `mkdocs serve` working in a checkout where the package is
not installed — including inside the Docker images, which mount the repository rather than
installing anything. It does not duplicate any logic: the config loader and the pattern
expansion have exactly one implementation, in `ovweb`.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from ovweb.config import load_site_config  # noqa: E402
from ovweb.redirects import resolve_patterns  # noqa: E402


def on_config(config, **kwargs):
    """Publish the layout and the 404 redirect patterns on `config.extra.ovweb`.

    ovweb sets `$OVWEB_SITE_CONFIG` when it invokes mike, so a publish build and the
    post-processing that follows it always read the same file — which matters for a past
    version, whose branch carries its own stale copy of ovweb.yaml.
    """
    site_config = load_site_config()
    config["extra"]["ovweb"] = {
        "versioned_pages": list(site_config.layout.versioned_pages),
        "non_versioned_pages": list(site_config.layout.non_versioned_pages),
        "redirect_patterns": [
            {"id": pattern.id, "match": pattern.match, "to": pattern.to}
            for pattern in resolve_patterns(site_config)
        ],
    }
    return config
