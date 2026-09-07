# Await cooperative work

`async def` defines a coroutine function.
Calling it creates a coroutine object; its body runs when that object is awaited or scheduled by an event loop.
`asyncio.run(coroutine)` creates an event loop, runs the coroutine to completion, and closes the loop.
Use it once at a normal script boundary, not inside a running event loop.

```python
import asyncio


async def greet(person):
    await asyncio.sleep(0)
    return "Hello, " + person


# A script can print(asyncio.run(greet("Nora"))).
```

`await` suspends this coroutine until an awaitable completes.
`asyncio.sleep(0)` explicitly lets other ready tasks take a turn.
Coroutines provide cooperative concurrency; a long CPU loop or blocking `time.sleep` still blocks the event loop.
Async does not automatically make CPU-bound code run in parallel.

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
Restore both the numeric contract and the async behavior.

The [official coroutine guide](https://docs.python.org/3.11/library/asyncio-task.html) provides further examples when you are online.
All required material is included here.
