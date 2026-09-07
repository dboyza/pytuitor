# Project: bounded async work

Unbounded concurrency can overwhelm a service or exhaust local resources.
An `asyncio.Semaphore(limit)` permits at most that many tasks into a protected section.
Acquiring it with `async with` ensures the permit is released even when the work raises or is cancelled.

```python
semaphore = asyncio.Semaphore(3)


async def guarded(operation):
    async with semaphore:
        return await operation()
```

A semaphore limits active work, not the total number of scheduled tasks.
This project intentionally accepts a finite, reasonably sized batch; a production system with an unbounded source would need a bounded queue and fixed worker pool too.
TaskGroup supplies the sibling cancellation and cleanup behavior from the previous lesson.

## Build

Write `async def run_limited(values, worker, limit)`.
`values` is a finite iterable, `worker(value)` returns a fresh coroutine, and `limit` is an integer.
Reject a limit below one with `ValueError`, even for empty input.
Run up to limit worker calls concurrently while never exceeding that bound.
Use the available capacity rather than always running sequentially.
Call worker once for each input and return results in original input order.
Empty input returns `[]`.
If a worker fails, cancel unfinished sibling work, wait for cleanup, and propagate the grouped error from a TaskGroup.
No real networking or dependency installation is required.

For a worker that doubles its argument, inputs `[4, 2, 5]` with limit two produce `[8, 4, 10]`.
Checks use controlled yielding workers to inspect concurrency, not a speed benchmark.

## Repair

The broken batch runner schedules all calls without a bound.
Restore input validation, bounded execution, and the shared task lifetime.
