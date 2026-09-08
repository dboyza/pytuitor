## Pull out fields, then replace spans
Parentheses in a regex capture part of a match.
`re.findall` returns matches in their original order; with one capture group it returns that group's strings.
`re.sub(pattern, replacement, text)` returns text with every matching span replaced.

```python
import re

message = "{item:tea} and {item:rice}"
pattern = r"\{item:([a-z]+)\}"
names = re.findall(pattern, message)
print(names)  # ['tea', 'rice']
mask = "{item:sold}"
updated = re.sub(pattern, mask, message)
print(updated)
```

The parentheses capture a name while the surrounding pattern matches the complete marker.
Regex metacharacters have special meanings: `[` starts a character class, so `\[` matches a literal opening bracket.
Likewise, `\]`, `\{`, and `\}` match literal brackets or braces.
Backslashes inside raw strings reach the regex engine unchanged.
A regex sees text, not meaning; use structured parsers for JSON or CSV instead of trying to describe their full grammar with a pattern.

## Build
Define `redact_tags(text)` returning a tuple `(names, redacted)`.
A valid tag is exactly `[user:name]`, where `name` contains one or more lowercase ASCII letters.
`names` is a list of names from every valid tag, preserving order and duplicates.
`redacted` replaces every complete valid tag with `[user:hidden]` and preserves all other text exactly.
For `"[user:ada] met [user:bob]"`, return `(["ada", "bob"], "[user:hidden] met [user:hidden]")`.
Invalid tags such as `[user:Ada]`, `[user:]`, and `[user:ab2]` remain unchanged and contribute no names.
Empty input returns `([], "")`.
The input is always a string; do not print.

## Repair
Names are extracted correctly, but only the first matching tag is replaced.
Make extraction and replacement agree about which tags they process.
