# Curriculum review: Build and Repair

This document records the original MVP.
For the current release candidate, use the [v1 scope](v1-plan.md) and [curriculum map](curriculum.md).

Each lesson requires a complete program from a blank editor, followed by repair of a separate program against the same behavioral requirements.
The table records the prerequisites checked during the content review and the missing instructions filled in for this flow.
The beginner sequence introduces syntax before requiring it; the experienced sequence assumes general programming knowledge and supplies Python-specific syntax.

| Lesson | Prior knowledge used | Instructions verified or added | Repair defect |
| --- | --- | --- | --- |
| Your first program | None | Strings, integers, quotes, print, multiplication, exact two-line output | A calculation is printed as text |
| Variables and input | Strings and print | Assignment, input prompts, conversion, f-strings, required student and greeting variables | Missing f-string prefix |
| Making decisions | Variables and input | Booleans, comparison, indentation, if/elif/else, input and final print | Separate if statements overwrite a valid result |
| Lists and loops | Integers, input, conditions, indentation | Lists, for, split, append, conversion, input setup and total | Total is reset inside the loop |
| Writing functions | Arithmetic, variables, conditions | def, parameters, arguments, return, None, function signature and demonstration call | One branch prints instead of returning |
| Build a text adventure | All beginner lessons | Tuple return, boolean state, and/not, game rules, input and function call | Collection state is reset on every move |
| Objects and copying | Programming in another language | Python def and indentation, dictionary access, import, return, identity and deepcopy | Shallow copy shares nested data |
| Arguments and decorators | Python functions, lists, imports, identity | Explicit signatures, None sentinel, closures, argument forwarding and wraps | Mutable default persists between calls |
| Iterators and generators | Functions, loops and arguments | Iterator protocol, yield, filtering, laziness and generator examples | return ends iteration immediately |
| Context managers and async | Decorators and generators | contextmanager import, try/finally, coroutine definition, sleep, gather and return order | Cleanup is skipped after an exception |
| Types and tests | Functions and exception handling | Type annotations, int conversion, validation, assert and test function contract | Zero is incorrectly rejected |
| Build a log analyzer | Dictionaries, iteration, functions and testing | sys/json imports, whitespace parsing, dictionary membership/increment, main guard and EOF | Lowercase severities are ignored |

Reference solutions pass the authored behavioral checks, and every broken Repair program fails at least one check.
These checks verify behavior rather than enforce one exact implementation.
Keyboard journeys cover both stages, and profile tests preserve their separate drafts across navigation and restart.
The next content validation step is observing a beginner and an experienced programmer complete the lessons without coaching.
