## JSON stores familiar data structures
JSON is a text format for exchanging structured data.
JSON uses the name **object** for a collection of named values, like a Python dictionary.
It uses **array** for an ordered collection, like a Python list.
It also supports strings, numbers, Boolean values, and `null`, which represents no value.
Python's `json` module converts between JSON and Python values.
In JSON, `true`, `false`, and `null` become Python's `True`, `False`, and `None`.

```python
import json

text = json.dumps({"city": "Oslo", "days": 2})
record = json.loads(text)
print(record["city"])
```

`dumps` creates a string; `loads` reads a string.
`dump(value, handle)` and `load(handle)` work directly with an open text file.
Invalid JSON raises `json.JSONDecodeError`.
Use UTF-8 when opening the file.
JSON object keys are strings.

## Build
Define `save_scores(path, scores)`.
`scores` is a dictionary mapping names to nonnegative integer scores.
Write it as JSON to the supplied path and return the sum of its scores.
A dictionary's `.values()` method gives its values for a loop.
An empty dictionary must save an empty JSON object and return `0`.
Keep every name exactly as given, including names with accented letters or characters from other languages.
These characters are represented using Unicode, the character system Python strings use.
Formatting and JSON key order do not matter.
The parent folder already exists.

## Repair
The broken program writes the text Python shows when displaying a dictionary.
That text is not reliably valid JSON, which has its own rules for quotes and values.
