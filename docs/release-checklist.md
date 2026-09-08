# Release checklist

This checklist describes required evidence, not completed release work.
A configured CI workflow is not evidence that its jobs passed, and a built wheel is not a published release.

## Product and content

- Verify the course contains 48 teaching lessons and 12 chapter projects across both supported paths.
- Verify every Build reference passes, every original Repair fails meaningfully, and every corrected Repair passes.
- Check prerequisite order, worked examples, input/output contracts, and unfamiliar syntax in each chapter.
- Complete the [learner study](learner-study.md) and resolve observed blockers.
- Preserve existing profiles, drafts, known topics, and completion information during upgrades.
- Confirm reference-solution reveal does not replace a learner's code.

## Engineering and terminals

Run the locked tests, lint, formatting checks, and package build:

```sh
uv sync --locked
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
uv build
```

Inspect the wheel to confirm all authored Markdown resources are included.
Install that wheel into a fresh isolated environment outside the checkout, launch it, and complete an onboarding-to-lesson journey.
Run macOS and Linux CI on the supported Python versions and record the actual job links and outcomes.
Verify real terminal control-key behavior in addition to synthetic Textual key events.
Inspect 80 × 24 and 140 × 44 layouts, including errors, dialogs, multi-file controls, and the console.
Exercise interrupted execution, EOF, infinite loops, excessive output, cancelled environment creation, failed package installation, and full progress reset.
Confirm offline startup and course completion do not contact package indexes or update services.

## Installation and supply chain

Publish only after explicit release authorization.
Review the distribution name and ownership before making installation instructions public.
Prefer a version-pinned package installed with a trusted, already-installed `uv` or `pipx`:

```sh
uv tool install 'pytuitor==<reviewed-version>'
# Alternatively:
pipx install 'pytuitor==<reviewed-version>'
```

Replace the placeholder with an actual reviewed release before users copy these commands.
Do not recommend piping a downloaded shell script into a shell.
For a pre-publication review, install the locally built wheel directly instead of assuming a registry package belongs to this project.
Record the release artifact's SHA-256 digest and verify it against the separately trusted release record before installation.
Pinning the tutor's version alone does not lock every transitive dependency; review the built artifact and its resolved dependency set together.
Keep signing or registry credentials out of the repository, logs, learner feedback, and release artifacts.
Use the package registry's trusted publishing mechanism when configured, with release jobs restricted to reviewed tags and the minimum necessary permissions.

## Upgrade and recovery

Back up a representative profile and test upgrading it from the previous supported schema.
Verify the old drafts survive changed lesson revisions and that resetting an exercise remains explicit.
Test invalid or interrupted profile writes, single-writer locking, and clear recovery messages.
Document the supported rollback behavior before publication; do not assume an older app can read a newer profile schema.
Make upgrade checks explicit so offline launch remains predictable.
After release, reproduce reported problems using scratch profiles and keep regression tests with the fix.
