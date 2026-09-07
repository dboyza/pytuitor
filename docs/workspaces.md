# Project workspaces

A lesson workspace contains editable text files, with one entry point used by Run and Check.
Build and Repair keep separate drafts.
Run and Check use temporary copies so experiments cannot overwrite the saved draft automatically.
Export creates a new directory containing the complete saved workspace; it refuses to replace an existing destination.

## Keep files produced by Run

When Run creates or changes eligible UTF-8 text files, the console shows **Run files**.
Open it to select a file and inspect its contents in a read-only preview.
Choose **Save to workspace** to keep all the previewed files in the current Build or Repair stage.
The tutor backs up the complete current stage first, then adds or replaces the previewed files without deleting other files.
If you edited an affected file after that Run, saving refuses to overwrite it; run the current draft again before keeping its output.
Saved files become inputs for later Run and Check attempts and are included in workspace exports.

Closing the preview does not save files, and generated files are never imported automatically.
Check discards its generated files because test fixtures and side effects belong to each isolated case.
Binary files, symbolic links, unsafe paths, and files beyond the workspace limits are omitted from Run's preview, with a notice when output cannot be included.
To retain larger or binary outputs, export the workspace and run it in a folder you control.

## Files and boundaries

Use relative names such as `main.py`, `helpers.py`, or `data/settings.json`.
The tutor rejects absolute paths, `..`, ambiguous names, case-only duplicates, reserved internal directories, and file/directory collisions.
A workspace permits 32 files, 256 KiB per file, and 1 MiB in total, measured as UTF-8 text.
Exports reject symbolic-link destinations and ancestors.
Keep binary data and large datasets outside the editor.

These checks protect file management from accidental traversal or replacement.
Learner code still runs as your user; process isolation and virtual environments are not an operating-system security sandbox.
Only run code and install packages you trust.

## Virtual environments

Creating an environment uses Python's built-in `venv` module and does not download packages.
The environment belongs to the learner's local profile and is separate from the Python environment that runs the tutor.
The tutor never creates or updates an environment merely because a lesson was opened.
If creation fails or is cancelled, its incomplete directory is removed.

Package installation is an explicit operation that requires a network connection.
Enter one package name, optionally with an exact version such as `rich==13.9.4`.
Check the spelling and publisher before installing; similar names can belong to different projects.
The tutor uses PyPI, accepts wheels only, disables interactive prompts, and does not accept URLs, filesystem paths, additional pip options, or shell commands.
A pinned top-level version does not pin all transitive dependencies.
Packages are third-party executable code even when distributed as wheels.
All authored lessons can be completed with the standard library, without installing third-party packages.

Environment commands have a time limit and an output limit.
Cancelling an operation stops its subprocess group.
An interrupted package installation can leave some dependencies installed; recreating the environment is the clean recovery when its state is uncertain.

## Working outside the tutor

Export a project to a new folder when you want to continue in your own terminal or editor.
Create a new environment there and install only the dependencies the project actually uses.
Keep dependency declarations in a project file and record versions for reproducibility.
Do not copy an existing virtual environment to a new location; recreate it because its executable scripts contain environment-specific paths.
