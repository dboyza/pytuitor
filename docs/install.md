# Installation and upgrades

Pytuitor targets macOS and Linux with Python 3.11 or newer.
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
