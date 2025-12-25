"""video-tools public surface."""

from __future__ import annotations

from . import scraper, youtube

try:  # pragma: no cover
    from ._version import version as __version__
except ImportError:  # pragma: no cover
    __version__ = "0.0.0"

__all__ = ["scraper", "youtube", "__version__"]
