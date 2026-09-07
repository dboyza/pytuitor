# Pytuitor MVP

This document records the original MVP.
For the current release candidate, use the [v1 scope](v1-plan.md) and [curriculum map](curriculum.md).

## Product contract

Pytuitor is a local Python apprenticeship for motivated complete beginners and learners with a computer science or programming background.
Its first release supports two short paths with a built-in editor, authored offline teaching, and persistent local progress.
The visual direction is a calm dark developer workspace with Python blue/yellow accents on unchanged gray backgrounds, minimal borders, readable spacing, and keyboard navigation.

The MVP demonstrates the complete learning loop rather than claiming that twelve exercises produce expert-level proficiency.
Experienced lessons introduce semantics, advanced features, and tooling; these become deeper modules in later releases.

## First launch and navigation

Onboarding lets learners choose Beginner, Experienced, or Custom, with a preview of each path's lesson topics.
Custom includes both courses in order, with familiar concepts checked off to skip lessons the learner already knows.
The same checklist is available with either standard path.
There are no placement questions or diagnostic.

The dashboard shows the chosen path, its progress, one Continue action, and one lesson list with projects included.
Edit path is the single entry point for changing paths and known topics; alternate paths are not dashboard navigation.
Start over remains available as a secondary action.
Every lesson in the selected path stays accessible even if its concepts were skipped.
States distinguish new, in progress, familiar, and completed.
Continue resumes the latest unfinished lesson in the selected path, otherwise selecting its first unfinished lesson whose concepts are not all familiar.
Passing Build and Repair marks a lesson completed.
Build starts blank and unlocks Repair, which contains a complete but broken program with the same requirements.
The concept question is optional practice.
Completion is historical: later experimentation does not erase demonstrated progress, while resetting an exercise does.

## Curriculum

| Stage | Beginner | Experienced |
| --- | --- | --- |
| 1 | Your first program: strings, integers, output | Objects and copying |
| 2 | Variables and input | Arguments and decorators |
| 3 | Making decisions: if, elif, else | Iterators and generators |
| 4 | Lists and loops | Context managers and async |
| 5 | Writing functions | Types and tests |
| Project | Build a text adventure | Build a log analyzer |

Each unit has an explanation, two coding stages, optional prediction, hints, behavioral checks, and a reference solution used in curriculum validation.
Learners can experiment using Run and validate requirements using Check.
Checks stream running and finished events and show inputs, the operation being tested, expected and actual results, printed output, and pass/fail for every case.
Console output and function return values are labeled separately; tests that do not require printing say so explicitly.
Each case executes the learner's program in a fresh namespace with its own supplied input.
The experienced testing lesson validates learner-authored tests against deliberately broken implementations.
The async lesson checks concurrent scheduling, and the generator lesson checks lazy consumption of an infinite stream.

The CLI capstone exports as a runnable single Python file.
Packaging and environments are introduced through explanations; an interactive multi-file packaging lab is future work.

## Architecture

- `curriculum.py` holds immutable lesson and check definitions, separately from UI behavior.
- `lessons/*.md` contains authored explanations, worked examples, and exercise instructions.
- `state.py` owns versioned JSON profiles, atomic replacement, and an advisory single-writer lock.
- `runner.py` manages asynchronous child execution, cancellation, output limits, and temporary workspaces.
- `_worker.py` runs in Python isolated mode using only the standard library and evaluates authored checks.
- `app.py` owns the theme, profile, command palette, and application navigation.
- `screens.py` implements the dashboard for the selected path; `setup.py` owns path selection and known topics together.
- `lesson_screen.py` owns the editor and interactive console; `dialogs.py` owns keyboard help and reset confirmations.

Each run uses a fresh process and working directory, a five-second active execution timeout, a CPU limit, and bounded output capture.
Run streams output and accepts keyboard input through a subprocess pipe.
The execution timeout pauses while the program waits for an answer.
Check supplies authored inputs, with independent executions for input-specific test cases.
The worker inherits a minimal environment rather than account tokens or project environment variables.
Linux also applies an address-space limit.
Cancellation terminates the process group so ordinary child processes are cleaned up as well.
Process isolation and Python isolated mode are not an OS security sandbox: learner code retains the user's filesystem and network permissions.
Exercise checks are teaching aids, not adversarial grading infrastructure.

Profiles store drafts, hints, prediction state, completion, and familiar concepts.
Older profiles retain progress and drafts when loaded; obsolete onboarding answers are removed.
Revised exercises preserve older drafts and offer a backed-up reset to the current starter.
Unreadable or unsupported profiles are preserved and reported rather than silently overwritten.
Reset exercise first exports a timestamped backup, then clears the current stage's pass status and restores its initial code: blank for Build, broken for Repair.
The other stage's draft remains intact.
The same export action is available independently from the command palette.
Start over requires confirmation, stops any running program, clears the active profile, and returns to onboarding.
Previously exported files remain available.

Every flow supports keyboard navigation, with F10 help and a command palette.
Ctrl+T cycles through the lesson, editor, and console, switching visible panes on narrow terminals.
F7 focuses the lesson question, F8 stops execution, and Ctrl+B returns to the dashboard.

## Validation

Tests exercise path selection, skipped-topic revisiting, keyboard-only lesson completion, next-lesson navigation, restart and resume, projects, export, reset, and execution cancellation.
Curriculum tests verify that every reference solution passes, every Build starts blank, and every Repair contains a failing case.
Runner tests cover syntax errors, interactive input, end of input, timeouts, excessive output, and recovery.
Profile tests cover persistence, malformed data, and concurrent writers.
Visual artifacts are generated at 80 × 24 and 140 × 44 for layout inspection.
The CI workflow runs the suite on macOS and Linux with Python 3.11 and 3.13.
Adding that workflow does not mean those remote jobs have run; local validation is reported separately.

## Next milestones

1. Observe beginners and experienced programmers using the first chapter without coaching.
2. Expand the experienced lessons into focused modules with multiple transfer exercises per concept.
3. Add multi-file projects, guided environments, and a packaging lab.
4. Add curated execution walkthroughs with variables and call frames.
5. Introduce spaced review based on observed mistakes and independent follow-up challenges.

Accounts, cloud synchronization, AI tutoring, third-party course loading, and Windows support are outside this MVP.
