## A test is an executable expectation
You have used Check to compare actual results with expected ones.
You can write expectations for your own programs too.
`assert expression` raises `AssertionError` if the expression is false.
For larger test suites, the standard-library `unittest` module organizes tests and reports failures.

```python
import unittest


class AdditionTests(unittest.TestCase):
    def test_two_numbers(self):
        self.assertEqual(2 + 3, 5)
```

A test class inherits from `unittest.TestCase`; the parentheses name the base class whose testing tools it uses.
Methods beginning with `test_` are discovered as tests.
`self.assertEqual(actual, expected)` reports a failure if values differ.
In an external terminal, `python -m unittest` discovers tests in files named `test*.py`.
Here, Check will load and run the test class for you.

## Build
Define `clamp(value, low, high)` that returns `low` below the lower boundary, `high` above the upper boundary, and the original value otherwise.
Assume `low <= high`.
Also define a `unittest.TestCase` subclass named `ClampTests` with at least three test methods: `test_below`, `test_inside`, and `test_above`.
Each must call `clamp` and assert its expected result.
Use distinct cases that would detect a clamp implementation always returning the lower bound, the original value, or the upper bound.
Do not call `unittest.main()` at top level because Check manages the run.

## Repair
A boundary comparison is reversed in the provided function.
Use the provided tests to identify and fix it.
