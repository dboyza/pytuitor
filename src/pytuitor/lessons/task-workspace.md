## Build a small application across files
Keep data rules in a reusable module and application orchestration in the entry point.
Your workspace contains `tasks.py` and `lesson.py`.
Both start blank for Build.

## Requirements
In `tasks.py`, define `TaskList`.
Each instance starts empty.
Its `add(title)` method strips surrounding whitespace, ignores empty titles, and stores each exact cleaned title at most once.
Capitalization matters: `"Read"` and `"read"` are different tasks.
Its `pending()` method returns the titles in insertion order as a new list.
Changing that returned list must not change the task list itself.
For a list, `.copy()` returns a new outer list with the same items.
Strings are immutable, so this shallow copy is sufficient here.

In `lesson.py`, import `TaskList` and define `build_report(titles)`.
Create a fresh task list, add every supplied title, and return its pending list.
For `[" Read ", "", "Read", "Walk"]`, return `["Read", "Walk"]`.
An empty input list returns an empty list.
No input prompts, file persistence, or printed output are required for this version.

## Repair
The supplied app leaks its internal list to callers.
Find a fix that protects the object while leaving callers free to edit their returned list.
As an optional extension after passing, add your own `test_tasks.py` using the unittest pattern from the previous lesson.
