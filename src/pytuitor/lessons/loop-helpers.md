## Generate a sequence of numbers

`range()` supplies whole numbers for a loop without requiring a written list.
`range(4)` gives `0`, `1`, `2`, `3`: it starts at zero and stops before `4`.
`range(2, 5)` gives `2`, `3`, `4`.
An optional third argument sets the step, so `range(6, 0, -2)` gives `6`, `4`, `2`.
A range that cannot reach any values in its direction is empty, as in `range(1, 1)`.

```python
for floor in range(2, 5):
    print(floor)
```

This prints `2`, `3`, and `4` on separate lines.
When counting upward one at a time, use one more than the final number as the stopping value.

## Number items while visiting them

`enumerate()` supplies a pair containing a counter and the current item.
It starts counting at zero unless you provide `start=1` or another starting value.
`start=1` is a **keyword argument**: it names the setting whose value you are passing.
Unpack each pair into two loop variables:

```python
for position, task in enumerate(["wash", "dry"], start=1):
    print(f"{position}: {task}")
```

This prints `1: wash` and `2: dry`.
The list remains unchanged.
If the list is empty, the loop does not run.

## Walk through two collections together

`zip()` supplies pairs of corresponding items from two collections.
Its default behavior stops when the shorter collection runs out.
Extra items in the longer collection are ignored.

```python
foods = ["soup", "salad", "bread"]
prices = [4, 6]
for food, price in zip(foods, prices):
    print(f"{food}: {price}")
```

This prints `soup: 4` and `salad: 6`; there is no pair for `bread`.
If either collection is empty, there are no pairs.
When mismatched lengths would be a mistake in a real program, check the lengths first.
In this exercise, ignoring unpaired items is intentional.

## Build

Read three input lines, with any prompts you choose.
The first is a nonnegative whole number called `count`.
The second contains space-separated names; store its split result in `names`.
The third contains space-separated colors; store its split result in `colors`.
Either word line may be empty.

Create these three result lists:

- `slots`: integers from `1` through `count`, inclusive; use `[]` when `count` is zero.
- `numbered`: a tuple `(number, name)` for each name, counting from `1` in input order.
- `pairs`: a tuple `(name, color)` for each corresponding name and color, stopping at the shorter input list.

Start each result as an empty list and append its values inside a loop, or use another implementation that produces the same results.
To append one pair, write `result.append((left, right))`; the inner parentheses create the tuple passed to `append`.
Try `range`, `enumerate`, and `zip` for the three loops.
Checks compare the lists and tuples, so printing is optional.
You may print all three lists to inspect them with Run.

For input lines `2`, `Mira Sol`, and `red`, the results are `slots = [1, 2]`, `numbered = [(1, "Mira"), (2, "Sol")]`, and `pairs = [("Mira", "red")]`.
Preserve duplicate names and colors in their original positions.
If both word lines are empty, `numbered` and `pairs` are both empty regardless of `count`.

## Repair

The supplied program omits the final slot, starts numbering at zero, and reverses the items in each name/color pair.
Fix each result while preserving the intentional behavior of stopping at the shorter input list.
