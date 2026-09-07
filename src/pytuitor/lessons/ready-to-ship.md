## State a function's expected types

In `def parse_count(text: str) -> int:`, the annotations say that `text` should be a string and the result should be an integer.
They help readers, editors, and static type checkers understand your code.
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
To test that an error occurs without a testing library:

```python
try:
    parse_count("-1")
except ValueError:
    pass
else:
    raise AssertionError("Negative input was accepted")
```

The `except` block handles the expected error.
`pass` means "do nothing".
The `else` block runs only when the `try` block raised no error.

## Exercise

Implement `parse_count(text: str) -> int` to accept nonnegative integers with optional surrounding whitespace.
Use `int(text)` to convert text to an integer; it already accepts surrounding whitespace and raises `ValueError` for non-integer text.
Return `0` for `"0"` and `12` for `" 12 "`.
Raise `ValueError` for negative values and non-integer text such as `"2.5"` or `"hello"`.

Write assertions and exception checks in `test_parse_count()` for zero, whitespace, and invalid input.
Check runs your test against your implementation and deliberately broken versions to see whether it detects mistakes.

## Use the code in a project

A virtual environment gives a project its own installed packages.
Create one with `python -m venv .venv` in your project folder and activate it before installing tools.
On macOS and Linux, activation is `source .venv/bin/activate`.
Then `python -m pip install pytest` installs pytest into that environment and `python -m pytest` runs its tests.
These setup commands require your regular terminal, outside this lesson's Python console.

A `pyproject.toml` file records package metadata, dependencies, supported Python versions, and build configuration.
A console entry point maps a command name to a callable such as `package.cli:main`.
In later projects, keep calculation separate from command-line input and output so it can be tested independently.
