# Scout 0.6.1 file URI fix: local preview

This is a draft fork for local testing before the GitHub repository is finalized.
It is based on the latest published Scout release verified on October 26, 2026:
[`0.6.1`](https://pypi.org/project/inspect-scout/0.6.1/), upstream commit
[`9db31e47de985a0f8098f326184efe0a41d5c3a5`](https://github.com/meridianlabs-ai/inspect_scout/tree/9db31e47de985a0f8098f326184efe0a41d5c3a5).

The fix converts percent-encoded local `file://` addresses to filesystem paths
before opening transcript sources. This addresses the viewer showing no
transcripts when a folder name contains spaces or Unicode characters.
The same change applies when opening a transcript's metadata, messages, and
events. Raw paths and remote URLs keep their existing behavior.

## Try the local preview

The prepared Windows checkout has its own `.venv` and an ignored
`scout.local.yaml` pointing to the selected runs directory. It runs on
**http://127.0.0.1:7577**. The previous viewer uses port 7576.

To start or restart this preview from the fork directory:

```powershell
& .\.venv\Scripts\scout.exe --version
& .\.venv\Scripts\scout.exe view --host 127.0.0.1 --port 7577 --no-browser
```

The installed preview identifies itself as `0.6.1+fileuri.1`. Its dependencies
are separate from the harness environment. Local configuration, virtual
environments, logs, and scan output are ignored by Git.

In the preview:

1. Open **Transcripts** and confirm that the expected runs are listed.
2. Open several runs and check their messages and events.
3. Refresh the browser and confirm the list still loads.

The selected GitHub destination is
[nurlaub-nlr/SCOUT-FIX](https://github.com/nurlaub-nlr/SCOUT-FIX). The local
`origin` remote points there; `upstream` retains the original Scout repository.
Publication and a final release tag remain pending the interactive preview test.
No source changes have been pushed. Draft GitHub installation commands are in
[README.md](README.md).

## Regression checks

The regression test uses an upstream fixture log and follows the browser's
configuration, listing, details, and message-loading requests. It covers both
directories and individual log files under paths containing spaces and Unicode.

Additional exploratory checks found an existing dependency issue on Windows
with literal `%20` or `#` in folder names: even native paths return no transcripts
in unmodified Scout 0.6.1 with Inspect AI 0.3.285. That separate issue remains
outside this preview; avoid those characters when testing. The affected
exploratory results are saved locally in `.venv/file-uri-before.xml` and
`.venv/file-uri-after.xml`.

```powershell
& .\.venv\Scripts\python.exe -m pytest -n 0 tests/view/test_file_uri_transcripts.py
```

The viewer assets in this preview are the unmodified assets from the official
0.6.1 wheel, checked against the release's Git LFS hashes.

## Preview validation (October 26, 2026)

- Built and installed the patched wheel as `0.6.1+fileuri.1` in the isolated `.venv`.
- All 277 targeted viewer and transcript tests passed against the installed wheel.
- Ruff lint/format and strict mypy checks passed for the two changed Python files.
- `pip check` found no broken requirements.
- The live viewer returned all 10 transcripts from the configured runs directory
  using the exact encoded URI supplied to the browser.
- Metadata, messages, and events loaded for three runs; refreshing returned all 10.
- Viewer HTML and its nine entry assets loaded successfully. All 30 packaged
  frontend files match upstream 0.6.1 LFS hashes; the frontend submodule is unchanged.

The preview was tested on Windows with Python 3.14.6 and Inspect AI 0.3.285.
The full upstream suite and cross-platform installation checks remain for
finalization after the interactive preview test. Dependency deprecation warnings
were emitted by the targeted tests; there were no test failures.

Local evidence is in `.venv/preview-tests.xml`, `.venv/preview-smoke.json`, and
`.venv/preview-build.json`. The wheel is
`.venv/preview-dist/inspect_scout-0.6.1+fileuri.1-py3-none-any.whl`.

Wheel SHA256:
`d411a55eb644d426b3a5b09a16394a68a18cc88b333d4ffe1ee44f63f9f227ae`.

The launch logs are `.venv/scout-preview.stdout.log` and
`.venv/scout-preview.stderr.log`.
