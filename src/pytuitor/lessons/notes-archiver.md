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
