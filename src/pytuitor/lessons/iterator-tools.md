# Consume only what you need

An iterable can provide an iterator; an iterator remembers its position.
`iter(values)` obtains an iterator, and `next(iterator)` advances it or raises `StopIteration` when exhausted.
The optional second argument to `next` supplies a default instead of raising.
A generator function uses `yield` and pauses between values, as in the previous lesson.

```python
from itertools import islice

source = iter(range(100))
first_three = list(islice(source, 3))
next_two = list(islice(source, 2))
```

`islice` requests only the selected part of a stream.
Collecting an infinite stream into a list would never finish.
A lazy operation must read only enough input to produce the next requested result.
Once you yield a mutable object, callers may keep it.
Reusing and clearing that same list for the next batch would change the caller's previous result too.

## Build

Write the generator `batches(items, size)`.
`size` is an integer and must be positive; raise `ValueError` for zero or negative sizes when iteration starts.
Yield lists containing up to `size` consecutive items.
Yield a shorter final list if necessary, but never an empty batch.
For example, `list(batches('abcde', 3))` is `[['a', 'b', 'c'], ['d', 'e']]`.
Accept one-pass and infinite iterables while consuming only enough input for the next requested batch.
Each yielded batch must be a separate list.
Do not print or read input.

## Repair

Repair currently drops useful data when the final batch is short.
Restore that behavior and add the argument validation.
