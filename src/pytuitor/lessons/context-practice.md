# Restore temporary state

A context manager performs setup before a `with` block and cleanup afterward.
The `with` statement runs its exit behavior even if the block raises an exception.
A generator decorated with `contextlib.contextmanager` expresses this using one `yield`.

```python
from contextlib import contextmanager


@contextmanager
def marked(events):
    events.append("enter")
    try:
        yield events
    finally:
        events.append("leave")


log = []
with marked(log) as current:
    current.append("work")
```

The value yielded becomes the value after `as`.
When the block ends normally, execution resumes after `yield`.
If it raises, that exception is raised at the suspended `yield`.
A `finally` clause runs in both cases.
Suppressing an exception means handling it without passing it back to the caller.
Do this only when the required behavior explicitly calls for it.

## Build

Create `temporary_value(mapping, key, value)` as a context manager.
During `with temporary_value(...) as current`, the mapping must contain the temporary value and `current` must be that same mapping object.
On exit, restore the previous value if the key originally existed; otherwise remove the newly added key.
Restore on both normal exit and exceptions, allowing the original exception to propagate.
A preexisting value of `None` is a real value and must be restored.
The with-body will not remove the target key; nested use of your context manager should work.
For example, temporarily changing `{'mode': 'safe'}` to mode `'fast'` must leave mode `'safe'` afterward.
Do not print.

## Repair

Check both exception cleanup and absent-key cleanup.
`mapping.get(key)` alone cannot tell an absent key from a key holding `None`.
