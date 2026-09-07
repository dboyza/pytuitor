# Program to a small protocol

Python often works best when a function asks an object to perform an operation rather than checking its concrete class.
This is duck typing.
A `typing.Protocol` describes that expected shape for static type checkers without requiring inheritance by users of your API.

```python
from typing import Protocol


class Named(Protocol):
    name: str


def title(item: Named) -> str:
    return item.name.upper()
```

`class Named(Protocol)` declares a protocol; annotated members describe its contract.
For a method declaration, a body of `...` is an ellipsis placeholder.
Annotations do not enforce the protocol at runtime.
`@runtime_checkable` enables limited runtime attribute checks, but it does not validate full type signatures and is unnecessary here.

`io.StringIO` is an in-memory text stream useful for testing.
Its `write(text)` method adds text, and `getvalue()` returns all accumulated text.
Other writers may return `None` from `write`; avoid depending on that return value.

## Build

Define a `Writer` protocol with a `write(self, text: str)` method, then implement `emit_lines(writer: Writer, lines)`.
For each string in the finite iterable `lines`, call `writer.write` once with that string followed by exactly one newline character.
Input strings do not already contain newline characters.
Return the number of input lines written.
Accept any object with the required method, including unrelated classes; do not require `isinstance` or inheritance.
Empty input returns zero without writes.
For `['one', 'two']`, a StringIO should contain `'one\ntwo\n'` and the return value should be two.
Do not write to global stdout.

## Repair

Repair needs correct line endings and a count independent of the writer's return value.
