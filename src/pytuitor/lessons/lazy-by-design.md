## Iterables and iterators

An **iterable** is something you can loop over, such as a list.
`iter(values)` gets an **iterator**, which keeps track of the current position.
`next(iterator)` returns the next item or raises `StopIteration` when no items remain.
A `for` loop handles this protocol for you.

## Build a list with a comprehension

A **list comprehension** combines a loop, an optional condition, and an expression for each result:

```python
numbers = [-2, 0, 3, 2]
squares = [n * n for n in numbers if n > 0]
print(squares)
```

This displays `[9, 4]`.
Python visits each `n`, keeps it if `n > 0`, and puts `n * n` in a new list.
The loop variable does not escape the comprehension's scope in Python 3.

## Produce values only when requested

A **generator** is an iterator that produces values on demand.
A function containing `yield` creates a generator when called:

```python
def doubles(values):
    for value in values:
        yield value * 2


stream = doubles([1, 2])
print(next(stream))
print(next(stream))
```

This prints `2`, then `4`.
`yield` pauses the function and supplies a value; the next request resumes it after that line.
Unlike `return`, it does not finish the function immediately.
Generator expressions use parentheses, as in `(n * 2 for n in values)`.

Generators are consumed once, and their work, including possible errors, happens as values are requested.
They are useful for large or infinite streams because they do not need to build a complete output list.

## Exercise

Write `def positive_squares(numbers):` as a generator that yields the square of each strictly positive number in order.
Skip zero and negative numbers.
Accept any iterable, including another generator, and do not convert the input or output to a list inside the function.

Check uses both finite input and the first few results from an infinite stream.
