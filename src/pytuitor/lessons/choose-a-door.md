## Compare two values

A **condition** is an expression used to decide whether some code should run.
The comparisons in this lesson produce either `True` or `False`.
These two values are called booleans, or `bool` in Python.

```python
print(3 > 2)
print(3 == 2)
```

This displays `True`, then `False`.
`>` means greater than, `<` means less than, and `==` asks whether two values are equal.
`>=` and `<=` include equality, while `!=` means not equal.
Remember: `=` assigns a value; `==` compares values.

## Choose which instructions to run

Use `if` to run instructions only when a condition is true.
Use `elif`, short for "else if", to test another condition when the earlier one was false.
Use `else` for everything not handled by the earlier conditions.

```python
weather = "rain"

if weather == "sun":
    print("Bring sunglasses")
elif weather == "rain":
    print("Bring an umbrella")
else:
    print("Bring a jacket")
```

The first comparison is false, so Python tries the `elif` comparison.
That one is true, so it displays `Bring an umbrella`.
A **branch** is one of the groups of instructions the program can choose.
Only one branch in this chain runs; the `else` is skipped.

Each `if`, `elif`, and `else` line ends with a colon, `:`.
The instructions belonging to that branch begin four spaces farther to the right.
This is called **indentation**, and it tells Python which instructions belong together.
The editor inserts spaces when you press Tab.

## Exercise

Start your program with `key = input("Which key? ")` to ask for a key and store the answer.
Set the variable `destination` to:

- `"treasure"` when `key` is `"gold"`;
- `"garden"` when `key` is `"green"`;
- `"locked"` for any other answer.

Use `if`, `elif`, and `else`, then print `destination` after the whole chain.
That last print should have no indentation because it runs whichever branch was chosen.

Run the program once with `gold`, once with `green`, and once with `blue`.
Check tries those cases for you as well.

After Build passes, Repair classifies a parcel by its integer item count.
It must distinguish zero, the inclusive small range from 1 through 3, and counts above 3.
The equality boundaries are part of the practice.
