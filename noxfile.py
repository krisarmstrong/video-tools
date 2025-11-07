"""Automation sessions for video-tools."""

from __future__ import annotations

import nox

nox.options.sessions = ["tests"]


@nox.session(python=["3.10", "3.11", "3.12"])
def tests(session: nox.Session) -> None:
    session.install(".[test]")
    session.run("pytest", "--cov=video_tools", "--cov-report=term-missing", "--cov-report=html")
