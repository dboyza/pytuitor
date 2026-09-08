# Preserve the reason for failure

Custom exceptions give callers a meaningful category to catch.
Subclass an appropriate built-in exception and use `pass` when no additional behavior is needed.
`raise NewError(...) from error` records the original exception in `__cause__`, preserving diagnostic context.
Catch only errors you can meaningfully handle or translate.

```python
class ConfigurationError(ValueError):
    pass


try:
    timeout = int("soon")
except ValueError as error:
    raise ConfigurationError("Timeout must be an integer") from error
```

`finally` runs when a `try` block exits, including through a return or an exception.
Use it for cleanup; avoid returning from `finally`, which would hide failures.
A following lesson introduces context managers to package this pattern.

```python
handle = open("notes.txt")
try:
    text = handle.read()
finally:
    handle.close()
```

## Build

Define `RecordError` as a subclass of `ValueError`.
Write `parse_record(text)` accepting a string and returning its `int` conversion, including whitespace, signs, and zero.
Translate a conversion `ValueError` into `RecordError` with the original exception as its explicit cause; the message is your choice.
Write `read_record(stream)` to call `stream.read()` once and pass its result to `parse_record`.
Always call `stream.close()` once after attempting the read, whether reading or parsing succeeds or fails.
Return the parsed integer on success; let reading errors such as `OSError` propagate unchanged.
Assume `close()` succeeds.
The stream is supplied by the caller; do not open files, print, or read console input.

## Repair

Invalid records currently expose the raw conversion error, and a failure prevents cleanup.
Restore the custom exception, original cause, and unconditional closing.
