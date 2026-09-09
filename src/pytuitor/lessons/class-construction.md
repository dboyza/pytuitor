# Separate instances, classes, and helpers

A subclass extends another class: `class Child(Parent):` inherits methods from `Parent` unless it replaces them.
Creating an instance means calling a class to make an object, as in `Coordinate(2, 3)`.
An ordinary method receives `self`, the instance.
A `@classmethod` receives `cls`, the class used for the call, making it useful for alternate constructors: named methods that create instances.
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

`cls(*pair)` unpacks the two values in `pair` into positional arguments and calls the class stored in `cls`.
Using `cls` rather than a fixed class name lets an inherited constructor create the subclass that was called.

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
Define `PrefixRenderer(Renderer)` as a subclass implementing that method.
Its constructor must store the supplied string prefix, and its `render` method must prepend that prefix to string text.
Provide static helper `valid_prefix(value)` returning whether a string contains any non-whitespace character.
Provide class method `from_text(text)` stripping surrounding whitespace and rejecting blank prefixes with `ValueError`.
The factory must return an instance of the class it was called on, including subclasses that inherit the constructor.
`Renderer` and subclasses that omit `render` must not be instantiable.
Do not print or read input.

## Repair

The base class does not enforce its interface, the factory ignores subclasses and whitespace, and rendering uses the wrong order.
Restore each contract.
