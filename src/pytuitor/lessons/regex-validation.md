## Describe a text shape
A regular expression, or regex, describes a pattern in text.
Python includes the `re` module; `import re` makes its functions available as `re.function_name(...)`.
A raw string such as `r"[a-z]+"` keeps backslashes available to the regex engine.
`[a-z]` matches one lowercase ASCII letter, `+` repeats one or more times, and `{2}` repeats exactly twice.
A literal hyphen outside square brackets matches a hyphen.

```python
import re

pattern = r"[a-z]+:[0-9]{2}"
print(re.fullmatch(pattern, "room:42") is not None)  # True
print(re.fullmatch(pattern, "room:420") is not None)  # False
```

A match function returns a match object when successful and `None` otherwise.
`is not None` turns that result into a Boolean.
`fullmatch` checks the whole string, while `search` finds a matching portion anywhere inside it.
Prefer ordinary string methods for simple operations; use regex when a text shape combines several rules.

## Build
Define `valid_code(text)` returning `True` only for exactly two uppercase ASCII letters, one hyphen, and exactly three ASCII digits.
`"AB-123"` and `"ZZ-000"` are valid.
Lowercase letters, spaces, extra characters, trailing newlines, and non-ASCII digits are invalid.
An empty string is invalid.
The input is always a string; do not strip or otherwise normalize it.
Use `[A-Z]` for uppercase ASCII letters and `[0-9]` for ASCII digits.
Return a Boolean without printing.

## Repair
The broken version accepts a valid-looking substring inside invalid text.
Choose the matching operation that enforces the complete contract.
