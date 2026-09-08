# Curriculum map

The release candidate has 48 lessons and 12 chapter projects, split evenly between Beginner and Experienced.
Every course unit uses blank Build followed by Repair.
Prerequisites are advisory, and familiar topics remain available from the dashboard.

## Beginner

### First programs

Read input, calculate, and choose what happens.

- **Your first program**: Strings, integers, and output.
- **Variables and input**: Store values and ask the user a question.
- **Numbers from input**: Convert text and calculate whole-number results.
- **Making decisions**: Comparisons, booleans, if, elif, and else.
- **Project: the ticket desk**: Combine input, arithmetic, and decisions.

### Working with collections

Process lists and dictionaries without losing track of state.

- **Lists and loops**: Work through a collection and calculate a total.
- **Finding items in a list**: Indexes, length, and empty collections.
- **Dictionaries and counts**: Associate keys with values.
- **Repeating until done**: While loops and stopping conditions.
- **Project: supply report**: Summarize a collection without changing it.

### Reusable programs

Organize behavior into functions and handle invalid input.

- **Writing functions**: Parameters, return values, and debugging.
- **Cleaning strings**: Methods, whitespace, and reusable transformations.
- **Function options**: Default arguments, keyword calls, and local variables.
- **Handling invalid input**: Exceptions and deliberate recovery.
- **Build a text adventure**: Build a tiny branching adventure.

### Files and structured data

Read, transform, and save text, JSON, and CSV.

- **Reading and writing files**: Use a context manager to close files reliably.
- **Paths and folders**: Navigate paths without fragile string concatenation.
- **Saving structured data**: JSON, dictionaries, and lists on disk.
- **Working with CSV tables**: Read headers and quoted fields correctly.
- **Project: an expense report**: Transform CSV records into a JSON summary.

### Tools you can maintain

Build modules, command-line interfaces, classes, and tests.

- **Writing your own modules**: Share functions across Python files.
- **Command-line arguments**: Give a tool a predictable interface.
- **Your first class**: Keep state and related operations together.
- **Writing automated tests**: Use assertions and unittest to catch regressions.
- **Project: a task list workspace**: Separate a reusable model from its entry point.

### Dependable automation

Combine data, dates, validation, and safe file operations.

- **Readable comprehensions**: Transform and filter without hiding the intent.
- **Dates and deadlines**: Use date arithmetic instead of counting calendar days yourself.
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

- **Arguments and decorators**: Scope, defaults, and decorators.
- **Iterators and generators**: Comprehensions and generator protocols.
- **Restore temporary state**: Exception-safe context managers.
- **Consume only what you need**: Iterator composition.
- **Project: a streaming report**: Lazy pipeline project.

### Design and verify

Model data, express protocols, and test behavior at boundaries.

- **Types and tests**: Types, tests, and project boundaries.
- **Model a small value object**: Classes & dataclasses.
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

Each lesson specifies the names, inputs, return values or printed output, and edge cases needed to build its program without starter code.
Repair uses the same contract and a deliberately defective implementation.
Checks report their operation, input, expected result, actual result, printed output, and status.
Reference solutions show one valid approach and never overwrite learner drafts.

Automated checks establish executable consistency, not whether a first-time learner understands the explanation.
Use the [learner study](learner-study.md) to test that distinction before calling the release final.
