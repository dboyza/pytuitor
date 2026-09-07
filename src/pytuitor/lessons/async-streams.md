# Consume an async stream

Some producers must await I/O before the next item is ready.
An async iterator exposes that waiting through `__anext__`; `async for` handles the protocol for you.
An async function containing `yield` is an async generator.
It can both await and yield during iteration.

```python
import asyncio


async def messages():
    for message in ["start", "finish"]:
        await asyncio.sleep(0)
        yield message


async def lengths():
    result = []
    async for message in messages():
        result.append(len(message))
    return result
```

A normal `for` cannot consume an async generator.
`async for` belongs inside an async function and may suspend between iterations.
Returning a final list is appropriate when the contract needs the whole finite result; streaming outputs would instead call for another async generator.

## Build

Write `async def collect_nonempty(source)`.
The source is a finite async iterable of strings.
Strip surrounding whitespace from each string, discard empty results, and return a list of the remaining strings in source order.
Preserve duplicates and internal whitespace.
Empty input returns `[]`.
For an async source yielding `'  east '`, `' '`, and `'west'`, return `['east', 'west']`.
Allow source exceptions to propagate.
Do not print, modify the source, or run a new event loop inside the function.

## Repair

Repair already iterates asynchronously but does not fulfill the normalization contract.
Fix that behavior while keeping the async interface.
