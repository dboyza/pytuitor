## Turn repeated data into a report
Your input is a delivery list, with one word for each item delivered.
Use a list to keep input order and a dictionary to calculate counts.
The `in` operator checks membership: `"rope" in counts` asks whether `"rope"` is a key.
`"rope" not in counts` asks whether it is absent.
This lets you remember the first time each word appears.

## Build
Read one space-separated input line.
Create `counts`, a dictionary counting each word, and `order`, a list containing each distinct word once in the order it first appeared.
Print one line per word in `order`, formatted `word: count`.
Print `No supplies` if the input is empty.
For `rope lamp rope map lamp`, print:

```text
rope: 2
lamp: 2
map: 1
```

Preserve capitalization and do not alphabetize the report.
You do not need to define your own functions yet.
Create the empty list and dictionary before the loop, then decide which changes happen inside it.

## Repair
The supplied program adds duplicate entries to the reporting order.
Fix it while retaining the same counting behavior.
