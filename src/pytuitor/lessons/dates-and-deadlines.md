## Dates have calendar rules
Months have different lengths, and leap years add another complication.
The standard-library `datetime` module handles calendar arithmetic.
A `date` represents a calendar day without a clock time.
It also has no time zone, a region's convention for setting its clocks.

```python
from datetime import date, timedelta

start = date.fromisoformat("2024-02-28")
finish = start + timedelta(days=2)
print(finish.isoformat())
```

This prints `2024-03-01` because 2024 is a leap year.
We use the ISO date format `YYYY-MM-DD`: a four-digit year, two-digit month, and two-digit day.
For example, `2024-03-01` means March 1, 2024.
`.fromisoformat()` reads the text and creates a date object; `.isoformat()` converts a date back to that text format.
`timedelta(days=...)` represents a duration in days.
Subtracting two dates returns a `timedelta` object whose `.days` attribute gives the number of days between them.
Text that does not describe a valid date raises `ValueError`.

## Build
Define `due_date(start, days)`.
`start` is a valid ISO date string and `days` is a nonnegative integer.
Return the ISO date exactly that many days after `start`.
Zero days returns the same date.
Handle month ends, year ends, and leap days by using date arithmetic.
For `due_date("2023-12-31", 1)`, return `"2024-01-01"`.
Do not use today's date: the supplied start makes results predictable and easy to test.

## Repair
The broken calculation counts the starting day as an elapsed day.
Check the zero-day case to make the intended meaning clear.
