## A Python file can be a module
You have imported standard-library modules such as `json`.
Your own `.py` files can be imported too.
A module name is usually the filename without `.py`.

```python
# In greetings.py:
def hello(person):
    return f"Hello, {person}"
```

```python
# In lesson.py, in the same folder:
from greetings import hello

print(hello("Sam"))
```

Python runs a module's top-level instructions the first time it imports it in a process.
Keep reusable modules free of input prompts and unexpected print calls.
An `if __name__ == "__main__":` guard runs its indented instructions only when that file is the program entry point, not when it is imported.
The tutor runs `lesson.py` as the entry point unless the exercise says otherwise.
Use the workspace file selector to edit each file.

## Build
Create `conversions.py` with a function `minutes_to_seconds(minutes)` that returns `minutes * 60`.
Inputs are nonnegative integers.
In `lesson.py`, import that function so it is available there under the same name.
Do not print or request input at import time.
Both files are part of this exercise and both begin blank in Build.

## Repair
Fix the unit conversion in the reusable module, then check the complete workspace.
