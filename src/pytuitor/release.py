"""Explicit release lookup; never called during startup or learning."""

import json
from importlib.metadata import version
from urllib.request import urlopen


def installed_version() -> str:
    return version("pytuitor")


def check_upgrade() -> str:
    with urlopen("https://pypi.org/pypi/pytuitor/json", timeout=5) as response:
        payload = response.read(1024 * 1024 + 1)
    if len(payload) > 1024 * 1024:
        raise ValueError("Release response was too large")
    latest = json.loads(payload)["info"]["version"]
    if (
        not isinstance(latest, str)
        or len(latest) > 80
        or not all(char.isalnum() or char in ".+-" for char in latest)
    ):
        raise ValueError("Invalid release version")
    return f"Installed: {installed_version()}\nLatest published version: {latest}\nNo changes made."
