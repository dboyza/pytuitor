## JSON stores familiar data structures
JSON is a text format for exchanging structured data.
It supports objects like dictionaries, arrays like lists, strings, numbers, booleans, and null.
Python's `json` module converts between JSON and Python values.
In JSON, `true` and `null` become Python's `True` and `None`.

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
Keep every name exactly as given, including Unicode names.
Formatting and JSON key order do not matter.
The parent folder already exists.

## Repair
The broken program saves the dictionary's display representation, which is not reliably valid JSON.
