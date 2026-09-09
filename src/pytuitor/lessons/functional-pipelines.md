# Transform, select, accumulate

A **predicate** is a callable used to decide whether an item should be kept, usually by returning `True` or `False`.
A **lazy** operation does work only as results are requested.
An iterator provides those results one at a time and remembers its current position.
`map(function, iterable)` lazily transforms each value.
`filter(predicate, iterable)` lazily keeps values for which a callable returns a truthy result.
They return iterators, so `list(...)` consumes them to produce a list.
A comprehension often expresses the same operation more clearly.

```python
lengths = list(map(len, ["oak", "willow"]))
long_names = list(filter(lambda name: len(name) > 3, ["oak", "willow"]))
```

An **accumulator** holds the result built so far.
A **fold** repeatedly combines that result with the next item.
`functools.reduce(combine, items, initial)` performs a left fold.
Here `combine` is a **callback**, a function passed in for another operation to call.
Its first argument is the current accumulator and its second is the next item.
The explicit initial value also defines the result for empty input.
Prefer `sum`, `min`, `max`, or `any` when one directly expresses your intent.

```python
from functools import reduce

path = reduce(lambda parent, name: parent + "/" + name, ["notes", "today"], "home")
```

## Build

Write `transform_selected(items, predicate, transform)` returning a list of transformed values whose original values satisfy `predicate`.
Test the predicate before transforming; preserve order and accept finite one-pass iterables.
Write `fold(items, combine, initial)` applying `combine(accumulator, item)` once per item from left to right.
Return the final accumulator, or the original initial value for empty input.
The accumulator need not be numeric.
For example, `fold([2, 3], lambda acc, x: acc - x, 10)` returns `5`.
Loops, comprehensions, and library implementations are all valid.
Do not print or read input.

## Repair

The pipeline keeps every item, and the fold reverses the callback arguments.
Restore selection and left-to-right accumulation.
