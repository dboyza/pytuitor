## Build a small data pipeline
A data pipeline is a sequence of steps that reads data, changes it, and saves the result.
Here, the input format is CSV and the output format is JSON.
You have already practiced all three operations separately.
This project connects them in one function.

## Build
Define `summarize_expenses(source, destination)`.
Read a UTF-8 CSV file with headers `category,amount` from `source`.
Amounts are nonnegative integer cents, so you can add them exactly without decimal rounding.
Group amounts by category into a dictionary, write that dictionary as JSON to `destination`, and return it.
The destination's parent folder already exists.
A header-only file produces `{}`.
Preserve category text exactly, including commas represented by CSV quoting.
Do not change the source file.

For these CSV rows:

```text
category,amount
travel,250
food,600
travel,150
```

Return and save `{"travel": 400, "food": 600}`.
JSON whitespace and key order do not matter.
The tools you have practiced fit together here: `csv.DictReader` reads rows, a dictionary keeps each category's running total, and `json.dump` saves the result.
The function receives paths from its caller, so it does not need input prompts.

## Repair
The broken program overwrites the previous amount for repeated categories.
Check a category that appears more than once, not just distinct categories.
