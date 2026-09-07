# Control attribute access

A descriptor is an object whose class defines `__get__`, `__set__`, or `__delete__`.
Placed on another class, it participates in that class's attribute access.
A property is a familiar descriptor; custom descriptors let multiple classes reuse a rule.

`__set_name__(self, owner, name)` is called when the owner class is created, supplying the attribute's declared name.
`__get__(self, instance, owner=None)` handles reads; instance is None when the attribute is read through the class.
`__set__(self, instance, value)` handles writes.
A descriptor with `__set__` or `__delete__` is a data descriptor and takes precedence over the instance dictionary.
A descriptor with only `__get__` may be shadowed by an instance attribute.

```python
class Label:
    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return "ready"


class Job:
    label = Label()
```

`Job().label` returns a string while `Job.label` returns the descriptor.
The descriptor itself is shared, so per-instance state belongs on the owner instance.
`getattr(obj, name, default)` reads a named attribute; `setattr(obj, name, value)` writes one.

## Build

Define the descriptor class `NonNegative` and a `Counter` class with `value = NonNegative()`.
Reading an unset Counter value returns zero.
All supplied values are finite real numbers.
Writing a nonnegative number stores it for that Counter only.
Writing a negative number raises ValueError without replacing an earlier valid value.
Class access, `Counter.value`, returns the descriptor itself.
Use `__set_name__` to derive a private storage name, allowing the descriptor pattern to work under other attribute names too.
For two new counters, setting one's value to six must leave the other's value at zero.
No printing is required.

## Repair

Repair stores state on the descriptor, accidentally sharing it across counters, and omits validation.

See the [data model reference](https://docs.python.org/3.11/reference/datamodel.html#implementing-descriptors) for lookup details.
