# SCOUT-FIX

A fork of [Inspect Scout](https://github.com/meridianlabs-ai/inspect_scout),
based on release **0.6.1**, with a fix for local transcript folders whose paths
contain spaces or Unicode characters. The viewer now decodes local `file://`
addresses before opening the transcript source.

Repository: [nurlaub-nlr/SCOUT-FIX](https://github.com/nurlaub-nlr/SCOUT-FIX).

**Published preview:** install this fork from the GitHub URL below. It retains
the `inspect-scout` package name and `scout` command. See
[preview notes](FORK_TESTING.md) for validation results and known limitations.

## Install from GitHub

Requires Python 3.11 or later and Git. Run these commands from the project where
you want to use Scout.

### PowerShell

```powershell
py -m venv .venv-scout
& .\.venv-scout\Scripts\python.exe -m pip install --upgrade "inspect-scout @ git+https://github.com/nurlaub-nlr/SCOUT-FIX.git@main"
& .\.venv-scout\Scripts\scout.exe view --transcripts "C:/path/to/Peer Review/runs" --host 127.0.0.1 --port 7577 --no-browser
```

### Bash (Linux, macOS, or WSL)

```bash
python3 -m venv .venv-scout
.venv-scout/bin/python -m pip install --upgrade "inspect-scout @ git+https://github.com/nurlaub-nlr/SCOUT-FIX.git@main"
.venv-scout/bin/scout view --transcripts "/path/to/Peer Review/runs" --host 127.0.0.1 --port 7577 --no-browser
```

Replace the example path with your runs directory, then open
<http://127.0.0.1:7577>. In Git Bash on Windows, use the `.venv-scout/Scripts/`
executables instead of `.venv-scout/bin/`. WSL uses Linux paths such as
`/mnt/c/Users/.../runs`.

For a persistent project configuration, set `transcripts` in `scout.yaml` or
an ignored `scout.local.yaml`. Quote paths containing spaces when passing them
on the command line.

The package and command remain `inspect-scout` and `scout`. This fork retains
the upstream MIT license. General usage is covered in the
[upstream documentation](https://meridianlabs-ai.github.io/inspect_scout/).

## Using an existing Scout environment

Run the GitHub install command with the Python interpreter from the environment
where you already use Scout:

```bash
python -m pip install --upgrade "inspect-scout @ git+https://github.com/nurlaub-nlr/SCOUT-FIX.git@main"
scout --version
python -m pip check
```

This replaces upstream Scout in that environment. Installing or upgrading plain
`inspect-scout` from PyPI later can replace the fork, so keep the GitHub requirement
in your project dependency file. For a reproducible install, replace `@main` with
the full commit SHA you have tested.

The fork uses upstream's Git-based version calculation, so `scout --version`
shows a development version such as `0.6.2.dev2` while the code is based on 0.6.1.
The `0.6.1` tag identifies the unmodified upstream release; use `main` or a fixed
commit SHA to install the file-path fix.

The Python package includes the built viewer assets. Node.js and pnpm are needed
only for frontend development. Git LFS downloads those assets during checkout
when available; Scout also retains upstream's on-demand asset download fallback.

## When the viewer shows no files

Each computer needs its own runs path. On macOS, use an absolute `/Users/...`
path that exists on that Mac, or use `"$HOME/..."` in a shell command. A Windows
`C:/Users/...` path will not work there. A quoted `"~/..."` is not expanded by the
shell. Check that OneDrive logs are available locally.

Pulling the repository updates the checkout; it does not update an existing
non-editable installation or a running Scout process. Use the GitHub pip command
above in the environment that launches Scout, stop that viewer, then restart it.

To diagnose an empty viewer, leave Scout running and run this from the cloned
SCOUT-FIX repository, using the same Python environment as Scout:

```bash
python scripts/diagnose_transcripts.py http://127.0.0.1:7577
```

Replace the URL with your viewer's local address and port (often 7576 or 7577).
For the environment created above, use `.venv-scout/bin/python` on macOS/Linux
or `.venv-scout/Scripts/python.exe` on Windows. The script also runs with plain
Python 3.11+ without installing Scout, but then its package-version details
will describe that Python environment rather than the running server.

The output reports the selected folder, whether it exists, the number of `.eval`
files on disk, and transcript counts through the viewer API using both the native
path and browser URI. It reports whether a project filter is active. It prints
paths and counts, without transcript contents, and does not change configuration.
Share this output to distinguish path, installation, filter, and browser issues.

## Development

To work on development of Inspect Scout, clone the repository and install with the `-e` flag and `[dev]` optional dependencies:

```bash
git clone https://github.com/nurlaub-nlr/SCOUT-FIX.git
cd SCOUT-FIX
pip install -e ".[dev]"
```

Run linting, formatting, and tests via

```bash
make check
make test
```

### Frontend development (TypeScript)

The web UI lives in a git submodule and uses Git LFS for binary assets. **These steps are only needed if you plan to work on the TypeScript/React frontend** — Python-only contributors can skip this entirely.

1. [Install Git LFS](https://git-lfs.com/) and run `git lfs install`
2. Initialize the submodule and install dependencies — see the [one-time setup guide](src/inspect_scout/_view/ts-mono/docs/submodule-guide.md#one-time-setup)


