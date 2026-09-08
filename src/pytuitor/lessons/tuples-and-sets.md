## Keep a fixed group together

A **tuple** is an ordered collection whose items cannot be replaced, added, or removed after creation.
Write a pair with parentheses and a comma, such as `point = (3, 8)`.
The comma makes it a tuple; a one-item tuple needs a trailing comma, as in `(3,)`.
`tuple([3, 8])` converts a list into a tuple.
Tuples support indexing and `len()` just like lists.

**Unpacking** assigns the items of a collection to separate names in order:

```python
point = (3, 8)
x, y = point
print(x)
print(y)
```

This prints `3` and then `8`.
The number of names must match the number of items; otherwise Python raises `ValueError`.
Unpacking also works with lists and with the pairs produced by loop helpers in the next lesson.

## Keep unique values in a set

A **set** holds distinct values, with no guaranteed display or iteration order.
Create one from a list with `set(...)`.
Repeated values appear only once.
An empty set is `set()`, not `{}`.

```python
colors = set(["blue", "gold", "blue"])
print(len(colors))
print("gold" in colors)
print("red" not in colors)
```

This prints `2`, `True`, and `True`.
`True` and `False` are Boolean values, the results of yes-or-no questions.
The **membership** operator `in` asks whether a value is present; `not in` asks whether it is absent.
These operators also work with lists and tuples.
Sets do not support indexing, because there is no first or last position.

## Build

Read two input lines; you may choose any prompts.
The first line contains exactly two space-separated names.
Store them as a tuple called `pair`, then assign its first item to `first` and its second item to `second`.
The second line contains zero or more space-separated visitor names, possibly repeated.
Store the distinct visitors in a set called `seen`.
Names are case-sensitive, so `Ada` and `ada` are different.

Print three lines: whether `first` is in `seen`, whether `second` is in `seen`, and the number of distinct visitors.
Use Python's `True` and `False` spelling for membership results.
For first line `Mira Sol` and second line `Sol Sol Bo`, print `False`, `True`, and `2` on separate lines.
For an empty second line, print `False`, `False`, and `0`.
Keep `pair`, `first`, `second`, and `seen` available for checks; do not print the set itself, since its order is not guaranteed.

## Repair

The supplied program reverses the two names and counts repeat visits as separate visitors.
Fix it to preserve the first line's order and count only distinct visitor names.
