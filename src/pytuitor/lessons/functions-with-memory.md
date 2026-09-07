## Defaults are created when a function is defined

Python evaluates a default argument once, when it executes the `def` statement.
The same default object is reused whenever a caller omits that argument.

```python
def collect(item, bucket=[]):
    bucket.append(item)
    return bucket


print(collect(1))
print(collect(2))
```

The second call returns `[1, 2]`, not `[2]`.
Use `None` as the default and create a new list inside the function when `bucket is None`.
Do not use `if not bucket`: an explicitly supplied empty list is false in a condition but should still be reused.

## Functions can wrap other functions

A **decorator** is a function that receives another function and returns its replacement.
Functions are values in Python: you can pass them as arguments, return them, and call them through variables.

```python
from functools import wraps


def announce(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print("Calling", fn.__name__)
        return fn(*args, **kwargs)

    return wrapper
```

Inside the wrapper, `*args` collects positional arguments in a tuple and `**kwargs` collects keyword arguments in a dictionary.
Using them in `fn(*args, **kwargs)` passes those arguments on to the original function.
The wrapper remembers `fn` from the enclosing function; this is a **closure**.
Python looks up names in local, enclosing, global, then built-in scopes.
`@wraps(fn)` preserves useful metadata, including the original function's name and docstring.

Writing `@announce` above a function definition is shorthand for replacing the function with `announce(function)`.

## Exercise

Write `def collect(item, bucket=None):` so calls without a bucket get independent lists, while a supplied list is appended to and returned.
Append `item` to the list using `.append(item)`.
Then implement `twice(fn)`: its wrapper should call `fn` once and multiply the returned result by two.
Forward positional and keyword arguments and preserve metadata with `@wraps(fn)`.

Try wrapping a function that adds two numbers.
The check suite also verifies that the wrapped function is called only once.
