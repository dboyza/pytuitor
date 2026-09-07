# Register classes deliberately

A class is itself an object, usually created by `type`.
A metaclass customizes that creation process.
Use one when a class-level invariant needs it; a decorator or `__init_subclass__` is often simpler for ordinary registration.

```python
class NamedMeta(type):
    def __new__(mcls, name, bases, namespace, **kwargs):
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        cls.display_name = name.lower()
        return cls


class Report(metaclass=NamedMeta):
    pass
```

`namespace` is the dictionary created by executing the class body.
`bases` is a tuple of parent classes.
Call `super().__new__` with the original namespace to preserve Python's class machinery, including the `__classcell__` used by zero-argument super.
The metaclass can also be called directly, such as `NamedMeta('Report', (), {})`.
Checking namespace distinguishes an attribute explicitly defined by this class from one inherited from a parent.

## Build

Implement `RegistryMeta(type)` with an initially empty class dictionary `registry`.
Its `__new__` must create the class using the normal type machinery.
Declared kind values are strings or None.
If that class body explicitly declares a non-None `kind` string, register the new class under that string.
If the key already exists, raise `ValueError` without replacing the existing registration.
Classes without an explicit kind, including subclasses that only inherit one, are not registered.
For `class Csv(metaclass=RegistryMeta): kind = 'csv'`, `RegistryMeta.registry['csv']` must be Csv itself.
Do not define example classes at module level in your answer, since the registry must initially be empty.
Do not print.

## Repair

Repair registers class names regardless of the declared contract.
Use explicit kinds and reject collisions.

The [class creation reference](https://docs.python.org/3.11/reference/datamodel.html#customizing-class-creation) explains the complete sequence.
