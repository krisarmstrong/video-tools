from types import SimpleNamespace
from pathlib import Path

from video_tools import __main__ as cli


def test_run_youtube(monkeypatch):
    called = {}

    def fake_download(url, **kwargs):
        called["url"] = url
        called["kwargs"] = kwargs

    monkeypatch.setattr(cli.youtube, "download_channel", fake_download)

    args = SimpleNamespace(
        url="https://youtube.com/c/example",
        output_dir=Path("out"),
        format="best",
        no_resume=False,
        rate_limit=None,
        cookies=None,
        retries=2,
    )

    assert cli._run_youtube(args) == 0
    assert called["url"].startswith("https://youtube")


def test_run_scrape(monkeypatch, tmp_path):
    class DummyStore:
        def __init__(self):
            self.saved = None

        def get(self, alias):
            return ("stored", "password")

        def store(self, alias, username, password):
            self.saved = (alias, username, password)

    dummy_store = DummyStore()

    monkeypatch.setattr(cli.scraper, "CredentialStore", lambda: dummy_store)
    monkeypatch.setattr(
        cli.scraper, "scrape_portal", lambda **kwargs: "https://video.example/stream"
    )

    args = SimpleNamespace(
        url="https://portal.example",
        username=None,
        password=None,
        username_field="Email",
        password_field="Password",
        navigation=["css:.nav"],
        video_selector="css:video",
        video_attribute="src",
        credential_alias="example",
        remember=False,
        download=False,
        output_file=Path("dummy.mp4"),
        headless=True,
        wait_timeout=5,
    )

    assert cli._run_scrape(args) == 0
