## Programs can receive arguments when they start
A command such as `python greet.py Sam --loud` starts a program with arguments.
Python's `argparse` module parses arguments and generates help text.
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
Without a list, `parse_args()` reads the process's real command-line arguments.
`type=int` converts an argument to an integer; `default=...` supplies an optional argument's fallback.

## Build
Define `make_parser()` that returns an `argparse.ArgumentParser`.
Add a required positional argument `name` and an optional `--count` integer argument whose default is `1`.
Do not parse arguments inside `make_parser()`.
The checks call `.parse_args(...)` on your returned parser.
For `["Ada", "--count", "3"]`, its attributes should be `.name == "Ada"` and `.count == 3`.
No top-level input or output is required.

## Repair
The broken parser leaves count as text and has the wrong default.
