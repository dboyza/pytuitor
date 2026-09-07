## Build a log analyzer

Write a program that counts log messages by severity and displays a JSON report.
Use only Python's standard library, so the exported program can run without extra packages.

`import sys` makes standard input available as `sys.stdin`.
It is an iterable of text lines; a `for` loop reads until end-of-input.
`import json` gives you `json.dumps(value)`, which converts a dictionary into JSON text.

## Implement the counting function

`summarize(lines)` should return a dictionary with exactly these keys: `"INFO"`, `"WARNING"`, and `"ERROR"`.
Start every count at zero, including levels that never appear.
Each valid line contains a level, whitespace, and a nonempty message.
Ignore empty lines, unknown levels, and lines with no message.
Allow surrounding whitespace and normalize the level to uppercase.

```python
line = " warning   low disk "
parts = line.strip().split(maxsplit=1)
print(parts)
```

This gives `['warning', 'low disk']`.
`.strip()` removes whitespace from the ends; `.split(maxsplit=1)` separates the level from the rest of the message.
`parts[0].upper()` gives `WARNING`.
Check that `len(parts) == 2` before accessing the message.
`level in counts` checks whether a dictionary contains that key.
`counts[level] += 1` increments the corresponding count.
Process the input iterable once without converting it to a list.

## Add a command-line entry point

Implement `main()` to pass `sys.stdin` to `summarize`, then print the result using `json.dumps`.
At the bottom of your program, write `if __name__ == "__main__":` and put an indented `main()` call underneath it.
Python sets `__name__` to `"__main__"` when running the file directly; when another file imports it, the guarded call does not run.

Use Run, type log lines into the console, and press Enter after each line.
Press **Ctrl+D** in the console to signal end-of-input and see the report.
Check supplies example logs automatically.

## Try it on a real file

Use **Ctrl+P**, search for **Export code**, and press Enter.
In your regular terminal, run the exported file with `python your_export.py < app.log`.
The shell's `<` supplies the contents of `app.log` as standard input.

Next, add a pytest suite for `summarize` and package the program with a console entry point.
