## Give fixed choices names
An enumeration, or enum, represents a fixed set of named choices.
It helps avoid misspelled strings spreading through a program.
`from enum import Enum` imports the standard-library base class.
Writing `class Size(Enum):` creates a class that inherits enum behavior, including named members and lookup by value.

```python
from enum import Enum


class Size(Enum):
    SMALL = "small"
    LARGE = "large"


choice = Size("small")
print(choice is Size.SMALL)  # True
print(choice.name)  # SMALL
print(choice.value)  # small
```

Members belong to the class, so use `Size.SMALL` rather than constructing an ordinary object with instance fields.
`is` checks identity: each member is the same unique enum object every time you access it.
`Size("missing")` raises `ValueError`; convert untrusted strings at an input boundary and handle that exception there.
Enums suit fixed states, while ordinary strings suit open-ended text such as a user's name.

## Build
Import `Enum` and define `Status(Enum)` with exactly three members in this order: `TODO = "todo"`, `DOING = "doing"`, and `DONE = "done"`.
Define `next_status(status)` returning the next enum member: TODO becomes DOING, DOING becomes DONE, and DONE stays DONE.
The argument is always a `Status` member; string conversion or invalid-input handling is not required in this function.
Return enum members, not their string values, and do not print.

## Repair
The broken transition sends active and finished work back to TODO.
A completed task must stay completed.
