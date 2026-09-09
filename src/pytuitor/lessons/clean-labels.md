## String methods return changed text
A method is an operation accessed through a value with a dot.
**Whitespace** includes spaces, tabs, and line breaks.
`"  Sunset  ".strip()` removes whitespace from both ends.
`"Sunset".lower()` returns `"sunset"`.
These methods return new strings; they do not change the original string.
You can chain methods because each returned string has its own methods.
`"  Sunset  ".strip().lower()` returns `"sunset"`.

`" ".join(["one", "two"])` joins strings with a space between them.
With no arguments, `.split()` splits on whitespace and ignores repeated whitespace.
Combining split and join can replace any run of whitespace with one separator.

```python
def tidy_title(text):
    words = text.strip().split()
    return " ".join(words)


print(tidy_title("  Night   sky  "))
```

## Build
A **slug** is a short text label often used in a web address or filename.
Define `slug(text)` that returns a lowercase label with words separated by single hyphens.
Ignore whitespace at the beginning and end; treat repeated spaces and tabs as one separator.
Do not remove punctuation.
`slug("  Blue   Moon ")` returns `"blue-moon"`.
Empty or whitespace-only input returns `""`.
This function takes its argument from its caller, so it should not call `input()`.
Return the result instead of only printing it.

## Repair
The broken program calls a string method but ignores the returned value.
It also uses `text.replace(" ", "-")`, which replaces each ordinary space with a hyphen.
That method does not combine repeated spaces or handle tabs; use the split-and-join approach above.
