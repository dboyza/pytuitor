# One Python app that grows through the course

Status: proposal for review, not an implemented curriculum change.

## Recommendation

Give Pytuitor a continuing project called **Fieldbook**, a local command-line app for tracking small jobs, notes, supplies, and activity reports.
The name is provisional; the important decision is one understandable domain and the learner's own code carried forward.
It starts as a few printed lines and becomes a tested, persistent, exportable Python application.
Optional chapters extend it with streaming, typed boundaries, asynchronous processing, packaging, and plugins.
The core course should end with a useful, complete app even if the learner never takes those extensions.

Dockyard provides the relevant pattern: an evolving Dispatch application, immutable mission checkpoints, explicit continuation, and supplied checkpoints for later entry.
Its supplied business logic is appropriate for teaching infrastructure.
Pytuitor should instead make writing and understanding that business logic the learning activity.

## Learning rhythm

Keep short lessons and their independent blank Build and authored Repair exercises.
Each lesson includes a short connection to the relevant Fieldbook feature, without requiring an extra project assignment after every lesson.
At chapter boundaries, a project milestone asks the learner to extend their last working Fieldbook checkpoint.
Show three things: what already works, the new user-visible behavior, and how to demonstrate it.
After checking the extension, the learner fixes a separate, authored incident in the same domain.

Milestone **Extend** starts from previous project code and therefore needs its own explicit stage policy.
Do not silently redefine ordinary blank Build exercises or add a third mandatory stage to all 75 lessons.
Milestone **Repair** uses an authored broken workspace with a distinct scenario and matching prerequisite level, rather than trying to inject defects into arbitrary learner code.
The successful Extend snapshot supplies future milestones; Repair code never replaces it.
Passing Extend produces a usable checkpoint, while passing both stages records the milestone as complete.
Require an explicit action to advance so an asynchronous check cannot unexpectedly change the learner's workspace.

## Course-wide progression

These are proposed feature outcomes aligned with the current chapter order, not final exercise contracts.
Small chapters get small milestones; avoid turning every checkpoint into a capstone.

| Current chapter | What Fieldbook gains |
| --- | --- |
| First programs | Print a job card, ask for a name and quantities, calculate an estimate, and label its priority. |
| Lists and sets | List several jobs and identify unique or missing supply labels. |
| Loops and dictionaries | Store job records, count states, edit records, and repeat a small menu. |
| Functions and input | Extract reusable operations and recover from invalid commands and numbers. |
| Files and structured data | Save and reload JSON; import or export a documented CSV report. |
| Text patterns | Validate job reference codes and extract references from notes. |
| Modules and library tools | Split the app into modules; add CLI options, summary statistics, and repeatable sample data. |
| Dates and times | Add due dates and an overdue report. |
| Collection tools | Filter and group jobs and process a first-in, first-out work queue. |
| Classes and tested tools | Model a job and named states; write tests for the existing behavior. |
| Careful automation | Preview an archive/export operation and refuse accidental overwrites. |
| Python semantics | Make update and copy behavior deliberate so editing a draft cannot mutate an original record. |
| Recursion and functional tools | Traverse nested job groups and support selectable sort/filter functions. |
| Decorators | Wrap operations with activity recording while preserving arguments and metadata. |
| Iterators and streaming | Process large activity files incrementally and bound report consumption. |
| Exceptions and contexts | Add domain errors and reliably restore resources during failed operations. |
| Dataclasses and types | Introduce typed record values with validated defaults and updates. |
| Object protocols and testing | Separate storage/reporting interfaces and test effects through injected dependencies. |
| Coordinate async work | Coordinate several supplied offline async sources with bounded work and cancellation. |
| Build distributable tools | Package the CLI with predictable imports, paths, exit behavior, and metadata. |
| Understand the machinery | Add an optional formatter extension system and inspect its callable contracts. |

Early versions must use only syntax already taught: no supplied class framework, hidden persistence layer, or decorators in the first chapters.
Keep one source file until modules have been introduced.
Use fixed local fixtures and standard-library operations for course checks.
No database, web server, account, or network API is required to complete the app.
Advanced refactors should solve an explained problem; they do not imply that every small Python app needs these abstractions.

## Fit with the existing projects

For an initial pilot, add Fieldbook alongside the unchanged course and keep its completion separate.
After validating the learning flow, make its milestones the recommended cumulative project sequence.
Map the 12 existing standalone projects to suitable milestones and retain their original IDs, drafts, and completion as optional independent practice.
Do not require both the old standalone projects and their replacements in the recommended sequence.
Use the text adventure as optional creative practice rather than forcing its story into a job tracker.
Update the curriculum map, project counts, preparation map, and navigation together when that transition is approved.

## Learner experience

The dashboard gets a compact **Your app** entry showing the latest working version and next feature.
The syllabus marks Fieldbook milestones next to their chapters.
Continue follows the chosen learning path, including recommended milestones, with separate course and project resume anchors.
Opening a checkpoint history or preview must not change the resume target.
Milestones reuse the existing lesson/editor/console workbench and conditional file explorer.
Use the existing F10 help, keyboard focus rules, and narrow-terminal pane switching.
Do not add a permanently visible fourth pane.

At milestone entry, default to a compatible learner checkpoint and show its origin.
If none exists, offer a supplied checkpoint for the required base version, explicitly labeled as supplied earlier code.
This is distinct from revealing the current milestone's solution and never marks skipped work complete.
Known topics remain skippable and chapter access remains advisory.
Running a historical checkpoint uses a temporary copy; editing from one creates a new draft.
Export creates a normal Python folder with source, sample data, run instructions, and checkpoint provenance, without requiring Pytuitor to run it.

## Implementation boundaries

The existing `StageContract` in `src/pytuitor/models.py` already carries stage instructions, checks, hints, input, starter files, and reference files.
The current profile in `src/pytuitor/state.py` is version 3 and keeps independent lesson stage drafts.
These are useful foundations, but there is no cross-lesson project history in that profile schema.

1. Add immutable `ProjectDefinition` and `ProjectMilestone` content models with stable IDs, chapter links, preparation, required base capabilities, revision, entrypoint, Extend/Repair contracts, and acceptance suites.
   Keep a dedicated project catalog instead of disguising project lineage as a `Lesson.project` boolean.
2. Add a project workspace service that resolves a base checkpoint, creates a draft, checks compatibility, records snapshots, restores backups, and exports.
   Reuse path validation, file limits, execution policy, runner, and atomic storage helpers.
3. Add a backed-up profile migration for project drafts, independent stage status, checkpoint references, and the project resume anchor.
   Keep existing lesson records intact and create no project achievements from old lesson completion.
4. Adapt the workbench through a small shared exercise interface exposing the active contract, entrypoint, revision, and workspace operations.
   Put project lifecycle rules in the service, not conditional branches throughout the screen.
5. Add dashboard, syllabus, milestone navigation, checkpoint history, and explicit export actions.
   Keep authored content separate from persistence and widgets.

Each checkpoint records its project/milestone revision, parent snapshot, required capabilities, full source-file map, content hash, and passing check evidence.
Record supplied-base and reference-use provenance separately from the learner's own successful extension.
Use immutable snapshots initially, with bounded workspace sizes and an explicit history storage policy; no learner-facing Git dependency is needed.
Write and sync the snapshot before atomically recording its pointer in the profile.
A crash may leave an unreferenced snapshot, but must never leave a completed milestone pointing to missing files.

## Carry-forward and checking rules

The milestone receives a copy of the learner's successful previous source, not the author's full solution.
Keep existing behavior plus the new feature under executable acceptance checks.
Validate public behavior and documented interfaces, allowing alternative internal implementations.
Version acceptance suites at refactors: a move from dictionaries to classes must not keep obsolete source-shape requirements.
Intentional behavior changes need an explicit new contract rather than silently removing failing regressions.
Keep fixtures, temporary outputs, and test effects isolated from persistent learner drafts.
Only record success if the complete current file snapshot still matches the checked snapshot.

For new files, add only declared non-conflicting scaffolding and explain its role.
Never silently overwrite changed files or splice arbitrary Python with text substitutions.
When a learner skips ahead or a curriculum update changes the required base, offer an explicit supported-base branch or guided adaptation of their copy.
Preserve the old checkpoint and label old evidence with its original revision.
Restoring or resetting a draft backs up the full workspace first.

The advanced course is a dependency graph rather than a single mandatory line.
Optional extensions declare actual capabilities they require; packaging must not acquire an async prerequisite merely because it appears later in the syllabus.
A compatible checkpoint can include other extensions, but unrelated branches are not automatically merged.
If an optional feature is incompatible, preserve both branches and require an authored integration task to combine them.

## Delivery and evidence

Start with a vertical slice across First programs, Lists and sets, and Loops and dictionaries.
This proves real code continuity while keeping the learner-facing content small enough to inspect closely.
Deliver the milestone model, durable checkpoint history, Extend/Repair separation, later entry from supplied code, resume, and runnable export in that slice.
Then complete the core app through Careful automation, followed by the optional extensions and standalone-project migration.

The first slice is ready when a learner can build version one, extend their own code twice, repair an independent incident, restart Pytuitor, and export a working version without losing any draft.
Also verify later entry, reference provenance, changed-file checks, reset recovery, curriculum revisions, disk failures, and unsupported optional combinations.
Exercise the flow with Textual Pilot and a real PTY at 80 by 24 and 140 by 44, with scratch profiles.
Use the repository's lint, tests, build, and installed-wheel smoke checks for implementation releases, including supported Windows journeys.
Learner observation must assess whether the app creates ownership and continuity without making each lesson feel longer; passing automated tests cannot establish that.

## Decisions to review

The recommended shape is a practical Fieldbook CLI, chapter milestones, and focused lessons between them.
A text adventure campaign is an alternative if creative engagement matters more than natural CLI, reporting, and automation features.
A Dispatch-like job processor is another alternative if closer continuity with Dockyard matters more than a gentle starting domain.
The first review should settle the app domain and learning rhythm before authoring all milestone contracts.

## Evidence inspected

- Dockyard: `README.md`, `docs/user-guide.md` (Grow the Dispatch project), and `docs/implementation-plan.md` (Dispatch).
- Pytuitor: `AGENTS.md`, `docs/curriculum.md`, `src/pytuitor/course_map.py`, `models.py`, `state.py`, `lesson_screen.py`, and `theme.tcss`.
- This proposal does not claim implementation, runtime verification, or measured teaching effectiveness.
