## Compare groups of values

Sets hold unique values and support questions about whole groups.
The operators below create new sets without changing their inputs.

```python
morning = set(["Mira", "Sol"])
evening = set(["Sol", "Bo"])
print(morning & evening)
print(morning - evening)
```

`&` is intersection: the values in both groups, here `Sol`.
`-` is difference: values in the left group that are absent from the right, here `Mira`.
Swapping the left and right sets changes which group you subtract from.
`|` is union, containing everyone from either group.
`^` is symmetric difference, containing only people in exactly one group.

`morning <= evening` asks whether every morning value is also in evening.
A **subset** contains only values that are also in the other set.
Equal sets count as subsets of each other.
`<` means a proper subset: equality is excluded.
An empty set is a subset of every set.
For predictable display, `sorted(values)` returns a new sorted list; a set itself has no guaranteed display order.

## Build

Read two lines of space-separated words, with any prompts.
Either line may be empty, and duplicate words count once.
Store the first line's set as `required` and the second as `available`.
Create `shared`, `missing`, `combined`, and `exclusive` as sets representing intersection, missing requirements, union, and symmetric difference respectively.
Set `ready` to whether every requirement is available, including when there are no requirements.
Comparisons are case-sensitive.
For `rope lamp` and `lamp food`, only `lamp` is shared and only `rope` is missing.
Printing is optional; checks inspect your result variables.

## Repair

The broken program mixes up the set operations and rejects equal sets as ready.
Correct its results, including empty groups and equality.
