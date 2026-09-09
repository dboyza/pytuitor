## Dictionaries for counting and grouping
The standard-library `collections` module provides dictionaries with useful extra behavior.
`Counter` counts how many times each item appears and treats an unseen key as zero.
`defaultdict` creates a default value when you access a missing key.

```python
from collections import Counter, defaultdict

colors = Counter(["blue", "gold", "blue"])
print(colors["blue"])  # 2
print(colors["green"])  # 0

by_initial = defaultdict(list)
for word in ["tea", "toast", "rice"]:
    by_initial[word[0]].append(word)
print(dict(by_initial))  # {'t': ['tea', 'toast'], 'r': ['rice']}
```

Pass `list`, not `list()`, so `defaultdict` can call it to create a separate empty list for each missing key.
`dict(...)` converts either type to an ordinary dictionary to return to the caller.
Counting and grouping preserve different information: counts keep quantities, while grouped lists keep the original items.

## Build
Define `summarize_visits(visits)` returning `(counts, pages)` as two dictionaries.
`visits` is a list of `(user, page)` string pairs.
`counts[user]` is the total number of that user's visits.
`pages[user]` is a list of their pages in the order they appeared in the input, including duplicates.
For `[("ada", "home"), ("ada", "help")]`, return `({"ada": 2}, {"ada": ["home", "help"]})`.
An empty list returns `({}, {})`.
Empty strings are valid values, and only users present in the input appear in the results.
Do not change the input or print.
Try `Counter` and `defaultdict`; ordinary dictionaries implementing the same behavior are accepted.

## Repair
Counts are correct, but each page replaces the user's previous pages.
Keep the whole ordered history for each user.
