# Model a small value object

A class groups state with behavior.
Methods receive the instance as their first parameter, conventionally named `self`.
A regular class initializes attributes in `def __init__(self, ...)`.
For records, `dataclasses.dataclass` can generate initialization, equality, and readable text for inspecting an object.
A **field** is a named piece of stored data, such as `x` or `y` below.
`@dataclass(...)` applies this behavior to the class written immediately below it, using its annotated fields.

`frozen=True` prevents normal attribute assignment; it does not recursively freeze objects stored in fields.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def shifted(self, dx, dy):
        return Point(self.x + dx, self.y + dy)
```

`Point(2, 4).shifted(1, 0)` constructs a new point.
Value equality compares field values, unlike the identity comparison `is`.
Annotations describe intended types but do not automatically validate values.
A hand-written class with equivalent behavior is also valid.

## Build

Implement `Item(name, quantity)` with accessible `name` and `quantity` attributes and value equality.
Names are strings and initial quantities are nonnegative integers.
Its method `restock(amount)` accepts an integer, returning a new Item with the same name and its quantity increased by amount.
Never change the original Item.
Reject negative amounts with `ValueError`; zero is valid and still returns a new Item.
For example, restocking `Item('washers', 8)` by two produces an Item with quantity ten while the original remains eight.
Two Items with the same name and quantity must compare equal.
Do not print.

## Repair

Repair mutates an existing object, surprising callers holding another reference to it.
Return a new object for an update and restore the invalid-amount check.
