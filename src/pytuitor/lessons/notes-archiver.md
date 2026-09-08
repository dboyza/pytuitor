## Build a careful notes archiver
Build a tool that copies selected notes into an archive while preserving originals and existing archive files.
A **dry run** reports what would happen without making changes.
Make that the default so a caller must deliberately request writes.

A `Path` object's `.iterdir()` visits the immediate entries of a directory.
`.is_file()` asks whether an entry is a file, `.is_symlink()` checks whether it is a symbolic link, and `.exists()` checks whether a target exists.
A symbolic link is a reference to another filesystem location; this project skips source links.
`continue` skips the rest of the current loop iteration and moves to the next item.
You already know sorting, suffixes, module imports, and exclusive binary copying.

## Build
In `selection.py`, define `eligible(source)`.
Return an alphabetically sorted list of filenames for immediate regular files whose suffix is exactly `.txt`.
Skip directories, symbolic links, and other extensions, including `.TXT`.
Do not recurse into subfolders.

In `lesson.py`, import `eligible` and define `archive_notes(source, destination, dry_run=True)`.
Return sorted filenames that can be copied because their destination names do not already exist.
In dry-run mode, create no files or directories.
When `dry_run=False`, create the destination directory if needed and copy those files byte-for-byte using exclusive creation.
If exclusive creation reports a collision, skip that file and omit it from the returned list.
Preserve every source file and every existing destination file.
An empty source returns `[]` and need not create the destination.
The source directory exists; callers provide ordinary local directories under their control.
Other I/O errors should remain visible rather than being silently ignored.

For a source containing `b.txt`, `a.txt`, and `photo.png`, with no existing destination files, return `["a.txt", "b.txt"]`.
After successful checks, export the workspace and try a dry run on a small folder of disposable sample notes.

## Repair
The supplied app ignores dry-run mode.
Find the condition controlling writes and restore the preview contract.
