## A path describes a location
Python's standard library contains modules: collections of reusable code shipped with Python.
`from pathlib import Path` imports the `Path` class from the `pathlib` module.
A class lets you create objects with related data and operations; we will write our own classes later.
`Path("notes/today.txt")` creates an object describing a relative path: a location starting from the folder where the program runs.
An absolute path instead starts from the root of the filesystem, such as `/tmp/notes/today.txt` on macOS or Linux.
It does not create a file by itself.

```python
from pathlib import Path

folder = Path("notes")
file = folder / "today.txt"
print(file.name)  # today.txt
print(file.suffix)  # .txt
```

The `/` operator joins paths when its left side is a `Path`.
Here, `file.name` is the filename and `file.suffix` is its extension, including the dot.
These named pieces of object data are called attributes.
A method, such as `file.read_text()`, is an operation called through the object.
`#` starts a comment, which Python ignores until the end of the line.
`.mkdir(parents=True, exist_ok=True)` creates a folder and any missing folders that contain it.
For `notes/drafts`, `notes` is the parent folder.
`exist_ok=True` means an already-existing folder is allowed.
`.write_text(text, encoding="utf-8")` writes text and replaces an existing file.
`.read_text(encoding="utf-8")` reads it.

## Build
Define `save_note(folder, text)`.
Create the requested folder, including missing parents.
Write `text` exactly as given to `note.txt` inside it, using UTF-8.
Return the resulting `Path` object.
The caller supplies a folder path as a string.
If `note.txt` already exists, replace its contents deliberately.
Do not add a newline unless `text` already has one.

## Repair
The supplied code writes beside the requested folder instead of inside it and fails when parents are missing.
