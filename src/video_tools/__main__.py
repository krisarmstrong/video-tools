"""CLI entry point for video-tools."""

from __future__ import annotations

import argparse
import logging
import subprocess
import sys
import time
from pathlib import Path

from . import scraper, youtube


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unified CLI for video downloads.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging.")
    parser.add_argument("-l", "--logfile", type=Path, help="Optional logfile.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    youtube_parser = subparsers.add_parser("youtube", help="Download via yt-dlp.")
    youtube_parser.add_argument("--url", required=True, help="Channel, playlist, or video URL.")
    youtube_parser.add_argument("--output-dir", type=Path, default=Path("downloads"), help="Output directory.")
    youtube_parser.add_argument("--format", default="bestvideo+bestaudio", help="yt-dlp format string.")
    youtube_parser.add_argument("--no-resume", action="store_true", help="Disable resume for partially downloaded files.")
    youtube_parser.add_argument("--rate-limit", help="Network rate limit (e.g., 2M).")
    youtube_parser.add_argument("--cookies", type=Path, help="Path to cookies.txt for authenticated downloads.")
    youtube_parser.add_argument("--retries", type=int, default=3, help="Number of yt-dlp retries.")

    scrape_parser = subparsers.add_parser("scrape", help="Automate an authenticated browser session and extract video URLs.")
    scrape_parser.add_argument("--url", required=True, help="Portal URL to authenticate against.")
    scrape_parser.add_argument("--username", help="Login username/email.")
    scrape_parser.add_argument("--password", help="Login password.")
    scrape_parser.add_argument("--username-field", default="Email", help="HTML name attribute for username field.")
    scrape_parser.add_argument("--password-field", default="Password", help="HTML name attribute for password field.")
    scrape_parser.add_argument(
        "--navigation",
        action="append",
        default=[
            "xpath://*[@id='body-pendingSeminar']/tr[1]/td[2]/div[2]/a[1]",
            "xpath://*[@id='myTab']/li[2]/a",
        ],
        help="Selectors to click after login (repeatable). Default matches the legacy workflow.",
    )
    scrape_parser.add_argument(
        "--video-selector",
        default="xpath://*[@id='grid-list-courseSchedule']/div[1]/table/tbody/tr/td[2]/div/a[1]/span",
        help="Selector pointing at the video link element.",
    )
    scrape_parser.add_argument(
        "--video-attribute",
        default="href",
        help="Attribute to read from the video element (default: href).",
    )
    scrape_parser.add_argument(
        "--credential-alias",
        help="Name used to store/retrieve credentials (defaults to hostname).",
    )
    scrape_parser.add_argument("--remember", action="store_true", help="Persist provided credentials for future runs.")
    scrape_parser.add_argument("--download", action="store_true", help="Automatically download via ffmpeg.")
    scrape_parser.add_argument("--output-file", type=Path, help="Video output filename (used with --download).")
    scrape_parser.add_argument("--headless", action=argparse.BooleanOptionalAction, default=True, help="Run Chrome headless.")
    scrape_parser.add_argument("--wait-timeout", type=int, default=15, help="Seconds to wait for page elements.")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    setup_logging(args.verbose, args.logfile)

    if args.command == "youtube":
        return _run_youtube(args)
    if args.command == "scrape":
        return _run_scrape(args)
    parser.error("Unknown command")
    return 1


def setup_logging(verbose: bool, logfile: Path | None) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    handlers = [logging.StreamHandler(sys.stdout)]
    if logfile:
        handlers.append(logging.FileHandler(logfile))
    logging.basicConfig(level=level, handlers=handlers, format="%(asctime)s [%(levelname)s] %(message)s")


def _run_youtube(args: argparse.Namespace) -> int:
    try:
        youtube.download_channel(
            args.url,
            output_dir=args.output_dir,
            video_format=args.format,
            resume=not args.no_resume,
            rate_limit=args.rate_limit,
            cookies=args.cookies,
            retries=args.retries,
        )
    except Exception as exc:  # pragma: no cover - network dependent
        logging.critical("yt-dlp failed: %s", exc)
        return 1
    return 0


def _run_scrape(args: argparse.Namespace) -> int:
    alias = args.credential_alias or scraper.hostname_alias(args.url)
    store = scraper.CredentialStore()

    username = args.username
    password = args.password

    if (not username or not password):
        stored = store.get(alias)
        if stored:
            username, password = stored

    if not username or not password:
        logging.error("Credentials are required. Provide --username/--password or store them with --remember.")
        return 1

    if args.remember and args.username and args.password:
        store.store(alias, args.username, args.password)

    output_file = args.output_file or Path(f"video_{int(time.time())}.mp4")

    try:
        video_url = scraper.scrape_portal(
            url=args.url,
            username=username,
            password=password,
            username_field=args.username_field,
            password_field=args.password_field,
            navigation_steps=args.navigation,
            video_selector=args.video_selector,
            video_attribute=args.video_attribute,
            download=args.download,
            output_file=output_file,
            headless=args.headless,
            wait_timeout=args.wait_timeout,
        )
        logging.info("Video URL: %s", video_url)
        print(video_url)
    except subprocess.CalledProcessError as exc:  # pragma: no cover - depends on ffmpeg
        logging.critical("FFmpeg failed: %s", exc)
        return 1
    except Exception as exc:  # pragma: no cover - depends on remote portal
        logging.critical("Scrape failed: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
