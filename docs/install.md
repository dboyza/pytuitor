# Installation and upgrades

Pytuitor supports Windows 10/11, macOS, and Linux with Python 3.11 or newer, including Python 3.14.
Use a trusted checkout or a verified wheel from the maintainer.
This release candidate has not been published to a package index.
Do not install an unrelated package merely because it uses the same name.

## Install this checkout as a standalone tool

With [uv](https://docs.astral.sh/uv/guides/tools/) installed, run these commands from the checkout:

```sh
uv build
uv tool install ./dist/pytuitor-1.0.0rc1-py3-none-any.whl
pytuitor --version
pytuitor
```

The tool gets a separate environment and does not change your system Python packages.
If uv reports that its executable directory is missing from PATH, follow its `uv tool update-shell` instructions and reopen your terminal.
Initial installation may download dependencies; subsequent learning works offline.

If you already use [pipx](https://packaging.python.org/en/latest/guides/installing-stand-alone-command-line-tools/), the equivalent installation is:

```sh
pipx install ./dist/pytuitor-1.0.0rc1-py3-none-any.whl
pytuitor --version
```

No administrator privileges or downloaded shell installer is required for Pytuitor itself.
Before installing a downloaded release, compare its SHA-256 checksum against the manifest obtained from the trusted release page.
A checksum detects changed bytes; it does not establish the identity of an untrusted publisher.

## Windows Terminal and PowerShell

Use Windows Terminal with Windows PowerShell 5.1 or PowerShell 7 and a window at least 80 columns by 24 rows.
The current [Windows Terminal requirements](https://github.com/microsoft/terminal#installing-and-running-windows-terminal) specify Windows 10 version 2004 (build 19041) or newer; Windows 11 meets that requirement.
PowerShell ISE is a script editor, not a supported interactive terminal host.
WSL is not required.

From a trusted checkout, run:

```powershell
uv sync --locked
uv run --locked pytuitor
```

For a standalone installation from that checkout:

```powershell
uv build
uv tool install .\dist\pytuitor-1.0.0rc1-py3-none-any.whl
pytuitor --version
pytuitor
```

These commands do not activate a PowerShell script, so no execution-policy change is needed.
Administrator access and Developer Mode are not required to complete the authored exercises.
If an external project needs a virtual environment, invoke its interpreter directly with `& .\.venv\Scripts\python.exe` rather than requiring activation.
Use `py -3.14 -m venv .venv` to create it when that Python version is installed through the Python launcher.

The default profile is `%LOCALAPPDATA%\pytuitor`; use `--data-dir` to select a separate profile, including paths containing spaces or Unicode:

```powershell
uv run --locked pytuitor --data-dir "$env:LOCALAPPDATA\pytuitor-review"
```

Ctrl+T cycles panes, F4 focuses exercise requirements, F5 checks, Ctrl+R runs, and F8 stops execution.
While the console is waiting for input, Enter sends an answer and Ctrl+D ends input on Windows too.
F10 lists every shortcut.
If a custom Windows Terminal shortcut intercepts a key, remove that binding or use the alternative shown in F10.

## Recover a broken checkout environment

If `uv run --locked pytuitor` fails while querying Python or reports `No module named 'encodings'`, the checkout's `.venv` may point to a removed or incomplete Python installation.
Check `.venv/pyvenv.cfg` for the base interpreter location.
Keep that interpreter in a persistent location, not `/tmp` or `/private/tmp`.

Close Pytuitor, then run these commands from the checkout with no virtual environment activated:

```sh
uv python install 3.12
mv .venv .venv-backup
uv sync --locked --managed-python --python 3.12
uv run --locked pytuitor
```

In PowerShell, use `Rename-Item .venv .venv-backup` in place of `mv .venv .venv-backup`.
Choose a different backup name if `.venv-backup` already exists.
Leave `UV_PYTHON_INSTALL_DIR` unset so uv uses its persistent default installation directory.
This rebuilds dependencies without changing your saved learner profile.
The old environment is retained as a backup, but should not be run from its moved location.

## Upgrade deliberately

Close Pytuitor before replacing its installed version.
Back up your profile directory before upgrading, especially when trying prereleases.
Install the exact replacement wheel with `uv tool install --force /path/to/verified-wheel.whl` or `pipx install --force /path/to/verified-wheel.whl`.
These are placeholder paths; substitute the actual artifact you reviewed.

`pytuitor --check-upgrade` explicitly contacts PyPI and prints installed and published versions without installing anything.
It can report an error while this project has no published release.
Startup and lessons never run this lookup.

Version 3 profiles preserve previous lesson drafts and create `profile-before-v3.json` when first saving a migrated profile.
Old drafts remain available when a lesson changes, with an explicit reset option.
The previous application may not understand a newer profile, so use the backup with a separate `--data-dir` when testing a downgrade.

Project virtual environments and dependency installation are described in [workspace behavior](workspaces.md).
Third-party packages run with your user's permissions, so install only packages you trust.
