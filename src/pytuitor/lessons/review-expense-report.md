## Practice: a JSON roster
Define `roster(text)`.
Parse a JSON string containing a list of objects with a `name` key.
Return a list of their names, in the same order.
For `'[{"name": "Mia"}, {"name": "Jo"}]'`, return `["Mia", "Jo"]`.
An empty JSON array returns an empty list.
Inputs are valid JSON with all required keys.
Import `json`, use `json.loads`, and append names inside a loop.
