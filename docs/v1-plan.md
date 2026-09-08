# Pytuitor v1 implementation plan

## Accepted scope

Deliver 75 authored lessons and 12 chapter projects across two paths.
Each path contains six chapters ending in a project.
Beginner has 40 lessons; Experienced has 35.
Beginner graduates should independently build command-line tools that use files, structured data, modules, classes, and tests.
Experienced graduates should understand idiomatic Python and its object model, including descriptors, metaclasses, protocols, asynchronous code, and implementation details.

Preserve the gray interface, Python blue/yellow accents, keyboard navigation, and an 80 × 24 minimum terminal size.
Keep learning and checks offline after installation.
Dependency installation is an explicit network action in an isolated project environment.
No account, telemetry, automatic package installation, or mandatory daily practice is required.

## Delivery workstreams

1. Curriculum: coherent prerequisites, complete exercise contracts, blank Build then broken Repair, chapter projects, and verified reference implementations.
2. Workspace: multiple files, saved stage drafts, local imports, isolated check fixtures, exports, environments, and explicit package installation.
3. Learning feedback: progressive hints, useful error explanations, transparent checks, and explicitly revealed reference solutions.
4. Navigation: chapter browsing within the selected path, advisory prerequisites, and a browsable syllabus.
5. Learner validation: self-run study scripts and user-recorded observations.
6. Release readiness: migration checks, installed-package validation, secure installation guidance, macOS/Linux CI, and release checks.

## Completion evidence

Run the reference solution and broken Repair program for every course unit.
Exercise onboarding, chapter browsing, editing, checking, repair, reset, persistence, and multi-file exports through the TUI.
Inspect the interface at 80 × 24 and 140 × 44.
Run the test suite, lint, formatting, package build, and an installed-wheel smoke test.
Remote CI and learner studies remain unverified until actually run.
Publishing a release remains a separate user action.
