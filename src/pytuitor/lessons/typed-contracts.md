# Describe relationships between types

Annotations document expectations; Python does not automatically enforce them.
`str | None` is a union allowing a string or `None`.
After checking `value is None`, a static checker can narrow the remaining branch to `str`.
`list[int]` describes a list containing integers; `Iterable[int]` also permits tuples, generators, and other iterable sources.

A type alias gives a longer annotation a reusable name: `Row = tuple[str, int]` lets you annotate `rows: list[Row]`.
It describes the same underlying types rather than creating a new runtime class.

A type variable connects input and output types without forcing one concrete type.
This Python 3.11-compatible example preserves the caller's element type:

```python
from collections.abc import Iterable
from typing import TypeVar

T = TypeVar("T")


def last_or(items: Iterable[T], default: T) -> T:
    result = default
    for item in items:
        result = item
    return result
```

`TypeVar` is for static reasoning, not runtime conversion.
For a reusable container, `class Box(Generic[T]):` uses `Generic` from `typing`, and `Box[int]` describes a box for integers.
Use a type variable when types must relate; use a union when a value has several permitted forms.

## Build

Write `first_or(items: Iterable[T], default: T) -> T`, using a type variable to describe the relationship.
Return the first value unchanged, or the supplied default when input is empty.
Accept one-pass iterables and consume at most one item.
Keep falsey values such as `0`, `False`, and `''`.
Write `parse_optional(text: str | None) -> int | None` returning `None` for `None` or whitespace-only text and otherwise the `int` conversion.
Allow signs and surrounding whitespace; invalid nonblank text raises `ValueError`.
Checks assess behavior, so annotation spelling is not prescribed.
Do not print or read input.

## Repair

The first-value helper fails on empty input and discards falsey values.
The parser confuses missing input with zero.
Restore the distinction and document the type relationships.
