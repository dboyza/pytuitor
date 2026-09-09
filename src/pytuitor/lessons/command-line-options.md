## Programs can receive arguments when they start
A command such as `python greet.py Sam --loud` starts a program with arguments.
Python's `argparse` module reads those command-line arguments, checks their expected form, and generates help text.
A flag such as `--loud` enables an option; a positional argument such as `Sam` supplies a required value.

```python
import argparse


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--loud", action="store_true")
    return parser.parse_args(args)
```

Calling `parse_args(["Sam", "--loud"])` returns an object with `.name` equal to `"Sam"` and `.loud` equal to `True`.
Passing a list makes parsing easy to test without starting another terminal.
Without a list, the parser's `.parse_args()` method reads the arguments used to start the running program.
When passed to `.add_argument(...)`, `type=int` converts the argument to an integer.
`default=1` supplies `1` when the caller leaves out that optional argument.

## Build
Define `make_parser()` that returns an `argparse.ArgumentParser`.
Add a required positional argument `name` and an optional `--count` integer argument whose default is `1`.
Do not parse arguments inside `make_parser()`.
The checks call `.parse_args(...)` on your returned parser.
For `["Ada", "--count", "3"]`, its attributes should be `.name == "Ada"` and `.count == 3`.
Do not request keyboard input or print anything when this file runs.

## Repair
The broken parser leaves count as text and has the wrong default.
