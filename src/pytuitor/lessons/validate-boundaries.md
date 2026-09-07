## Validation belongs at a program's boundary
A reusable function needs a clear contract for acceptable input.
Checking that contract early prevents later operations from guessing what the caller meant.
`raise ValueError("message")` deliberately reports an unacceptable value.
A caller can catch it with the `try`/`except` pattern you learned earlier.
For a predicate, a function answering yes or no, returning `True` or `False` can be clearer.

Boolean operators combine conditions.
`a and b` is true when both conditions are true; `a or b` is true when at least one is true; `not a` reverses the truth value.
`part in text` asks whether one string occurs inside another.

## Build
Define `valid_filename(name)` that returns a boolean.
For this exercise, a valid name is a nonempty string other than `"."` or `".."`, containing neither `/` nor a backslash, and with no leading or trailing whitespace.
Names may contain internal spaces and Unicode letters.
`"meeting notes.txt"` is valid; `"../notes.txt"` and `" notes.txt"` are not.
The argument is always a string.
This is an exercise-specific naming policy, not a complete defense against every filesystem attack.
Your function must not create or read files.
In Python source, write `"\\"` to represent one literal backslash in a string.

## Repair
The broken version checks only for empty strings.
Use ordinary valid names as well as invalid boundary cases in your own experiments.
