## First in, first out
A queue serves work in arrival order, also called first in, first out or FIFO.
A stack serves the newest item first, also called last in, first out or LIFO.
`collections.deque` efficiently adds or removes items at either end.
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
Removing from an empty deque raises `IndexError`.

## Build
Define `process_queue(waiting, arrivals, limit)` returning `(served, remaining)` as two lists.
`waiting` and `arrivals` are lists of strings, and `limit` is a nonnegative integer.
Place every arrival after everyone already waiting, then serve up to `limit` entries from the front.
Preserve order and duplicate entries.
For `(["a", "b"], ["c"], 2)`, return `(["a", "b"], ["c"])`.
A zero limit serves nobody; a limit larger than the queue serves everyone; two empty lists return `([], [])`.
Do not change either input list or print.
Try a deque; any implementation with the same observable behavior is accepted.

## Repair
The broken function serves from the back.
People who arrived first should be served first.
