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

## Build
Define `valid_filename(name)` that returns a boolean.
For this exercise, a valid name is a nonempty string other than `"."` or `".."`, containing neither `/` nor a backslash, and with no leading or trailing whitespace.
Names may contain spaces between words and letters from any language.
`"meeting notes.txt"` is valid; `"../notes.txt"` and `" notes.txt"` are not.
The argument is always a string.
These are the naming rules for this exercise; other file tools may need additional checks.
Your function must not create or read files.
In Python source, write `"\\"` to represent one literal backslash in a string.

## Repair
The broken version checks only for empty strings.
Try ordinary valid names as well as special cases such as an empty string, a single dot, and leading whitespace.
