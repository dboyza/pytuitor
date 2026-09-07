# Project: a streaming report

A running report should produce useful output before its entire source is available.
Compose parsing, filtering, and accumulation without collecting the input first.
This project uses only strings, integer conversion, and the generator behavior already covered.

## Build

Define the generator `running_totals(lines)`.
Each input item is a string.
Strip surrounding whitespace; ignore empty strings and strings whose first non-whitespace character is `#`.
Every other string must be converted with `int` and added to the running total.
Yield the new total after every accepted integer.
Let `ValueError` propagate when a non-comment string is not a valid integer.
Do not ignore malformed data or round decimal strings.
An empty source yields nothing.
Accept a one-pass or infinite source without exhausting it before the first result.
Do not print or read input.

For example, `['10', ' # corrected', '-3', ' 2 ']` yields `10`, `7`, then `9`.
A comment or blank line produces no result.
`str.startswith('#')` checks the prefix after stripping.
`continue` skips the remaining statements in the current loop iteration.

## Repair

The broken implementation assumes every line contains an integer.
Preserve strict parsing for actual data while accepting the documented annotations.
