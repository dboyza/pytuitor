# Register classes deliberately

A class is itself an object, usually created by `type`.
A metaclass customizes that creation process.
A metaclass can enforce rules while classes are created, such as rejecting duplicate registration names.
For simpler registration, a class decorator or the `__init_subclass__` method taught in the chapter project may be enough.

```python
class NamedMeta(type):
    def __new__(mcls, name, bases, namespace, **kwargs):
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        cls.display_name = name.lower()
        return cls


class Report(metaclass=NamedMeta):
    pass
```

`__new__` creates an object; here the object being created is a class.
`mcls` is the metaclass receiving the call, a conventional parameter name like `self`.
`name` is the new class's name.
`namespace` is the dictionary created by executing the class body.
`bases` is a tuple of parent classes.
`super().__new__` delegates creation to the next implementation in the inheritance order.
The example passes every received argument onward, including extra keyword arguments collected by `**kwargs`.
Keep the original namespace dictionary so Python can preserve internal entries needed by methods using `super()`.
The returned `cls` is the new class object; return it after adding or checking attributes.
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
Register only kinds declared in the new class body and reject duplicate keys.

The [class creation reference](https://docs.python.org/3.11/reference/datamodel.html#customizing-class-creation) explains the complete sequence.
