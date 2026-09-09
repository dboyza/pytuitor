# Project: an extensible formatter

A **plugin** is an additional component that a program can use without changing the code that selects components.
A **registry** maps names to the available components.
Build a formatter registry so a caller can request a formatter by name without knowing which class implements it.
Earlier lessons showed metaclass registration; this project uses the narrower `__init_subclass__` hook.
A **hook** is a method called automatically at a particular point; Python calls this one on a parent when a subclass is created.
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
In `registry.py`, define `Formatter` with an initially empty `registry` dictionary and an `__init_subclass__` method.
Have that method call `super().__init_subclass__(**kwargs)` so other parent classes can also handle subclass creation.
Register subclasses that explicitly declare a non-None kind string, mapping kind to the class.
Reject duplicate kinds with ValueError without overwriting the existing class.
A subclass that only inherits a kind must not create another registration.

In `formats.py`, import Formatter and define Upper and Surround as subclasses.
Upper declares kind `'upper'` and its `render(self, text)` returns the text in uppercase.
Surround declares kind `'surround'` and returns the text between square brackets, including `'[]'` for an empty string.

In `lesson.py`, import Formatter, Upper, and Surround, then define `format_text(kind, text)`.
Look up the registered class, create an instance, and return its render result.
Raise ValueError for an unknown kind.
The **dispatcher** is the function selecting which formatter to call, here `format_text`.
Look up its selection in the registry rather than writing separate branches for the two built-in names: new subclasses defined after import must work immediately.
Keep import-time behavior limited to definitions and registration; do not print or read input.
For example, `format_text('surround', 'ready')` returns `'[ready]'`.

## Repair

Repair contains errors in registration, formatting, and selecting a formatter.
Use the Check results to identify which required behavior belongs in each file.
After both stages pass, consider whether a plain dictionary supplied explicitly would be simpler for a smaller application.
