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

## Race results without leaving work behind

A different concurrency problem is waiting for the first successful result among several attempts.
`asyncio.create_task(coroutine)` starts an independent task in the current event loop.
Unlike TaskGroup membership, creating a task this way gives your code responsibility for its lifetime.
`asyncio.as_completed(tasks)` supplies awaitables in completion order; iterate normally and await each to receive its value or exception.
An ordinary failed attempt need not stop the other attempts.

```python
for pending in asyncio.as_completed(tasks):
    try:
        value = await pending
    except Exception:
        continue
    print(value)
```

`task.done()` reports whether a task has finished, and `task.cancel()` requests cancellation.
Cancellation is a request, so await the cancelled task to let its `finally` blocks finish.
`await asyncio.gather(*tasks, return_exceptions=True)` joins every task and collects errors as results during cleanup.
Put cancellation and joining in a `finally` block so they also run when the caller cancels your function.
`CancelledError` inherits from `BaseException`, not `Exception`; catching ordinary attempt failures must not hide caller cancellation.
