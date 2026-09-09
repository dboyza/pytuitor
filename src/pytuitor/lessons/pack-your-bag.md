## Keep several values in a list

A **list** holds values in order.
Write square brackets around the values and separate them with commas:

```python
pouches = [2, 5, 1]
```

This list contains three integers.
`[]` is an empty list.
A list can also contain strings, such as `["map", "rope"]`.

## Repeat an instruction with for

A **loop** runs instructions repeatedly.
Each repetition is called an **iteration**.
A `for` loop works through a collection, one item at a time:

```python
for coins in pouches:
    print(coins)
```

On the first repetition, `coins` is `2`; on the next it is `5`; on the last it is `1`.
The program prints those three numbers on separate lines.
Choose any helpful variable name in place of `coins`.
The colon and indentation work just as they do with `if`.

## Build a running total

Start at zero before the loop and add each item:

```python
prices = [3, 4]
total = 0
for price in prices:
    total = total + price
print(total)
```

The total changes from `0` to `3`, then to `7`.
Python calculates the right side before assigning the new total.
`total += price` is a shorter way to write this addition.

## Exercise

Your program needs to build `pouches` from the numbers you type.
Use the following input-handling pattern before calculating the total:

```python
pouches = []
for amount in input("Coins in each pouch: ").split():
    pouches.append(int(amount))
```

A **method** is a function that belongs to a value and is called with a dot, such as `text.split()`.
`.split()` turns a string like `"2 5 1"` into the list `["2", "5", "1"]`.
`int(amount)` converts each string to an integer.
`pouches.append(...)` adds that integer to the end of the list.
You now have `[2, 5, 1]` to work with.

Write the input setup in your editor, then add your total calculation below it.
Create `total = 0`, loop over `pouches`, add each number, then print `total` after the loop.

Try `2 5 1`, which should give `8`.
Then run again and press Enter without typing any numbers: an empty list should give `0`.
Putting `total = 0` inside the loop would reset it on every repetition, so keep that line before the loop.

Typing a word instead of a number will produce the `ValueError` introduced in the input lesson.
Run again and enter whole numbers to continue.
