# Await cooperative work

Asynchronous code can pause while waiting, allowing other work to make progress.
A **coroutine function**, written with `async def`, is a function that can use `await` to pause and resume.
Calling a coroutine function creates a coroutine object; its body runs when that object is awaited or scheduled.

An **event loop** coordinates this work, running ready operations and waiting when none are ready.
`asyncio.run(coroutine)` creates an event loop, runs the coroutine to completion, and closes the loop.
Use it once at a normal script boundary, not inside a running event loop.

```python
import asyncio


async def greet(person):
    await asyncio.sleep(0)
    return "Hello, " + person


# A script can print(asyncio.run(greet("Nora"))).
```


An **awaitable** is an object accepted by `await`, such as a coroutine object.
`await operation()` waits for that operation to finish and gives its result to the surrounding expression.
While an operation is waiting, the event loop can run other scheduled work.
Awaiting an already completed operation may not give other work a turn.
`asyncio.sleep(0)` explicitly lets other ready tasks take a turn.

This is **concurrency**: multiple operations make progress during the same period.
It is cooperative because each running operation must reach a point that lets others run.
A long calculation or `time.sleep` blocks the event loop, preventing other tasks from running on it.

**Parallelism** means executing work at the same instant, for example on multiple processor cores; async alone does not provide that.

## Build

Write `async def delayed_total(values)`.
Accept a finite iterable of numbers, await `asyncio.sleep(0)` once per value, and return their sum.
An empty iterable returns zero.
Accept a one-pass iterator and negative values.
Do not modify input, print, create your own event loop inside the function, or use `time.sleep`.
For `[4, -2, 6]`, awaiting the function produces eight.
The checks call `asyncio.run` for you; Run may use your own temporary script-level demonstration.

## Repair

Repair returns an incorrect total and omits the cooperative await.
Restore the required total and give other tasks a turn during each iteration.

The [official coroutine guide](https://docs.python.org/3.11/library/asyncio-task.html) provides further examples when you are online.
All required material is included here.
