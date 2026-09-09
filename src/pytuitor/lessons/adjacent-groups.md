# Group consecutive items

`itertools.groupby(items, key=function)` splits an iterable whenever its key changes.
The same key can appear in several separate groups.
A **run** is an uninterrupted sequence of items with the same key.
For example, `A, A, B, A` has three runs: `A, A`, then `B`, then `A`.
Sorting first would change the meaning when original order matters.

```python
from itertools import groupby

readings = [12, 14, 21, 13]
for decade, group in groupby(readings, key=lambda value: value // 10):
    print(decade, list(group))
```

The result contains decade labels `1`, `2`, then `1` again.
A group's iterator shares its input with the outer iterator.
Consume or copy the group before advancing the outer iterator if its values must remain available.
The tool compares adjacent keys using equality, so labels can even be lists.
Lists are **unhashable**, meaning they cannot be dictionary keys or set members, but they can still be compared for equality.

## Build

Write `runs(items, key)` returning an iterator of `(label, values)` tuples for consecutive equal keys.
`key` is a one-argument callable, and each `values` must be a separate list retaining the original items in order.
Accept finite one-pass input; empty input yields nothing.
Do not sort, merge nonadjacent groups, or require hashable labels.
For example, `list(runs('aba', str))` is `[('a', ['a']), ('b', ['b']), ('a', ['a'])]`.
Saved lists must remain usable after the outer iterator advances.
Do not print or read input.

## Repair

The dictionary implementation combines nonadjacent occurrences and rejects unhashable labels.
Keep each consecutive group separate instead of combining all occurrences of a label.
