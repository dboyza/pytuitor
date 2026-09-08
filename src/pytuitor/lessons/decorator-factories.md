# A decorator with configuration

An ordinary decorator receives a function and returns its replacement.
A decorator factory receives configuration and returns that decorator.
There are three layers: configuration, the original function, then the arguments of each call.

```python
from functools import wraps


def repeated(times):
    def decorate(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs) * times

        return wrapper

    return decorate


@repeated(2)
def cheer(name):
    return name + "!"
```

`*args` collects positional arguments and `**kwargs` collects keyword arguments.
Using them in a call forwards those arguments.
`wraps` preserves metadata and exposes the original function as `__wrapped__`.
Stacked decorators apply bottom-up: `@outer` above `@inner` means `outer(inner(function))`.

## Build

Write the decorator factory `prefixed(prefix)` for functions returning strings.
The resulting decorated function must call the original once per invocation with unchanged positional and keyword arguments, then prepend the string prefix to its result.
Preserve `__name__`, `__doc__`, and `__wrapped__` metadata.
Factories must compose: `prefixed('A')(prefixed('B')(lambda: 'C'))()` returns `'ABC'`.
Empty prefixes are allowed.
Do not print or read input.

## Repair

The wrapper appends the prefix, accepts only one positional argument, and loses metadata.
Repair all three problems without evaluating the original function during decoration.
