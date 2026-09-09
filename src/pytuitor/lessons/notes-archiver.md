## Build a careful notes archiver
Build a tool that copies selected notes into an archive folder while preserving originals and files already in the archive.
A **dry run** reports what would happen without making changes.
Make that the default so a caller must deliberately request writes.

A directory is another name for a folder.
A `Path` object's `.iterdir()` visits the files and folders directly inside a directory, without visiting their contents.
`.is_file()` asks whether an entry is a file, `.is_symlink()` checks whether it is a symbolic link, and `.exists()` checks whether a target exists.
A symbolic link is a reference to another filesystem location; this project skips source links.
`continue` skips the rest of the current pass through a loop and moves to the next item.
You already know sorting, suffixes, module imports, and exclusive binary copying.

## Build
In `selection.py`, define `eligible(source)`.
Return an alphabetically sorted list of filenames for regular files directly inside `source` whose suffix is exactly `.txt`.
Skip directories, symbolic links, and other extensions, including `.TXT`.
Do not look inside subfolders.

In `lesson.py`, import `eligible` and define `archive_notes(source, destination, dry_run=True)`.
Return sorted filenames that can be copied because their destination names do not already exist.
In dry-run mode, create no files or directories.
When `dry_run=False`, create the destination directory if needed and copy each file's exact bytes using exclusive creation.
If another file already has the destination name when you try to create it, skip that file and leave its name out of the returned list.
Preserve every source file and every existing destination file.
An empty source returns `[]` and need not create the destination.
The source directory exists; callers provide ordinary local directories under their control.
Let other errors reading or writing files reach the caller.

For a source containing `b.txt`, `a.txt`, and `photo.png`, with no existing destination files, return `["a.txt", "b.txt"]`.
After successful checks, export the workspace and try a dry run on a small folder of disposable sample notes.

## Repair
The supplied app ignores dry-run mode.
Find the condition controlling writes so previewing the operation leaves files unchanged.
