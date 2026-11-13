"""MkDocs hook that fetches the GitHub facts shown in the header at build time.

Material's repository widget (partials/source.html) makes the visitor's browser call
api.github.com for the latest release, stars and forks, and caches the answer in the browser's
session storage. To keep that look without the visitor contacting GitHub, this hook asks the
API once per build and puts the result in `config.extra.github_facts`, which
`overrides/partials/header.html` renders with Material's own markup and styles. The numbers are
frozen until the next publish.

Set GITHUB_TOKEN to avoid the API's 60-requests-per-hour limit for anonymous calls. If the API
cannot be reached the build carries on and the widget shows the repository name only.
"""

import json
import logging
import os
import urllib.request

log = logging.getLogger("mkdocs.hooks.github_facts")

_REPO = "OpenVidu/openvidu"
_API = "https://api.github.com/repos/" + _REPO
#: `mkdocs serve` re-runs on_config on every rebuild; ask GitHub once per process.
_cache = None


def _get(url):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "openvidu.io-build"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=10) as r:
        return json.load(r)


def _round(value):
    """Material's own number formatting (javascripts/utilities/round): 2160 -> 2.2k."""
    if value > 999:
        digits = 1 if (value - 950) % 1000 > 99 else 0
        return f"{(value + 0.000001) / 1000:.{digits}f}k"
    return str(value)


def _fetch():
    facts = {"name": _REPO.lower(), "url": "https://github.com/" + _REPO}
    try:
        repo = _get(_API)
        facts["stars"] = _round(repo["stargazers_count"])
        facts["forks"] = _round(repo["forks_count"])
        facts["version"] = _get(_API + "/releases/latest")["tag_name"]
    except Exception as e:  # the facts are decoration; never fail the build
        log.warning("GitHub facts not available (%s); the header shows the repository name only", e)
    return facts


def on_config(config, **kwargs):
    global _cache
    if _cache is None:
        _cache = _fetch()
    config.extra["github_facts"] = _cache
    return config
