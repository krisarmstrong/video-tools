# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.4](https://github.com/krisarmstrong/video-tools/compare/v2.0.3...v2.0.4) (2026-06-16)


### Bug Fixes

* **ci:** add missing noxfile and correct matrix python-version ([#10](https://github.com/krisarmstrong/video-tools/issues/10)) ([b6f35f6](https://github.com/krisarmstrong/video-tools/commit/b6f35f6805fbb16593a5adacde140c2c7eee95aa))

## [Unreleased]

## [2.0.3] - 2024-12-24

### Changed
- Flatten project structure: move video_tools/ to root level
- Restore pre-commit configuration

## [2.0.2] - 2024-12-20

### Changed
- Standardized tooling and project configuration

## [2.0.1] - 2024-12-20

### Added
- Initial release with unified CLI for video downloads
- YouTube/yt-dlp download support with resume, rate limiting, cookies
- Selenium-based scraper for authenticated video portals
- Credential storage using system keyring
- FFmpeg integration for video downloads
