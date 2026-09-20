## Check inputs before using them
Validation means checking whether input meets your program's rules.
A function's contract describes its accepted inputs and promised results.
Check inputs when they enter the function, before other operations rely on them.
`raise ValueError("message")` deliberately reports an unacceptable value.
A caller can catch it with the `try`/`except` pattern you learned earlier.
A function that answers a yes-or-no question is often called a predicate.
It can return `True` or `False` instead of raising an error.

Boolean operators combine conditions.
`a and b` is true when both conditions are true; `a or b` is true when at least one is true; `not a` reverses the truth value.
`part in text` asks whether one string occurs inside another.
