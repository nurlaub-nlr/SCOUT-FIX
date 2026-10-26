"""Report why a running local Scout viewer may show no transcripts.

Uses only the Python standard library. Prints paths and counts, never transcript
contents, and does not change project settings or install packages.
"""

import argparse
import base64
import importlib.metadata
import json
import os
import platform
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def _object(value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError("Expected a JSON object from Scout")
    return {str(key): item for key, item in value.items()}


def _request(base: str, endpoint: str, payload: object = None) -> dict[str, object]:
    parsed = urllib.parse.urlsplit(base)
    headers = {
        "Origin": f"{parsed.scheme}://{parsed.netloc}",
        "Accept-Encoding": "identity",
    }
    data = None
    if payload is not None:
        data = json.dumps(payload).encode()
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(base + endpoint, data=data, headers=headers)
    # Local viewer requests must not go through a corporate HTTP proxy.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(request, timeout=120) as response:
        return _object(json.load(response))


def _count(base: str, source: str) -> int:
    encoded = base64.urlsafe_b64encode(source.encode()).decode().rstrip("=")
    result = _request(
        base,
        f"/api/v2/transcripts/{encoded}",
        {"pagination": {"limit": 1, "cursor": None, "direction": "forward"}},
    )
    count = result.get("total_count")
    if not isinstance(count, int):
        raise ValueError("Scout did not return a transcript count")
    return count


def _raise_walk_error(error: OSError) -> None:
    raise error


def _local_eval_count(source: Path) -> int:
    if source.is_file():
        return int(source.suffix == ".eval")
    return sum(
        name.endswith(".eval")
        for _, _, files in os.walk(source, onerror=_raise_walk_error)
        for name in files
    )


def _diagnose(base: str, report: dict[str, object]) -> None:
    config = _request(base, "/api/v2/app-config")
    report["project_uri"] = config.get("project_dir")
    report["project_filter_active"] = bool(config.get("filter"))
    configured = config.get("transcripts")
    if configured is None:
        report["finding"] = (
            "No transcript source configured. Start Scout with --transcripts pointing to the runs folder."
        )
        return
    source_config = _object(configured)
    uri = source_config.get("dir")
    if not isinstance(uri, str):
        raise ValueError("Scout did not return a transcript folder")
    report["configured_source"] = source_config
    parsed = urllib.parse.urlsplit(uri)
    local_source = None
    if parsed.scheme == "file" and parsed.netloc in ("", "localhost"):
        local_source = Path(urllib.request.url2pathname(parsed.path))
        report["local_path"] = str(local_source)
        report["path_exists"] = local_source.exists()
        if not local_source.exists():
            report["finding"] = (
                "The configured path does not exist on this computer. Use this computer's own absolute path; in shell commands use $HOME instead of a quoted ~."
            )
            return
        report["eval_files_on_disk"] = _local_eval_count(local_source)

    browser_count = _count(base, uri)
    report["browser_uri_transcripts"] = browser_count
    native_count = _count(base, str(local_source)) if local_source else None
    report["native_path_transcripts"] = native_count
    if browser_count:
        report["finding"] = (
            "The viewer API finds transcripts. Clear browser filters, select this source, and reload the viewer."
        )
    elif native_count:
        report["finding"] = (
            "The native path works but the browser URI does not. Reinstall SCOUT-FIX in the environment running Scout and restart the viewer."
        )
    elif report["project_filter_active"]:
        report["finding"] = (
            "The API returned zero transcripts and a project filter is active. Check the filter in scout.yaml and scout.local.yaml."
        )
    else:
        report["finding"] = (
            "The API returned zero transcripts. Check the selected folder, file types, and the Scout terminal for read errors. For OneDrive, check that the logs are downloaded locally."
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "url", nargs="?", default="http://127.0.0.1:7577", help="Local viewer URL"
    )
    args = parser.parse_args()
    parsed = urllib.parse.urlsplit(args.url)
    if parsed.scheme not in ("http", "https") or parsed.hostname not in (
        "localhost",
        "127.0.0.1",
        "::1",
    ):
        parser.error("Use the local viewer URL on the computer running Scout")
    base = urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, parsed.path.rstrip("/"), "", "")
    )
    report: dict[str, object] = {
        "viewer_url": base,
        "platform": platform.platform(),
        "python": sys.executable,
        "scout_on_path": shutil.which("scout"),
        "environment_note": "Package details describe this Python environment; restart Scout from the same environment to compare.",
    }
    try:
        distribution = importlib.metadata.distribution("inspect-scout")
        report["installed_version"] = distribution.version
        origin = _object(json.loads(distribution.read_text("direct_url.json") or "{}"))
        vcs = origin.get("vcs_info")
        report["installed_git_commit"] = _object(vcs).get("commit_id") if vcs else None
    except importlib.metadata.PackageNotFoundError:
        report["installed_version"] = (
            "Scout is not installed in this Python environment"
        )
    status = 0
    try:
        _diagnose(base, report)
    except (OSError, ValueError, urllib.error.URLError) as error:
        report["error"] = str(error)
        report["finding"] = (
            "Could not complete the check. Verify the viewer URL and inspect the Scout terminal for errors."
        )
        status = 1
    print(json.dumps(report, indent=2, ensure_ascii=True))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
