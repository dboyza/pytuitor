# Pytuitor agent guide

## Keep this document useful

Keep durable decisions and recurring pitfalls here, not a chronological work log.
After meaningful changes, update the relevant section, merge duplicates, and remove superseded guidance.
Stay below roughly 100 lines and 1,000 words; put details in `docs/`.
Do not record temporary paths, screenshots, test counts, speculative plans, or secrets.
Verify implementation details against code.

## Product direction

- Use Textual with an OpenCode feel, Python blue/yellow accents, and unchanged gray backgrounds.
- Serve motivated complete beginners and programmers seeking Python depth.
- The v1 candidate has 75 lessons and 12 chapter projects.
- One syllabus has 21 chapters in five sections; the first three form the core sequence, with optional Python depth and specialized topics; see [the curriculum map](docs/curriculum.md).
- Keep authored learning and checks offline, progress local, and accounts unnecessary.
- Welcome offers Start learning or Browse syllabus; Known topics is a category-grouped checklist.
- Batch onboarding screen changes so the dashboard stays behind the destination without flashing.
- Known topics are skipped by Continue but remain accessible; project concepts describe their relevant preparation.
- Dashboard browses all chapters; Continue resumes the active chapter, then the core sequence or explicitly selected optional section.
- Every course unit has blank Build followed by broken Repair, with separate saved drafts and both required for new completion.
- Prerequisites advise without blocking; reference solutions require explicit reveal and never replace drafts.
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
- Keep prose, hints, checks, repair code, and references synchronized.

## Interaction contracts

- Support keyboard-only use at 80 × 24; keep keybind help solely in F10, labeled Keybinds.
- Ctrl+T cycles lesson/editor/console, displayed `^t`; avoid Ctrl+number in legacy terminals.
- Footer order is numbered function keys, Ctrl shortcuts, then other keys.
- Thin blue outlines track actual focus, including mouse and Tab; omit pane tabs.
- Dashboard single-click selects; double-click or Enter opens.
- Label the dashboard chapter selector and its lesson list explicitly; use odd-height Continue buttons so their labels center on terminal rows.
- Legacy track, practice, and study-note profile fields remain loadable but inert.
- Syllabus groups chapters by section with collapsed details and advisory prerequisites; only opening a lesson changes the resume anchor.
- Run streams output and accepts console answers; Enter submits and Ctrl+D ends input.
- Check reports each operation, input, expected/actual result, printed output, and running/pass/fail status.
- Reset exercise backs up the complete current stage before restoring blank Build or broken Repair.
- Preserve drafts across curriculum updates, including renamed or additional required files.
- Start over is discoverable and confirmed; stop execution/autosave before clearing active progress.
- Run files previews generated text; saving explicitly backs up the workspace and refuses newer-draft conflicts.
- Project environments are optional; creation is offline and package installation is an explicit network action.
- Install named wheels into a project venv, without shell interpolation, source builds, or automatic downloads.

## Code map and pitfalls

- `models.py` defines contracts; `beginner_course.py`, `beginner_extensions.py`, and `experienced_course.py` author courses; `curriculum.py` assembles catalog; `legacy.py` preserves original contracts.
- `lessons/*.md` contains prose; update [the curriculum map](docs/curriculum.md) when scope changes.
- Stage-specific authoring uses `StageContract`; see [the authoring guide](docs/authoring.md).
- `lesson_screen.py` owns stage/editor/console execution; `screens.py` owns chapter navigation; `setup.py` owns onboarding.
- `learning_tools.py` owns file, reference, and environment dialogs; `app.py`, `ui.py`, `dialogs.py`, `theme.tcss` handle shell/shared UI.
- `course_map.py` defines section/chapter order and project preparation; `syllabus.py` renders it.
- `state.py` owns version 3 profiles, atomic writes, migration backups and locks.
- Build lives in the lesson entry; Repair is nested under `repair`; each stage has a `files` map and compatibility `code` for its entry point.
- `runner.py` launches `_worker.py` with isolated Python; worker must remain standard-library-only.
- Checks receive fresh namespaces, local imports, working directories, and supplied stdin.
- Compare the entire file snapshot before marking an asynchronous check successful.
- Input-wait time must not consume execution timeout; kill descendant processes during cancellation.
- Process isolation, venvs, and resource limits are not an OS security sandbox.
- Guard async UI callbacks against cancellation, changed drafts, and unmounted screens.
- Keep pane selection and focus synchronous; ignore bubbled focus notifications for widgets that no longer hold focus.
- `workspace.py` validates paths and limits, exports without overwrite, and manages explicit environment commands.
- Create venvs at their final path; moving them breaks interpreter paths and shebangs.
- OptionList custom click handlers need `prevent_default()` to suppress inherited activation.

## Working and verification

- Keep the README's centered branding, authentic app preview, and curated directory layout; store its visual assets in `docs/assets/`.
- Reproduce bugs through the learner UI first; retain meaningful regressions.
- Use scratch `--data-dir` profiles; never test against the user's progress.
- Keep the checkout's Python interpreter in a persistent installation, never a temporary directory; virtual environments depend on that base interpreter remaining intact.
- Run `uv sync --locked`, `uv run pytest`, `uv run ruff check .`, and `uv run ruff format --check .`.
- Use Textual Pilot for journeys and real PTY input for terminal shortcut compatibility.
- Inspect 80 × 24 and 140 × 44 screenshots; fix clipping, wrapping, focus ambiguity, lint failures, and flakiness.
- Use `env -u NO_COLOR TERM=xterm-256color COLORTERM=truecolor` for visual checks; temporary artifacts belong in `.artifacts/`.
- Build with `uv build`; run `scripts/smoke_installed.py` against the installed wheel with isolated Python.
- See [release checks](docs/release-checklist.md) and [learner study](docs/learner-study.md); report only validation actually performed.
- Never use em dashes, add agent co-authors, or manually edit changelogs/generated files.
- Put each full sentence on its own physical line in long Markdown.
- Use subagents only when explicitly requested for the current task.
- Make local commits when Git metadata exists; only push or publish when instructed.
- Suggest a concrete next step after major work.

## Maintaining this file

Keep this file for knowledge useful to almost every future agent session in this project.
Do not repeat what the codebase already shows; point to the authoritative file or command instead.
Prefer rewriting or pruning existing entries over appending new ones.
When updating this file, preserve this bar for all agents and keep entries concise.
