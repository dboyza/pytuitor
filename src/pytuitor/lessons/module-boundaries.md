# Keep imports predictable

A Python file is a module.
Its **namespace** is the collection of names it defines, such as function and variable names.
`from tools import normalize` imports a named object from `tools.py`.
The module body executes on its first import in a process, and later imports normally reuse its entry in `sys.modules`.
A module's **API**, or application programming interface, is the set of functions and other objects that callers use.
Importing a reusable module should usually define these objects without printing, asking for input, or starting work.

```python
# helpers.py
def loud(text):
    return text.upper()


if __name__ == "__main__":
    print(loud("demo"))
```

The guard runs the demonstration when that file is executed as the main program, but not when imported as helpers.
A local file named `json.py` or `typing.py` may be imported instead of the standard-library module with that name.
This is called **shadowing**; choose a different name to avoid it.
Packages group modules under directories, conventionally with an `__init__.py`; imports inside a package may be absolute or explicitly relative, such as `from .helpers import loud`.

## Build

The workspace has `lesson.py` and `tools.py`.
Implement `normalize(text)` in tools.py, then import it into lesson.py.
Return the words of text in lowercase, joined by single hyphens.
Whitespace includes spaces, tabs, and newlines; discard surrounding whitespace and collapse runs.
A blank string returns `""`.
For example, `'  Build  REPORT '` becomes `'build-report'`.
`text.split()` without a separator splits on runs of whitespace, and `'-'.join(words)` joins strings with hyphens.
Importing or reloading tools must produce no output.
Do not read input.

## Repair

Fix the reusable module, including the unwanted printing when another file imports it.
That printing is a **side effect**, an action beyond defining the objects the importer needs.
Each Check case runs in a fresh project workspace to avoid results depending on an earlier import.
