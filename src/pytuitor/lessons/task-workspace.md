## Build a small application across files
Keep the rules for adding and storing tasks in a reusable module.
The entry point calls that module to produce the application's result.

## Return an independent list

For a list, `.copy()` returns a new outer list with the same items.
A shallow copy makes a new outer list while keeping references to the same items.
Strings cannot be changed after creation, a property called immutability.
Because the items here are strings, copying the outer list is enough to let callers safely edit their result.
