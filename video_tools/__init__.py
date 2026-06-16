"""video-tools public surface."""

from __future__ import annotations

from . import scraper, youtube

try:  # pragma: no cover
    from ._version import version as __version__
except ImportError:  # pragma: no cover
    __version__ = "2.0.4"

__all__ = ["__version__", "scraper", "youtube"]
