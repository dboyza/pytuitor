## Clean up even when something fails

A **context manager** handles setup and cleanup around a block of code.
For example, `with open("notes.txt") as file:` opens a file and closes it when the block ends, even if an exception occurs.
The methods `__enter__` and `__exit__` implement this protocol for a class.

For a small context manager, `contextlib.contextmanager` lets you write a generator with exactly one `yield`:

```python
from contextlib import contextmanager


@contextmanager
def example():
    print("Starting")
    try:
        yield "ready"
    finally:
        print("Finished")


with example() as status:
    print(status)
```

Code before `yield` runs when entering the block.
The yielded value becomes `status`.
Code in `finally` runs during cleanup, whether the block finishes normally or raises an exception.
An exception is an error that interrupts normal execution; a `try`/`finally` ensures cleanup without suppressing that error.

## Await asynchronous operations

`async def` defines a coroutine function.
Calling it creates a coroutine object; `await` executes it and waits for its result within an event loop.
Use `asyncio.run(coroutine)` to run an async entry point from ordinary synchronous code.

`asyncio.gather(first, second)` schedules the supplied coroutine objects so they can make progress together.
Awaiting the result waits for their values and returns a list in argument order, even if the second operation finishes first.
The expression `(double(v) for v in values)` creates a generator of coroutine objects.
Putting `*` before it in a function call passes those objects as separate arguments, equivalent to `gather(double(a), double(b))` for two values.
Calling `gather` with no arguments produces an empty result list when awaited.
**I/O** means input/output, such as reading from a network connection.
Async helps when operations can let other work run while waiting for I/O; ordinary blocking calls still prevent the event loop from progressing.

## Exercise

Import `contextmanager` from `contextlib`, then write `def session(events):` with `@contextmanager` directly above it so it appends `"open"` on entry, yields the events list, and always appends `"close"` on exit.
Use `try`/`finally` so cleanup also happens when the caller raises an error.

Next, write `import asyncio`.
Define `async def double(value):` with `await asyncio.sleep(0)` followed by `return value * 2`.
The sleep yields control so other scheduled coroutines can run.
Then define `async def double_all(values):` using `await asyncio.gather(...)` to call `double` for every value.
Return results in input order, including an empty list for empty input.
Schedule all operations together rather than awaiting each one in a loop.
