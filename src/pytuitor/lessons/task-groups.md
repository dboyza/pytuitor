# Give tasks a shared lifetime

Awaiting one operation at a time is sequential.
A task schedules a coroutine so it can make progress alongside other tasks when they yield control.
Python 3.11 introduced `asyncio.TaskGroup` to give related tasks a shared lifetime.

```python
import asyncio


async def pair():
    async with asyncio.TaskGroup() as group:
        first = group.create_task(asyncio.sleep(0, result="left"))
        second = group.create_task(asyncio.sleep(0, result="right"))
    return [first.result(), second.result()]
```

The async context manager waits for its tasks before exiting.
If a task fails with an ordinary exception, the group cancels remaining tasks, waits for their cleanup, and raises an `ExceptionGroup` containing failures.
`try` with `except* ValueError` can handle matching parts of an exception group; do not combine ordinary `except` and `except*` clauses in the same try statement.
Cancellation is a control signal: use `finally` for cleanup and normally let `asyncio.CancelledError` propagate.

## Build

Define `async def collect_jobs(jobs)`.
`jobs` is a finite iterable of no-argument callables; each call returns a fresh coroutine.
Call each factory once and schedule all jobs in a TaskGroup.
Return their results in input order, regardless of completion order.
Empty input returns `[]`.
On failure, let the TaskGroup's exception group propagate after sibling cleanup.
Do not suppress errors or create a nested event loop.
For factories returning 8 then 3, return `[8, 3]`.
No printing is required.

## Repair

The broken function processes jobs sequentially and reverses the result order.
Repair the task lifetime and ordering contract.

See the [TaskGroup reference](https://docs.python.org/3.11/library/asyncio-task.html#task-groups) for additional detail.
