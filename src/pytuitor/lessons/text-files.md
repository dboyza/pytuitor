## Keep data after the program ends
Variables disappear when a program exits; files can keep data for another run.
`open(path, "r", encoding="utf-8")` opens a text file for reading.
`"w"` opens it for writing and replaces existing contents, so choose the path carefully.
A `with` statement closes the file when its indented block finishes, including if an error occurs.
This pattern is called a context manager.

```python
with open("message.txt", "w", encoding="utf-8") as handle:
    handle.write("See you tomorrow\n")

with open("message.txt", "r", encoding="utf-8") as handle:
    message = handle.read()
print(message)
```

In Python source, `\n` inside a string represents a newline character.
`.read()` returns the file's entire contents as a string.
`.splitlines()` turns that string into a list of lines without newline characters.
Trying to read a missing file raises `FileNotFoundError`.
We will supply existing files for this exercise.

The tutor runs your code in temporary copies of the workspace.
When Run creates or changes eligible text files, a **Run files** button appears in the console.
Open it to inspect each file, then choose **Save to workspace** to keep the files for later runs or exports.
Saving first backs up your current stage, then adds or replaces the previewed files without deleting other files.
Files are not saved automatically, and Check always discards its file changes.
Binary files, symbolic links, and files beyond the workspace limits are omitted from the preview.
For experiments with those files, export the workspace and run it in a folder you control.

## Build
Define `line_total(path)` that reads a UTF-8 file of integers, one per line, and returns their sum.
Ignore blank and whitespace-only lines.
All nonblank lines contain valid integers, including negatives.
An empty file returns `0`.
For file contents `4`, a blank line, and `-1`, return `3`.
Read only the supplied path and do not change its contents.
Checks create temporary files before calling your function.

## Repair
The broken version tries to convert blank lines to integers.
Decide which lines contain a number before converting them.
