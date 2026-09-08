## Read a measurement with a fractional part

A `float` stores a number that can have a fractional part, such as `3.5`.
`float()` converts a numeric string, so `float("3.5")` gives `3.5`.
Unlike `int()`, it accepts a decimal point in the input.
Use ordinary `/` division when the fractional part matters.

```python
seconds = float(input("Seconds: "))
minutes = seconds / 60
print(minutes)
```

Typing `90` gives `1.5` minutes.
Typing `30.6` gives `0.51` minutes.
For this lesson, inputs are valid nonnegative measurements, so you do not need to handle invalid text.

## Choose how the result looks

An **f-string** starts with `f` before its opening quote.
Put an expression inside braces to insert its value into the text.
The format specifier `:.2f` inside the braces displays a number rounded to two digits after the decimal point.
It includes trailing zeros when necessary.

```python
liters = 2.5
print(f"Water: {liters:.2f} L")
```

This prints `Water: 2.50 L`.
Formatting creates display text; it does not change the number stored in `liters`.
Keep the calculated value in a variable and format it when printing.

Floats store binary approximations of many decimal fractions.
For example, `0.1 + 0.2` may display as `0.30000000000000004`.
Formatting helps present a measurement, but does not make the underlying arithmetic exact.
For money, use whole-number cents when exact cent arithmetic is needed.

## Build

Read one line containing a valid nonnegative measurement in centimeters, including decimal values.
You may choose any input prompt.
Store the converted number in `centimeters` and the measurement divided by `100` in `meters`.
Keep the unrounded calculated value in `meters`.
Print exactly one line containing the meters value with two decimal places followed by ` m`.
For input `234.56`, `meters` is approximately `2.3456` and the output is `2.35 m`.
For input `0`, print `0.00 m`; for `100`, print `1.00 m`.
Checks allow tiny floating-point differences in the calculated value and require the specified display text.

## Repair

The supplied program discards the fractional part during conversion and does not format the display.
Fix both problems using the same input and output contract.
