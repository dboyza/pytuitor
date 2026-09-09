## File operations need deliberate behavior
Before automation writes files, decide what happens if a destination already exists.
The `"w"` mode replaces a file.
The `"x"` mode creates a new file only if that name is unused and raises `FileExistsError` otherwise.
This is called exclusive creation.
A prior existence check alone has a gap: another program could create the file before the write starts.
Exclusive creation enforces the rule at the write itself.

Binary mode adds `b`, such as `"rb"` and `"xb"`.
It reads and writes raw bytes, the units used to store file data, without interpreting them as text.
Use it when copying a file exactly.
`shutil.copyfileobj(source_handle, destination_handle)` copies bytes between open files.

```python
import shutil

with open("source.dat", "rb") as source:
    with open("new.dat", "xb") as destination:
        shutil.copyfileobj(source, destination)
```

## Build
Define `copy_new(source, destination)`.
Copy the source's bytes to the destination and return `True` if a new destination was created.
If the destination already exists, return `False` without changing either file.
Use exclusive creation so the overwrite rule also holds if the file appears just before opening it.
The source is an existing regular file, meaning a file containing data rather than a folder or symbolic link.
The destination's parent folder exists.
Input/output errors, often shortened to I/O errors, report problems reading or writing data.
Let errors other than `FileExistsError` reach the caller instead of catching them or reporting a successful copy.

## Repair
The broken function uses a mode that destroys an existing destination.
Fix the open mode and catch `FileExistsError` when the destination name is already taken.
