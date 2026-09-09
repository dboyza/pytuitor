## Reproduce a sequence of choices

The `random` module produces pseudorandom values: a repeatable calculation generates a sequence that looks random.
A **seed** lets you reproduce a sequence, which helps tests and simulations.
A random generator is an object that keeps track of where it is in that sequence.
Create your own generator so your function does not change the sequence used by other code.

```python
import random

generator = random.Random(42)
for number in range(3):
    print(generator.choice(["north", "south"]))
```

`random.Random(42)` creates a random generator object with its own state, the data it keeps between calls.
Calling its `.choice(items)` method selects one item from a nonempty sequence and advances that state.
Starting again with a new generator and the same seed repeats the choices for the same inputs in the same Python environment.
Repeated choices are possible: drawing does not remove an item.

Other tools include `.randint(a, b)` for an integer from `a` through `b`, including both.
`.sample(items, count)` chooses list positions without choosing the same position twice.
`.shuffle(items)` rearranges the supplied list itself instead of returning a new list.
The functions called directly through `random`, such as `random.choice(...)`, share a generator.
`random.seed(...)` resets that shared generator and affects other callers, so avoid it in reusable functions.
Use the separate `secrets` module for values that must be hard to guess, such as password-reset codes; ordinary random choices are for simulations and similar tasks.

## Build

Define `draw(items, count, seed)`.
`items` is a list, `count` is an integer, and `seed` is an integer.
Use an independent `random.Random(seed)` and call its `choice(items)` exactly once per draw, in order.
Return the choices in a new list, leaving both `items` and the module's shared random generator state unchanged.
Reject negative counts, or a positive count with empty items, using `ValueError`.
Zero draws return an empty list even when items is empty.
The same arguments must give the same result on repeated calls.
Do not read input or print.

## Repair

The supplied program changes shared random state.
Give each call its own generator while preserving the same seeded sequence of choices.
