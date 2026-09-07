## Dates have calendar rules
Months have different lengths, and leap years add another complication.
The standard-library `datetime` module handles calendar arithmetic.
A `date` represents a calendar day without a time or timezone.

```python
from datetime import date, timedelta

start = date.fromisoformat("2024-02-28")
finish = start + timedelta(days=2)
print(finish.isoformat())
```

This prints `2024-03-01` because 2024 is a leap year.
ISO date strings use `YYYY-MM-DD` so they are unambiguous.
`.fromisoformat()` parses them; `.isoformat()` returns that format.
`timedelta(days=...)` represents a duration in days.
Subtracting two dates returns a timedelta whose `.days` attribute gives the whole-day difference.
Malformed dates raise `ValueError`.

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
