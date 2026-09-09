## Repeat while a condition stays true
A `for` loop visits a known collection.
A `while` loop repeats as long as its condition is true.
A variable used in that condition usually needs to change, or the loop may never stop.

```python
remaining = 3
while remaining > 0:
    print(remaining)
    remaining = remaining - 1
```

This prints `3`, `2`, `1`, then stops when `remaining` becomes zero.
`break` immediately stops the loop that contains it.
If loops are nested, it stops only the innermost one.
`while True:` creates a loop that keeps going until something such as `break` stops it.
This is useful when the user decides when they are finished.

## Build
Keep reading one integer per input line until the user enters `0`.
Add all the nonzero integers into a variable called `total`, initially zero.
Stop immediately at `0` and print `total` once after the loop.
Inputs are always valid integers; negative numbers are allowed and reduce the total.
Input lines `5`, `-2`, `0` should print `3`.
If the first line is `0`, print `0`.
Check supplies the stopping zero automatically.
When using Run, remember to type it yourself.

## Repair
Investigate why the loop stops before processing all the numbers.
The input value decides when to stop; the running total records how much has been added.
