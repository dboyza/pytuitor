# pytuitor

An offline Python tutor for complete beginners and programmers who want to understand Python deeply.
The v1 release candidate contains 75 lessons and 12 chapter projects, with a blank Build exercise followed by a broken program to Repair.

## Start learning

From this checkout, with [uv](https://docs.astral.sh/uv/getting-started/installation/) installed:

```sh
uv run --locked pytuitor
```

The first run installs Python and dependencies if needed.
Lessons, hints, reference solutions, checks, and progress then work offline.
Choose a path, mark topics you already know, and select **Continue**.
Browse chapters to revisit any lesson; prerequisites are guidance, not barriers.

Designed for macOS and Linux, Python 3.11+, and terminals at least 80 × 24.
Press **Ctrl+T** to cycle through lesson, editor, and console, **Ctrl+R** to run, **F5** to check, and **F10** for all keybinds.
When your program asks a question, type the answer in the console and press Enter.
Use the file menu for multi-file projects and **Ctrl+P** for export, reset, and project tools.

Progress and separate Build/Repair drafts are saved locally.
**Start over** resets the active profile after confirmation; exported work is kept.
Use `uv run --locked pytuitor --data-dir ./practice-profile` for a separate profile.

This candidate is not yet published to PyPI.
See [installation and upgrades](docs/install.md) for a standalone installation from the local wheel.

## Development

```sh
uv sync --locked
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv build
```

See [workspace behavior](docs/workspaces.md), [the curriculum map](docs/curriculum.md), [learner study scripts](docs/learner-study.md), and [release checks](docs/release-checklist.md).
Learner code runs locally with resource limits; a subprocess or virtual environment is not an operating-system security sandbox.
