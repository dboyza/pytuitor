# Curriculum map

The release candidate has one syllabus with 75 lessons and 12 projects across 21 chapters.
The first three sections form the recommended sequence; Python depth and Specialized topics are optional.
Start learning begins with Foundations, and learners can open any chapter directly.
Each chapter lists useful preparation without locking access.
Every course unit uses blank Build followed by Repair.
See [topic coverage](coverage.md) for the mapping to Pythonlings and the boundaries of that comparison.

## Foundations

Start here: values, decisions, collections, and reusable functions.

### First programs

Read input, calculate, and choose what happens.

- **Your first program**: Strings, integers, and output.
- **Variables and input**: Store values and ask the user a question.
- **Numbers from input**: Convert text and calculate whole-number results.
- **Decimal measurements**: Read decimal input and format a calculated measurement.
- **Making decisions**: Comparisons, booleans, if, elif, and else.
- **Project: the ticket desk**: Combine input, arithmetic, and decisions.

### Lists and sets

Process ordered items and compare unique values.

Useful preparation: First programs.

- **Lists and loops**: Work through a collection and calculate a total.
- **Finding items in a list**: Indexes, length, and empty collections.
- **Tuples, sets, and unpacking**: Group a fixed pair and recognize unique items.
- **Comparing sets**: Find shared, missing, and combined values.

### Loops and dictionaries

Traverse, edit, and summarize collections.

Useful preparation: Lists and sets.

- **Numbering and pairing items**: Use range, enumerate, and zip to organize loops.
- **Working with nested lists**: Traverse rows and columns without losing empty rows.
- **Dictionaries and counts**: Associate keys with values.
- **Editing lists and dictionaries**: Insert, remove, sort, and delete deliberately.
- **Repeating until done**: While loops and stopping conditions.
- **Project: supply report**: Summarize a collection without changing it.

### Functions and input

Write reusable functions and recover from invalid input.

Useful preparation: Loops and dictionaries.

- **Writing functions**: Parameters, return values, and debugging.
- **Cleaning strings**: Methods, whitespace, and reusable transformations.
- **Function options**: Default arguments, keyword calls, and local variables.
- **Handling invalid input**: Exceptions and deliberate recovery.
- **Build a text adventure**: Build a tiny branching adventure.

## Everyday Python

Read data and use Python's everyday library tools.

### Files and structured data

Read, transform, and save text, JSON, and CSV.

Useful preparation: Functions and input.

- **Reading and writing files**: Open files and close them reliably.
- **Paths and folders**: Build file paths without joining strings by hand.
- **Saving structured data**: JSON, dictionaries, and lists on disk.
- **Working with CSV tables**: Read headers and quoted fields correctly.
- **Project: an expense report**: Transform CSV records into a JSON summary.

### Text patterns

Validate, extract, and replace text with regular expressions.

Useful preparation: Functions and input.

- **Matching text patterns**: Validate complete text with regular expressions.
- **Extracting and replacing text**: Find values and replace matching text.

### Modules and library tools

Organize modules, calculate summaries, and expose command-line options.

Useful preparation: Files and structured data.

- **Writing your own modules**: Share functions across Python files.
- **Math and statistical summaries**: Use library calculations and distinguish mean from median.
- **Repeatable random choices**: Repeat random choices without affecting other code.
- **Command-line arguments**: Give a tool a predictable interface.

### Dates and times

Calculate deadlines and parse calendar and clock values.

Useful preparation: Modules and library tools.

- **Dates and deadlines**: Use date arithmetic instead of counting calendar days yourself.
- **Parsing dates and times**: Combine calendar dates, clock times, and explicit formats.

### Collection tools

Transform, count, group, and queue data.

Useful preparation: Modules and library tools.

- **Readable comprehensions**: Transform and filter without hiding the intent.
- **Counting and grouping**: Use Counter and defaultdict for collections.
- **Queues with deque**: Process work in arrival order.

## Building programs

Build tested tools and automate work safely.

### Classes and tested tools

Model state, name choices, and verify a multi-file application.

Useful preparation: Modules and library tools.

- **Your first class**: Keep state and related operations together.
- **Named states with enums**: Represent a fixed set of meaningful values.
- **Writing automated tests**: Use unittest to check expected results.
- **Project: a task list workspace**: Keep task rules in a reusable Python module.

### Careful automation

Validate inputs and protect files while automating work.

Useful preparation: Files and structured data, Modules and library tools, Collection tools.

- **Validating a tool’s inputs**: State acceptable inputs before touching files.
- **Copying without overwriting**: Preview work and protect existing data.
- **Project: a careful notes archiver**: Preview a multi-file automation tool before it writes.

## Python depth (optional)

Explore Python's behavior, composition, and object protocols.

### Python semantics

Understand truthiness, copying, arguments, and collection idioms.

Useful preparation: Functions and input, Collection tools.

- **Expressions with intent**: Python syntax & truthiness.
- **Objects and copying**: Identity, aliasing, and mutability.
- **Make call sites readable**: Positional & keyword arguments.
- **Group without losing order**: Dictionaries, sets & comprehensions.
- **Project: a record index**: Record indexing project.

### Recursion and functional tools

Solve recursive problems and compose function values.

Useful preparation: Python semantics.

- **Recursion and base cases**: Solve a smaller version of the same problem.
- **Nested lists with recursion**: Traverse collections at different depths.
- **Callable tools and sorting**: Callables, lambdas & partial.
- **Map, filter, and folds**: Map, filter & reduce.

### Decorators

Wrap functions with predictable arguments, state, and metadata.

Useful preparation: Recursion and functional tools.

- **Arguments and decorators**: Scope, defaults, and decorators.
- **Configure and stack decorators**: Decorator factories & stacking.

### Iterators and streaming

Compose lazy, bounded, one-pass data pipelines.

Useful preparation: Python semantics.

- **Iterators and generators**: Comprehensions and generator protocols.
- **Consume only what you need**: Iterator composition.
- **Combine and bound iterators**: Chain, islice, zip_longest & product.
- **Group consecutive values**: Consecutive grouping with itertools.
- **Project: a streaming report**: Lazy pipeline project.

### Exceptions and contexts

Preserve errors and restore resources reliably.

Useful preparation: Classes and tested tools, Decorators, Iterators and streaming.

- **Exceptions with context**: Custom exceptions & chaining.
- **Restore temporary state**: Exception-safe context managers.
- **Implement the context protocol**: Class-based context managers.

### Dataclasses and types

Express and test value objects and their lifecycle.

Useful preparation: Classes and tested tools, Python semantics.

- **Types and tests**: Types, tests, and project boundaries.
- **Model a small value object**: Classes & dataclasses.
- **Dataclass defaults and updates**: Dataclass factories & post-init.

### Object protocols and testing

Define typed interfaces and verify behavior at boundaries.

Useful preparation: Dataclasses and types, Decorators.

- **Unions and generic contracts**: Union types & TypeVar generics.
- **Objects that fit Python**: Properties & special methods.
- **Factories and abstract interfaces**: Class methods, static methods & ABCs.
- **Program to a small protocol**: Structural typing & protocols.
- **Inject effects for reliable tests**: Dependency injection & mocking.
- **Project: an inventory library**: Typed multi-file project.

## Specialized topics (optional)

Choose async, distribution, or language machinery when you need it.

### Coordinate async work

Schedule work and clean up on cancellation.

Useful preparation: Exceptions and contexts, Iterators and streaming.

- **Await cooperative work**: Coroutines & event loops.
- **Context managers and async**: Resources, exceptions, and async.
- **Give tasks a shared lifetime**: Task groups & cancellation.
- **Consume an async stream**: Async iteration.
- **Project: bounded async work**: Bounded concurrency project.

### Build distributable tools

Organize imports, package metadata, and a predictable CLI.

Useful preparation: Classes and tested tools, Files and structured data.

- **Keep imports predictable**: Modules & import boundaries.
- **Understand package metadata**: Virtual environments & packaging.
- **Define a predictable CLI**: Argument parsing & exit behavior.
- **Read data with explicit paths**: Pathlib & structured files.
- **Build a log analyzer**: Build a log-analysis CLI.

### Understand the machinery

Use descriptors, class hooks, inheritance, and introspection.

Useful preparation: Object protocols and testing.

- **Control attribute access**: Descriptors & attribute lookup.
- **Register classes deliberately**: Metaclasses & class creation.
- **Method lookup and inheritance**: Inheritance & super.
- **Inspect without executing**: Inspect function parameters.
- **Project: an extensible formatter**: Plugin architecture project.

## Teaching and validation

Chapters group related work rather than requiring a project at the end of every group.
Projects remain where their required concepts have been introduced, including preparation from earlier chapters.
Recursion is optional depth rather than a prerequisite for an introductory text adventure.
Generator and class context managers follow generators, decorators, and classes.
Packaging does not require async, and language machinery does not require packaging.

Each lesson states the names, inputs, outputs, and edge cases needed to build its program from a blank editor.
Repair uses the same contract with a deliberately defective implementation.
Checks report expected and actual behavior; reference solutions never replace learner drafts.
All existing lesson IDs, exercise contracts, revisions, and saved drafts remain intact through this reorganization.
Retired authoring paths remain implementation provenance, not learner navigation.

See the [language review](language-review.md) for terminology and prerequisite review coverage.
Automated checks establish executable consistency.
Use the [learner study](learner-study.md) to assess teaching effectiveness with real learners.
