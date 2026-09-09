## Build a small application across files
Keep the rules for adding and storing tasks in a reusable module.
The entry point calls that module to produce the application's result.
Your workspace contains `tasks.py` and `lesson.py`.
Both start blank for Build.

## Build
In `tasks.py`, define `TaskList`.
Each instance starts empty.
Its `add(title)` method strips surrounding whitespace, ignores empty titles, and stores each exact cleaned title at most once.
Capitalization matters: `"Read"` and `"read"` are different tasks.
Its `pending()` method returns a new list of titles in the order they were first added.
Changing that returned list must not change the task list itself.
For a list, `.copy()` returns a new outer list with the same items.
A shallow copy makes a new outer list while keeping references to the same items.
Strings cannot be changed after creation, a property called immutability.
Because the items here are strings, copying the outer list is enough to let callers safely edit their result.

In `lesson.py`, import `TaskList` and define `build_report(titles)`.
Create a fresh task list, add every supplied title, and return its pending list.
For `[" Read ", "", "Read", "Walk"]`, return `["Read", "Walk"]`.
An empty input list returns an empty list.
Do not request input, save tasks to files, or print output for this version.

## Repair
The supplied app returns the very list it uses to store tasks.
A caller can accidentally change the task list by editing that returned list.
Find a fix that protects the object while leaving callers free to edit their returned list.
As an optional extension after passing, add your own `test_tasks.py` using the unittest pattern from the previous lesson.
