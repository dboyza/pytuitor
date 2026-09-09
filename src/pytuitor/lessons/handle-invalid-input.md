## An exception reports a failed operation
An **exception** reports an error while a program runs.
**Raising** an exception means reporting that error; **catching** or **handling** it means running code that responds to it.
`int("twelve")` raises `ValueError` because the text is not a valid integer.
A **block** is a group of indented instructions.
A `try` block lets you attempt an operation, and an `except` block handles a particular exception.

```python
def read_count(text):
    try:
        number = int(text)
    except ValueError:
        return 0
    return number
```

If conversion succeeds, Python skips the `except` block.
If it raises `ValueError`, Python runs that block instead.
Catch the specific exception you expect so unrelated programming mistakes remain visible.
`None` is a value used to represent the absence of a result.
It is different from the string `"None"` and the number `0`.
`result is None` is the conventional way to test for it.

## Build
To **parse** text is to read it as a value or structure your program can use.
Define `parse_quantity(text)`.
Convert a string to an integer and return it if it is nonnegative.
Return `None` if conversion fails or the integer is negative.
Surrounding whitespace and a leading plus sign are valid because `int()` accepts them.
`"3.5"` and `""` are invalid.
The input will always be a string; no input prompts or printed output are required.

## Repair
The provided function does not handle conversion errors and accepts negative quantities.
