## Change a list deliberately

`items.insert(index, value)` inserts before the given position.
`items.append(value)` adds at the end.
`items.remove(value)` deletes the first matching value, raising `ValueError` if none exists.
Use membership to guard an optional removal.
`items.pop(index)` instead removes and returns the item at an index; without an index it uses the last item.

```python
colors = ["red", "blue", "red"]
colors.remove("red")
colors.insert(0, "gold")
colors.sort()
print(colors)
```

This prints `['blue', 'gold', 'red']`.
`sort()` changes the list and returns `None`; do not assign its result back to the list.
`sorted(colors)` would return a new sorted list instead.

## Change a dictionary

Assigning `counts[key] = value` inserts or replaces an entry.
`del counts[key]` removes an existing entry and raises `KeyError` for an absent key.
`counts.pop(key, default)` removes and returns the value, or returns the default when absent.
`keys()`, `values()`, and `items()` provide views of keys, values, and key/value pairs.
Views reflect later dictionary changes; `list(counts.keys())` takes a separate snapshot.
Avoid changing the number of dictionary entries while iterating its live view.

## Build

Read three lines: space-separated `items`, one word `target`, and one word `incoming`.
Only the first line may be empty; use any prompts.
Remove just the first occurrence of `target` from `items`, if present.
Insert `incoming` at the beginning, then sort `items` alphabetically using Python's case-sensitive string ordering.
Build `counts`, mapping each resulting item to its count.
Then remove the `target` entry from `counts`, saving its former value in `removed`, or zero when absent.
Create `keys` as a sorted list of the remaining dictionary keys.
Do not remove any further items from the list when deleting the dictionary entry.
Printing is optional.

For `pear apple pear`, `pear`, `pear`, the final list is `['apple', 'pear', 'pear']`, counts is `{'apple': 1}`, removed is `2`, and keys is `['apple']`.

## Repair

The program removes all occurrences instead of one, misses sorting, and discards repeat counts.
Restore the required sequence of operations.
