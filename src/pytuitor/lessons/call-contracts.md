# Make call sites readable

Python callers can usually pass arguments by position or by parameter name.
Defaults apply when an argument is omitted.
A bare `*` in a parameter list makes all following parameters keyword-only.
A `/` marks preceding parameters positional-only, useful when names should not become part of your public API.

```python
def label(text, /, prefix="item", *, upper=False):
    result = prefix + ": " + text
    return result.upper() if upper else result


label("report", prefix="file", upper=True)
```

The conditional expression is `value_if_true if condition else value_if_false`.
Ordinary `if` statements are equally appropriate when they are clearer.
Defaults are evaluated when `def` executes, a rule we will examine with mutable objects in the next chapter.

Use `raise ValueError("explanation")` when an argument has an unacceptable value.
Python supports chained comparisons: `0 <= rate <= 1` tests both boundaries.
`round(number, 2)` rounds to two decimal places.
Binary floats cannot exactly represent every decimal fraction; this exercise teaches call contracts, not production money arithmetic.
Financial applications often use `decimal.Decimal` with an explicit rounding policy.

## Build

Define `quote(price, quantity=1, *, discount=0)`.
Arguments are finite numbers; quantity is a nonnegative integer.
Reject a negative price, negative quantity, or discount outside the inclusive range zero through one with `ValueError`.
Return the price times quantity after applying the fractional discount, rounded to two decimal places.
For example, `quote(8, 4, discount=0.25)` returns `24.0`.
Zero quantity and a discount of one are valid and return zero.
Do not print or read input.

## Repair

Apply the same signature and behavior to Repair.
A fractional discount must scale the subtotal, and invalid arguments must not silently produce a quote.
