# Understand method lookup with multiple inheritance

The **method resolution order (MRO)** is the sequence of classes Python searches to find an attribute or method.
`Class.__mro__` contains that sequence as a tuple.
**Multiple inheritance** means a class has more than one parent, written as `class Combined(First, Second):`.
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

For methods to cooperate, each must accept the arguments passed by the previous method and call `super()` once when more work should follow.
For example, `return ["tag"] + super().steps()` puts one list item before the list returned by the next method.
Calling a particular base directly can skip siblings or execute a shared ancestor twice.
**Composition** means putting another object in an attribute and using that object's methods, instead of inheriting from its class.
It can be easier to follow than many interconnected parent classes.

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

Repair calls Root directly and skips the other parent class.
This arrangement is called **diamond inheritance** because Left and Right share Root, and Pipeline inherits both Left and Right.
Restore cooperation through the actual method resolution order.
