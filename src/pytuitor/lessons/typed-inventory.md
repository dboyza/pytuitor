# Project: an inventory library

Split a reusable calculation from the file that exposes it to the tutor.
The workspace contains `lesson.py` and `inventory.py`.
Use the file picker to edit each; Build starts with both files empty.
Python treats a `.py` file as a module, so `from inventory import total_value` makes that module's function available in `lesson.py`.
Both files live together, and the workspace includes that directory among the locations Python searches when importing modules.

A `TypedDict` describes the expected keys of an ordinary dictionary to static type checkers.
It does not construct a special runtime container or enforce types.

```python
from typing import TypedDict, Iterable


class Measurement(TypedDict):
    unit: str
    amount: float


def units(rows: Iterable[Measurement]) -> list[str]:
    return [row["unit"] for row in rows]
```

## Build

In `inventory.py`, define a `Stock` TypedDict with `quantity: int` and `price: float` and implement `total_value(rows)`.
Annotate the function's iterable argument and numeric return value.
Each row contains those two keys, with a finite numeric price and integer quantity.
Return the sum of quantity times price across the rows, without rounding.
Reject a negative quantity or price with `ValueError`.
Zero values and an empty iterable are valid.
Do not mutate rows, print, or read input.
For three units priced at 4.5 and one unit priced at 2, return 15.5.

In `lesson.py`, import `total_value` from inventory so the tutor can call it.
Keep the implementation in its own module; the entry file is the public bridge.
The behavior checks run offline without a third-party type checker.
Review the annotations as part of your code review rather than treating passing runtime checks as proof of type correctness.

## Repair

Repair starts from the same two-file project with a faulty calculation.
Fix the module and retain the public import.
