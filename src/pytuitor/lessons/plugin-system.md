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
