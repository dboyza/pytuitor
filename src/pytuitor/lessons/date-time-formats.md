## Calendar dates and clock times

A `date` identifies a calendar day, a `time` identifies a clock reading, and a `datetime` combines both.
`datetime.strptime(text, format)` reads text using a format string that describes where the date and time parts appear.
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

A datetime's `.date()` and `.time()` methods return just its date or time part.
`datetime.combine(day, clock)` joins a date and time into one datetime.
Do arithmetic on the combined datetime so crossing midnight preserves the new day.
These examples use calendar dates and clock readings without time-zone information.
They do not account for clocks changing for daylight saving or compare times in different time zones.

## Build

Define `appointment(day, clock, minutes)`.
`day` uses `DD/MM/YYYY` and `clock` uses `HH:MM` on a 24-hour clock.
`minutes` is the integer number of minutes to add; a negative value moves backward and zero leaves the date and time unchanged.
Return the resulting date and time as `YYYY-MM-DD HH:MM`.
Reject invalid dates and clock values with `ValueError`; you may let parsing raise it.
Inputs otherwise follow the stated formats, and results remain in Python's supported year range.
Do not read input or print.
`appointment('31/12/2024', '23:50', 20)` returns `'2025-01-01 00:10'`.

## Repair

The program confuses day/month ordering and interprets minutes as hours.
Correct both conversions, including month boundaries and leap days.
