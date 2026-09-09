## First in, first out
A queue serves work in arrival order, also called first in, first out or FIFO.
A stack serves the newest item first, also called last in, first out or LIFO.
A deque, pronounced "deck," is a double-ended queue: you can add or remove items at either end.
Python provides it as `collections.deque`.
A list can act as a queue, but removing its first item shifts all later items; `deque.popleft()` avoids that work.

```python
from collections import deque

jobs = deque(["wash", "dry"])
jobs.append("fold")
print(jobs.popleft())  # wash
print(list(jobs))  # ['dry', 'fold']
```

`append` adds one item on the right, `extend` adds each item from a collection on the right, and `popleft` removes and returns the leftmost item.
`pop` removes the rightmost item instead.
An empty deque is false in a condition; check it before removing anything.
For example, `if jobs:` runs its block only while the queue has items.
Removing from an empty deque raises `IndexError`.

## Build
Define `process_queue(waiting, arrivals, limit)` returning `(served, remaining)` as two lists.
`waiting` and `arrivals` are lists of strings, and `limit` is a nonnegative integer.
Place every arrival after everyone already waiting, then serve up to `limit` entries from the front.
Preserve order and duplicate entries.
For `(["a", "b"], ["c"], 2)`, return `(["a", "b"], ["c"])`.
A zero limit serves nobody; a limit larger than the queue serves everyone; two empty lists return `([], [])`.
Do not change either input list or print.
Try a deque; any implementation that returns the required results without changing the inputs is accepted.

## Repair
The broken function serves from the back.
People who arrived first should be served first.
