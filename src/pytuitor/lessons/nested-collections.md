## Lists can contain other lists

A grid can be represented as a list of rows, each itself a list.
Rows do not have to have equal lengths.

```python
grid = [[4, 7], [], [2]]
print(grid[0][1])
```

`grid[0]` selects the first row; its item at index `1` is `7`.
Indexing an empty row raises `IndexError`, just like indexing an empty ordinary list.
A nested loop visits only the elements that exist:

```python
for row_number, row in enumerate(grid):
    for column_number, value in enumerate(row):
        print(row_number, column_number, value)
```

The inner loop finishes before the outer loop advances to another row.
An empty row runs the inner loop zero times.
Create a new row list for each row; reusing and changing one row object would change every reference to it.

## Build

Read a nonnegative integer `count` on the first line, then exactly `count` lines of space-separated integers.
Each row may be empty or a different length.
Negative integers and repeated values are valid.
Use any input prompts.
Build a list of lists named `grid` using `int()` on each word.

Create `row_totals`, with one sum per row, including zero for empty rows.
Create `flat`, containing every value in row order and then column order.
Create `positions`, containing tuples `(row_index, column_index, value)` for those values, using zero-based indexes.
Reset a row's sum before its inner loop and append the sum after that loop.
With rows `[2, 3]` and `[4]`, the totals are `[5, 4]`, flat values are `[2, 3, 4]`, and positions are `[(0, 0, 2), (0, 1, 3), (1, 0, 4)]`.
For zero rows, all four lists are empty.
Printing is optional.

## Repair

The program carries a running total between rows and swaps row and column indexes.
Fix both while preserving empty rows.
