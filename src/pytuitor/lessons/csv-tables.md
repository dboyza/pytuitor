## Rows and columns in a text file
CSV stores tabular data as rows of separated fields.
A field can contain a comma if it is quoted, so splitting each line at commas is not a reliable parser.
Python's `csv` module handles those details.

```python
import csv

with open("stock.csv", newline="", encoding="utf-8") as handle:
    for row in csv.DictReader(handle):
        print(row["item"], int(row["count"]))
```

`DictReader` uses the first row as column names and returns one dictionary for each remaining row.
Every field starts as a string, even when it contains digits.
`newline=""` lets the CSV module handle line endings correctly.
`print(a, b)` prints its arguments separated by a space.

## Build
Define `csv_total(path)` for a UTF-8 CSV with headers `item,quantity,price`.
Return the sum of `quantity * price` across all data rows.
Quantities and prices are nonnegative integers; prices represent whole credits.
A header-only file returns `0`.
Item names may contain quoted commas and should not affect the calculation.
Read the file without modifying it.

## Repair
The broken calculation adds quantity and price instead of multiplying them.
Use a small row you can calculate by hand to locate the mistake.
