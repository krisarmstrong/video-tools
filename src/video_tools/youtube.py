"""Helpers for YouTube/yt-dlp downloads."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict

try:  # pragma: no cover - optional dependency
    import yt_dlp  # type: ignore
except ImportError:  # pragma: no cover
    yt_dlp = None  # type: ignore


def build_yt_dlp_options(
    output_dir: Path,
    video_format: str,
    resume: bool,
    rate_limit: str | None,
    cookies: Path | None,
    retries: int,
) -> Dict[str, Any]:
    """Return a configured options dict ready for YoutubeDL."""

    output_dir.mkdir(parents=True, exist_ok=True)

    opts: Dict[str, Any] = {
        "format": video_format,
        "merge_output_format": "mp4",
        "continuedl": resume,
        "retries": retries,
        "outtmpl": str(output_dir / "%(uploader)s/%(upload_date)s_%(title)s.%(ext)s"),
        "progress_hooks": [_log_download_progress],
    }
    if rate_limit:
        opts["ratelimit"] = rate_limit
    if cookies:
        opts["cookiefile"] = str(cookies)
    return opts


def download_channel(
    url: str,
    *,
    output_dir: Path,
    video_format: str = "bestvideo+bestaudio",
    resume: bool = True,
    rate_limit: str | None = None,
    cookies: Path | None = None,
    retries: int = 3,
) -> None:
    """Download all videos from a YouTube channel/playlist."""

    opts = build_yt_dlp_options(
        output_dir=output_dir,
        video_format=video_format,
        resume=resume,
        rate_limit=rate_limit,
        cookies=cookies,
        retries=retries,
    )

    if yt_dlp is None:  # pragma: no cover - run-time error
        raise RuntimeError("yt-dlp is not installed. Please install video-tools with its default dependencies.")

    logging.info("Starting yt-dlp download for %s", url)
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    logging.info("Download completed for %s", url)


def _log_download_progress(status: dict) -> None:
    if status.get("status") == "downloading":
        logging.info(
            "Downloading %s %s",
            status.get("filename", "unknown"),
            status.get("_percent_str", "0%"),
        )
    elif status.get("status") == "finished":
        logging.info("Finished downloading %s", status.get("filename", "unknown"))
