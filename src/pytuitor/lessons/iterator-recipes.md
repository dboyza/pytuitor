# Assemble iterator recipes

`itertools` contains small tools for combining streams.
`chain.from_iterable(groups)` flattens one level lazily.
`islice(source, count)` requests at most that many items without exhausting the source.
Together they support previews even when a group is infinite.

```python
from itertools import chain, islice, zip_longest, product

preview = list(islice(chain.from_iterable([["a"], ["b", "c"]]), 2))
```

Ordinary `zip` stops at the shortest input.
`zip_longest(left, right, fillvalue=None)` continues to the longest and pads missing values.
`product(left, right)` produces every pair, with the left item changing slowest.
Unlike chain, product stores its input pools and requires finite inputs.

```python
rows = list(zip_longest(["name", "age"], ["Lin"], fillvalue=None))
outfits = list(product(["blue", "green"], ["small", "large"]))
```

## Build

Write `preview(groups, limit)` returning up to `limit` values flattened from an iterable of iterables.
`limit` is an integer; reject negative values with `ValueError`, and consume no items for zero.
Never consume more inner values than requested, and support one-pass groups and infinite inner iterables.
Write `align(left, right)` returning a list of pairs padded with `None` through the longer finite input.
Write `combinations(left, right)` returning all pairs of values from finite inputs, with the left input changing slowest.
An empty input produces no combinations.
Return lists of tuples for pairs; do not print or read input.
Equivalent implementations are welcome.

## Repair

The preview eagerly exhausts its inputs, alignment truncates, and combinations omit pairs.
Restore each tool's distinct contract.
