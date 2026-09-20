# Exercise authoring

`StageContract` in `src/pytuitor/models.py` is the typed boundary for stage-specific learner instructions, starter files, reference files, checks, hints, and input.

`Lesson.stage_contract("build")` and `Lesson.stage_contract("repair")` provide compatible Build defaults for existing units.

The six First programs units use the `_FOUNDATION_STAGES` table in `src/pytuitor/beginner_course.py` as their canonical active stage content.

The legacy `Lesson` fields remain populated as compatibility projections for imports and saved drafts.

New authoring should provide both stage contracts when Build and Repair need different scenarios or checks.

Keep each Repair solvable with concepts already taught, behavior-based, and meaningfully different from its Build scenario.

The remaining 40 beginner units use `BUILD_INSTRUCTIONS` and `REPAIR_STAGES` in `src/pytuitor/beginner_stage_refresh.py`.
Their Build references and checks remain in `beginner_course.py` and `beginner_extensions.py`; the course assembly projects active contracts into the compatibility fields.

Lesson Markdown keeps teaching and worked examples; stage requirements, starters, references, checks, and hints belong to the stage contracts.
Instructions render as Markdown: use code spans for names, explicit input/output examples, and separate paragraphs for distinct requirements.
Keep the complete contract when moving it out of lesson prose, including file names, return shapes, output, input assumptions, and edge cases.
Keep prerequisite explanations in the teaching body, especially when removing an old exercise section.

Before `small-superpowers`, Repair programs use top-level input, variables, and loops rather than function definitions or comprehensions.
Do not introduce dictionaries before `word-counts`.
Describe the desired behavior in the prompt; reserve diagnosis and fixes for progressive hints.
Check-specific nudges override the first stage hint; the first hint is the fallback when every case concerns the same defect.

For multi-step checks, `_scenario_check` keeps setup and assertions readable without adding runner APIs.
Its script assigns `result` in the worker's fresh namespace; give it a plain-language description of the operation and fixture.
Test observable behavior, including written files, input preservation, and conflicts, rather than source spelling.
Retain plausible incomplete repairs that must fail and valid alternative implementations that must pass.

Increase the lesson revision when changing either executable stage contract.
Old drafts and historical completion stay preserved, but an old checked revision must not unlock or pass a changed stage.
Use each stage's `reference_files` in journeys and exports; the legacy `lesson.solution` describes Build only.

Run the catalog tests and `scripts/smoke_installed.py` after changing a stage contract.
