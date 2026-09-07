## A compact form of a familiar loop
A list comprehension builds a list from an iterable in one expression.
`[number * 2 for number in [1, 2, 3]]` produces `[2, 4, 6]`.
The expression before `for` describes the output item.
An optional final `if` filters input items.

```python
lengths = [len(word) for word in ["sun", "a", "moon"] if len(word) > 1]
```

This produces `[3, 4]`.
A regular loop is often clearer when each item needs several decisions or side effects.
`sorted(values)` returns a new sorted list, leaving its input unchanged.
For integers, the default order is smallest first.
A set, created with `set(values)`, keeps distinct items but has no reliable display order.
Sorting a set gives a predictable list of distinct values.

## Build
Define `positive_squares(numbers)`.
Return the squares of the strictly positive integers in `numbers`, sorted from smallest to largest.
Keep duplicates: two occurrences of `3` produce two occurrences of `9`.
Do not change the original list.
For `[3, -2, 1, 3, 0]`, return `[1, 9, 9]`.
An empty list or a list with no positive numbers returns `[]`.
A comprehension or a regular loop is acceptable.

## Repair
The broken version includes zero and removes duplicates.
Read each part of the contract before choosing a collection type.
