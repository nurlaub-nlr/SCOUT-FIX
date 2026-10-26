"""Exercise the file URIs returned to Scout View for local transcript sources."""

import base64
import json
import shutil
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from inspect_scout._view._api_v2 import v2_api_app

EVAL_LOG = (
    Path(__file__).resolve().parent.parent
    / "recorder"
    / "logs"
    / "2025-11-07T10-59-47-05-00_websearch-addition-problem_LqPDntDnkk4h2fSqQ8i6CE.eval"
)


def _encode_location(location: str) -> str:
    return base64.urlsafe_b64encode(location.encode()).decode().rstrip("=")


@pytest.mark.parametrize("folder_name", ["Peer Review", "café"])
@pytest.mark.parametrize("source_kind", ["directory", "file"])
def test_viewer_lists_and_opens_encoded_local_transcripts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    folder_name: str,
    source_kind: str,
) -> None:
    """The browser's configured URI must read the same samples as the raw path."""
    runs = tmp_path / folder_name
    nested = runs / "nested"
    nested.mkdir(parents=True)
    log_file = nested / EVAL_LOG.name
    shutil.copyfile(EVAL_LOG, log_file)
    source = runs if source_kind == "directory" else log_file
    monkeypatch.chdir(tmp_path)
    (tmp_path / "scout.yaml").write_text(
        json.dumps({"transcripts": str(source)}), encoding="utf-8"
    )

    with TestClient(v2_api_app()) as client:
        native = client.post(f"/transcripts/{_encode_location(str(source))}", json={})
        assert native.status_code == 200
        assert native.json()["total_count"] > 0

        config = client.get("/app-config")
        assert config.status_code == 200
        uri = config.json()["transcripts"]["dir"]
        assert uri == source.resolve().as_uri()
        endpoint = f"/transcripts/{_encode_location(uri)}"
        listing = client.post(endpoint, json={})
        assert listing.status_code == 200
        assert listing.json() == native.json()

        transcript_id = listing.json()["items"][0]["transcript_id"]
        info = client.get(f"{endpoint}/{transcript_id}/info")
        assert info.status_code == 200
        assert info.json()["transcript_id"] == transcript_id

        content = client.get(f"{endpoint}/{transcript_id}/messages-events")
        assert content.status_code == 200
        assert content.json()["messages"]
