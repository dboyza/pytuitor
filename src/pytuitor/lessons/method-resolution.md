# Cooperate through the MRO

Python resolves inherited methods using a consistent method resolution order, available as `Class.__mro__`.
It includes each class once in an order compatible with the declared bases.
`super()` continues lookup after the current class in the actual instance's MRO.
It does not simply mean calling a fixed parent.

```python
class Base:
    def describe(self):
        return "base"


class Tagged(Base):
    def describe(self):
        return "tag:" + super().describe()
```

In multiple inheritance, cooperative methods share compatible signatures and each delegates through super exactly once when continuation is required.
Calling a particular base directly can skip siblings or execute a shared ancestor twice.
Composition is often easier to understand than a deep inheritance graph; this exercise teaches how the mechanism works when you encounter it.

## Build

Define four classes: Root, Left, Right, and Pipeline.
Root has a `steps(self)` method returning `['root']`.
Left and Right each inherit Root and prepend their respective names, `'left'` and `'right'`, to the result of a cooperative call to the next steps method.
Pipeline inherits Left first and Right second without overriding steps.
`Pipeline().steps()` must return `['left', 'right', 'root']`.
`Left().steps()` must still return `['left', 'root']`.
Reversing the bases in a new class must produce `['right', 'left', 'root']` without changing Left or Right.
Return a fresh list each time and do not print.
`pass` is the placeholder statement for a class body that adds no behavior.

## Repair

Repair names Root directly and bypasses the other branch of the diamond.
Restore cooperation through the actual method resolution order.
