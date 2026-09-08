# Functions are values

A callable is an object you can call with parentheses, including a function.
Pass a function without parentheses when another function should call it later.
`sorted(items, key=function)` calls the key function for each item and sorts by those keys, returning a new list.
Sorting is stable: items with equal keys retain their original order.

```python
names = ["Ada", "Christopher", "Lin"]
by_length = sorted(names, key=len)
by_last_letter = sorted(names, key=lambda name: name[-1])
```

`lambda name: expression` creates a small anonymous function that returns the expression.
Use `def` when a function needs several statements or a descriptive name.
A closure can remember values from its enclosing function.
`functools.partial` is another way to make a callable with arguments already supplied.

```python
from functools import partial


def surround(text, left, right):
    return left + text + right


quote = partial(surround, left='"', right='"')
print(quote("hello"))
```

## Build

Write `rank(records, key)` to return a new list sorted by the supplied one-argument callable.
Accept finite one-pass iterables, preserve equal-key order, and leave a caller's list unchanged.
Empty input returns `[]`.
Write `make_scaler(factor)` to return a reusable callable accepting one numeric value and multiplying it by the numeric factor.
Negative values and zero are allowed.
For example, `make_scaler(3)(4)` returns `12`.
A closure, partial application, or another equivalent callable is valid.
Do not print or read input.

## Repair

The sorter ignores its key, and the scaler adds instead of multiplying.
Fix both contracts.
