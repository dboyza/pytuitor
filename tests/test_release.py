import io
import json

import pytest

from pytuitor import release


def test_upgrade_lookup_is_explicit_read_only(monkeypatch):
    calls = []

    def response(url, timeout):
        calls.append((url, timeout))
        return io.BytesIO(json.dumps({"info": {"version": "1.0.0"}}).encode())

    monkeypatch.setattr(release, "urlopen", response)
    result = release.check_upgrade()
    assert calls == [("https://pypi.org/pypi/pytuitor/json", 5)]
    assert "No changes made" in result
    assert "1.0.0" in result


@pytest.mark.parametrize(
    "payload",
    [b"not json", b"x" * (1024 * 1024 + 1), b'{"info":{"version":"bad\\nversion"}}'],
    ids=["invalid-json", "oversized-response", "invalid-version"],
)
def test_bad_release_response_is_rejected(monkeypatch, payload):
    monkeypatch.setattr(release, "urlopen", lambda *args, **kwargs: io.BytesIO(payload))
    with pytest.raises(ValueError):
        release.check_upgrade()
