"""One recommended sequence with optional depth, independent of authoring provenance."""

from pytuitor.models import Chapter, Section

SECTIONS = (
    Section(
        "foundations",
        "Foundations",
        "Start here: values, decisions, collections, and reusable functions.",
    ),
    Section(
        "everyday-python", "Everyday Python", "Read data and use Python's everyday library tools."
    ),
    Section(
        "building-programs", "Building programs", "Build tested tools and automate work safely."
    ),
    Section(
        "python-depth",
        "Python depth",
        "Explore Python's behavior, composition, and object protocols.",
        True,
    ),
    Section(
        "specialized-topics",
        "Specialized topics",
        "Choose async, distribution, or language machinery when you need it.",
        True,
    ),
)

# Each entry is (chapter ID, section ID, title, outcome, prerequisite chapter IDs, units).
# Prerequisites describe useful preparation; they never lock a chapter.
_OUTLINE = (
    (
        "first-programs",
        "foundations",
        "First programs",
        "Read input, calculate, and choose what happens.",
        (),
        (
            "first-light",
            "names-and-voices",
            "numbers-from-input",
            "decimal-measurements",
            "choose-a-door",
            "ticket-desk",
        ),
    ),
    (
        "lists-and-sets",
        "foundations",
        "Lists and sets",
        "Process ordered items and compare unique values.",
        ("first-programs",),
        ("pack-your-bag", "list-positions", "tuples-and-sets", "comparing-sets"),
    ),
    (
        "loops-and-dictionaries",
        "foundations",
        "Loops and dictionaries",
        "Traverse, edit, and summarize collections.",
        ("lists-and-sets",),
        (
            "loop-helpers",
            "nested-collections",
            "word-counts",
            "editing-collections",
            "repeat-until-done",
            "supply-report",
        ),
    ),
    (
        "functions-and-input",
        "foundations",
        "Functions and input",
        "Write reusable functions and recover from invalid input.",
        ("loops-and-dictionaries",),
        (
            "small-superpowers",
            "clean-labels",
            "function-options",
            "handle-invalid-input",
            "lantern-quest",
        ),
    ),
    (
        "files-and-data",
        "everyday-python",
        "Files and structured data",
        "Read, transform, and save text, JSON, and CSV.",
        ("functions-and-input",),
        ("text-files", "paths-and-folders", "json-records", "csv-tables", "expense-report"),
    ),
    (
        "text-patterns",
        "everyday-python",
        "Text patterns",
        "Validate, extract, and replace text with regular expressions.",
        ("functions-and-input",),
        ("regex-validation", "regex-transformations"),
    ),
    (
        "modules-and-library-tools",
        "everyday-python",
        "Modules and library tools",
        "Organize modules, calculate summaries, and expose command-line options.",
        ("files-and-data",),
        ("your-own-modules", "numeric-tools", "repeatable-randomness", "command-line-options"),
    ),
    (
        "dates-and-times",
        "everyday-python",
        "Dates and times",
        "Calculate deadlines and parse calendar and clock values.",
        ("modules-and-library-tools",),
        ("dates-and-deadlines", "date-time-formats"),
    ),
    (
        "collection-tools",
        "everyday-python",
        "Collection tools",
        "Transform, count, group, and queue data.",
        ("modules-and-library-tools",),
        ("comprehensions", "counting-and-grouping", "queues-with-deque"),
    ),
    (
        "classes-and-tested-tools",
        "building-programs",
        "Classes and tested tools",
        "Model state, name choices, and verify a multi-file application.",
        ("modules-and-library-tools",),
        ("your-first-class", "named-states", "tests-for-your-code", "task-workspace"),
    ),
    (
        "careful-automation",
        "building-programs",
        "Careful automation",
        "Validate inputs and protect files while automating work.",
        ("files-and-data", "modules-and-library-tools", "collection-tools"),
        ("validate-boundaries", "copy-with-care", "notes-archiver"),
    ),
    (
        "python-semantics",
        "python-depth",
        "Python semantics",
        "Understand truthiness, copying, arguments, and collection idioms.",
        ("functions-and-input", "collection-tools"),
        (
            "python-expressions",
            "objects-not-boxes",
            "call-contracts",
            "collection-idioms",
            "index-records",
        ),
    ),
    (
        "recursion-and-callables",
        "python-depth",
        "Recursion and functional tools",
        "Solve recursive problems and compose function values.",
        ("python-semantics",),
        ("recursion-basics", "recursive-collections", "callable-tools", "functional-pipelines"),
    ),
    (
        "decorators",
        "python-depth",
        "Decorators",
        "Wrap functions with predictable arguments, state, and metadata.",
        ("recursion-and-callables",),
        ("functions-with-memory", "decorator-factories"),
    ),
    (
        "iterators-and-streaming",
        "python-depth",
        "Iterators and streaming",
        "Compose lazy, bounded, one-pass data pipelines.",
        ("python-semantics",),
        (
            "lazy-by-design",
            "iterator-tools",
            "iterator-recipes",
            "adjacent-groups",
            "stream-report",
        ),
    ),
    (
        "exceptions-and-contexts",
        "python-depth",
        "Exceptions and contexts",
        "Preserve errors and restore resources reliably.",
        ("classes-and-tested-tools", "decorators", "iterators-and-streaming"),
        ("exception-boundaries", "context-practice", "managed-contexts"),
    ),
    (
        "dataclasses-and-types",
        "python-depth",
        "Dataclasses and types",
        "Express and test value objects and their lifecycle.",
        ("classes-and-tested-tools", "python-semantics"),
        ("ready-to-ship", "data-models", "dataclass-lifecycle"),
    ),
    (
        "object-protocols-and-testing",
        "python-depth",
        "Object protocols and testing",
        "Define typed interfaces and verify behavior at boundaries.",
        ("dataclasses-and-types", "decorators"),
        (
            "typed-contracts",
            "practical-object-protocols",
            "class-construction",
            "structural-typing",
            "test-doubles",
            "typed-inventory",
        ),
    ),
    (
        "async-work",
        "specialized-topics",
        "Coordinate async work",
        "Schedule work and clean up on cancellation.",
        ("exceptions-and-contexts", "iterators-and-streaming"),
        ("coroutine-basics", "clean-exits", "task-groups", "async-streams", "concurrent-batch"),
    ),
    (
        "distributable-tools",
        "specialized-topics",
        "Build distributable tools",
        "Organize imports, package metadata, and a predictable CLI.",
        ("classes-and-tested-tools", "files-and-data"),
        (
            "module-boundaries",
            "package-metadata",
            "cli-contracts",
            "resource-paths",
            "signal-from-noise",
        ),
    ),
    (
        "python-machinery",
        "specialized-topics",
        "Understand the machinery",
        "Use descriptors, class hooks, inheritance, and introspection.",
        ("object-protocols-and-testing",),
        ("descriptors", "metaclasses", "method-resolution", "runtime-inspection", "plugin-system"),
    ),
)

CHAPTERS = tuple(
    Chapter(identifier, "", title, outcome, section, prerequisites)
    for identifier, section, title, outcome, prerequisites, _ in _OUTLINE
)
CHAPTER_UNITS = {entry[0]: entry[5] for entry in _OUTLINE}

# Projects integrate the concepts their exercise actually uses, including earlier chapters.
PROJECT_PREPARATION = {
    "ticket-desk": ("names-and-voices", "numbers-from-input", "choose-a-door"),
    "supply-report": ("pack-your-bag", "list-positions", "word-counts"),
    "lantern-quest": ("choose-a-door", "pack-your-bag", "tuples-and-sets", "small-superpowers"),
    "expense-report": ("text-files", "paths-and-folders", "json-records", "csv-tables"),
    "task-workspace": (
        "clean-labels",
        "your-own-modules",
        "your-first-class",
        "tests-for-your-code",
    ),
    "notes-archiver": (
        "paths-and-folders",
        "your-own-modules",
        "validate-boundaries",
        "copy-with-care",
    ),
    "index-records": ("objects-not-boxes", "call-contracts", "collection-idioms"),
    "stream-report": ("clean-labels", "handle-invalid-input", "lazy-by-design", "iterator-tools"),
    "typed-inventory": ("your-own-modules", "ready-to-ship", "typed-contracts"),
    "concurrent-batch": ("coroutine-basics", "clean-exits", "task-groups", "async-streams"),
    "signal-from-noise": (
        "module-boundaries",
        "package-metadata",
        "cli-contracts",
        "resource-paths",
    ),
    "plugin-system": ("descriptors", "metaclasses", "method-resolution", "runtime-inspection"),
}
