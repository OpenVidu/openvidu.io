"""Shared fixtures.

The `config` fixture loads the **real** ovweb.yaml rather than a test double, so a change to
the site layout that breaks an assumption shows up here instead of in production.

Fixtures are hand-written minimal markup rather than captured pages. Real built pages are
~100 KB each of theme chrome and would add megabytes to the repository for no extra coverage:
the substitutions only ever look at a few characters around a link. Realism is the parity
gate's job — it runs against genuine `mike` output (see tests/parity/).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from ovweb.config import load_site_config
from ovweb.model import SiteLayout

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "publish-tool" / "ovweb.yaml"


@pytest.fixture(scope="session")
def config():
    return load_site_config(CONFIG_PATH)


@pytest.fixture(scope="session")
def layout(config) -> SiteLayout:
    return config.layout


@pytest.fixture
def version() -> str:
    return "3.8"
