# Construct valid, independent values

A dataclass generates initialization and equality from annotated fields.
For mutable defaults, `field(default_factory=list)` calls `list()` for each new instance instead of sharing one list.
Pass the callable `list`, not an already-created `list()`.

`__post_init__` runs after the generated initializer, making it a useful place to normalize and validate fields.
`dataclasses.replace(instance, field=value)` constructs a new instance and runs initialization again.
It is a shallow operation: unchanged mutable fields are shared unless explicitly copied.

```python
from dataclasses import dataclass, field, replace


@dataclass
class Team:
    title: str
    members: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.title = self.title.strip()


original = Team(" Helpers ", ["Lin"])
copy = replace(original, title="Reviewers", members=original.members.copy())
```

## Build

Define a dataclass `Batch(name: str, tags: list[str])` whose tags default to a fresh empty list for each instance.
Strip surrounding whitespace from the name during initialization and raise `ValueError` if the result is empty.
Implement `renamed(self, name)` returning a different `Batch` with the normalized, validated new name and a copy of the original tags.
The original name and tags must remain unchanged when the returned batch is modified.
Tags contain strings, so a shallow list copy is sufficient.
Preserve dataclass value equality.
Do not print or read input.

## Repair

The current class skips validation and mutates itself during renaming.
Restore independent defaults, normalization, and a validated new value.
