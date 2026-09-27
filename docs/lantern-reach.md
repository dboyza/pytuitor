# Your growing game: Lantern Reach

Lantern Reach is an offline text adventure about exploring a valley, helping its residents, and restoring an outpost.
You write the Python yourself, starting with a few questions and growing it into a persistent, tested game.
The first three course sections finish a playable core adventure.
Optional depth adds capabilities such as cave traversal, streaming chronicles, concurrent scouts, packaging, and journal formatters.

## Find your game

Choose **Your game** on the dashboard, press **G** there, or search **Your game** in the command palette.
The overview lists all 21 milestones, their progress, and working checkpoint history.
Choose a milestone to see its story and starting-code origin, then open it with Enter or **Open milestone**.
The syllabus also lists each milestone at the end of its chapter.
Continue follows the recommended lessons and milestones; optional sections still require an explicit choice.

The original 12 projects remain under **Optional independent practice** in their syllabus chapters.
Their existing drafts and achievements are preserved, and they do not block recommended course progression.

## Extend, check, and repair

Ordinary lessons begin with blank Build exercises.
Game milestones use **Extend**: the first starts blank, and later ones continue a compatible working checkpoint from your own code.
Required new files start blank unless they contain supplied earlier code.
Your extra files and creative changes are retained.
Refactors such as splitting modules or creating a package are explicit learner tasks; Pytuitor does not rewrite your Python.

Use Run to play and Check to exercise the stated behavior and retained capabilities.
A successful Extend saves an immutable working checkpoint only for the exact checked file snapshot.
Editing the current draft requires checking again, while its earlier working version remains in history.
Repair opens a separate authored incident, preserving your Extend draft and checkpoint.
Complete both stages, then choose Next to continue.

Every focused lesson includes a concrete connection to the game feature its chapter prepares.
Hints and references remain explicit.
Revealing a reference records that support; it does not replace your draft.
When continuing extra optional features, keep those features while adapting the canonical reference's approach.

## Skip ahead without losing your work

If no compatible earlier checkpoint exists, the milestone starts from clearly labeled supplied earlier code.
This is the previous working game, not the current milestone's completed solution.
Skipped milestones remain incomplete, and the source provenance stays visible in future checkpoints.

**Supplied base** in the game overview starts a fresh supported attempt after confirmation.
If a draft already exists, both Extend and Repair source files are exported before the attempt is replaced.
Historical checkpoints remain intact.
For manual adaptation, continue your existing source and use the new requirements and explicit reference comparison.

Optional capabilities follow their real preparation rather than a single compulsory chain.
Packaging can be entered from the core game without completing async.
Compatible earlier extra capabilities are carried forward and included in later checks; silently dropping them cannot earn a new working checkpoint.
Independent histories are not automatically merged.

## Revisit, play, restore, and export

**History** lists immutable versions with the milestone revision and support provenance.
**Play** runs a temporary copy of the selected checkpoint; its source and your active drafts remain unchanged.
Close it with Escape, or end an input stream with Ctrl+D.
Temporary checkpoint play does not retain generated saves.

**Restore copy** requires confirmation, backs up both current stage drafts, and copies the selected compatible source into a new attempt.
The restored draft must be checked against the current milestone contract.
A damaged or missing checkpoint produces an error; use another version or a supplied base without discarding your draft.
History shows its source-storage size and is retained until you explicitly start over; there is no automatic pruning.

**Export** in History exports that checkpoint; **Export latest** exports the latest successful version.
Exports go to a newly created directory under the profile's `exports/` folder and never overwrite an existing destination.
The folder includes Python source, instructions, and a provenance manifest.
Use Python 3.11 or newer to run `python game.py` from that folder.
The packaging milestone also supports `python -m lantern_reach` and authors installable package metadata.
Build tooling may require an explicitly requested download; normal source play is offline and requires no third-party runtime packages.

A core expedition starts at the outpost.
Visit the forest and gather wood, return to deliver two pieces to Mira, then restore the beacon.
Help Oren with rope and Tess with wood to improve the settlement.
Use help to discover the current version's commands and keep exploring after the ending.
Earlier checkpoints intentionally have fewer commands and may start with an arrival questionnaire.

## Keep player saves

Your program's save files are separate from your Python source and from tutor checkpoints.
In an editable milestone, a Run happens in a temporary workspace.
After using the game's save command, select **Run files**, inspect the generated save, and explicitly keep it to use it in the next run.
Pytuitor backs up the workspace first and refuses a newer-draft conflict.
An exported game writes its saves normally in the folder where you run it.

## Existing profiles and recovery

Existing supported profiles migrate to version 4 with the original JSON retained as `profile-before-v4.json`.
Lesson IDs, both old stage drafts, known topics, and historical completion remain intact.
Game records are separate and do not fabricate achievements from old project completion.
Older Pytuitor versions cannot read the new schema; close the tutor and copy the preserved original backup into a separate profile if you need to return to that older version.
Keep the current profile and project checkpoint directory intact when doing so.

Resetting a stage backs up its source and restores its chosen Extend base or the authored broken Repair.
Starting over clears profile progress and references to history after confirmation; files already exported remain separate.
Do not use your personal profile for experiments or automated validation; use `--data-dir` with a scratch directory.
