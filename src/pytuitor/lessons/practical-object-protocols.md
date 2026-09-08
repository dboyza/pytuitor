# Join Python's object conventions

Special methods let user-defined objects participate in ordinary syntax.
`__repr__` supplies a debugging representation, `__len__` supports `len`, `__eq__` supports equality, and `__add__` supports `+`.
Return `NotImplemented` from a binary special method for unsupported operand types so Python can try the other operand or report an error.
This is a special value, not an exception to raise.

```python
class Label:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"Label({self.text!r})"

    def __eq__(self, other):
        if not isinstance(other, Label):
            return NotImplemented
        return self.text == other.text
```

`!r` in an f-string uses a value's representation, including quotes for strings.
A property keeps attribute syntax while running controlled access code.

```python
class Temperature:
    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Below absolute zero")
        self._celsius = value
```

The underscore is a convention for internal storage, not access enforcement.
Validate before assigning so rejected updates leave the previous state intact.

## Build

Define `Score(points)` for nonnegative integers, with a readable and writable `points` property.
Reject negative initialization or assignment with `ValueError`, leaving an existing value unchanged after a rejected update.
You may assume supplied point values are integers.
`repr(Score(3))` must be `'Score(3)'`, and `len(score)` must equal its points.
Two scores compare equal exactly when their points match; a score is unequal to a plain integer.
Adding two scores returns a new score with their summed points and changes neither operand.
Adding a score and an unsupported type must raise `TypeError`.
Do not print or read input.

## Repair

The current object accepts invalid updates, compares everything equal, and mutates the left operand during addition.
Restore the value contracts and useful representation.
