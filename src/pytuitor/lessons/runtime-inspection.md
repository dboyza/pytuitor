# Inspect without executing

Functions are objects with metadata such as `__name__`, defaults, annotations, and a code object.
`inspect.signature` offers a higher-level view of their call contract.
Code objects also expose implementation details, but local-variable storage is not the same thing as a parameter list.

```python
import inspect

signature = inspect.signature(lambda count, *, verbose=False: None)
for name, parameter in signature.parameters.items():
    has_default = parameter.default is not inspect.Parameter.empty
```

Parameters have kinds such as POSITIONAL_ONLY, POSITIONAL_OR_KEYWORD, VAR_POSITIONAL for `*args`, KEYWORD_ONLY, and VAR_KEYWORD for `**kwargs`.
A variadic parameter accepts zero values even though it has no ordinary default.
Inspection should not call the function whose interface you are describing.

CPython compiles source into code objects and executes bytecode; `dis.dis(fn)` displays that bytecode for investigation.
Opcodes and optimizations vary across Python versions, so program behavior should not depend on an exact instruction sequence.
CPython uses reference counting with cycle detection, but Python programs should use explicit context-managed cleanup instead of relying on object destruction timing.
Closures keep references to captured variables in cells; a closure sees later assignments to those variables rather than freezing their values automatically.
The language contract and one interpreter's storage strategy are different levels of explanation.

## Build

Write `describe_callable(fn)` for an ordinary Python function.
Return a dictionary with `name` from fn.__name__, `parameters` listing all parameter names in declaration order, and `required` listing only parameters without defaults that are not variadic.
Include required keyword-only parameters.
Ignore local variables, annotations, and return values.
Never execute fn.
For `def send(message, times=1, *, destination): ...`, required is `['message', 'destination']`.
An argument-free function produces empty lists.
Do not print.

## Repair

Repair treats code-object local storage as a complete signature.
Replace that assumption with inspect's parameter information.
