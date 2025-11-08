# Video Tools Documentation

Command-line utilities for video file manipulation and processing.

## Quick Links

- [Installation](installation.md)
- [Usage Guide](usage.md)
- [API Reference](api.md)
- [Contributing](../CONTRIBUTING.md)

## Overview

Video Tools provides utilities for common video file operations:

- Video conversion and transcoding
- Metadata extraction and editing
- Thumbnail generation
- Format conversion
- Batch processing

## Features

- **Multiple format support** (MP4, AVI, MKV, MOV, etc.)
- **Metadata operations** - Extract and modify video metadata
- **Thumbnail generation** - Create preview images
- **Batch processing** - Process multiple files efficiently
- **Quality presets** - Predefined encoding settings
- **CLI and library** - Use as command-line tool or Python library

## Installation

```bash
pip install -e .
```

## Quick Start

```bash
# Convert video format
video-tools convert input.avi output.mp4

# Extract metadata
video-tools metadata video.mp4

# Generate thumbnail
video-tools thumbnail video.mp4 --time 00:01:30

# Batch process
video-tools batch ./videos --format mp4
```

## Requirements

- Python 3.x
- FFmpeg (for video processing)

## Testing

```bash
pytest tests/ -v
```

## License

MIT License - See [LICENSE](../LICENSE) for details.

## Author

Kris Armstrong
