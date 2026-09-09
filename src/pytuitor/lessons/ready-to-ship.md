## State a function's expected types

A **type hint** describes the type a value is expected to have.
Python writes these hints as **annotations**, extra information attached to parameters, return values, or variables.
In `def parse_count(text: str) -> int:`, `text: str` says the parameter should be a string, and `-> int` says the return value should be an integer.
A static type checker is a tool that inspects code for inconsistent types without running it.
Annotations help these tools, editors, and readers understand your code.
Python does not enforce them at runtime, so validation still belongs in your code when needed.

## Test behavior with assertions

An `assert` checks a condition and raises `AssertionError` if it is false:

```python
def test_zero():
    assert parse_count("0") == 0
```

The pytest tool discovers functions whose names start with `test_` and runs them.
The tutor can call your test directly, so you do not need to install pytest to complete this exercise.
Do not use `assert` to validate user input in production code: assertions can be disabled.

Use `raise ValueError("message")` when an input has an unacceptable value.
To test that an error occurs without a testing library, combine `try`, `except`, and `else`.
The `except` block handles the expected error.
`pass` means "do nothing".
The `else` block runs only when the `try` block raised no error.

```python
try:
    parse_count("-1")
except ValueError:
    pass
else:
    raise AssertionError("Negative input was accepted")
```


## Exercise

Implement `parse_count(text: str) -> int` to accept nonnegative integers with optional surrounding whitespace.
Use `int(text)` to convert text to an integer; it already accepts surrounding whitespace and raises `ValueError` for non-integer text.
Return `0` for `"0"` and `12` for `" 12 "`.
Raise `ValueError` for negative values and non-integer text such as `"2.5"` or `"hello"`.

Write assertions and exception checks in `test_parse_count()` for zero, whitespace, and invalid input.
Check runs your test against your implementation and deliberately broken versions to see whether it detects mistakes.

## Use the idea in a project

Keep calculation separate from command-line input and output so it can be tested independently.
The tutor runs this exercise and its tests offline without any package installation.
For setting up test tools outside the tutor and sharing a program with others, continue later to Build distributable tools in the syllabus.
