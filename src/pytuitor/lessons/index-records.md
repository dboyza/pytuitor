# Project: a record index

Build a small library function that makes incoming records fast to look up.
This combines dictionary membership, iteration, validation, and the independent copies from Objects and copying.
Your caller must be able to edit an indexed record without changing the original data.

## Take it further

After both stages pass, think about whether your application's duplicate policy should reject, merge, or replace records.
That is a contract decision, not an implementation detail to leave to dictionary assignment.

## Let the caller choose a key

A function is also a value that can be passed to another function.
A **key function** accepts one record and returns the value used to identify or group it.
For example, `def record_city(record): return record["city"]` defines a key function for cities.
Inside a function receiving a parameter named `key`, call `key(record)` to obtain that record's key.
Evaluate it once per record: a caller-supplied function may count calls or perform work beyond a simple lookup.
