# Pytuitor agent guide

## Keep this document useful

Keep verified, durable decisions here; update existing guidance instead of appending a work log.
Stay near 100 lines and 1,000 words; put details in `docs/`, never secrets or temporary artifacts.

## Product direction

- Use Textual with an OpenCode feel, Python blue/yellow accents, and unchanged gray backgrounds.
- Serve motivated complete beginners and programmers seeking Python depth.
- The recommended course has 75 lessons and 21 Lantern Reach game milestones; standalone practice projects were retired in favor of the game.
- One syllabus has 21 chapters in five sections; the first three form the core sequence, with optional Python depth and specialized topics; see [the curriculum map](docs/curriculum.md).
- Keep authored learning and checks offline, progress local, and accounts unnecessary.
- Welcome offers Start learning or Browse syllabus; Known topics groups concepts by category.
- Batch onboarding transitions to avoid dashboard flashes.
- Known topics are skipped by Continue but remain accessible.
- Dashboard browses all chapters; Continue resumes the active chapter, then the core sequence or explicitly selected optional section.
- Lessons use blank Build then Repair; game milestones use cumulative Extend then independent Repair, with both required for completion.
- Prerequisites advise without blocking; references require explicit reveal and never replace drafts.
- Learner studies are user-run; automated tests do not establish teaching effectiveness.

## Teaching standards

- Explain new terms and syntax before requiring their use; use plain English and standard programming names.
- Foundations grows from values/input through collections/functions; Everyday Python and Building programs add files, modules, classes, tests, and automation.
- Depth lessons build on core concepts and explain Python-specific syntax and behavior.
- Make blank-editor exercises solvable: specify names, signatures, input handling, output, and edge cases.
- Prefer natural explanations and worked examples distinct from the required solution.
- Distinguish variables/values, print/return, and user input/prompt text.
- Verify correct reference programs pass and broken Repair programs fail meaningfully.
- Accept valid alternative implementations; test observable behavior rather than source spelling.
- Keep prose, hints, checks, repair code, and references synchronized; preserve full contracts when moving prose, and bump revisions when stage behavior changes.

## Interaction contracts

- Support keyboard-only use at 80 × 24; keep keybind help solely in F10, labeled Keybinds.
- Ctrl+T cycles lesson/editor/console, displayed `^t`; avoid Ctrl+number in legacy terminals.
- Footer order is numbered function keys, Ctrl shortcuts, then other keys.
- Thin blue outlines track actual focus, including mouse and Tab; omit pane tabs.
- Show the compact explorer only for stages with multiple files, inside the workbench directly left of the editor; Ctrl+E focuses it and Files toggles it.
- Mark required files and the Run starting file; keep the active file's role and Run target visible even with the explorer hidden, and refresh roles per stage.
- Dashboard single-click selects; double-click or Enter opens.
- Label the dashboard chapter selector and its lesson list explicitly; use odd-height Continue buttons so their labels center on terminal rows.
- Compact the dashboard for short as well as narrow terminals; at 120 × 30 keep the first chapter visible without resizing the user's window.
- At launch, local macOS Terminal/iTerm2 may receive one grow-only request for 120 × 30; never shrink or repeatedly resize, and honor `--no-resize`.
- Legacy track, practice, and study-note profile fields remain loadable but inert.
- Syllabus groups chapters by section with collapsed details and advisory prerequisites; only opening a lesson changes the resume anchor.
- Run streams output and accepts console answers; Enter submits and Ctrl+D ends input.
- Check selects the first failure; Checks and Details retain full evidence, including bounded authored observations without repeating learner operations.
- Restore per-stage file positions and check selection; saved reports require matching revision and source to describe current work.
- Optional mixed reviews use separate drafts and local scheduling; suggestions never block Continue or change the course resume anchor.
- Reset exercise backs up the complete current stage before restoring blank Build or broken Repair.
- Preserve drafts across curriculum updates, including renamed or additional required files.
- Start over is discoverable and confirmed; stop execution/autosave before clearing active progress.
- Run files previews generated text; saving explicitly backs up the workspace and refuses newer-draft conflicts.
- The tutor manages no virtual environments or packages; lessons need only the standard library, and `--check-upgrade` is its only network action.

## Code map and pitfalls

- `models.py` defines contracts; `beginner_course.py`, `beginner_extensions.py`, and `experienced_course.py` author courses; `curriculum.py` assembles catalog; `legacy.py` preserves original contracts.
- `lessons/*.md` contains prose; update [the curriculum map](docs/curriculum.md) when scope changes.
- Stage contracts live in `content/` chapter modules and the five Foundation records; see [the authoring guide](docs/authoring.md) and [challenge criteria](docs/teaching-criteria.md).
- `lesson_screen.py` owns stage/editor/console execution; `file_tree.py` renders workspace files; `screens.py` owns chapter navigation; `setup.py` owns onboarding.
- `learning_tools.py` owns file and reference dialogs; `app.py`, `ui.py`, `dialogs.py`, `theme.tcss` handle shell/shared UI.
- `course_map.py` defines chapter order; `project_catalog.py` assembles game content from `content/lantern/`; `syllabus.py` lists chapters by section.
- `project_workspace.py` owns immutable checkpoints and continuation; keep extra inherited capability checks via its active contract and never replace learner source silently.
- `project_screen.py` owns game history, explicit supplied bases, restoration, temporary checkpoint play, and portable exports.
- `review_screen.py` and `review_progress.py` own optional review; `content/reviews/` authors 21 mixed sessions.
- `state.py` owns version 4 profiles, atomic writes, migration backups and locks.
- Save with file sync and Unix directory sync or Windows write-through replacement; never roll back memory after a committed rename.
- Build lives in the lesson entry; Repair is nested under `repair`; each stage has a `files` map and compatibility `code` for its entry point.
- `runner.py` launches standard-library-only `_worker.py`; `execution_policy.py` owns process rules, `_windows.py` owns Win32 jobs and handles, and `run_files.py` reads bounded snapshots.
- Checks receive fresh namespaces, local imports, working directories, supplied stdin, and individual execution time budgets.
- Compare the entire file snapshot before marking an asynchronous check successful.
- Input-wait time must not consume execution timeout; kill descendant processes during cancellation.
- Process isolation and resource limits are not an OS security sandbox.
- Guard async UI callbacks against cancellation, changed drafts, and unmounted screens.
- Keep pane selection and restored focus synchronous; delayed view restoration must not steal newer focus, and stale bubbled focus notifications must be ignored.
- `workspace.py` validates paths and limits, and exports without overwrite.
- OptionList custom click handlers need `prevent_default()` to suppress inherited activation.

## Working and verification

- Keep the README's centered branding, authentic app preview, and curated directory layout; store its visual assets in `docs/assets/`.
- Reproduce bugs through the learner UI first; retain meaningful regressions.
- Use scratch `--data-dir` profiles; never test against the user's progress.
- Keep the checkout's Python interpreter in a persistent installation, never a temporary directory; virtual environments depend on that base interpreter remaining intact.
- Run `uv sync --locked`, `uv run pytest`, `uv run ruff check .`, and `uv run ruff format --check .`.
- Keep verification local; do not create or enable GitHub CI unless the user explicitly requests it.
- Give large pytest parameters short explicit IDs; Windows limits the `PYTEST_CURRENT_TEST` environment value.
- Use Textual Pilot plus real Unix PTY and Windows ConPTY journeys; test Windows PowerShell 5.1/7, Unicode paths, EOF, cancellation, and resizing.
- Windows support uses Job Objects, byte-range profile locks, and reparse-point-safe reads; do not substitute Unix APIs or require symlink privileges.
- Inspect 80 × 24 and 140 × 44 screenshots; fix clipping, wrapping, focus ambiguity, lint failures, and flakiness.
- Use `env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor` for visual checks; temporary artifacts belong in `.artifacts/`.
- Build with `uv build`; run `scripts/smoke_installed.py` against the installed wheel with isolated Python.
- See [release checks](docs/release-checklist.md) and [learner study](docs/learner-study.md); report only validation actually performed.
- Never use em dashes, agent co-authors, or manual changelog/generated-file edits.
- Long Markdown uses one sentence per line; subagents need per-task permission.
- Make local commits when Git metadata exists; only push or publish when instructed.
- Suggest a concrete next step after major work.
