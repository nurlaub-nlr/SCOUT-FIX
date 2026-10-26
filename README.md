# SCOUT-FIX

A fork of [Inspect Scout](https://github.com/meridianlabs-ai/inspect_scout),
based on release **0.6.1**, with a fix for local transcript folders whose paths
contain spaces or Unicode characters. The viewer now decodes local `file://`
addresses before opening the transcript source.

Repository: [nurlaub-nlr/SCOUT-FIX](https://github.com/nurlaub-nlr/SCOUT-FIX).

**Draft status:** local preview testing is in progress. The installation commands
below are for after the fixed revision has been published to `main`; GitHub
installation validation is still pending. See [preview notes](FORK_TESTING.md)
for the completed checks, restart instructions, and known limitations.

## Install from GitHub

Requires Python 3.11 or later and Git. Run these commands from the project where
you want to use Scout, after the fork is published.

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


