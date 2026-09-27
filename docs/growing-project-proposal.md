# Lantern Reach implementation plan

Status: implemented locally on 2026-09-27 after the product decisions agreed with the user on 2026-09-26.
The sections below record the agreed design and acceptance criteria; the verification record at the end distinguishes executed checks from unavailable platform and learner-study evidence.

## Product

Lantern Reach is an offline expedition and settlement text game authored by the learner throughout Pytuitor.
The learner explores a small valley, collects supplies, helps its residents, and restores an abandoned outpost.
The tone is welcoming and curious, with recoverable mistakes, concise scenes, and no required combat, real-time pressure, network services, or accounts.
A fixed world and explicit behavior contracts make checks understandable while permitting alternative implementations and personal extensions.
The game uses standard-library Python with print/input commands and exports as a normal runnable project.
Pytuitor remains the existing Textual tutor with its current colors, focus conventions, and keyboard support.

## Agreed learning structure

- Keep 75 focused teaching lessons with blank Build and independent Repair.
- Add one cumulative game milestone to each of the 21 chapters, scaled to the chapter's size.
- Make the milestones the recommended project path; keep all 12 original projects as optional practice with their existing IDs, drafts, and historical completion.
- Finish a satisfying playable game by the end of the three core sections; all optional chapters receive authored extensions but remain optional.
- Ordinary lessons explain how their concepts connect to the game without requiring another compulsory task after every lesson.
- Milestones use Extend followed by a separate authored Repair scenario; the first milestone starts blank.
- Extend continues the learner's own successful source; Repair never replaces that source.
- Permit later entry through clearly labeled supplied base code or adaptation of the learner's own copy.
- Keep references explicitly revealed, record their use, and never mark supplied earlier code as learner-completed work.

## Game progression and authored contracts

Each milestone needs complete requirements, prerequisite links, worked examples distinct from the solution, progressive hints, runnable reference files, observable checks, and a meaningful broken Repair with its own reference.
Every newly required language construct must already be taught in the chapter or its declared preparation.

| Chapter | Milestone | Playable outcome and check boundaries |
| --- | --- | --- |
| First programs | Arrival at Lantern Reach | Name the explorer, calculate starting supplies, and choose a safe route using input, numbers, formatting, and decisions; check both routes and resource boundaries. |
| Lists and sets | Pack for the trail | Display an ordered pack, retain repeated supplies, and identify unique or missing equipment; check empty, repeated, and reordered collections. |
| Loops and dictionaries | Open the outpost | Track locations and supplies and repeat look, travel, gather, inventory, and quit commands; reject unknown commands without losing state. |
| Functions and input | Help the first resident | Extract reusable state and command operations, complete a small delivery quest, normalize input, and recover from invalid quantities without mutation. |
| Files and structured data | Keep a journal | Save/reload game state as JSON and exchange a CSV supply ledger; verify round trips, quoted fields, missing files, and malformed saves. |
| Text patterns | Decode trail markers | Validate and extract route or quest codes from notes; require complete matches and preserve unrelated text. |
| Modules and library tools | Organize the expedition | Split engine and entrypoint; add CLI options, repeatable local encounters, and supply summaries; keep imports quiet. |
| Dates and times | Plan the supply run | Track a specified in-game calendar and delivery deadlines; test month/year/leap boundaries without wall-clock dependence. |
| Collection tools | Run the supply depot | Group supplies, filter active jobs, and process residents' requests in arrival order without mutating caller input. |
| Classes and tested tools | Build the expedition engine | Model independent expeditions and named quest states; write learner tests that reject broken transitions and shared state. |
| Careful automation | Restore the beacon | Complete the core story and provide previewable journal/archive exports that refuse overwrite and validate paths before writing. |
| Python semantics | Try another route | Branch a nested game-state snapshot without sharing mutable inventory or losing valid zero/empty values. |
| Recursion and functional tools | Explore the cave network | Traverse nested locations and select route ordering with callable strategies; handle empty branches and stable order. |
| Decorators | Record expedition actions | Wrap operations with event recording and configurable policies while preserving results, keywords, and metadata. |
| Iterators and streaming | Read the expedition chronicle | Stream bounded reports from a one-pass event source without consuming unnecessary events. |
| Exceptions and contexts | Recover the field station | Raise useful domain failures and restore temporary resources/state on success, failure, and nested use. |
| Dataclasses and types | Define field records | Introduce validated record values, independent defaults, and deliberate updates; distinguish invalid construction and shared state. |
| Object protocols and testing | Connect supply stores | Use small storage/reporting contracts and injected effects with meaningful learner tests; accept equivalent implementations. |
| Coordinate async work | Coordinate scout teams | Consume deterministic offline scout sources with bounded concurrency, ordered results, and cancellation cleanup measured with events. |
| Build distributable tools | Share the expedition | Provide installable metadata, predictable CLI behavior, explicit data paths, and a portable offline source export. |
| Understand the machinery | Add journal formatters | Register and inspect formatter extensions; exercise descriptor state, duplicate rejection, inheritance, and callable contracts. |

The game stays in one source file before the modules chapter.
Later refactors must retain the previous behavior or explicitly document the changed public interface.
Advanced features must connect to a playable command or visible game behavior rather than existing only as isolated library exercises.
Use fixed seeds, explicit game dates, local fixtures, and deterministic async probes.
Personal creative additions are retained but are outside the authored acceptance contract.

## Catalog and navigation

Keep the original lesson catalog as a stable compatibility and practice catalog.
Add explicit project/milestone definitions and a recommended activity sequence containing the 75 teaching lessons and 21 milestones.
Each chapter's recommended sequence ends with its milestone; standalone practice appears separately and does not delay Continue.
Known topics can skip teaching lessons but never award project completion.
Continue resumes active work and respects the existing optional-section boundary.
The dashboard offers a compact Your game entry.
The overview selects the last-opened milestone or first unfinished feature and provides access to the latest working checkpoint.
A game overview lists milestones, status, prerequisite guidance, checkpoint provenance, and actions to continue, start with supplied code, revisit history, and export.
Opening history or reading a preview does not change the course resume anchor.
The syllabus distinguishes lessons, milestones, and optional practice and permits explicit entry to all of them.

## Workspace and checkpoint lifecycle

A milestone has a stable ID, revision, chapter, required base capabilities, entrypoint, two independent contracts, and a known-good supplied base containing only earlier capabilities.
Use a small adapter into the existing workbench and runner instead of copying their execution and editing logic.
Keep project lifecycle and persistence rules in a dedicated service.
Internal storage may retain the existing build/repair keys, but all learner-facing milestone copy must consistently say Extend/Repair.

Opening an unstarted milestone presents its compatible learner checkpoint or a labeled supplied base.
A prior successful source snapshot is copied into a fresh draft, with new non-conflicting files added only when declared.
Never splice arbitrary Python or overwrite a same-named learner file with authored code.
If adaptation is necessary, show the old files and the new contract while keeping the source unchanged; an explicit supported-base action creates a separately backed-up attempt.
A first milestone has a blank Extend workspace.

Passing Extend stores an immutable full-source checkpoint tied to the exact checked draft and current content revision.
The snapshot records its parent, milestone, capabilities, hash, check evidence, base origin, and reference-use provenance.
Passing Repair completes the milestone without altering its Extend checkpoint.
Further edits invalidate current-draft success while keeping historical snapshots and evidence.
Only an explicit Next action changes the activity or stage.

Write and sync snapshot content before atomically persisting its profile pointer.
On failure, preserve the draft and show actionable recovery; no completed state may point to absent or corrupt source.
Validate snapshot paths and file maps through existing workspace boundaries, and verify stored hashes on load.
Deduplicate identical snapshots; retain history without silent destructive pruning and expose size/retention information.
Reset, branch replacement, and restore must back up the full current workspace before changing it.
Historical snapshots remain read-only; restoring creates a current draft and does not manufacture current-revision success.

## Migration, optional branches, and export

Add a backed-up profile schema migration without rewriting existing lesson IDs, drafts, or achievements.
Keep project progress, project resume state, and checkpoint metadata separate from lesson records.
Old supported profiles remain loadable; document that older app versions cannot read the new schema and provide the original backup for rollback.
Never test against personal learning progress.

Optional extensions form a capability graph matching real chapter preparation.
Packaging must not require async merely because its chapter appears later in the syllabus.
Preserve compatible extra files from learner checkpoints; do not automatically merge competing branches.
Offer a suitable supplied base when no compatible checkpoint exists and retain every previous branch.
Curriculum revisions retain historical evidence, require rechecking changed contracts, and never discard the learner's source.

Export a normal folder containing source, safe sample data, run instructions, and a provenance manifest.
The exported core game runs with Python 3.11 or newer and no tutor dependency.
Keep source checkpoints distinct from a player's game saves, and teach save persistence explicitly in the files chapter.
Within Pytuitor, generated save files use the existing Run files preview-and-keep workflow.
Reference exports or supplied-base provenance must be labeled honestly.
Exports refuse to replace an existing destination.

## Implementation sequence

1. Establish baseline checks and finish canonical project models, content layout, and prerequisite mapping.
2. Implement migration, immutable checkpoint storage, draft continuation, provenance, reset/restore, and export with failure-path tests.
3. Integrate the first three milestones through dashboard, syllabus, Continue, Extend/Repair, restart, and export.
4. Author and validate the entire core game through Restore the beacon, including the real module/class refactors and persistence.
5. Author and validate all optional extensions and their independent entry paths, including packaging and async cancellation.
6. Connect every teaching lesson to its chapter milestone; make old projects discoverable as optional practice and update documentation and counts.
7. Complete end-to-end journeys, terminal and visual review, regression checks, installed-wheel verification, and local commits.

These are execution stages, not approval gates or a reduced MVP delivery scope.
Work proceeds directly without subagents and without pushing or publishing.

## Acceptance and verification

- Audit all 21 milestone Extend references, broken Repairs, and corrected Repair references through the real runner.
- Demonstrate cumulative source continuity across the core sequence, including a valid alternative implementation and a retained personal file.
- Verify existing behavior survives each extension; test deliberate mutants for important boundaries and learner-authored testing tasks.
- Complete full UI journeys for first start, chapter transition, later entry, hints/reference, Repair independence, history/restore, reset, restart, and export.
- Exercise optional branches independently and verify packaging does not depend on async.
- Test migration from supported schemas, corrupt snapshots, missing files, failed writes, stale asynchronous results, and conflicting draft edits.
- Run the exported core game and the final supported extended game outside Pytuitor with scripted inputs and actual observable outcomes.
- Inspect real Textual output at 80 by 24 and 140 by 44, including dialogs, long contracts, file controls, failure messages, and keyboard focus.
- Use scratch profiles, Textual Pilot, real Unix PTY journeys, and the existing platform-specific tests; report Windows execution only if actually available and performed.
- Run locked dependency sync, full pytest, Ruff checks and formatting, package build, and isolated installed-wheel smoke.
- Keep reviewed visual baselines honest and update them only for intentional changes after direct image inspection.
- Update AGENTS.md, curriculum/authoring/release documentation, and user guidance with durable decisions; do not edit generated files or changelogs manually.
- Report exact validation evidence and any unavailable platform checks; automated consistency checks do not establish learner effectiveness.

## Evidence and decisions

The architecture was reviewed against Pytuitor's current models, state, runner, workbench, navigation, authoring rules, and release checks.
Dockyard's local README and checkpoint guide informed the continuity and provenance model.
All eight initial product questions and the game-setting follow-up were answered before implementation.
The user delegated remaining product details to the agent and authorized complete implementation without routine interruptions.


## Local implementation verification

The recommended path contains 75 teaching lessons and 21 Lantern Reach milestones, with all 12 original projects retained as optional practice.
All 75 teaching lessons have specific game connections.
A complete authored 21-milestone journey retains personal files and optional capabilities, exports successfully, and runs independently.
The core and fully extended games were exercised through settlement help, beacon restoration, optional commands, and saved state.

On macOS with Python 3.12, the full locked suite passed with **837 passed and 7 skipped**.
Ruff lint, Ruff formatting, and ordinary visual-baseline comparisons passed.
Real Unix PTY journeys covered lesson and game navigation, keyboard focus, delayed focus delivery, and resizing at both required terminal sizes.
Actual Textual screenshots were rendered and directly inspected at 80 by 24 and 140 by 44, including game overview, provenance, history, restore confirmation, and the multi-file workbench.
Recovery tests cover checkpoint integrity, failed profile saves, old revisions, preservation of both drafts, full-size exports/backups, and restoration from an active editor without stale autosave overwrite.

The tutor source distribution and wheel built successfully, including the new game content and excluding local editor logs, caches, and scratch artifacts.
An isolated installed-wheel smoke outside the checkout passed all **216 stage reference programs**, onboarding and lesson completion, game continuation, profile reopening, and checkpoint export.
The fully extended learner game built as its own source distribution and wheel; its installed CLI passed settlement/beacon play, optional commands, saving, Unicode story paths, and nonzero error exit status.

Windows ConPTY, PowerShell, and Windows desktop execution were unavailable on this macOS host and were not claimed.
No learner study was performed, and these automated checks do not establish teaching effectiveness.
The implementation is committed locally; no remote push or publication is part of this delivery.
