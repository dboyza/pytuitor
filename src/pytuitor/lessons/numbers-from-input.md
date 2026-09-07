## Text must become a number before arithmetic
`input()` always gives you a string, including when someone types digits.
Use `int()` to convert a whole-number string into an integer.
You can store the result in another variable.

```python
boxes_text = input("Boxes: ")
boxes = int(boxes_text)
bottles = boxes * 6
print(bottles)
```

Typing `4` prints `24`.
Typing `four` raises a `ValueError` because it cannot be converted to an integer.
For now, our exercise inputs will always be valid whole numbers.
We will handle invalid answers in a later lesson.

`//` divides and rounds down to a whole number.
`%` gives the remainder after division.
For example, `17 // 5` is `3`, while `17 % 5` is `2`.
Ordinary `/` division gives a decimal number, called a `float`, even when the division is exact.

## Build
Read one line of input containing a nonnegative whole number of minutes.
Convert it to an integer called `minutes`.
Store the number of complete hours in `hours` and the leftover minutes in `remaining`.
Print `hours` on the first line and `remaining` on the second line.
For input `125`, the output is `2` followed by `5`.
For input `0`, both lines contain `0`.
You may choose any input prompt.

## Repair
The supplied program calculates the two parts incorrectly.
Fix it to satisfy the same requirements.
