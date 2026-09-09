## Find values, then replace matching text
Parentheses in a regex create a **capture group**, which saves one part of the matched text for you to use.
`re.findall` returns matches in their original order; with one capture group it returns that group's strings.
`re.sub(pattern, replacement, text)` returns a new string with every matching part replaced.

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
Some characters have special meanings in a regex.
For example, `[` starts a character class, a set of allowed characters such as `[a-z]`.
To match an actual opening bracket instead, write `\[`.
Likewise, `\]`, `\{`, and `\}` match literal brackets or braces.
Backslashes inside raw strings reach the regex code unchanged.
Use the `json` and `csv` modules to read those file formats; their parsing rules handle details a small regex would miss.

## Build
Define `redact_tags(text)` returning a tuple `(names, redacted)`.
Here, redacting means hiding the names in the returned text.
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
