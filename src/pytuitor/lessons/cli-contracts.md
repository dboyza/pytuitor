# Define a predictable CLI

A **command-line interface (CLI)** lets someone run a program by typing its name and arguments in a terminal.
Python's standard-library `argparse` provides positional arguments, options, conversion, and generated help.
An argument list passed explicitly is easier to test than code that reads global `sys.argv` everywhere.

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("name")
parser.add_argument("--repeat", type=int, default=1)
parser.add_argument("--loud", action="store_true")
options = parser.parse_args(["Ada", "--repeat", "2"])
```

A **positional argument**, such as `name`, is identified by its position.
An **option** starts with a name such as `--repeat` and may take a value.
A **flag**, such as `--loud`, is an option whose presence switches something on.
The returned object holds parsed values as attributes such as `options.repeat`.
Here, `type=int` converts text to an integer and `default=1` supplies a value when the option is absent.
`store_true` sets a Boolean when the flag appears.
An **exit status** is the number a program reports when it ends: zero usually means success.
Argparse raises `SystemExit` after printing a usage message for invalid arguments (status two), or help for `--help` (status zero).
**Standard output (stdout)** carries normal results, usually from `print`.
**Standard error (stderr)** carries error messages separately, which helps when another program reads the results.
Reusable functions should normally return values or raise exceptions so their callers choose how to display them.

## Build

Implement `parse_options(argv)` with argparse.
`argv` is a list of strings excluding the program name.
Require one positional argument named `path`.
Accept `--limit` as an integer with default ten and `--json` as a Boolean flag defaulting to false.
Return a plain dictionary containing `path`, `limit`, and `json`.
Options may occur before or after the path.
A path containing spaces arrives as one list item; do not split it again.
Zero and negative limits are accepted here, leaving their application meaning to the caller.
For `['report.txt', '--json']`, return `{'path': 'report.txt', 'limit': 10, 'json': True}`.
Let argparse handle invalid input and help in its normal way.
Do not parse arguments at import time.

## Repair

Replace manually reading fixed list positions with parsing that supports the advertised options and ordering.
