"""Build, version and publish the openvidu.io website.

The package is split deliberately:

* **Pure** modules take and return strings and dataclasses and touch nothing else, so the
  link rewriting, sitemap surgery, redirect rendering and version arithmetic — where every
  behavioural risk lives — are unit-testable in isolation:
  :mod:`ovweb.model`, :mod:`ovweb.config`, :mod:`ovweb.versions`, :mod:`ovweb.rewrite`,
  :mod:`ovweb.releases`, :mod:`ovweb.redirects`, :mod:`ovweb.plan`.

* **Impure** modules own the filesystem, git and mike:
  :mod:`ovweb.fsops`, :mod:`ovweb.gitrepo`, :mod:`ovweb.mikewrap`, :mod:`ovweb.pipeline`.

:mod:`ovweb.cli` only parses flags and wires the two together.
"""

__version__ = "1.0.0"
