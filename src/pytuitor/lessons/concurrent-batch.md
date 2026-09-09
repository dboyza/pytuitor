# Project: bounded async work

Starting too much work at once can overwhelm the service receiving it or use too much memory.
**Bounded concurrency** means setting a maximum number of operations allowed to run at once.
An `asyncio.Semaphore(limit)` permits at most that many tasks into a protected section.
Think of a **permit** as one available place in that limit.
Entering `async with semaphore:` waits until a place is available; leaving returns that place, including after an exception or cancellation.

```python
import asyncio

semaphore = asyncio.Semaphore(3)


async def guarded(operation):
    async with semaphore:
        return await operation()
```

A semaphore limits active work, not the total number of scheduled tasks.
This project accepts a finite, reasonably sized collection of inputs.
For an endless source, a real application would also need to limit how much work it holds waiting in memory.
TaskGroup supplies the cancellation and cleanup behavior taught in Give tasks a shared lifetime.
Create the semaphore inside the running function so each call has its own limit.

## Build

Write `async def run_limited(values, worker, limit)`.
`values` is a finite iterable, `worker(value)` returns a fresh coroutine, and `limit` is an integer.
Reject a limit below one with `ValueError`, even for empty input.
Run up to limit worker calls concurrently while never exceeding that bound.
Use the available capacity rather than always running sequentially.
Call worker once for each input and return results in original input order.
Empty input returns `[]`.
If a worker fails, cancel the other unfinished tasks, wait for cleanup, and allow the TaskGroup error to reach the caller.
No real networking or dependency installation is required.

For a worker that doubles its argument, inputs `[4, 2, 5]` with limit two produce `[8, 4, 10]`.
Checks use controlled yielding workers to inspect concurrency, not a speed benchmark.

## Repair

The broken batch runner schedules all calls without a bound.
Restore input validation, bounded execution, and the shared task lifetime.
