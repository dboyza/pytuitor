# Returning, checking, and reviewing

## Resume work

Continue opens the saved activity and stage, including the active file, cursor, editor scroll, reading position, selected check, and focused pane.
Positions are stored separately for Build or Extend and Repair, and separately for each file.
A missing file or invalid position falls back safely without changing source drafts.

The dashboard recap describes unfinished work or remaining failed checks.
Use **Tools > Note for next time** to keep a personal reminder of up to 1,000 characters.
The dashboard shows a short preview; reopen the note to read or edit the complete text.
These notes are separate from retired study-note profile fields.

Saved check reports include a source fingerprint and curriculum revision.
A changed draft is labeled as requiring another check; a saved report never awards completion.
Reports have bounded previews, and unusually long output is explicitly marked as shortened.
Checking again produces fresh evidence.

## Investigate a check

The console initially selects the first failure and keeps passing cases out of the main view.
**Checks** opens the complete case list, and **Details** shows supplied input, expected output, printed output, and authored scenario observations for the selected case.
Selecting a case preserves that selection while other checks finish.
**Hint** offers guidance for that case.

Lantern Reach scenarios report concrete state differences such as a supply balance or quest status.
An observation captures the result of the operation already performed; diagnostics do not call learner operations a second time.
Exceptions, cancellation, and edits made during a check still prevent a stale success from being accepted.

The workbench keeps Run, Check, and the next required action prominent.
Stop appears while execution is active.
Occasional file, note, export, and reset actions live under Tools and remain available in the command palette.

## See the game grow

Every game milestone has an implementation brief describing the earlier capability, the addition, behavior to retain, and a suggested interaction.
The complete exercise requirements remain available alongside it.
After Extend passes, an inline summary describes the capability and **Play version** opens the immutable checked source.
Play does not launch automatically, change a draft, or satisfy the independent Repair.

Dashboard and game overview summaries separate core completion from optional depth.
Known topics are shown separately from work completed through checks.
The core game has 11 milestones; the 10 optional extensions remain accessible in any supported order.

## Required Repair pacing

Both required stages remain in every activity.
Focused Repairs target smaller concepts; concept Repairs trace a fuller behavior; project Repairs exercise a scenario.
The displayed ranges of roughly 3-5, 5-8, and 8-12 minutes are planning guidance, not measured completion times or timers.
They never affect access or completion.

No task is completed by reading a reference or using a hint.

## Optional mixed review

Open **Review** on the dashboard, press **R** there, or search for **Optional review** in the command palette.
Each of the 21 chapters has three authored tasks: predict output, repair a short program, and write a small program.
All chapters are available, with preparation shown as advisory.
Review drafts, choices, assistance, and the current task persist independently of the course resume point.
Hints and read-only references do not replace drafts.

A chapter becomes eligible for a suggestion when its recommended lessons and game milestone are completed or known where applicable.
Suggestions appear unobtrusively on the Review button and never intercept Continue.
After successful sessions, local calendar intervals are 2, 7, 21, and then 45 days.
Using assistance or making an incorrect attempt brings the next interval back to 2 days.
These intervals are a simple product default, not a claim of individually optimized learning.
**Suggest tomorrow** defers a chapter; **Pause suggestions** disables all suggestions while keeping manual review open.
No account, network service, streak, or course credit is involved.

Review records use an additive `reviews` field in version 4 profiles.
Optional presentation fields live beside their stage drafts; invalid presentation metadata is ignored.
Start over clears reviews and notes along with the rest of the active profile, after confirmation.

## Validation boundaries

Runner checks prove authored examples and observable contracts, not teaching effectiveness.
Textual journeys and screenshots verify navigation and layouts, including the 80 by 24 terminal.
Native terminal tests verify actual Unix control-key input.
Windows ConPTY and desktop checks require a Windows environment; a local macOS run does not substitute for them.
A learner study should evaluate the effort estimates, usefulness of feedback, and transfer from review to independent work.
