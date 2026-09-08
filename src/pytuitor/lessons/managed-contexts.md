# Context management is a protocol

`with manager as value:` calls `manager.__enter__()` and binds its result to `value`.
When the body finishes, Python calls `__exit__(exc_type, exc_value, traceback)`.
All three arguments are `None` for a normal exit.
On failure they describe the exception; returning a truthy value suppresses it.
Return `False` or `None` to let it propagate.
Cleanup normally should preserve failures.

A class defines a new kind of object, and calling the class constructs an instance.
Python then calls `__init__` with that instance as `self` and the supplied constructor arguments.
Instance methods also receive `self` automatically, so `self.label` stores a value on this particular object for later methods to use.

```python
class Announce:
    def __init__(self, label):
        self.label = label

    def __enter__(self):
        print("start", self.label)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("finish", self.label)
        return False


with Announce("report") as announcement:
    print(announcement.label)
```

Use suppression only for a narrow, deliberate contract.
`issubclass(error_type, ValueError)` includes subclasses; guard against `None` first.
If `__enter__` raises, Python does not call `__exit__` on that manager.

## Build

Define `Closing(resource)` as a context manager returning the supplied resource from `__enter__`.
After the body, call its `close()` exactly once on normal and exceptional exits, and suppress no exceptions.
Assume closing succeeds, and use a manager for only one `with` statement.
Also define `IgnoreValueError()` as a context manager suppressing only `ValueError` and its subclasses.
It must permit normal exit and propagate unrelated exceptions.
Do not print, open files, or read input.

## Repair

Closing returns the wrong object, omits cleanup, and hides errors.
The suppression manager hides every exception.
Restore cleanup and narrow suppression.
