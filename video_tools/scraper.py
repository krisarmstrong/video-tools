"""Selenium-based scraping helpers for authenticated video portals."""

from __future__ import annotations

import json
import logging
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, TYPE_CHECKING, Tuple
from urllib.parse import urlparse

try:  # pragma: no cover
    import keyring  # type: ignore
except ImportError:  # pragma: no cover
    keyring = None  # type: ignore
try:  # pragma: no cover
    from webdriver_manager.chrome import ChromeDriverManager  # type: ignore
except ImportError:  # pragma: no cover
    ChromeDriverManager = None  # type: ignore

if TYPE_CHECKING:  # pragma: no cover
    from selenium import webdriver


def default_store_path() -> Path:
    return Path.home() / ".video_tools" / "credentials.json"


@dataclass
class CredentialStore:
    """Persist username metadata + secrets in keyring."""

    path: Path = field(default_factory=default_store_path)

    def __post_init__(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save_metadata(self, alias: str, username: str) -> None:
        data = self.load()
        data[alias] = {"username": username}
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def get(self, alias: str) -> Tuple[str, str] | None:
        data = self.load()
        profile = data.get(alias)
        if not profile:
            return None
        username = profile["username"]
        if keyring is None:
            raise RuntimeError(
                "keyring is not installed. Install video-tools with its default extras."
            )
        password = keyring.get_password("video-tools", username)
        if not password:
            return None
        return username, password

    def store(self, alias: str, username: str, password: str) -> None:
        self.save_metadata(alias, username)
        if keyring is None:
            raise RuntimeError(
                "keyring is not installed. Install video-tools with its default extras."
            )
        keyring.set_password("video-tools", username, password)


def selector_to_by(selector: str) -> Tuple[str, str]:
    """Parse selector string; returns strategy + query."""

    if selector.startswith("xpath:"):
        return "xpath", selector.split(":", 1)[1]
    if selector.startswith("css:"):
        return "css", selector.split(":", 1)[1]
    if selector.startswith("name:"):
        return "name", selector.split(":", 1)[1]
    return "css", selector


def hostname_alias(url: str) -> str:
    host = urlparse(url).netloc or "default"
    return host.split(":")[0]


def _resolve_by(strategy: str, By) -> str:
    mapping = {
        "css": By.CSS_SELECTOR,
        "xpath": By.XPATH,
        "name": By.NAME,
    }
    return mapping[strategy]


def _selenium():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service

    return webdriver, By, EC, WebDriverWait, Options, Service


def create_driver(headless: bool = True):
    webdriver, _, _, _, Options, Service = _selenium()
    if ChromeDriverManager is None:
        raise RuntimeError(
            "webdriver-manager is not installed. Install video-tools with its default dependencies."
        )
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def login_and_navigate(
    driver: webdriver.Chrome,
    *,
    url: str,
    username: str,
    password: str,
    username_field: str,
    password_field: str,
    navigation_steps: Iterable[str],
    wait_timeout: int,
) -> None:
    _, By, EC, WebDriverWait, _, _ = _selenium()

    driver.get(url)
    wait = WebDriverWait(driver, wait_timeout)

    wait.until(EC.presence_of_element_located((By.NAME, username_field))).send_keys(username)
    wait.until(EC.presence_of_element_located((By.NAME, password_field))).send_keys(password + "\n")

    for raw_selector in navigation_steps:
        strategy, query = selector_to_by(raw_selector)
        locator = (_resolve_by(strategy, By), query)
        wait.until(EC.element_to_be_clickable(locator)).click()


def extract_video_url(
    driver: webdriver.Chrome,
    *,
    selector: str,
    attribute: str,
    wait_timeout: int,
) -> str:
    _, By, EC, WebDriverWait, _, _ = _selenium()

    wait = WebDriverWait(driver, wait_timeout)
    strategy, query = selector_to_by(selector)
    element = wait.until(EC.presence_of_element_located((_resolve_by(strategy, By), query)))
    return element.get_attribute(attribute)


def download_with_ffmpeg(video_url: str, output_file: Path) -> None:
    command = [
        "ffmpeg",
        "-y",
        "-i",
        video_url,
        "-c",
        "copy",
        str(output_file),
    ]
    logging.info("Running FFmpeg command: %s", " ".join(command))
    subprocess.run(command, check=True)


def scrape_portal(
    *,
    url: str,
    username: str,
    password: str,
    username_field: str,
    password_field: str,
    navigation_steps: Iterable[str],
    video_selector: str,
    video_attribute: str,
    download: bool,
    output_file: Path,
    headless: bool,
    wait_timeout: int = 15,
) -> str:
    """Navigate site, return video URL, optionally download via ffmpeg."""

    driver = create_driver(headless=headless)
    try:
        login_and_navigate(
            driver,
            url=url,
            username=username,
            password=password,
            username_field=username_field,
            password_field=password_field,
            navigation_steps=navigation_steps,
            wait_timeout=wait_timeout,
        )
        video_url = extract_video_url(
            driver,
            selector=video_selector,
            attribute=video_attribute,
            wait_timeout=wait_timeout,
        )
        if download:
            download_with_ffmpeg(video_url, output_file)
        return video_url
    finally:
        driver.quit()
