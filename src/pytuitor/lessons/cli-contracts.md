# Define a predictable CLI

A command-line interface turns text arguments into a stable contract.
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

The result is a namespace with attributes such as `options.repeat`.
`store_true` sets a Boolean when the flag appears.
Argparse normally prints usage and exits with status two for invalid arguments, and status zero for help.
A CLI should write results to stdout and diagnostics to stderr; library functions should normally return values or raise exceptions.

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

Replace ad hoc indexing with parsing that supports the advertised options and ordering.
