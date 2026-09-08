# Topic coverage

This maps Pytuitor's authored curriculum to the 31 topic families in the [Pythonlings curriculum](https://pythonlings.abhik.ai/curriculum/) and its [exercise manifest](https://github.com/abhiksark/pythonlings/blob/main/info.toml), reviewed on September 8, 2026.
Pytuitor has 75 teaching lessons and 12 projects, each with a blank Build stage and a broken Repair stage.
Pythonlings advertises 292 exercises.
These are different units of work; this map establishes subject coverage, not equal exercise volume or proven teaching effectiveness.

Each linked lesson contains an explanation, worked examples, a required exercise, and executable checks.
The focus column describes what is taught across those lessons; not every API mentioned in prose is independently required by a check.

| Pythonlings topic | Pytuitor lessons | Coverage focus |
|---|---|---|
| variables | [Variables and input](../src/pytuitor/lessons/names-and-voices.md), [Objects and copying](../src/pytuitor/lessons/objects-not-boxes.md) | Assignment, conversion, identity, aliasing, mutability |
| strings | [Cleaning strings](../src/pytuitor/lessons/clean-labels.md), [Decimal measurements](../src/pytuitor/lessons/decimal-measurements.md) | String methods, normalization, splitting, f-strings and formatting |
| conditionals | [Making decisions](../src/pytuitor/lessons/choose-a-door.md), [Expressions](../src/pytuitor/lessons/python-expressions.md) | Comparisons, branching, truthiness, Boolean expressions |
| loops | [Lists and loops](../src/pytuitor/lessons/pack-your-bag.md), [Loop helpers](../src/pytuitor/lessons/loop-helpers.md), [Nested lists](../src/pytuitor/lessons/nested-collections.md), [While loops](../src/pytuitor/lessons/repeat-until-done.md) | For/while loops, range, enumerate, zip, nested traversal, stopping conditions |
| functions | [Writing functions](../src/pytuitor/lessons/small-superpowers.md), [Function options](../src/pytuitor/lessons/function-options.md), [Call contracts](../src/pytuitor/lessons/call-contracts.md) | Parameters, return values, defaults, keyword and positional arguments, debugging |
| lists | [List positions](../src/pytuitor/lessons/list-positions.md), [Editing collections](../src/pytuitor/lessons/editing-collections.md), [Nested lists](../src/pytuitor/lessons/nested-collections.md) | Indexing, empty lists, insertion/removal, sorting, nested and ragged data |
| tuples | [Tuples and sets](../src/pytuitor/lessons/tuples-and-sets.md), [Loop helpers](../src/pytuitor/lessons/loop-helpers.md) | Ordered fixed groups, unpacking, tuple-producing iteration |
| dictionaries | [Dictionaries and counts](../src/pytuitor/lessons/word-counts.md), [Editing collections](../src/pytuitor/lessons/editing-collections.md) | Key/value access, counting, defaults, deletion, dictionary views |
| sets | [Tuples and sets](../src/pytuitor/lessons/tuples-and-sets.md), [Comparing sets](../src/pytuitor/lessons/comparing-sets.md) | Uniqueness, membership, union, intersection, differences, subsets |
| comprehensions | [Readable comprehensions](../src/pytuitor/lessons/comprehensions.md), [Collection idioms](../src/pytuitor/lessons/collection-idioms.md) | Transformation, filtering, dictionary/set comprehensions, order |
| exceptions | [Invalid input](../src/pytuitor/lessons/handle-invalid-input.md), [Exceptions with context](../src/pytuitor/lessons/exception-boundaries.md) | Recovery, custom errors, exception chaining, cleanup and propagation |
| file_io | [Text files](../src/pytuitor/lessons/text-files.md), [CSV tables](../src/pytuitor/lessons/csv-tables.md), [Safe copying](../src/pytuitor/lessons/copy-with-care.md) | Context-managed text files, structured tables, non-overwriting writes |
| classes | [Your first class](../src/pytuitor/lessons/your-first-class.md), [Object protocols](../src/pytuitor/lessons/practical-object-protocols.md), [Class construction](../src/pytuitor/lessons/class-construction.md) | Instance state, properties, representations, length, equality, operators, factories |
| functional | [Callable tools](../src/pytuitor/lessons/callable-tools.md), [Functional pipelines](../src/pytuitor/lessons/functional-pipelines.md) | Function values, lambdas, sorting keys, partial application, map/filter/reduce |
| decorators | [Arguments and decorators](../src/pytuitor/lessons/functions-with-memory.md), [Decorator factories](../src/pytuitor/lessons/decorator-factories.md) | Closures, argument forwarding, metadata, configured and stacked decorators |
| generators | [Iterators and generators](../src/pytuitor/lessons/lazy-by-design.md), [Iterator tools](../src/pytuitor/lessons/iterator-tools.md) | Yield, lazy consumption, iterator exhaustion, independent yielded values |
| context_managers | [Restore temporary state](../src/pytuitor/lessons/context-practice.md), [Context protocol](../src/pytuitor/lessons/managed-contexts.md) | Generator and class context managers, entry/exit, cleanup, suppression |
| dataclasses | [Value objects](../src/pytuitor/lessons/data-models.md), [Dataclass lifecycle](../src/pytuitor/lessons/dataclass-lifecycle.md) | Generated methods, value equality, mutable defaults, post-init validation, replacement |
| type_hints | [Types and tests](../src/pytuitor/lessons/ready-to-ship.md), [Typed contracts](../src/pytuitor/lessons/typed-contracts.md), [Protocols](../src/pytuitor/lessons/structural-typing.md) | Annotations, unions, aliases, generic relationships, structural typing |
| regex | [Matching patterns](../src/pytuitor/lessons/regex-validation.md), [Extracting and replacing](../src/pytuitor/lessons/regex-transformations.md) | Whole-string matching, groups, character classes, extraction and substitution |
| testing | [Automated tests](../src/pytuitor/lessons/tests-for-your-code.md), [Types and tests](../src/pytuitor/lessons/ready-to-ship.md), [Test doubles](../src/pytuitor/lessons/test-doubles.md) | Assertions, unittest, boundaries, dependency injection, mocking |
| recursion | [Base cases](../src/pytuitor/lessons/recursion-basics.md), [Recursive collections](../src/pytuitor/lessons/recursive-collections.md) | Stopping conditions, shrinking inputs, nested traversal and limits |
| modules | [Your own modules](../src/pytuitor/lessons/your-own-modules.md), [Module boundaries](../src/pytuitor/lessons/module-boundaries.md), [Numeric tools](../src/pytuitor/lessons/numeric-tools.md), [Randomness](../src/pytuitor/lessons/repeatable-randomness.md) | Imports, reusable modules, math/statistics, independent seeded generators |
| collections | [Counting and grouping](../src/pytuitor/lessons/counting-and-grouping.md), [Queues](../src/pytuitor/lessons/queues-with-deque.md) | Counter, defaultdict, deque, ordering and mutation boundaries |
| itertools | [Iterator tools](../src/pytuitor/lessons/iterator-tools.md), [Iterator recipes](../src/pytuitor/lessons/iterator-recipes.md), [Adjacent groups](../src/pytuitor/lessons/adjacent-groups.md) | islice, chain, zip_longest, product, groupby and one-pass group lifetimes |
| json | [Structured data](../src/pytuitor/lessons/json-records.md), [Expense report](../src/pytuitor/lessons/expense-report.md) | JSON reading/writing and structured-data transformation |
| datetime | [Dates and deadlines](../src/pytuitor/lessons/dates-and-deadlines.md), [Dates and times](../src/pytuitor/lessons/date-time-formats.md) | Date arithmetic, parsing, formatting, combining clock/calendar values, leap days |
| enums | [Named states](../src/pytuitor/lessons/named-states.md) | Named members, value conversion, validated state transitions |
| pathlib | [Paths and folders](../src/pytuitor/lessons/paths-and-folders.md), [Resource paths](../src/pytuitor/lessons/resource-paths.md), [Notes archiver](../src/pytuitor/lessons/notes-archiver.md) | Path composition, file queries, explicit roots, safe automation |
| oop_advanced | [Class construction](../src/pytuitor/lessons/class-construction.md), [Descriptors](../src/pytuitor/lessons/descriptors.md), [Metaclasses](../src/pytuitor/lessons/metaclasses.md), [Method resolution](../src/pytuitor/lessons/method-resolution.md) | Abstract interfaces, class/static methods, descriptors, class hooks, cooperative inheritance |
| async | [Coroutines](../src/pytuitor/lessons/coroutine-basics.md), [Task groups](../src/pytuitor/lessons/task-groups.md), [Async streams](../src/pytuitor/lessons/async-streams.md), [Bounded work](../src/pytuitor/lessons/concurrent-batch.md) | Await, resource lifetimes, cancellation, async iteration, bounded concurrency |

## Curriculum choices

Practical collection operations and ordinary class protocols precede specialized machinery.
Advanced topics remain in the Experienced path because descriptors, class hooks, and cooperative inheritance serve its Python-depth goal.
No existing lesson was removed or repurposed, preserving its exercise contract and saved drafts.
Each chapter still ends in a project that combines its concepts.
The topic map is a maintenance aid; learner studies are required to assess retention and transfer to unfamiliar problems.
