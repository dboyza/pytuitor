# Expressions with intent

This chapter builds on variables, conditions, loops, and functions to explore Python's rules and conventions.
Python uses indentation to group statements and a colon to introduce a block.
Use four spaces for each indentation level.
There are no braces around a function body or an `if` branch.

```python
def greeting(person):
    if person is None:
        return "Hello, guest"
    return "Hello, " + person
```

`def` defines a function, parentheses declare its parameters, and `return` supplies its result to the caller.
A function returns `None` if it reaches the end without a return statement.
Strings use single or double quotes; `None` represents the absence of a value.
Use `is None` for that singleton, and `==` when comparing values.

`text.strip()` returns a string without surrounding whitespace.
Strings are immutable: methods produce a new string rather than changing the original.
An empty string is false in a condition, while every nonempty string is true, including `"0"` and `"False"`.
`a or b` evaluates to `a` when `a` is truthy; otherwise it evaluates to `b`.
It does not necessarily return a Boolean.

## Build

Write `display_name(value)`.
Its argument is either `None` or a string.
Return `"Anonymous"` for `None` or a string containing only whitespace.
Otherwise return the string with surrounding whitespace removed, preserving its case and internal spaces.
For example, `display_name("  Ravi Shah  ")` returns `"Ravi Shah"`.
The string `"0"` must remain `"0"`.
Define the function without asking for input or printing.
Checks call it with several arguments; Run can be used with your own temporary print calls.

## Repair

After Build passes, repair the supplied implementation to meet the same contract.
Consider what converting `None` to a string actually produces.
