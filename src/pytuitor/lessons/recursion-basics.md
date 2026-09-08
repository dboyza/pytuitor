## A function can call itself
Recursion solves a problem by asking the same function to solve a smaller problem.
A base case returns immediately, without another recursive call.
Every other call must move toward that base case.

```python
def countdown(number):
    if number == 0:
        return "go"
    return str(number) + " " + countdown(number - 1)


print(countdown(3))  # 3 2 1 go
```

`countdown(3)` waits for `countdown(2)`, which waits for `countdown(1)`, which waits for `countdown(0)`.
The final call returns `"go"`, then each waiting call builds its result.
Each call has its own local `number`.
Without a reachable base case, Python eventually raises `RecursionError` because too many calls are waiting.
Use a loop for very long linear sequences; recursion is especially useful for nested structures, which come next.

## Build
Define `digit_sum(number)` for a nonnegative integer containing at most 12 digits.
Return the sum of its decimal digits as an integer; `digit_sum(204)` returns `6`, and `digit_sum(0)` returns `0`.
Inputs are always valid integers in this range, so no validation is needed.
`number % 10` gives the last digit and `number // 10` removes it.
Try a recursive solution: return a single digit directly, otherwise add the last digit to the sum of the remaining digits.
A correct loop-based solution is also accepted.
Return the result without printing.

## Repair
The broken base case throws away the final digit.
Trace a single-digit input before trying a longer number.
