# Separate instances, classes, and helpers

An ordinary method receives `self`, the instance.
A `@classmethod` receives `cls`, the class used for the call, making it useful for alternate constructors that respect subclasses.
A `@staticmethod` receives neither automatically; use it for a related helper that does not need instance or class state.

```python
class Coordinate:
    def __init__(self, x, y):
        self.x, self.y = x, y

    @classmethod
    def from_pair(cls, pair):
        return cls(*pair)

    @staticmethod
    def is_pair(value):
        return len(value) == 2
```

An abstract base class declares methods subclasses must implement before instances can be created.
Inherit from `abc.ABC` and mark required methods with `@abstractmethod`.
This provides explicit inheritance-based interfaces; the next lesson contrasts structural protocols.

```python
from abc import ABC, abstractmethod


class Writer(ABC):
    @abstractmethod
    def write(self, text):
        pass
```

## Build

Define abstract `Renderer` with required instance method `render(self, text)`.
Define concrete `PrefixRenderer(Renderer)` whose constructor stores the supplied string prefix and whose `render` prepends it to string text.
Provide static helper `valid_prefix(value)` returning whether a string contains any non-whitespace character.
Provide class method `from_text(text)` stripping surrounding whitespace and rejecting blank prefixes with `ValueError`.
The factory must return an instance of the class it was called on, including subclasses that inherit the constructor.
`Renderer` and subclasses that omit `render` must not be instantiable.
Do not print or read input.

## Repair

The base class does not enforce its interface, the factory ignores subclasses and whitespace, and rendering uses the wrong order.
Restore each contract.
