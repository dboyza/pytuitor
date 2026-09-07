# Read data with explicit paths

`pathlib.Path` represents a filesystem path and provides methods for reading and writing files.
Accepting a path argument makes code usable from different working directories and easy to test with temporary files.
Specify an encoding for text files so behavior does not depend on local defaults.

```python
from pathlib import Path
import json

path = Path("example.json")
text = path.read_text(encoding="utf-8")
value = json.loads(text)
```

JSON objects become dictionaries, arrays become lists, and null becomes None.
Parsing successfully does not mean the data has the shape your application expects.
`isinstance(value, dict)` tests whether the parsed value is a dictionary.
`json.JSONDecodeError` is a subclass of ValueError.
Catch only exceptions your application can recover from; a permissions error is different from an optional file being absent.
For data shipped inside an installed package, prefer `importlib.resources.files(package)` over assuming the current working directory or a source checkout exists.

## Build

Write `read_settings(path)` accepting a string path or a Path object.
Read UTF-8 text and parse it as JSON.
Return the parsed dictionary if the top-level value is an object.
Return `{}` only when the file does not exist.
Raise `ValueError` for a valid JSON value that is not a dictionary.
Let malformed JSON errors and other filesystem errors propagate.
Do not write to the file, change directories, or print.
For a file containing `{"theme": "blue"}`, return `{'theme': 'blue'}`.
Checks create their own temporary files, so you do not need to prepare sample data before pressing Check.

## Repair

Repair's broad handler converts every failure into apparently valid empty settings.
Restore the distinction between missing, malformed, and structurally invalid data.
