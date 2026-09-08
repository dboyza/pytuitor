# Curriculum map

The release candidate has 75 lessons and 12 chapter projects, with 40 beginner lessons and 35 experienced lessons.
Each path has six chapter projects.
Every course unit uses blank Build followed by Repair.
Prerequisites are advisory, and familiar topics remain available from the dashboard.
See [topic coverage](coverage.md) for the mapping to Pythonlings and the boundaries of that comparison.

## Beginner

### First programs

Read input, calculate, and choose what happens.

- **Your first program**: Strings, integers, and output.
- **Variables and input**: Store values and ask the user a question.
- **Numbers from input**: Convert text and calculate whole-number results.
- **Decimal measurements**: Read decimal input and format a calculated measurement.
- **Making decisions**: Comparisons, booleans, if, elif, and else.
- **Project: the ticket desk**: Combine input, arithmetic, and decisions.

### Working with collections

Process ordered items, unique values, and dictionaries.

- **Lists and loops**: Work through a collection and calculate a total.
- **Finding items in a list**: Indexes, length, and empty collections.
- **Tuples, sets, and unpacking**: Group a fixed pair and recognize unique items.
- **Comparing sets**: Find shared, missing, and combined values.
- **Numbering and pairing items**: Use range, enumerate, and zip to organize loops.
- **Working with nested lists**: Traverse rows and columns without losing empty rows.
- **Dictionaries and counts**: Associate keys with values.
- **Editing lists and dictionaries**: Insert, remove, sort, and delete deliberately.
- **Repeating until done**: While loops and stopping conditions.
- **Project: supply report**: Summarize a collection without changing it.

### Reusable programs

Organize behavior into functions and handle invalid input.

- **Writing functions**: Parameters, return values, and debugging.
- **Cleaning strings**: Methods, whitespace, and reusable transformations.
- **Function options**: Default arguments, keyword calls, and local variables.
- **Recursion and base cases**: Solve a smaller version of the same problem.
- **Nested lists with recursion**: Traverse collections at different depths.
- **Handling invalid input**: Exceptions and deliberate recovery.
- **Build a text adventure**: Build a tiny branching adventure.

### Files and structured data

Read, transform, and save text, JSON, and CSV.

- **Reading and writing files**: Use a context manager to close files reliably.
- **Paths and folders**: Navigate paths without fragile string concatenation.
- **Saving structured data**: JSON, dictionaries, and lists on disk.
- **Working with CSV tables**: Read headers and quoted fields correctly.
- **Matching text patterns**: Validate complete text with regular expressions.
- **Extracting and replacing text**: Capture fields and substitute matching spans.
- **Project: an expense report**: Transform CSV records into a JSON summary.

### Tools you can maintain

Build modules, command-line interfaces, classes, and tests.

- **Writing your own modules**: Share functions across Python files.
- **Math and statistical summaries**: Use library calculations and distinguish mean from median.
- **Repeatable random choices**: Generate reproducible samples without changing global random state.
- **Command-line arguments**: Give a tool a predictable interface.
- **Your first class**: Keep state and related operations together.
- **Named states with enums**: Represent a fixed set of meaningful values.
- **Writing automated tests**: Use assertions and unittest to catch regressions.
- **Project: a task list workspace**: Separate a reusable model from its entry point.

### Dependable automation

Combine data, dates, validation, and safe file operations.

- **Readable comprehensions**: Transform and filter without hiding the intent.
- **Counting and grouping**: Use Counter and defaultdict for collections.
- **Queues with deque**: Process work in arrival order.
- **Dates and deadlines**: Use date arithmetic instead of counting calendar days yourself.
- **Parsing dates and times**: Combine calendar dates, clock times, and explicit formats.
- **Validating a tool’s inputs**: State acceptable inputs before touching files.
- **Copying without overwriting**: Preview work and protect existing data.
- **Project: a careful notes archiver**: Preview a multi-file automation tool before it writes.

## Experienced

### Think in Python

Write clear functions without aliasing or argument surprises.

- **Expressions with intent**: Python syntax & truthiness.
- **Objects and copying**: Identity, aliasing, and mutability.
- **Make call sites readable**: Positional & keyword arguments.
- **Group without losing order**: Dictionaries, sets & comprehensions.
- **Project: a record index**: Record indexing project.

### Compose and stream

Compose decorators, lazy pipelines, and reliable resource cleanup.

- **Callable tools and sorting**: Callables, lambdas & partial.
- **Map, filter, and folds**: Map, filter & reduce.
- **Arguments and decorators**: Scope, defaults, and decorators.
- **Configure and stack decorators**: Decorator factories & stacking.
- **Iterators and generators**: Comprehensions and generator protocols.
- **Exceptions with context**: Custom exceptions & chaining.
- **Restore temporary state**: Exception-safe context managers.
- **Implement the context protocol**: Class-based context managers.
- **Consume only what you need**: Iterator composition.
- **Combine and bound iterators**: Chain, islice, zip_longest & product.
- **Group consecutive values**: Consecutive grouping with itertools.
- **Project: a streaming report**: Lazy pipeline project.

### Design and verify

Model data, express protocols, and test behavior at boundaries.

- **Types and tests**: Types, tests, and project boundaries.
- **Model a small value object**: Classes & dataclasses.
- **Dataclass defaults and updates**: Dataclass factories & post-init.
- **Unions and generic contracts**: Union types & TypeVar generics.
- **Objects that fit Python**: Properties & special methods.
- **Factories and abstract interfaces**: Class methods, static methods & ABCs.
- **Program to a small protocol**: Structural typing & protocols.
- **Inject effects for reliable tests**: Dependency injection & mocking.
- **Project: an inventory library**: Typed multi-file project.

### Coordinate async work

Schedule work, preserve order, and clean up on cancellation.

- **Await cooperative work**: Coroutines & event loops.
- **Context managers and async**: Resources, exceptions, and async.
- **Give tasks a shared lifetime**: Task groups & cancellation.
- **Consume an async stream**: Async iteration.
- **Project: bounded async work**: Bounded concurrency project.

### Build distributable tools

Separate modules, validate metadata, and expose a predictable CLI.

- **Make imports boring**: Modules & import boundaries.
- **Understand package metadata**: Virtual environments & packaging.
- **Define a predictable CLI**: Argument parsing & exit behavior.
- **Read data with explicit paths**: Pathlib & structured files.
- **Build a log analyzer**: Build a log-analysis CLI.

### Understand the machinery

Use descriptors and class hooks, and inspect Python execution.

- **Control attribute access**: Descriptors & attribute lookup.
- **Register classes deliberately**: Metaclasses & class creation.
- **Cooperate through the MRO**: Inheritance & super.
- **Inspect without executing**: Python internals & introspection.
- **Project: an extensible formatter**: Plugin architecture project.

## Teaching and validation

Each lesson states the names, inputs, outputs, and edge cases needed to build its program from a blank editor.
Repair uses the same contract with a deliberately defective implementation.
Checks report expected and actual behavior; reference solutions never replace learner drafts.
Existing lesson IDs and saved drafts remain intact when new lessons are inserted.

Automated checks establish executable consistency.
Use the [learner study](learner-study.md) to assess teaching effectiveness with real beginners and experienced programmers.
