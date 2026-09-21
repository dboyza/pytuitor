A **log** is a sequence of messages recording what a program did.
A message's **severity** identifies how serious it is, such as informational, warning, or error.
Line-oriented reports are useful because a program can process a large log without first copying every line into a list.

`sys.stdin` is an iterable of text lines.
A `for` loop can read those lines one at a time until the input ends.
`json.dumps(value)` converts a Python dictionary into JSON text that another program can read reliably.

`str.strip()` removes surrounding whitespace.
`str.split(maxsplit=1)` separates a leading field from the rest of a line while preserving spaces inside the message.

```python
line = " warning   low disk "
parts = line.strip().split(maxsplit=1)
print(parts)
```

This gives `['warning', 'low disk']`.
Check the number of fields before accessing a message field.
Normalize a severity field before looking it up in a fixed set of report categories.
Keep parsing separate from the command-line entry point so callers can provide any iterable of lines.

Python sets `__name__` to `"__main__"` when running a file directly.
An `if __name__ == "__main__":` guard prevents an imported module from unexpectedly reading standard input or printing output.

In a regular terminal, shell redirection such as `python report.py < app.log` supplies a file as standard input.
The same standard-library approach can support other line-oriented reports without installing packages.
