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
The tutor rejects absolute paths, `..`, ambiguous names, case-only duplicates, reserved internal directories, Windows device names such as `CON.py`, and file/directory collisions.
A workspace permits 32 files, 256 KiB per file, and 1 MiB in total, measured as UTF-8 text.
Exports reject symbolic-link destinations and ancestors, including Windows junctions.
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
Cancelling an operation stops its subprocess tree, using a process group on Unix or a kill-on-close Job Object on Windows.
An interrupted package installation can leave some dependencies installed; recreating the environment is the clean recovery when its state is uncertain.

## Working outside the tutor

Export a project to a new folder when you want to continue in your own terminal or editor.
Create a new environment there and install only the dependencies the project actually uses.
Keep dependency declarations in a project file and record versions for reproducibility.
Do not copy an existing virtual environment to a new location; recreate it because its executable scripts contain environment-specific paths.

Use the **Execution and privacy** command for the local execution and network-access contract.
Reference comparison is read-only and compares the selected stage file with a snapshot of your own draft.

## Platform guarantees

Tutor-owned text and learner subprocess I/O use UTF-8 on every platform, independent of the PowerShell code page.
Run-file previews normalize text line endings for the editor.
Windows run-file reads refuse reparse points and hold directory handles that prevent renaming while a snapshot is read.

Profiles use an operating-system lock that is released when the application closes or crashes.
Saving flushes the new file before replacement, then syncs the directory on Unix or requests write-through replacement on Windows.
Storage hardware and filesystem behavior still determine durability during a sudden power loss.

Every platform enforces execution time and captured-output limits.
Unix also applies CPU and file-size resource limits, with address-space limits on Linux; Windows applies CPU and job-memory limits through Job Objects.
Windows has no equivalent per-file `RLIMIT_FSIZE` here, so code can still write large files outside the preview limits.
These are accidental-run protections, not a filesystem or network security sandbox.
