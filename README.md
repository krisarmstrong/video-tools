# video-tools
[![Checks](https://github.com/krisarmstrong/video-tools/actions/workflows/checks.yml/badge.svg)](https://github.com/krisarmstrong/video-tools/actions/workflows/checks.yml)


![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white) ![License](https://img.shields.io/badge/License-MIT-green) ![Tests](https://img.shields.io/badge/Tests-pytest-passing) ![Status](https://img.shields.io/badge/Status-Active-success)


Unified toolkit for two previously separate utilities:
- **VideoScraperPlus** (authenticated Selenium scraping + FFmpeg downloads)
- **YouTube Channel Downloader** (yt-dlp channel/archive sync)

Everything is now accessible via one CLI (`video-tools`) and a reusable Python SDK.

## Features
- `video-tools youtube` wraps yt-dlp with sane defaults (per-channel folders, resumable downloads, cookie support).
- `video-tools scrape` automates login flows with Selenium + ChromeDriver, stores credentials securely via keyring, and optionally hands video URLs off to FFmpeg.
- Shared logging, config, tests, and CI pipeline with tag-driven versioning.

## Installation
```bash
pip install .
```

## CLI Usage

### YouTube / yt-dlp
```bash
video-tools youtube \
  --url https://www.youtube.com/@netally \
  --output-dir downloads \
  --format bestvideo+bestaudio --retries 5
```

Flags:
- `--no-resume` – disable resumable downloads.
- `--rate-limit 2M` – throttle bandwidth.
- `--cookies cookies.txt` – pass authenticated sessions for members-only content.

### Authenticated Scraping
```bash
video-tools scrape \
  --url https://training.example.com/login \
  --username alice@example.com --password secret \
  --remember --download --output-file webinar.mp4
```

Useful options:
- `--navigation` – repeat to list CSS/XPath selectors to click after login.
- `--video-selector` / `--video-attribute` – control how URLs are discovered.
- `--credential-alias` + `--remember` – reuse stored credentials via keyring.
- `--headless` / `--no-headless` – toggle browser visibility.

If credentials are omitted the tool looks up stored ones using the hostname alias.

## Library API
```python
from pathlib import Path
from video_tools import youtube, scraper

youtube.download_channel("https://youtube.com/c/example", output_dir=Path("downloads"))
url = scraper.scrape_portal(
    url="https://portal.example",
    username="alice@example.com",
    password="secret",
    username_field="Email",
    password_field="Password",
    navigation_steps=["css:.nav"],
    video_selector="css:video",
    video_attribute="src",
    download=False,
    output_file=Path("video.mp4"),
    headless=True,
)
```

## Development

Run the full local checks:

```bash
./check.sh
```

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .[test]
python -m pytest
```

Or run the same checks CI uses:
```bash
pip install nox
nox -s tests
```

## Releases & CI
- Versions are stored in `pyproject.toml`; release-please manages tags and changelog entries.
- `.github/workflows/ci.yml` runs `nox -s tests` on pushes, PRs, and tags.
- To release: merge the release-please PR (or tag manually if needed).
