## Look up a value by its key
A **dictionary**, or `dict`, connects keys to values.
A key is a label used to find its associated value.
For example, `stock = {"apple": 3, "pear": 8}` stores two fruit counts.
`stock["apple"]` returns `3`.
`stock["apple"] = 4` changes that count.
`{}` creates an empty dictionary.
Looking up a missing key with brackets raises `KeyError`, meaning that the dictionary has no entry for that key.

`stock.get("plum", 0)` returns the value for `"plum"` if present, otherwise `0`.
The method does not insert a missing key.
To count repeated items, read the previous count, add one, and assign the new count.

```python
counts = {}
for color in ["blue", "red", "blue"]:
    counts[color] = counts.get(color, 0) + 1
print(counts)
```

The result is `{'blue': 2, 'red': 1}`.

## Build
Read space-separated words from one input line.
Create a dictionary called `counts` whose keys are the words and whose values are the number of times each word appears.
Treat `Cat` and `cat` as different words.
An empty input produces `{}`.
You may print `counts` so Run shows your result.
Checks compare the dictionary itself, so printing is optional and key order does not matter.

## Repair
The broken version forgets earlier occurrences.
Make each repeated word increase its existing count.
