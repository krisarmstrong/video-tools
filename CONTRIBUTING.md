# Contributing to Video Tools

Thank you for your interest in contributing to Video Tools!

## Code of Conduct

This project follows standard open source etiquette. Be respectful, constructive, and helpful.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Video URL or command used (if applicable)
- Python version and OS

### Suggesting Enhancements

Open an issue describing:
- The enhancement you'd like to see
- Why it would be useful
- Example use cases

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Set up development environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   pip install -e .[test,dev]
   ```
4. **Make your changes**
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed
5. **Run tests:**
   ```bash
   pytest
   # or for full testing across Python versions:
   nox
   ```
6. **Commit your changes** (`git commit -m 'Add amazing feature'`)
7. **Push to your branch** (`git push origin feature/amazing-feature`)
8. **Open a Pull Request**

## Development Guidelines

### Code Style

- Follow PEP 8
- Use type hints for function signatures
- Use f-strings for string formatting
- Keep functions focused and small
- Add docstrings for public functions

### Testing

- Write tests for all new functionality
- Ensure existing tests still pass
- Aim for high code coverage
- Test edge cases and error conditions

### Module Organization

- `__main__.py` - CLI argument parsing and orchestration
- `youtube.py` - yt-dlp integration for YouTube downloads
- `scraper.py` - Selenium-based scraping for non-YouTube sites

### Adding New Site Support

1. Add site detection logic to `__main__.py`
2. Add scraping function to `scraper.py`
3. Add tests in `tests/`
4. Update README with examples
5. Document any site-specific quirks

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=video_tools --cov-report=html

# Run specific test
pytest tests/test_video_tools.py::test_name

# Run across all supported Python versions
nox
```

## Documentation

- Update README.md for user-facing changes
- Add/update docstrings for code changes
- Update CHANGELOG.md (if exists)

## Questions?

Open an issue or start a discussion. We're happy to help!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
