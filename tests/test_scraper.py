from types import SimpleNamespace

from video_tools import scraper


def test_selector_to_by_variants():
    assert scraper.selector_to_by("xpath://div") == ("xpath", "//div")
    assert scraper.selector_to_by("css:.btn") == ("css", ".btn")
    assert scraper.selector_to_by("name:Email") == ("name", "Email")
    assert scraper.selector_to_by("#id") == ("css", "#id")


def test_credential_store_roundtrip(tmp_path, monkeypatch):
    saved = {}

    fake_keyring = SimpleNamespace(
        set_password=lambda service, username, password: saved.__setitem__(username, password),
        get_password=lambda service, username: saved.get(username),
    )

    monkeypatch.setattr(scraper, "keyring", fake_keyring)

    store = scraper.CredentialStore(path=tmp_path / "creds.json")
    store.store("example", "user@example.com", "secret")

    username, password = store.get("example")
    assert username == "user@example.com"
    assert password == "secret"
