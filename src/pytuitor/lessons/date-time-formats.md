## Calendar dates and clock times

A `date` identifies a calendar day, a `time` identifies a clock reading, and a `datetime` combines both.
`datetime.strptime(text, format)` parses text with an explicit format.
`strftime(format)` formats an existing value as text.

```python
from datetime import datetime, timedelta

start = datetime.strptime("2024-07-08 14:30", "%Y-%m-%d %H:%M")
finish = start + timedelta(minutes=45)
print(finish.strftime("%d/%m/%Y %H:%M"))
```

The output is `08/07/2024 15:15`.
`%Y` means four-digit year, `%m` month, `%d` day, `%H` hour in a 24-hour clock, and `%M` minute.
Uppercase and lowercase format letters have different meanings.
Invalid dates or incompatible text raise `ValueError`.

A datetime's `.date()` and `.time()` methods extract those components.
`datetime.combine(day, clock)` joins a date and time into one datetime.
Do arithmetic on the combined datetime so crossing midnight preserves the new day.
These examples use local calendar times without timezone information.
They do not account for daylight-saving transitions or elapsed time across different timezones.

## Build

Define `appointment(day, clock, minutes)`.
`day` uses `DD/MM/YYYY`, `clock` uses `HH:MM` on a 24-hour clock, and `minutes` is an integer offset, which may be negative or zero.
Return the resulting date and time as `YYYY-MM-DD HH:MM`.
Reject invalid dates and clock values with `ValueError`; you may let parsing raise it.
Inputs otherwise follow the stated formats, and results remain in Python's supported year range.
Do not read input or print.
`appointment('31/12/2024', '23:50', 20)` returns `'2025-01-01 00:10'`.

## Repair

The program confuses day/month ordering and interprets minutes as hours.
Correct both conversions, including month boundaries and leap days.
