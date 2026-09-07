# Group without losing order

Lists preserve sequence order; dictionaries associate keys with values.
Dictionary insertion order is part of Python's language contract.
Sets efficiently represent membership and uniqueness but do not promise insertion order.
Choose your container according to the behavior your caller needs.

```python
counts = {}
for word in ["red", "blue", "red"]:
    counts[word] = counts.get(word, 0) + 1

lengths = {word: len(word) for word in counts}
short_words = [word for word in counts if len(word) < 4]
```

The last two expressions are dictionary and list comprehensions.
They work well for a direct transformation or filter; ordinary loops are clearer when an iteration performs several updates.
`mapping.setdefault(key, default)` inserts the default only if the key is absent, then returns the stored value.
`item in collection` tests membership.
`for key, value in pairs` unpacks each two-item pair into two variables.
A function accepting an iterable should not assume it has indexing or can be traversed twice.

## Build

Write `group_names(pairs)`.
Each pair contains a group string and a name string.
Return a dictionary mapping each group to its distinct names in first-seen order.
Keep groups in their first-seen order too.
Names are case-sensitive and already normalized.
For example, `[('team', 'Mina'), ('team', 'Sol'), ('team', 'Mina')]` becomes `{'team': ['Mina', 'Sol']}`.
Accept an empty iterable and a one-pass iterator.
Do not mutate the input or print.

## Repair

The broken comprehension replaces earlier names when a group appears again.
Repair the accumulation while retaining the order and uniqueness requirements.
