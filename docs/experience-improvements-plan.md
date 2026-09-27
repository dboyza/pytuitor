# Learning experience implementation plan

Status: all six improvements implemented and verified locally on 2026-09-27.

## Product decisions

Keep Build or Extend followed by a required, distinct Repair.
Use focused Repairs for smaller concepts and fuller debugging tasks where the chapter warrants them.
Reviews mix prediction, debugging, and small coding exercises, with gentle optional suggestions after chapter completion and on later visits.
Reviews never gate Continue or change course completion.
Milestone success is an inline capability summary with explicit Play and Next actions.
Returning learners resume their active file, cursor, pane, reading position, and selected check, with a dashboard recap and optional personal note.
Keep the Textual interface, existing colors, offline operation, and local progress.

## 1. Actionable check feedback

Show the first failing case before passing cases and preserve the learner's selected case during a running check.
Show a concrete scenario, expected value, actual value, and relevant hint.
Author structured observations inside compound Lantern Reach scenarios so an opaque boolean result is accompanied by the state or operation that differed.
Keep original inputs, printed output, running status, exceptions, and full check evidence accessible through explicit details and case selection.
Never evaluate learner operations twice merely to generate feedback.
Keep worker events bounded and validate optional evidence before it reaches the UI.
Preserve changed-draft, cancellation, and revision protections.

## 2. Visible game achievements

Author a concise capability outcome for every milestone and show it after the exact Extend source passes.
Offer Play this version directly from the workbench using the existing immutable-checkpoint player.
Next still enters the independent Repair until both stages pass.
Separate the core course and core game from optional extensions in dashboard and game progress summaries.
Known topics remain distinct from completed work.

## 3. Milestone implementation briefs

Author all 21 briefs with the existing capability, the addition, retained behavior, and an example interaction.
Refactoring briefs explain the intended file roles and public interfaces without rewriting learner code.
Show the brief before the longer explanation while retaining complete exercise contracts.
Use the same authored outcome for the game overview and success message.

## 4. Resume and personal notes

Save presentation state separately for each stage and each edited file.
Clamp restored cursor and scroll positions to current files and terminal dimensions; missing files and changed revisions fall back safely.
Retain bounded check evidence with a source fingerprint and revision, and label earlier results when the draft changes.
Persist the selected check and disclosure state without treating restored evidence as new completion.
Keep a short editable personal note per course activity, separate from legacy inert study-note fields.
Dashboard recaps identify the saved stage and meaningful next action; an old check must not imply that an edited draft still passes.
No background editor may overwrite restored or reset work.

## 5. A calmer workbench

Keep Run, Check, Next, file identity, and the current objective visible.
Move occasional workspace operations into a discoverable Tools surface while retaining command-palette access.
Keep the compact file tree conditional on multiple files.
Keep check summaries concise and expand full evidence deliberately.
Support keyboard-only operation at 80 by 24, and preserve focus indication and portable shortcuts.

## 6. Repair pacing and optional review

Audit all required Repairs for scope, prerequisites, and distinctness, then make targeted authored changes where the workload is disproportionate.
Expose honest stage-specific effort guidance and debugging focus; estimates are guidance rather than measured learner timings.
Do not weaken behavior checks just to shorten a task, and bump revisions when the learner contract changes.
Author one short mixed review session for every chapter, with three distinct tasks per session.
Prediction tasks explain the answer; debugging and coding tasks have explicit contracts, references, hints, and real runner checks.
Preserve unfinished review work separately from ordinary lesson drafts and the course resume anchor.
Schedule suggestions locally after completed chapters, then use a simple documented interval sequence after successful reviews.
Allow learners to defer or pause suggestions and to open any review explicitly with advisory preparation.
Review assistance and retries do not fabricate course achievements.

## Implementation and verification

Implement shared feedback and persistence boundaries first, then authored game briefs, workbench integration, review content and scheduling, and pacing refinements.
Use explicit content records and small services rather than duplicate execution engines or source rewriting.
Existing version 4 profiles must remain loadable; additive optional presentation/review fields must not alter existing course or checkpoint records.
Test damaged or stale presentation metadata, revised content, save failures, cancellation, changed drafts, and switching files or stages during delayed work.
Use scratch profiles for all journeys and leave the existing local Neovim log untouched.
Run reference and broken-program audits, complete review sessions, game success/play, reopen/resume, and keyboard navigation through real learner surfaces.
Inspect actual Textual screenshots at 80 by 24 and 140 by 44; regenerate visual baselines only for reviewed intentional changes.
Run locked sync, full tests, Ruff lint/formatting, package build, and isolated installed-wheel smoke.
Make local commits, with no push or publication.
Report unavailable platform checks and do not claim measured learning improvements without a learner study.

## Completed validation

- Locked dependency synchronization passed on macOS with Python 3.12.13.
- The full test suite passed: 916 passed, 7 platform-specific skips.
- The final layout and review checks passed: 84 tests, followed by 12 visual baseline tests without update mode.
- Ruff lint, formatting, and Git whitespace checks passed.
- The wheel and source distribution built successfully and exclude local logs, caches, and scratch artifacts.
- A fresh isolated wheel installation passed all 216 required stage references and 42 coding-review references, plus game continuation, reopening, and export.
- The review audit verified all 21 prediction answers and all 21 broken debugging starters in addition to the 42 coding references.
- All 19 command-based milestone examples ran and matched their displayed output.
- Direct screenshot inspection covered compact and wide workspaces, game success, review tasks, notes, tools, and the review hub.
- Real Unix PTY journeys passed as part of the full suite; native Windows ConPTY and Windows desktop checks were not run on this Mac.
- A user-run learner study remains the next step for evaluating pacing and teaching effectiveness.

The implementation and durable interaction rules are described in [the learning experience guide](learning-experience.md).
