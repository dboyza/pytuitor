<p align="center">
  <img src="docs/assets/logo.svg" width="96" height="96" alt="Pytuitor logo: an open book with a terminal prompt">
</p>
<h1 align="center">Pytuitor</h1>
<p align="center"><strong>Learn Python.
Build it.
Repair it.</strong><br>An offline Python tutor, right in your terminal.</p>
<p align="center">
  <a href="#start-learning">Start learning</a> ·
  <a href="#preview">Preview</a> ·
  <a href="docs/curriculum.md">Curriculum</a> ·
  <a href="#development">Development</a> ·
  <a href="https://github.com/dboyza/pytuitor/issues">Report an issue</a>
</p>
<p align="center"><strong>75 lessons</strong> &nbsp; / &nbsp; <strong>12 projects</strong> &nbsp; / &nbsp; <strong>No account required</strong></p>

## Start learning

For macOS and Linux, with [uv](https://docs.astral.sh/uv/getting-started/installation/) installed and a terminal at least **80 × 24**:

```sh
git clone https://github.com/dboyza/pytuitor.git
cd pytuitor
uv run --locked pytuitor
```

Already have the checkout?
Run the last command from its root.
The first launch installs Python 3.11+ and dependencies if needed, then opens the welcome screen.
Select **Start learning** for your first lesson or **Browse syllabus** to explore.
After setup, lessons, hints, reference solutions, and checks work offline, with progress saved locally.

**Release candidate:** Pytuitor is not yet published to PyPI.
See [installation and upgrades](docs/install.md) for a standalone wheel installation or help recovering a broken environment.

## Preview

<a href="docs/assets/learning.svg"><img src="docs/assets/learning.svg" width="100%" alt="Pytuitor at 140 by 44 terminal cells, with a Python lesson on the left and a blank Build editor and console on the right"></a>

*Read the lesson, write your code, and check the result in one workspace.*
At smaller terminal sizes, **Ctrl+T** switches between the lesson, editor, and console.

## Learn by doing

Start as a complete beginner or deepen your existing Python knowledge.

- **Build, then repair.** Start each unit with a blank editor, then debug a broken program.
  Both stages count toward completion, with separate saved drafts.
- **Understand the result.** Run code with interactive input, then check observable behavior against expected results.
  Hints and explicitly revealed reference solutions help when you get stuck.
- **Follow your own path.** Start from the basics or mark known topics to skip them when continuing.
  Prerequisites guide you without locking lessons.
- **Grow into real projects.** Work across files, export your code, and optionally create project environments.
  Package installation is an explicit network action.
- **Pick up where you left off.** Your progress and drafts stay on your machine, without an account.

### A course that grows with you

The 21 chapters span five sections.
The first three form the core sequence; the last two offer optional depth.

| Section | What you will explore |
| --- | --- |
| Foundations | Values, input, decisions, collections, loops, and functions |
| Everyday Python | Files, structured data, regular expressions, and library tools |
| Building programs | Modules, classes, tests, and automation |
| Python depth | Python-specific behavior, composition, and object protocols |
| Specialized topics | Async programming, distribution, and language machinery |

See the [curriculum map](docs/curriculum.md) for chapters, projects, and preparation.

## Make yourself at home

| Key | Action |
| --- | --- |
| **Ctrl+T** | Cycle through lesson, editor, and console |
| **Ctrl+R** | Run your program |
| **F5** | Check your work |
| **F10** | Open all keybinds |
| **Ctrl+P** | Open commands, including export, reset, and project tools |

When your program asks a question, type in the console and press **Enter**.
Use the file menu for multi-file projects.

For a separate learning profile, run:

```sh
uv run --locked pytuitor --data-dir ./practice-profile
```

**Start over** resets the active profile after confirmation; exported work is kept.
See [workspace behavior](docs/workspaces.md) for drafts, files, exports, and environments.
Learner code runs locally with resource limits; subprocesses and virtual environments are not an operating-system security sandbox.

## Development

### Repository layout

```text
pytuitor/
├── src/pytuitor/
│   ├── app.py              Textual application shell
│   ├── setup.py            Welcome and onboarding
│   ├── screens.py          Dashboard and chapter navigation
│   ├── lesson_screen.py    Build/Repair editor, console, and execution UI
│   ├── curriculum.py       Assembled lesson catalog
│   ├── course_map.py       Sections, chapters, and project preparation
│   ├── lessons/            Authored lesson explanations
│   ├── runner.py           Learner program execution
│   ├── _worker.py          Isolated Python worker
│   ├── state.py            Local profiles, progress, and drafts
│   ├── workspace.py        Project files, exports, and environments
│   └── theme.tcss          Terminal layout and styling
├── tests/                  Curriculum, execution, state, and UI journeys
├── scripts/                Installed-wheel smoke checks and release tooling
├── docs/                   Curriculum, installation, and contributor guides
│   └── assets/             README logo and application preview
├── pyproject.toml          Package metadata and development tools
└── uv.lock                 Locked dependencies
```

### Run the checks

From the repository root:

```sh
uv sync --locked
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv build
```

See the [release checklist](docs/release-checklist.md) for installed-wheel validation and the [learner study guide](docs/learner-study.md) for evaluating the teaching experience.
Found a problem?
[Open an issue](https://github.com/dboyza/pytuitor/issues) with your launch command, terminal, and the error or lesson involved.
