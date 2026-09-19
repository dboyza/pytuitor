# Exercise authoring

`StageContract` in `src/pytuitor/models.py` is the typed boundary for stage-specific learner instructions, starter files, reference files, checks, hints, and input.

`Lesson.stage_contract("build")` and `Lesson.stage_contract("repair")` provide compatible Build defaults for existing units.

The six First programs units use the `_FOUNDATION_STAGES` table in `src/pytuitor/beginner_course.py` as their canonical active stage content.

The legacy `Lesson` fields remain populated as compatibility projections for imports and saved drafts.

New authoring should provide both stage contracts when Build and Repair need different scenarios or checks.

Keep each Repair solvable with concepts already taught, behavior-based, and meaningfully different from its Build scenario.

Run the catalog tests and `scripts/smoke_installed.py` after changing a stage contract.
