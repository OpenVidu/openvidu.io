"""Build, version and publish the openvidu.io website.

The package is split between **pure** modules, which take and return strings and dataclasses and
touch nothing else (:mod:`ovweb.model`, :mod:`ovweb.config`, :mod:`ovweb.versions`,
:mod:`ovweb.rewrite`, :mod:`ovweb.releases`, :mod:`ovweb.redirects`, :mod:`ovweb.sources`,
:mod:`ovweb.plan`), and **impure** ones, which own the filesystem, git and mike
(:mod:`ovweb.fsops`, :mod:`ovweb.gitrepo`, :mod:`ovweb.mikewrap`, :mod:`ovweb.pipeline`). Every
behavioural risk lives in the pure layer, which is where the tests are. :mod:`ovweb.cli` parses
flags and wires the two together.
"""

__version__ = "1.0.0"
