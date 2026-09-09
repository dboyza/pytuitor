## Use standard-library calculations

The standard library includes mathematical and statistical tools.
Import the module and access functions through its name.

```python
import math
import statistics

readings = [2, 8, 5]
print(statistics.mean(readings))
print(statistics.median(readings))
print(math.ceil(7 / 3))
```

This prints `5`, `5`, and `3`.
The **mean** adds the values and divides by their count.
The **median** is the middle value after ordering; for an even count it averages the two middle values.
These functions do not change the input list.

`math.ceil(value)` rounds upward to an integer, while `math.floor(value)` rounds downward.
A partly filled final container still counts when calculating how many containers are needed.
`math.sqrt(value)` computes a square root for nonnegative numbers.
Calculations with Python floats can have small rounding differences.
`math.isclose(a, b)` checks whether two numbers are close enough rather than exactly equal.
Its tolerance settings control how much difference is allowed.

To reject an unacceptable value yourself, use `raise` with an exception:

```python
def square_root(value):
    if value < 0:
        raise ValueError("The value must be zero or positive")
    return math.sqrt(value)
```

This stops the function and reports the error to its caller, which can handle it with `try` and `except`.

## Build

Define `summarize(values, capacity)`.
`values` is a list of finite numbers: ordinary integers or floats, excluding infinity and the special not-a-number value `nan`.
`capacity` is an integer representing how many readings fit into one group.
Return a tuple containing the mean, the median, and the number of groups needed to hold all readings.
A partial last group counts, so four readings with capacity three need two groups.
Reject an empty values list or a capacity of zero or less with `ValueError`.
Do not change `values`, read input, or print.
For `[9, 1, 5, 3]` and capacity `3`, return `(4.5, 4.0, 2)`.

## Repair

The supplied program mistakes a middle input position for the median and drops a partial final group.
Use the data's statistics and round the group count in the appropriate direction.
