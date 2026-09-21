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
