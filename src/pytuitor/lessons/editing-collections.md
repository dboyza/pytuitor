## Change a list deliberately

`items.insert(index, value)` inserts before the given position.
`items.append(value)` adds at the end.
`items.remove(value)` deletes the first matching value, raising `ValueError` if none exists.
Check `if value in items:` before removing a value that might be absent.
`items.pop(index)` instead removes and returns the item at an index; without an index it uses the last item.

```python
colors = ["red", "blue", "red"]
colors.remove("red")
colors.insert(0, "gold")
colors.sort()
print(colors)
```

This prints `['blue', 'gold', 'red']`.
`sort()` changes the list and returns `None`, Python's value for no result.
Do not assign that result back to the list.
`sorted(colors)` would return a new sorted list instead.

## Change a dictionary

Assigning `counts[key] = value` inserts or replaces an entry.
`del counts[key]` removes an existing entry and raises `KeyError` for an absent key.
`counts.pop(key, default)` removes and returns the value, or returns the default when absent.
`keys()`, `values()`, and `items()` provide **views**: objects you can loop over to read the dictionary's keys, values, or key/value pairs.
Views reflect later dictionary changes; `list(counts.keys())` copies the current keys into a separate list.
Avoid adding or removing dictionary entries while looping over a view.

## Build

Read three lines: space-separated `items`, one word `target`, and one word `incoming`.
Only the first line may be empty; use any prompts.
Remove just the first occurrence of `target` from `items`, if present.
Insert `incoming` at the beginning, then sort `items` using Python's case-sensitive string ordering.
For ordinary English letters, uppercase letters come before lowercase letters: `"Z"` sorts before `"a"`.
Build `counts`, mapping each resulting item to its count.
Then remove the `target` entry from `counts`, saving its former value in `removed`, or zero when absent.
Create `keys` as a sorted list of the remaining dictionary keys.
Do not remove any further items from the list when deleting the dictionary entry.
Printing is optional.

For `pear apple pear`, `pear`, `pear`, the final list is `['apple', 'pear', 'pear']`, counts is `{'apple': 1}`, removed is `2`, and keys is `['apple']`.

## Repair

The program can remove a matching item twice instead of once, skips sorting, and loses the counts of repeated items.
Restore the required sequence of operations.
