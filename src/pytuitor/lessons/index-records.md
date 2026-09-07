# Project: a record index

Build a small library function that makes incoming records fast to look up.
This combines dictionary membership, iteration, validation, and the independent copies from Objects and copying.
Your caller must be able to edit an indexed record without changing the original data.

## Build

Write `index_records(records)`.
The input is a finite iterable of dictionaries.
Every record has an `"id"` key with a string value; all remaining fields contain values supported by `copy.deepcopy`.
Return a dictionary mapping each identifier to a deeply independent copy of its record, including its identifier.
Preserve identifier insertion order.
If an identifier occurs twice, raise `ValueError`, even when both records have equal contents.
Do not mutate any input record.
An empty iterable returns `{}`.
No input prompts or printed output are required.

For example, `[{'id': 'r7', 'tags': ['urgent']}]` produces `{'r7': {'id': 'r7', 'tags': ['urgent']}}`.
Appending a tag to that result must not change the source list.
Use `from copy import deepcopy` to access the copying function.
A dictionary comprehension alone would silently overwrite duplicate identifiers, so consider where validation belongs.

## Repair

Repair has the correct broad shape but loses information and shares mutable objects.
Use Check's duplicate and aliasing cases to distinguish these failures.

## Take it further

After both stages pass, think about whether your application's duplicate policy should reject, merge, or replace records.
That is a contract decision, not an implementation detail to leave to dictionary assignment.
