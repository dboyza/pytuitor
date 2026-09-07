# Project: an extensible formatter

Build a small plugin registry without making callers depend on concrete formatter classes.
Earlier lessons showed metaclass registration; this project uses the narrower `__init_subclass__` hook.
Python calls this hook on a parent when a subclass is created.
The hook receives the newly created subclass as cls, is implicitly a class method, and should call super to cooperate with other bases.

```python
class Base:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.label = cls.__name__.lower()
```

`cls.__dict__` contains attributes declared directly on that class.
Using it avoids mistaking an inherited attribute for an explicit new registration.
Classes are callable, so a registry holding a class can create an instance with `registry[key]()`.

## Build

Complete all three files.
In `registry.py`, define Formatter with an initially empty registry dictionary and a cooperative __init_subclass__ hook.
Register subclasses that explicitly declare a non-None kind string, mapping kind to the class.
Reject duplicate kinds with ValueError without overwriting the existing class.
A subclass that only inherits a kind must not create another registration.

In `formats.py`, import Formatter and define Upper and Surround as subclasses.
Upper declares kind `'upper'` and its `render(self, text)` returns the text in uppercase.
Surround declares kind `'surround'` and returns the text between square brackets, including `'[]'` for an empty string.

In `lesson.py`, import Formatter, Upper, and Surround, then define `format_text(kind, text)`.
Look up the registered class, create an instance, and return its render result.
Raise ValueError for an unknown kind.
Do not hardcode the two built-in names in the dispatcher: new subclasses defined after import must work immediately.
Keep import-time behavior limited to definitions and registration; do not print or read input.
For example, `format_text('surround', 'ready')` returns `'[ready]'`.

## Repair

Repair spans registration, formatting, and dispatch errors.
Use the Check results to locate which contract each file owns.
After both stages pass, consider whether a plain dictionary supplied explicitly would be simpler for a smaller application.
