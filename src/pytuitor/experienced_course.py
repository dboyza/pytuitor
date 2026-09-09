"""Python depth: six chapters and authored exercises."""

from dataclasses import replace

from pytuitor.legacy import BY_ID as LEGACY
from pytuitor.models import Chapter, Check, Lesson, code, lesson_text

CHAPTERS = (
    Chapter(
        "python-semantics",
        "experienced",
        "Think in Python",
        "Write clear functions without aliasing or argument surprises.",
    ),
    Chapter(
        "python-composition",
        "experienced",
        "Compose and stream",
        "Compose decorators, lazy pipelines, and reliable resource cleanup.",
    ),
    Chapter(
        "python-design",
        "experienced",
        "Design and verify",
        "Model data, express protocols, and test behavior at boundaries.",
    ),
    Chapter(
        "python-concurrency",
        "experienced",
        "Coordinate async work",
        "Schedule work, preserve order, and clean up on cancellation.",
    ),
    Chapter(
        "python-delivery",
        "experienced",
        "Build distributable tools",
        "Separate modules, validate metadata, and expose a predictable CLI.",
    ),
    Chapter(
        "python-internals",
        "experienced",
        "Understand the machinery",
        "Use descriptors and class hooks, and inspect Python execution.",
    ),
)


def check(
    label,
    expression,
    expected,
    nudge="Compare the actual and expected results for this input.",
):
    return Check(label, expression, expected, nudge)


def unit(
    lesson_id,
    chapter,
    title,
    concept,
    solution,
    repair,
    checks,
    hints,
    *,
    project=False,
    files=None,
):
    solution_files = {name: code(source) for name, source in files[0].items()} if files else None
    repair_files = {name: code(source) for name, source in files[1].items()} if files else None
    return Lesson(
        lesson_id,
        "experienced",
        title,
        concept,
        35 if project else 20,
        (concept,),
        lesson_text(lesson_id),
        code(repair),
        tuple(checks),
        tuple(hints),
        "",
        (),
        0,
        "",
        code(solution),
        project=project,
        revision=4,
        chapter_id=chapter,
        files=tuple(solution_files) if solution_files else ("lesson.py",),
        solution_files=solution_files,
        repair_files=repair_files,
    )


def legacy(lesson_id, chapter, *, project=False):
    return replace(LEGACY[lesson_id], chapter_id=chapter, revision=4, project=project)


LESSONS = (
    unit(
        "python-expressions",
        "python-semantics",
        "Expressions with intent",
        "Python syntax & truthiness",
        """
        def display_name(value):
            if value is None:
                return "Anonymous"
            return value.strip() or "Anonymous"
        """,
        """
        def display_name(value):
            return str(value).strip()
        """,
        [
            check("Trim a name", "display_name('  Lin  ')", "Lin"),
            check("Missing value", "display_name(None)", "Anonymous"),
            check("Blank name", "display_name('   ')", "Anonymous"),
            check("Do not discard zero text", "display_name('0')", "0"),
        ],
        [
            "Handle None before calling a string method.",
            "An empty string is false in a condition; the string '0' is true.",
        ],
    ),
    legacy("objects-not-boxes", "python-semantics"),
    unit(
        "call-contracts",
        "python-semantics",
        "Make call sites readable",
        "Positional & keyword arguments",
        """
        def quote(price, quantity=1, *, discount=0):
            if price < 0 or quantity < 0 or not 0 <= discount <= 1:
                raise ValueError("Invalid quote")
            return round(price * quantity * (1 - discount), 2)
        """,
        """
        def quote(price, quantity=1, *, discount=0):
            return round(price * quantity - discount, 2)
        """,
        [
            check("Defaults", "quote(12.5)", 12.5),
            check("Percentage discount", "quote(10, 3, discount=0.2)", 24.0),
            check("Free quote", "quote(9, 0)", 0),
            check("Reject negative price", "__raises_value_error__(quote, -1)", True),
            check(
                "Invalid discount",
                "__raises_value_error__(lambda _: quote(3, discount=2), None)",
                True,
            ),
        ],
        [
            "The discount is a fraction of the subtotal, not a fixed amount.",
            "Validate before calculating; round the final amount to two places.",
        ],
    ),
    unit(
        "collection-idioms",
        "python-semantics",
        "Group without losing order",
        "Dictionaries, sets & comprehensions",
        """
        def group_names(pairs):
            groups = {}
            for group, name in pairs:
                names = groups.setdefault(group, [])
                if name not in names:
                    names.append(name)
            return groups
        """,
        """
        def group_names(pairs):
            return {group: [name] for group, name in pairs}
        """,
        [
            check(
                "Group and deduplicate",
                "group_names([('ops', 'Ada'), ('dev', 'Lin'), ('ops', 'Bo'), ('ops', 'Ada')])",
                {"ops": ["Ada", "Bo"], "dev": ["Lin"]},
            ),
            check(
                "One-pass iterable",
                "group_names(iter([('x', 'a'), ('x', 'b')]))",
                {"x": ["a", "b"]},
            ),
            check("Empty input", "group_names([])", {}),
        ],
        [
            "Create a separate list for each key, then append new names.",
            "setdefault(key, []) returns the existing list or inserts a new one.",
        ],
    ),
    unit(
        "index-records",
        "python-semantics",
        "Project: a record index",
        "Record indexing project",
        """
        from copy import deepcopy

        def index_records(records):
            result = {}
            for record in records:
                key = record["id"]
                if key in result:
                    raise ValueError("Duplicate id")
                result[key] = deepcopy(record)
            return result
        """,
        """
        def index_records(records):
            return {record["id"]: record for record in records}
        """,
        [
            check(
                "Index records",
                "index_records([{'id': 'a', 'tags': ['cli']}, {'id': 'b', 'tags': []}])",
                {"a": {"id": "a", "tags": ["cli"]}, "b": {"id": "b", "tags": []}},
            ),
            check(
                "Nested copy is independent",
                "(lambda r: index_records([r])['a']['tags'] is r['tags'])({'id':'a','tags':[]})",
                False,
            ),
            check(
                "Reject duplicate ids",
                "__raises_value_error__(index_records, [{'id':'a'}, {'id':'a'}])",
                True,
            ),
            check("Empty iterator", "index_records(iter([]))", {}),
        ],
        [
            "Build the index incrementally so you can detect duplicates.",
            "Copy the whole record deeply after validating its identifier.",
        ],
        project=True,
    ),
    unit(
        "callable-tools",
        "python-composition",
        "Callable tools and sorting",
        "Callables, lambdas & partial",
        """
        from functools import partial

        def rank(records, key):
            return sorted(records, key=key)

        def make_scaler(factor):
            return partial(lambda value, factor: value * factor, factor=factor)
        """,
        """
        def rank(records, key):
            return sorted(records)

        def make_scaler(factor):
            return lambda value: value + factor
        """,
        [
            check("Custom key", "rank(['pear', 'fig', 'apple'], len)", ["fig", "pear", "apple"]),
            check("Stable equal keys", "rank(['bb', 'aa', 'z'], len)", ["z", "bb", "aa"]),
            check("One-pass records", "rank(iter([3, 1, 2]), lambda value: -value)", [3, 2, 1]),
            check("Empty records", "rank([], len)", []),
            check(
                "Reusable bound argument",
                "(lambda scale: [scale(2), scale(-3), scale(0)])(make_scaler(4))",
                [8, -12, 0],
            ),
            check(
                "Keep caller list",
                (
                    "(exec('values = [3, 1]\\nrank(values, lambda x: x)\\nresult = "
                    "values', globals()), result)[1]"
                ),
                [3, 1],
            ),
        ],
        [
            (
                "Pass the supplied key callable to sorted; sorted returns a n"
                "ew list and preserves equal-key order."
            ),
            (
                "Bind factor with a closure or functools.partial so each late"
                "r call multiplies its own value."
            ),
        ],
    ),
    unit(
        "functional-pipelines",
        "python-composition",
        "Map, filter, and folds",
        "Map, filter & reduce",
        """
        from functools import reduce

        def transform_selected(items, predicate, transform):
            return list(map(transform, filter(predicate, items)))

        def fold(items, combine, initial):
            return reduce(combine, items, initial)
        """,
        """
        def transform_selected(items, predicate, transform):
            return [transform(item) for item in items]

        def fold(items, combine, initial):
            for item in items:
                initial = combine(item, initial)
            return initial
        """,
        [
            check(
                "Select before transform",
                "transform_selected([-2, 0, 3], lambda x: x > 0, lambda x: x * 10)",
                [30],
            ),
            check(
                "One-pass transformation",
                "transform_selected(iter([1, 2, 3]), lambda x: x % 2, str)",
                ["1", "3"],
            ),
            check("Empty pipeline", "transform_selected([], bool, str)", []),
            check(
                "Transform only selected values",
                "transform_selected([0, 2], bool, lambda value: 10 / value)",
                [5.0],
            ),
            check("Left fold order", "fold([2, 3], lambda total, x: total - x, 10)", 5),
            check(
                "Generic accumulator",
                "fold(iter(['a', 'b']), lambda acc, x: acc + [x.upper()], [])",
                ["A", "B"],
            ),
            check("Empty fold keeps initial", "fold([], lambda a, b: None, 'seed')", "seed"),
        ],
        [
            (
                "Filter original values before applying the transform; reject"
                "ed values must never reach it."
            ),
            (
                "Start with initial and call combine(accumulator, item) in in"
                "put order, including for nonnumeric accumulators."
            ),
        ],
    ),
    legacy("functions-with-memory", "python-composition"),
    unit(
        "decorator-factories",
        "python-composition",
        "Configure and stack decorators",
        "Decorator factories & stacking",
        """
        from functools import wraps

        def prefixed(prefix):
            def decorate(function):
                @wraps(function)
                def wrapper(*args, **kwargs):
                    return prefix + function(*args, **kwargs)
                return wrapper
            return decorate
        """,
        """
        def prefixed(prefix):
            def decorate(function):
                def wrapper(value):
                    return function(value) + prefix
                return wrapper
            return decorate
        """,
        [
            check("Factory configuration", "prefixed('Hi: ')(lambda name: name)('Lin')", "Hi: Lin"),
            check(
                "Forward keyword arguments",
                "prefixed('>')(lambda *, name: name)(name='Ada')",
                ">Ada",
            ),
            check("Stack order", "prefixed('A')(prefixed('B')(lambda: 'C'))()", "ABC"),
            check(
                "Preserve function identity metadata",
                (
                    "(exec(\"def greet():\\n    'Greeting documentation.'\\n    retu"
                    "rn 'hello'\\nwrapped = prefixed('!')(greet)\\nresult = [wrappe"
                    'd.__name__, wrapped.__doc__, wrapped.__wrapped__ is greet]",'
                    " globals()), result)[1]"
                ),
                ["greet", "Greeting documentation.", True],
            ),
            check(
                "Evaluate each call",
                (
                    '(exec("calls = []\\ndef greet(value):\\n    calls.append(value'
                    ")\\n    return str(value)\\nf = prefixed('!')(greet)\\nresult ="
                    ' [f(1), f(2), calls]", globals()), result)[1]'
                ),
                ["!1", "!2", [1, 2]],
            ),
        ],
        [
            "Use three nested layers: configuration, original function, then invocation arguments.",
            (
                "Forward *args and **kwargs, prepend after calling, and use w"
                "raps to preserve metadata and __wrapped__."
            ),
        ],
    ),
    legacy("lazy-by-design", "python-composition"),
    unit(
        "exception-boundaries",
        "python-composition",
        "Exceptions with context",
        "Custom exceptions & chaining",
        """
        class RecordError(ValueError):
            pass

        def parse_record(text):
            try:
                return int(text)
            except ValueError as error:
                raise RecordError("Invalid integer record") from error

        def read_record(stream):
            try:
                return parse_record(stream.read())
            finally:
                stream.close()
        """,
        """
        class RecordError(ValueError):
            pass

        def parse_record(text):
            return int(text)

        def read_record(stream):
            result = parse_record(stream.read())
            stream.close()
            return result
        """,
        [
            check("Parse signed integer", "parse_record(' -12 ')", -12),
            check(
                "Custom error retains cause",
                (
                    "(exec(\"try:\\n    parse_record('bad')\\nexcept RecordError as "
                    'error:\\n    result = type(error.__cause__) is ValueError", g'
                    "lobals()), result)[1]"
                ),
                True,
            ),
            check(
                "Close on success",
                (
                    "(exec(\"from io import StringIO\\ns = StringIO('5')\\nvalue = r"
                    'ead_record(s)\\nresult = [value, s.closed]", globals()), resu'
                    "lt)[1]"
                ),
                [5, True],
            ),
            check(
                "Close on invalid record",
                (
                    "(exec(\"from io import StringIO\\ns = StringIO('x')\\ntry:\\n   "
                    ' read_record(s)\\nexcept RecordError:\\n    result = s.closed"'
                    ", globals()), result)[1]"
                ),
                True,
            ),
            check(
                "Preserve read errors and close",
                (
                    '(exec("class Broken:\\n    closed = False\\n    def read(self)'
                    ":\\n        raise OSError('disk')\\n    def close(self):\\n    "
                    "    self.closed = True\\ns = Broken()\\ntry:\\n    read_record("
                    "s)\\nexcept OSError as error:\\n    result = [str(error), s.cl"
                    'osed]", globals()), result)[1]'
                ),
                ["disk", True],
            ),
        ],
        [
            (
                "Catch ValueError around int conversion and raise RecordError"
                " from the caught exception."
            ),
            (
                "Read once in try and close once in finally so conversion and"
                " reading failures both clean up."
            ),
        ],
    ),
    unit(
        "context-practice",
        "python-composition",
        "Restore temporary state",
        "Exception-safe context managers",
        """
        from contextlib import contextmanager

        @contextmanager
        def temporary_value(mapping, key, value):
            existed = key in mapping
            previous = mapping.get(key)
            mapping[key] = value
            try:
                yield mapping
            finally:
                if existed:
                    mapping[key] = previous
                else:
                    del mapping[key]
        """,
        """
        from contextlib import contextmanager

        @contextmanager
        def temporary_value(mapping, key, value):
            previous = mapping.get(key)
            mapping[key] = value
            yield mapping
            mapping[key] = previous
        """,
        [
            check(
                "Restore after normal exit",
                (
                    "(lambda m: (exec(\"with temporary_value(m, 'x', 9):\\n    assert m["
                    "'x'] == 9\", globals(), {'m': m}), m)[1])({'x':1})"
                ),
                {"x": 1},
            ),
            check(
                "Remove a temporary key",
                (
                    "(lambda m: (exec(\"with temporary_value(m, 'x', 9):\\n    assert m["
                    "'x'] == 9\", globals(), {'m': m}), m)[1])({})"
                ),
                {},
            ),
            check(
                "Restore on exception",
                (
                    "(lambda m: (exec(\"try:\\n    with temporary_value(m, 'x', 9):\\n  "
                    "      raise ValueError('stop')\\nexcept ValueError:\\n    pass\", g"
                    "lobals(), {'m': m}), m)[1])({'x':None})"
                ),
                {"x": None},
            ),
        ],
        [
            "Remember whether the key existed separately from its previous value.",
            "Put restoration inside finally so exceptions cannot skip it.",
        ],
    ),
    unit(
        "managed-contexts",
        "python-composition",
        "Implement the context protocol",
        "Class-based context managers",
        """
        class Closing:
            def __init__(self, resource):
                self.resource = resource
            def __enter__(self):
                return self.resource
            def __exit__(self, exc_type, exc_value, traceback):
                self.resource.close()
                return False

        class IgnoreValueError:
            def __enter__(self):
                return self
            def __exit__(self, exc_type, exc_value, traceback):
                return exc_type is not None and issubclass(exc_type, ValueError)
        """,
        """
        class Closing:
            def __init__(self, resource):
                self.resource = resource
            def __enter__(self):
                return self
            def __exit__(self, exc_type, exc_value, traceback):
                return True

        class IgnoreValueError:
            def __enter__(self):
                return self
            def __exit__(self, exc_type, exc_value, traceback):
                return True
        """,
        [
            check(
                "Return and close resource",
                (
                    "(exec(\"from io import StringIO\\ns = StringIO('hello')\\nwith "
                    "Closing(s) as value:\\n    same = value is s\\n    text = valu"
                    'e.read()\\nresult = [same, text, s.closed]", globals()), resu'
                    "lt)[1]"
                ),
                [True, "hello", True],
            ),
            check(
                "Close and propagate failure",
                (
                    "(exec(\"from io import StringIO\\ns = StringIO('')\\ntry:\\n    "
                    "with Closing(s):\\n        raise RuntimeError('boom')\\nexcept"
                    " RuntimeError as error:\\n    result = [str(error), s.closed]"
                    '", globals()), result)[1]'
                ),
                ["boom", True],
            ),
            check(
                "Suppress value subclasses",
                (
                    '(exec("class Specific(ValueError):\\n    pass\\nwith IgnoreVal'
                    "ueError():\\n    raise Specific('bad')\\nresult = True\", globa"
                    "ls()), result)[1]"
                ),
                True,
            ),
            check(
                "Propagate unrelated failures",
                (
                    '(exec("result = False\\ntry:\\n    with IgnoreValueError():\\n '
                    "       raise TypeError('wrong')\\nexcept TypeError:\\n    resu"
                    'lt = True", globals()), result)[1]'
                ),
                True,
            ),
            check(
                "Normal context exit",
                "(exec('with IgnoreValueError():\\n    result = 3', globals()), result)[1]",
                3,
            ),
        ],
        [
            "Store resource in __init__, return it from __enter__, and close it once in __exit__.",
            (
                "Only suppress when exc_type is not None and is a subclass of"
                " ValueError; Closing suppresses nothing."
            ),
        ],
    ),
    unit(
        "iterator-tools",
        "python-composition",
        "Consume only what you need",
        "Iterator composition",
        """
        def batches(items, size):
            if size <= 0:
                raise ValueError("Size must be positive")
            batch = []
            for item in items:
                batch.append(item)
                if len(batch) == size:
                    yield batch
                    batch = []
            if batch:
                yield batch
        """,
        """
        def batches(items, size):
            batch = []
            for item in items:
                batch.append(item)
                if len(batch) == size:
                    yield batch
                    batch = []
        """,
        [
            check("Keep final partial batch", "list(batches(range(5), 2))", [[0, 1], [2, 3], [4]]),
            check("Empty input", "list(batches([], 3))", []),
            check(
                "Remain lazy",
                (
                    "list(__import__('itertools').islice(batches(__import__('itertools')."
                    "count(), 2), 2))"
                ),
                [[0, 1], [2, 3]],
            ),
            check(
                "Reject zero size",
                "__raises_value_error__(lambda size: list(batches([], size)), 0)",
                True,
            ),
        ],
        [
            "Yield a new list for each batch; do not clear a list already yielded.",
            "After the loop, yield a nonempty partial batch. Validate the size first.",
        ],
    ),
    unit(
        "iterator-recipes",
        "python-composition",
        "Combine and bound iterators",
        "Chain, islice, zip_longest & product",
        """
        from itertools import chain, islice, zip_longest, product

        def preview(groups, limit):
            if limit < 0:
                raise ValueError("Negative limit")
            return list(islice(chain.from_iterable(groups), limit))

        def align(left, right):
            return list(zip_longest(left, right, fillvalue=None))

        def combinations(left, right):
            return list(product(left, right))
        """,
        """
        def preview(groups, limit):
            return [value for group in groups for value in group][:limit]

        def align(left, right):
            return list(zip(left, right))

        def combinations(left, right):
            return list(zip(left, right))
        """,
        [
            check("Flatten bounded preview", "preview([[1, 2], [], [3, 4]], 3)", [1, 2, 3]),
            check(
                "Do not read extra input items",
                (
                    "(exec('source = iter([1, 2, 3])\\nvalues = preview([source], "
                    "2)\\nresult = [values, next(source)]', globals()), result)[1]"
                ),
                [[1, 2], 3],
            ),
            check(
                "Zero consumes nothing",
                (
                    "(exec('source = iter([7])\\nvalues = preview([source], 0)\\nre"
                    "sult = [values, next(source)]', globals()), result)[1]"
                ),
                [[], 7],
            ),
            check("Negative limit", "__raises_value_error__(lambda n: preview([], n), -1)", True),
            check(
                "Pad either side",
                "(align([1], [2, 3]), align([1, 2], []))",
                [[[1, 2], [None, 3]], [[1, None], [2, None]]],
            ),
            check(
                "All pairs",
                "combinations(iter('ab'), iter([1, 2]))",
                [["a", 1], ["a", 2], ["b", 1], ["b", 2]],
            ),
            check("Empty combinations", "combinations([], [1])", []),
        ],
        [
            (
                "Combine chain.from_iterable with islice to avoid exhausting "
                "input during a bounded preview."
            ),
            (
                "Use zip_longest for padded alignment and product for every p"
                "air; ordinary zip does neither."
            ),
        ],
    ),
    unit(
        "adjacent-groups",
        "python-composition",
        "Group consecutive values",
        "Consecutive grouping with itertools",
        """
        from itertools import groupby

        def runs(items, key):
            for label, group in groupby(items, key=key):
                yield label, list(group)
        """,
        """
        def runs(items, key):
            groups = {}
            for item in items:
                groups.setdefault(key(item), []).append(item)
            return iter(groups.items())
        """,
        [
            check(
                "Keep separate runs",
                "list(runs('aabba', lambda x: x))",
                [["a", ["a", "a"]], ["b", ["b", "b"]], ["a", ["a"]]],
            ),
            check(
                "Apply key",
                "list(runs(iter(['Ada', 'Al', 'Bo']), lambda name: name[0]))",
                [["A", ["Ada", "Al"]], ["B", ["Bo"]]],
            ),
            check("Empty runs", "list(runs([], str))", []),
            check(
                "Return an iterator",
                "(lambda grouped: iter(grouped) is grouped)(runs('a', str))",
                True,
            ),
            check(
                "Unhashable labels",
                "list(runs([1, 1, 2], lambda x: [x]))",
                [[[1], [1, 1]], [[2], [2]]],
            ),
            check(
                "Groups remain usable",
                (
                    "(exec(\"groups = list(runs('aba', str))\\nresult = [list(group"
                    ') for label, group in groups]", globals()), result)[1]'
                ),
                [["a"], ["b"], ["a"]],
            ),
        ],
        [
            "groupby compares adjacent keys without sorting or requiring dictionary keys.",
            (
                "Copy each group into its own list before advancing the outer"
                " iterator, and yield the label and list."
            ),
        ],
    ),
    unit(
        "stream-report",
        "python-composition",
        "Project: a streaming report",
        "Lazy pipeline project",
        """
        def running_totals(lines):
            total = 0
            for line in lines:
                text = line.strip()
                if not text or text.startswith("#"):
                    continue
                total += int(text)
                yield total
        """,
        """
        def running_totals(lines):
            total = 0
            for line in lines:
                total += int(line)
                yield total
        """,
        [
            check(
                "Ignore comments and blanks",
                "list(running_totals([' 3 ', '# adjustment', '', '-1', '5']))",
                [3, 2, 7],
            ),
            check(
                "Consume incrementally",
                (
                    "list(__import__('itertools').islice(running_totals(__import__('itert"
                    "ools').repeat('2')), 3))"
                ),
                [2, 4, 6],
            ),
            check(
                "Reject malformed numbers",
                "__raises_value_error__(lambda x: list(running_totals(x)), ['oops'])",
                True,
            ),
            check("Empty stream", "list(running_totals([]))", []),
        ],
        [
            (
                "Separate filtering from integer conversion; invalid non-comment lines sh"
                "ould still raise."
            ),
            "Keep a running total and yield after each accepted number.",
        ],
        project=True,
    ),
    legacy("ready-to-ship", "python-design"),
    unit(
        "data-models",
        "python-design",
        "Model a small value object",
        "Classes & dataclasses",
        """
        from dataclasses import dataclass

        @dataclass(frozen=True)
        class Item:
            name: str
            quantity: int

            def restock(self, amount):
                if amount < 0:
                    raise ValueError("Amount must be nonnegative")
                return Item(self.name, self.quantity + amount)
        """,
        """
        from dataclasses import dataclass

        @dataclass
        class Item:
            name: str
            quantity: int

            def restock(self, amount):
                self.quantity += amount
                return self
        """,
        [
            check(
                "Restock a value",
                "(lambda item: (item.name, item.quantity))(Item('bolts', 2).restock(3))",
                ["bolts", 5],
            ),
            check(
                "Original is unchanged",
                "(lambda item: (item.restock(2), item.quantity)[1])(Item('nuts', 4))",
                4,
            ),
            check("Value equality", "Item('bolts', 2) == Item('bolts', 2)", True),
            check("Negative restock", "__raises_value_error__(Item('x', 1).restock, -1)", True),
        ],
        [
            "A dataclass can generate initialization and equality from annotated fields.",
            "Construct a new Item in restock rather than updating self.",
        ],
    ),
    unit(
        "dataclass-lifecycle",
        "python-design",
        "Dataclass defaults and updates",
        "Dataclass factories & post-init",
        """
        from dataclasses import dataclass, field, replace

        @dataclass
        class Batch:
            name: str
            tags: list[str] = field(default_factory=list)
            def __post_init__(self):
                self.name = self.name.strip()
                if not self.name:
                    raise ValueError("Empty name")
            def renamed(self, name):
                return replace(self, name=name, tags=self.tags.copy())
        """,
        """
        from dataclasses import dataclass, field

        @dataclass
        class Batch:
            name: str
            tags: list[str] = field(default_factory=list)
            def renamed(self, name):
                self.name = name
                return self
        """,
        [
            check("Normalize name", "Batch('  parts ').name", "parts"),
            check("Reject blank", "__raises_value_error__(Batch, '  ')", True),
            check(
                "Separate defaults",
                (
                    "(exec(\"a = Batch('a')\\nb = Batch('b')\\na.tags.append('hot')\\"
                    'nresult = b.tags", globals()), result)[1]'
                ),
                [],
            ),
            check(
                "Copy on rename",
                (
                    "(exec(\"a = Batch('old', ['x'])\\nb = a.renamed(' new ')\\nb.ta"
                    "gs.append('y')\\nresult = [a.name, a.tags, b.name, b.tags, a "
                    'is b]", globals()), result)[1]'
                ),
                ["old", ["x"], "new", ["x", "y"], False],
            ),
            check("Validate rename", "__raises_value_error__(Batch('old').renamed, '')", True),
            check("Dataclass values", "Batch('x', ['a']) == Batch('x', ['a'])", True),
        ],
        [
            (
                "Use field(default_factory=list) for independent defaults and"
                " __post_init__ to normalize and validate."
            ),
            "replace is shallow: provide a copy of tags when constructing the renamed batch.",
        ],
    ),
    unit(
        "typed-contracts",
        "python-design",
        "Unions and generic contracts",
        "Union types & TypeVar generics",
        """
        from collections.abc import Iterable
        from typing import TypeVar

        T = TypeVar("T")

        def first_or(items: Iterable[T], default: T) -> T:
            return next(iter(items), default)

        def parse_optional(text: str | None) -> int | None:
            if text is None or not text.strip():
                return None
            return int(text)
        """,
        """
        def first_or(items, default):
            return next(iter(items)) or default

        def parse_optional(text):
            return int(text or 0)
        """,
        [
            check("Keep an item that tests as false", "first_or(iter([0, 2]), 9)", 0),
            check("Keep generic value", "first_or([{'a': 1}], {})", {"a": 1}),
            check("Empty uses default", "first_or(iter([]), 'fallback')", "fallback"),
            check(
                "Consume one only",
                (
                    "(exec('source = iter([1, 2])\\nfirst_or(source, 0)\\nresult = "
                    "next(source)', globals()), result)[1]"
                ),
                2,
            ),
            check(
                "Missing optional values",
                "[parse_optional(None), parse_optional('  ')]",
                [None, None],
            ),
            check("Signed integer", "parse_optional(' -4 ')", -4),
            check("Reject invalid input", "__raises_value_error__(parse_optional, '1.5')", True),
        ],
        [
            (
                "next(iter(items), default) returns the first item even if it tests as false, "
                "or default if there are no items. It reads at most one item."
            ),
            (
                "Handle None and blank text before int conversion; TypeVar re"
                "lates the iterable element and return types."
            ),
        ],
    ),
    unit(
        "practical-object-protocols",
        "python-design",
        "Objects that fit Python",
        "Properties & special methods",
        """
        class Score:
            def __init__(self, points):
                self.points = points
            @property
            def points(self):
                return self._points
            @points.setter
            def points(self, value):
                if value < 0:
                    raise ValueError("Negative points")
                self._points = value
            def __repr__(self):
                return f"Score({self.points})"
            def __len__(self):
                return self.points
            def __eq__(self, other):
                if not isinstance(other, Score):
                    return NotImplemented
                return self.points == other.points
            def __add__(self, other):
                if not isinstance(other, Score):
                    return NotImplemented
                return Score(self.points + other.points)
        """,
        """
        class Score:
            def __init__(self, points):
                self.points = points
            def __repr__(self):
                return str(self.points)
            def __len__(self):
                return self.points
            def __eq__(self, other):
                return True
            def __add__(self, other):
                self.points += other.points
                return self
        """,
        [
            check("Readable representation", "repr(Score(3))", "Score(3)"),
            check(
                "Length and equality",
                "[len(Score(0)), Score(2) == Score(2), Score(2) == Score(3), Score(2) == 2]",
                [0, True, False, False],
            ),
            check(
                "Independent sum",
                (
                    "(exec('a = Score(2)\\nb = Score(3)\\nc = a + b\\nresult = [a.po"
                    "ints, b.points, c.points, c is a, c is b]', globals()), resu"
                    "lt)[1]"
                ),
                [2, 3, 5, False, False],
            ),
            check("Reject negative creation", "__raises_value_error__(Score, -1)", True),
            check(
                "Reject assignment without mutation",
                (
                    "(exec('s = Score(4)\\ntry:\\n    s.points = -1\\nexcept ValueEr"
                    "ror:\\n    result = s.points', globals()), result)[1]"
                ),
                4,
            ),
            check(
                "Accept assignment",
                "(exec('s = Score(1)\\ns.points = 0\\nresult = s.points', globals()), result)[1]",
                0,
            ),
            check(
                "Unsupported addition",
                (
                    "(exec('try:\\n    Score(2) + 2\\nexcept TypeError:\\n    result"
                    " = True', globals()), result)[1]"
                ),
                True,
            ),
        ],
        [
            (
                "Validate before updating the backing attribute in the proper"
                "ty setter to preserve rejected updates."
            ),
            (
                "Return a new Score when adding and NotImplemented for unsupp"
                "orted operand types; compare point values."
            ),
        ],
    ),
    unit(
        "class-construction",
        "python-design",
        "Factories and abstract interfaces",
        "Class methods, static methods & ABCs",
        """
        from abc import ABC, abstractmethod

        class Renderer(ABC):
            @abstractmethod
            def render(self, text):
                pass

        class PrefixRenderer(Renderer):
            def __init__(self, prefix):
                self.prefix = prefix
            @staticmethod
            def valid_prefix(value):
                return bool(value.strip())
            @classmethod
            def from_text(cls, text):
                prefix = text.strip()
                if not cls.valid_prefix(prefix):
                    raise ValueError("Empty prefix")
                return cls(prefix)
            def render(self, text):
                return self.prefix + text
        """,
        """
        class Renderer:
            def render(self, text):
                pass

        class PrefixRenderer(Renderer):
            def __init__(self, prefix):
                self.prefix = prefix
            @staticmethod
            def valid_prefix(value):
                return bool(value)
            @classmethod
            def from_text(cls, text):
                return PrefixRenderer(text)
            def render(self, text):
                return text + self.prefix
        """,
        [
            check(
                "Factory normalization", "PrefixRenderer.from_text(' > ').render('hello')", ">hello"
            ),
            check(
                "Validation helper",
                '[PrefixRenderer.valid_prefix(" "), PrefixRenderer.valid_prefix("!")]',
                [False, True],
            ),
            check(
                "Reject blank factory",
                "__raises_value_error__(PrefixRenderer.from_text, ' ')",
                True,
            ),
            check(
                "Subclass factory",
                (
                    '(exec("class Special(PrefixRenderer):\\n    pass\\nobj = Speci'
                    "al.from_text(' ! ')\\nresult = [type(obj) is Special, obj.ren"
                    "der('ok')]\", globals()), result)[1]"
                ),
                [True, "!ok"],
            ),
            check(
                "Abstract base cannot instantiate",
                (
                    "(exec('try:\\n    Renderer()\\nexcept TypeError:\\n    result ="
                    " True', globals()), result)[1]"
                ),
                True,
            ),
            check(
                "Incomplete subclass cannot instantiate",
                (
                    "(exec('class Incomplete(Renderer):\\n    pass\\ntry:\\n    Inco"
                    "mplete()\\nexcept TypeError:\\n    result = True', globals()),"
                    " result)[1]"
                ),
                True,
            ),
        ],
        [
            "Inherit from ABC and mark render with abstractmethod to prevent incomplete instances.",
            (
                "The classmethod factory must construct cls, not a fixed "
                "class, after trimming and validating text."
            ),
        ],
    ),
    unit(
        "structural-typing",
        "python-design",
        "Program to a small protocol",
        "Structural typing & protocols",
        """
        from typing import Protocol

        class Writer(Protocol):
            def write(self, text: str) -> object: ...

        def emit_lines(writer: Writer, lines):
            count = 0
            for line in lines:
                writer.write(line + "\\n")
                count += 1
            return count
        """,
        """
        from typing import Protocol

        class Writer(Protocol):
            def write(self, text: str) -> object: ...

        def emit_lines(writer: Writer, lines):
            for line in lines:
                writer.write(line)
            return 0
        """,
        [
            check(
                "StringIO writer",
                (
                    "(lambda w: (emit_lines(w, ['a', 'b']), w.getvalue()))(__import__('io"
                    "').StringIO())"
                ),
                [2, "a\nb\n"],
            ),
            check(
                "An unrelated writer",
                (
                    "(lambda events: (emit_lines(type('Sink', (), {'write': lambda self, "
                    "text: events.append(text)})(), iter(['x'])), events))([])"
                ),
                [1, ["x\n"]],
            ),
            check("Empty input", "emit_lines(__import__('io').StringIO(), [])", 0),
        ],
        [
            "Use the write method promised by the protocol without inspecting the concrete class.",
            (
                "Count input lines, not the return value of write; different writers may "
                "return different values."
            ),
        ],
    ),
    unit(
        "test-doubles",
        "python-design",
        "Inject effects for reliable tests",
        "Dependency injection & mocking",
        """
        def retry(operation, attempts, pause):
            if attempts < 1:
                raise ValueError("Attempts must be positive")
            for attempt in range(attempts):
                try:
                    return operation()
                except ValueError:
                    if attempt == attempts - 1:
                        raise
                    pause()
        """,
        """
        def retry(operation, attempts, pause):
            for attempt in range(attempts):
                try:
                    return operation()
                except ValueError:
                    pause()
            return None
        """,
        [
            check(
                "Recover and pause once",
                (
                    "(lambda op, pause: (retry(op, 3, pause), op.call_count, pause.call_c"
                    "ount))(__import__('unittest.mock', fromlist=['Mock']).Mock(side_effe"
                    "ct=[ValueError('busy'), 7]), __import__('unittest.mock', fromlist=['"
                    "Mock']).Mock())"
                ),
                [7, 2, 1],
            ),
            check(
                "Final failure is raised",
                (
                    "__raises_value_error__(lambda _: retry(lambda: int('bad'), 2, lambda"
                    ": None), None)"
                ),
                True,
            ),
            check(
                "No final pause",
                (
                    "(lambda pause: (__raises_value_error__(lambda _: retry(lambda: int('"
                    "bad'), 2, pause), None), pause.call_count))(__import__('unittest.moc"
                    "k', fromlist=['Mock']).Mock())"
                ),
                [True, 1],
            ),
            check(
                "No attempts is invalid",
                "__raises_value_error__(lambda _: retry(lambda: 1, 0, lambda: None), None)",
                True,
            ),
        ],
        [
            "Only retry ValueError; let other exception types propagate.",
            (
                "Pause only when another attempt remains; a bare raise re-raises the curr"
                "ent exception."
            ),
        ],
    ),
    unit(
        "typed-inventory",
        "python-design",
        "Project: an inventory library",
        "Typed multi-file project",
        "from inventory import total_value\n",
        "from inventory import total_value\n",
        [
            check(
                "Inventory valuation",
                "total_value([{'quantity': 3, 'price': 2.5}, {'quantity': 2, 'price': 4.0}])",
                15.5,
            ),
            check("Empty stock", "total_value(iter([]))", 0),
            check(
                "Reject negative quantity",
                "__raises_value_error__(total_value, [{'quantity': -1, 'price': 2}])",
                True,
            ),
            check(
                "Reject negative price",
                "__raises_value_error__(total_value, [{'quantity': 1, 'price': -2}])",
                True,
            ),
        ],
        [
            "Keep the public calculation in inventory.py, then import it in lesson.py.",
            "Validate each row before adding quantity times price to the total.",
        ],
        project=True,
        files=(
            {
                "lesson.py": "from inventory import total_value\n",
                "inventory.py": """
            from typing import Iterable, TypedDict

            class Stock(TypedDict):
                quantity: int
                price: float

            def total_value(rows: Iterable[Stock]) -> float:
                total = 0.0
                for row in rows:
                    if row["quantity"] < 0 or row["price"] < 0:
                        raise ValueError("Stock values must be nonnegative")
                    total += row["quantity"] * row["price"]
                return total
            """,
            },
            {
                "lesson.py": "from inventory import total_value\n",
                "inventory.py": """
            def total_value(rows):
                return sum(row["quantity"] + row["price"] for row in rows)
            """,
            },
        ),
    ),
    unit(
        "coroutine-basics",
        "python-concurrency",
        "Await cooperative work",
        "Coroutines & event loops",
        """
        import asyncio

        async def delayed_total(values):
            total = 0
            for value in values:
                await asyncio.sleep(0)
                total += value
            return total
        """,
        """
        import asyncio

        async def delayed_total(values):
            return sum(values) + 1
        """,
        [
            check("Await a result", "__import__('asyncio').run(delayed_total([2, -1, 4]))", 5),
            check("Empty input", "__import__('asyncio').run(delayed_total([]))", 0),
            check("One-pass input", "__import__('asyncio').run(delayed_total(iter([3, 2])))", 5),
        ],
        [
            "Use async def for the coroutine; calling it alone does not produce the final value.",
            "Await asyncio.sleep(0) in each iteration to offer other tasks a turn.",
        ],
    ),
    legacy("clean-exits", "python-concurrency"),
    unit(
        "task-groups",
        "python-concurrency",
        "Give tasks a shared lifetime",
        "Task groups & cancellation",
        """
        import asyncio

        async def collect_jobs(jobs):
            async with asyncio.TaskGroup() as group:
                tasks = [group.create_task(job()) for job in jobs]
            return [task.result() for task in tasks]
        """,
        """
        import asyncio

        async def collect_jobs(jobs):
            results = []
            for job in jobs:
                results.append(await job())
            return list(reversed(results))
        """,
        [
            check(
                "Preserve input order",
                (
                    "__import__('asyncio').run(collect_jobs([lambda: __import__('asyncio'"
                    ").sleep(0, result=3), lambda: __import__('asyncio').sleep(0, result="
                    "1)]))"
                ),
                [3, 1],
            ),
            check("Empty group", "__import__('asyncio').run(collect_jobs([]))", []),
            check(
                "Group failures",
                (
                    "(lambda: exec(\"async def broken():\\n    raise ValueError('job')\\"
                    "ntry:\\n    __import__('asyncio').run(collect_jobs([broken]))\\nexce"
                    "pt ExceptionGroup as errors:\\n    assert any(isinstance(e, ValueErr"
                    "or) for e in errors.exceptions)\\nelse:\\n    raise AssertionError('"
                    "failure was hidden')\", globals()))()"
                ),
                None,
            ),
        ],
        [
            (
                "Call each job factory once, schedule its coroutine, and keep the task li"
                "st in input order."
            ),
            "TaskGroup waits on exit and groups failures. Read results only after successful exit.",
        ],
    ),
    unit(
        "async-streams",
        "python-concurrency",
        "Consume an async stream",
        "Async iteration",
        """
        async def collect_nonempty(source):
            result = []
            async for text in source:
                cleaned = text.strip()
                if cleaned:
                    result.append(cleaned)
            return result
        """,
        """
        async def collect_nonempty(source):
            result = []
            async for text in source:
                result.append(text)
            return result
        """,
        [
            check(
                "Trim and filter",
                (
                    "(lambda: (exec(\"async def source():\\n    for text in [' a ', ''"
                    ", '  ', 'b']:\\n        yield text\", globals()), __import__('as"
                    "yncio').run(collect_nonempty(source())))[1])()"
                ),
                ["a", "b"],
            ),
            check(
                "Empty stream",
                (
                    '(lambda: (exec("async def source():\\n    for text in []:\\n        '
                    "yield text\", globals()), __import__('asyncio').run(collect_nonempt"
                    "y(source())))[1])()"
                ),
                [],
            ),
        ],
        [
            "An async iterable is consumed with async for inside an async function.",
            "Strip each string once and append only nonempty results.",
        ],
    ),
    unit(
        "concurrent-batch",
        "python-concurrency",
        "Project: bounded async work",
        "Bounded concurrency project",
        """
        import asyncio

        async def run_limited(values, worker, limit):
            if limit < 1:
                raise ValueError("Limit must be positive")
            semaphore = asyncio.Semaphore(limit)

            async def run_one(value):
                async with semaphore:
                    return await worker(value)

            async with asyncio.TaskGroup() as group:
                tasks = [group.create_task(run_one(value)) for value in values]
            return [task.result() for task in tasks]
        """,
        """
        import asyncio

        async def run_limited(values, worker, limit):
            return await asyncio.gather(*(worker(value) for value in values))
        """,
        [
            check(
                "Ordered results",
                (
                    "__import__('asyncio').run(run_limited([3, 1, 2], lambda n: __import_"
                    "_('asyncio').sleep(0, result=n * 2), 2))"
                ),
                [6, 2, 4],
            ),
            check(
                "Concurrency respects the bound",
                (
                    '(lambda: (exec("async def probe():\\n    active = peak = 0\\n    asy'
                    "nc def worker(value):\\n        nonlocal active, peak\\n        acti"
                    "ve += 1\\n        peak = max(peak, active)\\n        await __import_"
                    "_('asyncio').sleep(0.001)\\n        active -= 1\\n        return val"
                    "ue\\n    result = await run_limited(range(5), worker, 2)\\n    retur"
                    "n [result, peak]\", globals()), __import__('asyncio').run(probe()))"
                    "[1])()"
                ),
                [[0, 1, 2, 3, 4], 2],
            ),
            check(
                "Zero limit is invalid",
                (
                    "__raises_value_error__(lambda _: __import__('asyncio').run(run_limit"
                    "ed([], lambda n: None, 0)), None)"
                ),
                True,
            ),
            check(
                "Empty batch", "__import__('asyncio').run(run_limited([], lambda n: None, 2))", []
            ),
        ],
        [
            (
                "A semaphore limits how many tasks are inside the protected section, not "
                "how many are created."
            ),
            (
                "Acquire the semaphore with async with around the awaited worker call; Ta"
                "skGroup handles sibling cleanup."
            ),
        ],
        project=True,
    ),
    unit(
        "module-boundaries",
        "python-delivery",
        "Keep imports predictable",
        "Modules & import boundaries",
        "from tools import normalize\n",
        "from tools import normalize\n",
        [
            check("Normalize a label", "normalize('  LOW   Disk  ')", "low-disk"),
            check("Blank label", "normalize('  ')", ""),
            check(
                "Import stays quiet",
                (
                    '(lambda output: (exec("import importlib\\nfrom contextlib import red'
                    "irect_stdout\\nwith redirect_stdout(output):\\n    importlib.reload("
                    "__import__('tools'))\", globals(), {'output': output}), output.ge"
                    "tvalue())[1])(__import__('io').StringIO())"
                ),
                "",
            ),
        ],
        [
            "Put reusable logic in tools.py and import it into lesson.py.",
            "Keep demonstration printing inside an if __name__ == '__main__' guard.",
        ],
        files=(
            {
                "lesson.py": "from tools import normalize\n",
                "tools.py": "def normalize(text):\n    return '-'.join(text.lower().split())\n",
            },
            {
                "lesson.py": "from tools import normalize\n",
                ("tools.py"): (
                    "print('loading tools')\ndef normalize(text):\n    return text.lower("
                    ").replace(' ', '-')\n"
                ),
            },
        ),
    ),
    unit(
        "package-metadata",
        "python-delivery",
        "Understand package metadata",
        "Virtual environments & packaging",
        """
        import tomllib

        def package_summary(text):
            project = tomllib.loads(text)["project"]
            return {
                "name": project["name"],
                "version": project["version"],
                "dependencies": sorted(project.get("dependencies", [])),
            }
        """,
        """
        import tomllib

        def package_summary(text):
            project = tomllib.loads(text)["project"]
            return {
                "name": project["name"],
                "version": project["version"],
                "dependencies": project["dependencies"],
            }
        """,
        [
            check(
                "Read and sort metadata",
                (
                    'package_summary(\'[project]\\nname = "weather-tool"\\nversion = "1.2'
                    '.0"\\ndependencies = ["zeta>=2", "alpha==1"]\')'
                ),
                {
                    "name": "weather-tool",
                    "version": "1.2.0",
                    "dependencies": ["alpha==1", "zeta>=2"],
                },
            ),
            check(
                "No dependencies",
                'package_summary(\'[project]\\nname = "local-tool"\\nversion = "0.1.0"\')',
                {"name": "local-tool", "version": "0.1.0", "dependencies": []},
            ),
        ],
        [
            "tomllib.loads parses TOML text into ordinary nested dictionaries.",
            "Use get with an empty list default for optional dependencies; sort into a new list.",
        ],
    ),
    unit(
        "cli-contracts",
        "python-delivery",
        "Define a predictable CLI",
        "Argument parsing & exit behavior",
        """
        import argparse

        def parse_options(argv):
            parser = argparse.ArgumentParser()
            parser.add_argument("path")
            parser.add_argument("--limit", type=int, default=10)
            parser.add_argument("--json", action="store_true")
            options = parser.parse_args(argv)
            return {"path": options.path, "limit": options.limit, "json": options.json}
        """,
        """
        def parse_options(argv):
            return {"path": argv[0], "limit": 10, "json": False}
        """,
        [
            check(
                "Default options",
                "parse_options(['input.txt'])",
                {"path": "input.txt", "limit": 10, "json": False},
            ),
            check(
                "Explicit flags",
                "parse_options(['--json', '--limit', '3', 'a b.txt'])",
                {"path": "a b.txt", "limit": 3, "json": True},
            ),
            check(
                "Flags after the path",
                "parse_options(['log.txt', '--limit', '0'])",
                {"path": "log.txt", "limit": 0, "json": False},
            ),
        ],
        [
            (
                "Pass argv to parse_args so the function can be tested without changing p"
                "rocess arguments."
            ),
            "Use type=int for --limit and action='store_true' for a flag without a value.",
        ],
    ),
    unit(
        "resource-paths",
        "python-delivery",
        "Read data with explicit paths",
        "Pathlib & structured files",
        """
        import json
        from pathlib import Path

        def read_settings(path):
            try:
                text = Path(path).read_text(encoding="utf-8")
            except FileNotFoundError:
                return {}
            result = json.loads(text)
            if not isinstance(result, dict):
                raise ValueError("Settings must be an object")
            return result
        """,
        """
        import json
        from pathlib import Path

        def read_settings(path):
            try:
                return json.loads(Path(path).read_text())
            except Exception:
                return {}
        """,
        [
            check("Missing file has defaults", "read_settings('absent-settings.json')", {}),
            check(
                "Read a JSON object",
                (
                    "(__import__('pathlib').Path('settings.json').write_text('{\"city"
                    "\": \"Montréal\"}', encoding='utf-8'), read_settings('settings.json"
                    "'))[1]"
                ),
                {"city": "Montréal"},
            ),
            check(
                "Reject an array",
                (
                    "(__import__('pathlib').Path('settings.json').write_text('[]', encodi"
                    "ng='utf-8'), __raises_value_error__(read_settings, 'settings.json'))"
                    "[1]"
                ),
                True,
            ),
            check(
                "Malformed JSON is visible",
                (
                    "(__import__('pathlib').Path('settings.json').write_text('{', encodin"
                    "g='utf-8'), __raises_value_error__(read_settings, 'settings.json'))["
                    "1]"
                ),
                True,
            ),
        ],
        [
            (
                "Catch only FileNotFoundError for an optional file; malformed content sho"
                "uld remain an error."
            ),
            "After parsing JSON, verify that the top-level value is a dictionary.",
        ],
    ),
    legacy(
        "signal-from-noise",
        "python-delivery",
        project=True,
    ),
    unit(
        "descriptors",
        "python-internals",
        "Control attribute access",
        "Descriptors & attribute lookup",
        """
        class NonNegative:
            def __set_name__(self, owner, name):
                self.storage = "_" + name

            def __get__(self, instance, owner=None):
                if instance is None:
                    return self
                return getattr(instance, self.storage, 0)

            def __set__(self, instance, value):
                if value < 0:
                    raise ValueError("Value must be nonnegative")
                setattr(instance, self.storage, value)

        class Counter:
            value = NonNegative()
        """,
        """
        class NonNegative:
            def __get__(self, instance, owner=None):
                return getattr(self, "value", 0)

            def __set__(self, instance, value):
                self.value = value

        class Counter:
            value = NonNegative()
        """,
        [
            check(
                "Default and assignment",
                "(lambda c: (c.value, setattr(c, 'value', 4), c.value))(Counter())",
                [0, None, 4],
            ),
            check(
                "Independent instances",
                "(lambda a, b: (setattr(a, 'value', 7), b.value)[1])(Counter(), Counter())",
                0,
            ),
            check(
                "Reject negatives",
                "__raises_value_error__(lambda n: setattr(Counter(), 'value', n), -1)",
                True,
            ),
            check(
                "Class access returns descriptor", "isinstance(Counter.value, NonNegative)", True
            ),
        ],
        [
            "Store values on the owner instance, not on the shared descriptor.",
            (
                "__get__ receives instance=None for class access; return the descriptor i"
                "tself in that case."
            ),
        ],
    ),
    unit(
        "metaclasses",
        "python-internals",
        "Register classes deliberately",
        "Metaclasses & class creation",
        """
        class RegistryMeta(type):
            registry = {}

            def __new__(mcls, name, bases, namespace, **kwargs):
                cls = super().__new__(mcls, name, bases, namespace, **kwargs)
                key = namespace.get("kind")
                if key is not None:
                    if key in mcls.registry:
                        raise ValueError("Duplicate kind")
                    mcls.registry[key] = cls
                return cls
        """,
        """
        class RegistryMeta(type):
            registry = {}

            def __new__(mcls, name, bases, namespace, **kwargs):
                cls = super().__new__(mcls, name, bases, namespace, **kwargs)
                mcls.registry[name] = cls
                return cls
        """,
        [
            check(
                "Register an explicit kind",
                (
                    "(lambda cls: RegistryMeta.registry['csv'] is cls)(RegistryMeta('CSV'"
                    ", (), {'kind': 'csv'}))"
                ),
                True,
            ),
            check(
                "Ignore classes without a kind",
                "(RegistryMeta('Base', (), {}), RegistryMeta.registry)[1]",
                {},
            ),
            check(
                "Reject duplicate kind",
                (
                    "(RegistryMeta('First', (), {'kind':'same'}), __raises_value_error__("
                    "lambda _: RegistryMeta('Second', (), {'kind':'same'}), None))[1]"
                ),
                True,
            ),
            check(
                "Inherited kind is not reregistered",
                (
                    "(lambda base: (RegistryMeta('Child', (base,), {}), list(RegistryMeta"
                    ".registry))[1])(RegistryMeta('Base', (), {'kind':'base'}))"
                ),
                ["base"],
            ),
        ],
        [
            (
                "Use namespace.get rather than getattr(cls, ...) so inherited kind values"
                " do not register again."
            ),
            (
                "Create the class with super().__new__, reject duplicate explicit keys, t"
                "hen store and return the class."
            ),
        ],
    ),
    unit(
        "method-resolution",
        "python-internals",
        "Method lookup and inheritance",
        "Inheritance & super",
        """
        class Root:
            def steps(self):
                return ["root"]

        class Left(Root):
            def steps(self):
                return ["left"] + super().steps()

        class Right(Root):
            def steps(self):
                return ["right"] + super().steps()

        class Pipeline(Left, Right):
            pass
        """,
        """
        class Root:
            def steps(self):
                return ["root"]

        class Left(Root):
            def steps(self):
                return ["left"] + Root.steps(self)

        class Right(Root):
            def steps(self):
                return ["right"] + Root.steps(self)

        class Pipeline(Left, Right):
            pass
        """,
        [
            check(
                "Diamond visits each class once", "Pipeline().steps()", ["left", "right", "root"]
            ),
            check("A single branch", "Left().steps()", ["left", "root"]),
            check(
                "Reversed branches cooperate",
                "type('Reversed', (Right, Left), {})().steps()",
                ["right", "left", "root"],
            ),
        ],
        [
            (
                "super() follows the method resolution order of the actual instance, not "
                "just the named parent."
            ),
            "Prepend your step to super().steps(); Root terminates the chain.",
        ],
    ),
    unit(
        "runtime-inspection",
        "python-internals",
        "Inspect without executing",
        "Inspect function parameters",
        """
        import inspect

        def describe_callable(fn):
            signature = inspect.signature(fn)
            required = [
                name for name, parameter in signature.parameters.items()
                if parameter.default is inspect.Parameter.empty
                and parameter.kind not in (
                    inspect.Parameter.VAR_POSITIONAL,
                    inspect.Parameter.VAR_KEYWORD,
                )
            ]
            return {
                "name": fn.__name__,
                "parameters": list(signature.parameters),
                "required": required,
            }
        """,
        """
        def describe_callable(fn):
            return {
                "name": fn.__name__,
                "parameters": list(fn.__code__.co_varnames),
                "required": list(fn.__code__.co_varnames),
            }
        """,
        [
            check(
                "Defaults and variadic parameters",
                "describe_callable(lambda x, y=2, *args, flag, **kwargs: None)",
                {
                    "name": "<lambda>",
                    "parameters": ["x", "y", "args", "flag", "kwargs"],
                    "required": ["x", "flag"],
                },
            ),
            check(
                "No parameters",
                "describe_callable(lambda: 1)",
                {"name": "<lambda>", "parameters": [], "required": []},
            ),
            check(
                "Ignore locals and never call",
                (
                    '(exec("def sample(a, b=1):\\n    local = a\\n    raise AssertionErro'
                    "r('called')\", globals()), describe_callable(sample))[1]"
                ),
                {"name": "sample", "parameters": ["a", "b"], "required": ["a"]},
            ),
        ],
        [
            (
                "inspect.signature provides parameter objects in declaration order withou"
                "t calling the function."
            ),
            "A required parameter has no default and is neither *args nor **kwargs.",
        ],
    ),
    unit(
        "plugin-system",
        "python-internals",
        "Project: an extensible formatter",
        "Plugin architecture project",
        (
            "from registry import Formatter\nfrom formats import Upper, Surround\n\ndef f"
            "ormat_text(kind, text):\n    if kind not in Formatter.registry:\n        rai"
            "se ValueError('Unknown formatter')\n    return Formatter.registry[kind]().re"
            "nder(text)\n"
        ),
        (
            "from registry import Formatter\nfrom formats import Upper, Surround\n\ndef f"
            "ormat_text(kind, text):\n    return Formatter.registry[kind]().render(text)"
            "\n"
        ),
        [
            check("Upper plugin", "format_text('upper', 'Hello')", "HELLO"),
            check("Surround plugin", "format_text('surround', 'hello')", "[hello]"),
            check(
                "Unknown name",
                "__raises_value_error__(lambda kind: format_text(kind, 'x'), 'missing')",
                True,
            ),
            check(
                "Runtime extension",
                (
                    "(type('Lower', (Formatter,), {'kind': 'lower', 'render': lambda self"
                    ", text: text.lower()}), format_text('lower', 'LOUD'))[1]"
                ),
                "loud",
            ),
            check(
                "Reject duplicate plugin",
                (
                    "__raises_value_error__(lambda _: type('Duplicate', (Formatter,), {'k"
                    "ind': 'upper'}), None)"
                ),
                True,
            ),
        ],
        [
            "Use __init_subclass__ to register an explicitly declared kind; call super first.",
            "The dispatcher should use the registry, so new plugins work without a new if branch.",
        ],
        project=True,
        files=(
            {
                ("lesson.py"): (
                    "from registry import Formatter\nfrom formats import Upper, Surround"
                    "\n\ndef format_text(kind, text):\n    if kind not in Formatter.regis"
                    "try:\n        raise ValueError('Unknown formatter')\n    return Form"
                    "atter.registry[kind]().render(text)\n"
                ),
                "registry.py": """
            class Formatter:
                registry = {}

                def __init_subclass__(cls, **kwargs):
                    super().__init_subclass__(**kwargs)
                    kind = cls.__dict__.get("kind")
                    if kind is not None:
                        if kind in Formatter.registry:
                            raise ValueError("Duplicate formatter")
                        Formatter.registry[kind] = cls
            """,
                "formats.py": """
            from registry import Formatter

            class Upper(Formatter):
                kind = "upper"

                def render(self, text):
                    return text.upper()

            class Surround(Formatter):
                kind = "surround"

                def render(self, text):
                    return "[" + text + "]"
            """,
            },
            {
                ("lesson.py"): (
                    "from registry import Formatter\nfrom formats import Upper, Surround"
                    "\n\ndef format_text(kind, text):\n    return Formatter.registry[kind"
                    "]().render(text)\n"
                ),
                "registry.py": """
            class Formatter:
                registry = {}

                def __init_subclass__(cls, **kwargs):
                    super().__init_subclass__(**kwargs)
                    Formatter.registry[cls.kind] = cls
            """,
                "formats.py": """
            from registry import Formatter

            class Upper(Formatter):
                kind = "upper"

                def render(self, text):
                    return text.upper()

            class Surround(Formatter):
                kind = "surround"

                def render(self, text):
                    return text
            """,
            },
        ),
    ),
)


def probe(label, source, expected, description, nudge):
    """Keep stateful behavior probes readable in source and in the learner's console."""
    return Check(
        label,
        f"(exec({code(source)!r}, globals()), __probe_result__)[1]",
        expected,
        nudge,
        description=description,
    )


EXTRA_CHECKS = {
    "exception-boundaries": (
        probe(
            "Read and close exactly once on every exit",
            """
            class CountingStream:
                def __init__(self, text, error=None):
                    self.text = text
                    self.error = error
                    self.reads = self.closes = 0
                def read(self):
                    self.reads += 1
                    if self.error is not None:
                        raise self.error
                    return self.text
                def close(self):
                    self.closes += 1
            results = []
            for text in ["7", "invalid"]:
                stream = CountingStream(text)
                try:
                    value = read_record(stream)
                except RecordError:
                    value = "invalid"
                results.append([value, stream.reads, stream.closes])
            original = OSError("disk")
            stream = CountingStream("", original)
            try:
                read_record(stream)
            except OSError as error:
                results.append([error is original, stream.reads, stream.closes])
            else:
                raise AssertionError("Reading failure was hidden")
            __probe_result__ = results
            """,
            [[7, 1, 1], ["invalid", 1, 1], [True, 1, 1]],
            "Count read and close calls on success, parsing failure, and reading failure; "
            "the original reading exception must propagate unchanged.",
            "Read once inside try, close once in finally, and preserve unrelated exceptions.",
        ),
    ),
    "managed-contexts": (
        probe(
            "Close exactly once on normal and exceptional exits",
            """
            class CountingResource:
                def __init__(self):
                    self.closes = 0
                def close(self):
                    self.closes += 1
            normal = CountingResource()
            with Closing(normal) as value:
                inside = [value is normal, normal.closes]
            failed = CountingResource()
            original = RuntimeError("body failed")
            try:
                with Closing(failed):
                    raise original
            except RuntimeError as error:
                unchanged = error is original
            else:
                raise AssertionError("Body failure was hidden")
            __probe_result__ = [inside, normal.closes, failed.closes, unchanged]
            """,
            [[True, 0], 1, 1, True],
            "The resource stays open inside the body and closes once afterward, "
            "including when the original body exception propagates.",
            "Close in __exit__ once; return a false value to preserve the body exception.",
        ),
    ),
    "metaclasses": (
        probe(
            "Duplicate registration preserves the original",
            """
            original = RegistryMeta("Original", (), {"kind": "saved"})
            try:
                RegistryMeta("Duplicate", (), {"kind": "saved"})
            except ValueError:
                pass
            else:
                raise AssertionError("Duplicate accepted")
            __probe_result__ = RegistryMeta.registry["saved"] is original
            """,
            True,
            "Reject a duplicate saved kind, then verify its original class remains registered.",
            "Check for collisions before assigning to the registry.",
        ),
    ),
    "async-streams": (
        probe(
            "Preserve duplicates and internal spaces",
            """
            import asyncio
            async def source():
                for text in [" same ", "same", " two  words "]:
                    yield text
            __probe_result__ = asyncio.run(collect_nonempty(source()))
            """,
            ["same", "same", "two  words"],
            "Read repeated strings and a string with two internal spaces; preserve both features.",
            "strip removes surrounding whitespace only; do not deduplicate the result.",
        ),
        probe(
            "Source errors remain visible",
            """
            import asyncio
            async def source():
                yield "first"
                raise ValueError("source failed")
            try:
                asyncio.run(collect_nonempty(source()))
            except ValueError:
                __probe_result__ = True
            else:
                __probe_result__ = False
            """,
            True,
            "Read one value before the source raises ValueError; expect the error to propagate.",
            "Do not replace a source failure with a partial success result.",
        ),
    ),
    "call-contracts": (
        probe(
            "Discount is keyword-only",
            """
            try:
                quote(10, 2, 0.1)
            except TypeError:
                __probe_result__ = True
            else:
                __probe_result__ = False
            """,
            True,
            "Call quote(10, 2, 0.1); expect TypeError because discount must be named.",
            "Place discount after a bare * in the signature.",
        ),
        check(
            "Reject negative quantity", "__raises_value_error__(lambda _: quote(2, -1), None)", True
        ),
    ),
    "context-practice": (
        probe(
            "Nested contexts preserve identity",
            """
            mapping = {"mode": "safe"}
            with temporary_value(mapping, "mode", "fast") as current:
                assert current is mapping
                with temporary_value(mapping, "mode", "test"):
                    assert mapping["mode"] == "test"
                assert mapping["mode"] == "fast"
            __probe_result__ = mapping
            """,
            {"mode": "safe"},
            (
                "Nest temporary modes fast and test over safe; verify the yielded object "
                "is the original mapping and each prior value returns."
            ),
            "Each context call needs its own remembered prior value.",
        ),
    ),
    "data-models": (
        check(
            "Zero restock still returns a new value",
            "(lambda item: item.restock(0) is item)(Item('x', 2))",
            False,
        ),
    ),
    "test-doubles": (
        probe(
            "Other errors are not retried",
            """
            calls = []
            def operation():
                calls.append("call")
                raise TypeError("programming error")
            try:
                retry(operation, 3, lambda: calls.append("pause"))
            except TypeError:
                __probe_result__ = calls
            else:
                raise AssertionError("TypeError was hidden")
            """,
            ["call"],
            "Raise TypeError from operation; expect it to propagate after one call and no pause.",
            "Catch ValueError specifically, not all exceptions.",
        ),
    ),
    "coroutine-basics": (
        probe(
            "Give another task a turn",
            """
            import asyncio
            async def probe_cooperation():
                progress = []
                observations = []
                def values():
                    for value in range(4):
                        progress.append(value)
                        yield value
                task = asyncio.create_task(delayed_total(values()))
                while not task.done():
                    observations.append(len(progress))
                    await asyncio.sleep(0)
                assert await task == 6
                return all(index in observations for index in (1, 2, 3))
            __probe_result__ = asyncio.run(probe_cooperation())
            """,
            True,
            (
                "Run delayed_total over four values beside an observer; verify the observ"
                "er can run between input values."
            ),
            "Await asyncio.sleep(0) once per value so the loop remains cooperative.",
        ),
    ),
    "task-groups": (
        probe(
            "Jobs start concurrently",
            """
            import asyncio
            async def probe_concurrency():
                started = []
                ready = asyncio.Event()
                async def job(value):
                    started.append(value)
                    if len(started) == 3:
                        ready.set()
                    await ready.wait()
                    return value
                factories = [lambda: job(1), lambda: job(2), lambda: job(3)]
                result = await asyncio.wait_for(collect_jobs(factories), 0.5)
                return result
            __probe_result__ = asyncio.run(probe_concurrency())
            """,
            [1, 2, 3],
            (
                "Three jobs wait until all have started; collect_jobs must schedule all t"
                "hree and preserve their order."
            ),
            "Create tasks for every job before awaiting group completion.",
        ),
    ),
    "concurrent-batch": (
        probe(
            "Failure cleans up other tasks",
            """
            import asyncio
            async def probe_cleanup():
                started = asyncio.Event()
                closed = []
                async def worker(value):
                    if value == "bad":
                        await started.wait()
                        raise ValueError("failed")
                    try:
                        started.set()
                        await asyncio.sleep(10)
                    finally:
                        closed.append(value)
                try:
                    await run_limited(["waiting", "bad"], worker, 2)
                except ExceptionGroup:
                    return closed
                raise AssertionError("Failure was hidden")
            __probe_result__ = asyncio.run(probe_cleanup())
            """,
            ["waiting"],
            (
                "One worker waits while another raises ValueError; expect sibling cleanup"
                " before the grouped error returns."
            ),
            "Use a TaskGroup to cancel and await other unfinished tasks on failure.",
        ),
    ),
    "descriptors": (
        probe(
            "Failed assignment preserves prior value",
            """
            counter = Counter()
            counter.value = 5
            try:
                counter.value = -2
            except ValueError:
                pass
            __probe_result__ = counter.value
            """,
            5,
            "Set a counter to five, then reject minus two; its value must remain five.",
            "Validate before writing the private instance attribute.",
        ),
        probe(
            "Descriptor works under another name",
            """
            class Gauge:
                count = NonNegative()
                total = NonNegative()
            gauge = Gauge()
            gauge.count = 2
            gauge.total = 8
            __probe_result__ = [gauge.count, gauge.total]
            """,
            [2, 8],
            (
                "Use two NonNegative attributes named count and total on one owner; their"
                " storage must be separate."
            ),
            "Derive the storage attribute from the name given to __set_name__.",
        ),
    ),
    "plugin-system": (
        probe(
            "Inherited kind is not a new registration",
            """
            class SpecialUpper(Upper):
                pass
            __probe_result__ = Formatter.registry["upper"] is Upper
            """,
            True,
            (
                "Create a subclass of Upper without declaring a kind; the original upper "
                "registration must remain."
            ),
            "Read cls.__dict__ rather than an inherited kind attribute.",
        ),
    ),
}
LESSONS = tuple(
    replace(lesson, checks=lesson.checks + EXTRA_CHECKS.get(lesson.id, ())) for lesson in LESSONS
)


# A path is an ordered course; prerequisites explain the prior unit without gating it.
LESSONS = tuple(
    replace(lesson, prerequisites=(LESSONS[index - 1].id,) if index else ())
    for index, lesson in enumerate(LESSONS)
)


# Known concepts also describe chapter projects, so familiar-topic skipping remains coherent.
LESSONS = tuple(
    replace(
        lesson,
        concepts=tuple(
            dict.fromkeys(
                concept
                for previous in LESSONS
                if previous.chapter_id == lesson.chapter_id and not previous.project
                for concept in previous.concepts
            )
        ),
    )
    if lesson.project
    else lesson
    for lesson in LESSONS
)
