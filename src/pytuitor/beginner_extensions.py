"""Focused collection and standard-library lessons inserted into the beginner path."""

from pytuitor.models import Check, Lesson, code, lesson_text


def _check(label, expression, expected, stdin=None):
    return Check(
        label,
        expression,
        expected,
        "Compare the actual and expected results for this input.",
        stdin=stdin,
    )


def _lesson(identifier, title, chapter, subtitle, solution, repair, checks, hints, stdin=""):
    return Lesson(
        id=identifier,
        track="beginner",
        title=title,
        subtitle=subtitle,
        minutes=20,
        concepts=(title,),
        body=lesson_text(identifier),
        repair=code(repair),
        checks=tuple(checks),
        hints=tuple(hints),
        prediction="",
        choices=(),
        answer=0,
        explanation="",
        solution=code(solution),
        chapter_id=chapter,
        stdin=stdin,
    )


# Anchors keep the order explicit without relying on a fixed chapter length.
INSERT_AFTER = {
    "tuples-and-sets": "comparing-sets",
    "loop-helpers": "nested-collections",
    "word-counts": "editing-collections",
    "dates-and-deadlines": "date-time-formats",
    "your-own-modules": "numeric-tools",
    "numeric-tools": "repeatable-randomness",
}

LESSONS = (
    _lesson(
        "comparing-sets",
        "Comparing sets",
        "b-collections",
        "Find shared, missing, and combined values",
        """
        required = set(input("Required: ").split())
        available = set(input("Available: ").split())
        shared = required & available
        missing = required - available
        combined = required | available
        exclusive = required ^ available
        ready = required <= available
        """,
        """
        required = set(input("Required: ").split())
        available = set(input("Available: ").split())
        shared = required | available
        missing = available - required
        combined = required & available
        exclusive = required | available
        ready = required < available
        """,
        [
            _check(
                label,
                "[sorted(shared), sorted(missing), sorted(combined), sorted(exclusive), ready]",
                [
                    sorted(set(a.split()) & set(b.split())),
                    sorted(set(a.split()) - set(b.split())),
                    sorted(set(a.split()) | set(b.split())),
                    sorted(set(a.split()) ^ set(b.split())),
                    set(a.split()) <= set(b.split()),
                ],
                a + "\n" + b + "\n",
            )
            for label, a, b in (
                ("Partial overlap", "rope lamp", "lamp food"),
                ("Equal sets", "rope lamp rope", "lamp rope"),
                ("Empty requirements", "", "lamp"),
                ("Nothing available", "rope", ""),
                ("Both empty", "", ""),
                ("Case-sensitive groups", "Ada ada", "ada"),
            )
        ],
        [
            "& finds shared values; | combines them; ^ finds values present in only one set.",
            "required - available keeps the missing requirements; <= includes equality.",
        ],
        "rope lamp\nlamp food\n",
    ),
    _lesson(
        "nested-collections",
        "Working with nested lists",
        "b-collections",
        "Traverse rows and columns without losing empty rows",
        """
        count = int(input("Rows: "))
        grid = []
        for number in range(count):
            row = []
            for word in input("Row: ").split():
                row.append(int(word))
            grid.append(row)
        row_totals = []
        flat = []
        positions = []
        for r, row in enumerate(grid):
            total = 0
            for c, value in enumerate(row):
                total += value
                flat.append(value)
                positions.append((r, c, value))
            row_totals.append(total)
        """,
        """
        count = int(input("Rows: "))
        grid = []
        for number in range(count):
            row = []
            for word in input("Row: ").split():
                row.append(int(word))
            grid.append(row)
        row_totals = []
        flat = []
        positions = []
        total = 0
        for r, row in enumerate(grid):
            for c, value in enumerate(row):
                total += value
                flat.append(value)
                positions.append((c, r, value))
            row_totals.append(total)
        """,
        [
            _check(
                label,
                "[grid, row_totals, flat, [list(item) for item in positions]]",
                [
                    grid,
                    [sum(row) for row in grid],
                    [v for row in grid for v in row],
                    [[r, c, v] for r, row in enumerate(grid) for c, v in enumerate(row)],
                ],
                str(len(grid)) + "\n" + "".join(" ".join(map(str, row)) + "\n" for row in grid),
            )
            for label, grid in (
                ("Unequal rows", [[2, 3], [4]]),
                ("Empty middle row", [[-2], [], [5, 5]]),
                ("No rows", []),
                ("Only empty rows", [[], []]),
            )
        ],
        [
            "Build one new row list per input line, then append that row to grid.",
            "Reset the total for each row; enumerate supplies row and column positions.",
        ],
        "2\n2 3\n4\n",
    ),
    _lesson(
        "editing-collections",
        "Editing lists and dictionaries",
        "b-collections",
        "Insert, remove, sort, and delete deliberately",
        """
        items = input("Items: ").split()
        target = input("Remove: ")
        incoming = input("Add: ")
        if target in items:
            items.remove(target)
        items.insert(0, incoming)
        items.sort()
        counts = {}
        for item in items:
            counts[item] = counts.get(item, 0) + 1
        removed = counts.pop(target, 0)
        keys = sorted(counts.keys())
        """,
        """
        items = input("Items: ").split()
        target = input("Remove: ")
        incoming = input("Add: ")
        if target in items:
            items.remove(target)
        if target in items:
            items.remove(target)
        items.insert(0, incoming)
        counts = {}
        for item in items:
            counts[item] = 1
        removed = counts.pop(target, 0)
        keys = list(counts.keys())
        """,
        [
            _check(
                "Remove only the first occurrence",
                "[items, counts, removed, keys]",
                [["apple", "pear", "pear"], {"apple": 1}, 2, ["apple"]],
                "pear apple pear\npear\npear\n",
            ),
            _check(
                "Absent target",
                "[items, counts, removed, keys]",
                [["apple", "pear"], {"apple": 1, "pear": 1}, 0, ["apple", "pear"]],
                "pear\nplum\napple\n",
            ),
            _check(
                "Start empty",
                "[items, counts, removed, keys]",
                [["z"], {"z": 1}, 0, ["z"]],
                "\na\nz\n",
            ),
            _check(
                "Repeated other items",
                "[items, counts, removed, keys]",
                [["a", "b", "b"], {"b": 2}, 1, ["b"]],
                "b b a\na\na\n",
            ),
        ],
        [
            "list.remove deletes the first match; check if target in items before removing it.",
            "sort changes the list; dict.pop(key, 0) removes a key with a safe default.",
        ],
        "pear apple pear\npear\npear\n",
    ),
    _lesson(
        "date-time-formats",
        "Parsing dates and times",
        "b-automation",
        "Combine calendar dates, clock times, and explicit formats",
        """
        from datetime import datetime, timedelta
        def appointment(day, clock, minutes):
            start = datetime.combine(datetime.strptime(day, "%d/%m/%Y").date(),
                                     datetime.strptime(clock, "%H:%M").time())
            end = start + timedelta(minutes=minutes)
            return end.strftime("%Y-%m-%d %H:%M")
        """,
        """
        from datetime import datetime, timedelta
        def appointment(day, clock, minutes):
            start = datetime.combine(datetime.strptime(day, "%m/%d/%Y").date(),
                                     datetime.strptime(clock, "%H:%M").time())
            return (start + timedelta(hours=minutes)).strftime("%Y-%m-%d %H:%M")
        """,
        [
            _check("Cross midnight", "appointment('31/12/2024', '23:50', 20)", "2025-01-01 00:10"),
            _check(
                "Day precedes month", "appointment('03/04/2024', '09:00', 0)", "2024-04-03 09:00"
            ),
            _check("Leap day", "appointment('28/02/2024', '23:30', 60)", "2024-02-29 00:30"),
            _check("Move backwards", "appointment('01/03/2024', '00:10', -20)", "2024-02-29 23:50"),
            _check(
                "Reject invalid clock",
                "[__raises_value_error__(lambda clock: appointment('01/01/2024', clock, 0), bad) "
                "for bad in ('24:00', '09:60')]",
                [True, True],
            ),
            _check(
                "Reject invalid date",
                "__raises_value_error__(lambda args: appointment(*args), "
                "('31/02/2024', '09:00', 5))",
                True,
            ),
        ],
        [
            "strptime parses with a format; strftime produces formatted text.",
            "Combine date and time before adding timedelta(minutes=minutes).",
        ],
    ),
    _lesson(
        "numeric-tools",
        "Math and statistical summaries",
        "b-tools",
        "Use library calculations and distinguish mean from median",
        """
        import math
        import statistics
        def summarize(values, capacity):
            if capacity <= 0 or not values:
                raise ValueError("Need data and positive capacity")
            return (statistics.mean(values), statistics.median(values),
                    math.ceil(len(values) / capacity))
        """,
        """
        import math
        import statistics
        def summarize(values, capacity):
            if capacity <= 0 or not values:
                raise ValueError("Need data and positive capacity")
            return (statistics.mean(values), values[len(values) // 2],
                    len(values) // capacity)
        """,
        [
            _check("Unsorted even sample", "list(summarize([9, 1, 5, 3], 3))", [4.5, 4.0, 2]),
            _check("Negative and positive", "list(summarize([-2, 0, 5], 2))", [1.0, 0, 2]),
            _check("One value", "list(summarize([7], 1))", [7, 7, 1]),
            _check(
                "No data", "__raises_value_error__(lambda args: summarize(*args), ([], 2))", True
            ),
            _check(
                "Invalid capacity",
                "__raises_value_error__(lambda args: summarize(*args), ([1], 0))",
                True,
            ),
            _check(
                "Negative capacity",
                "__raises_value_error__(lambda args: summarize(*args), ([1], -2))",
                True,
            ),
            _check("Fractional data", "list(summarize([1.5, -0.5, 3.0, 2.0], 3))", [1.5, 1.75, 2]),
            _check(
                "Input is untouched", "(lambda xs: (summarize(xs, 2), xs)[1])([8, 1, 4])", [8, 1, 4]
            ),
        ],
        [
            "statistics.mean averages; statistics.median finds the middle of the ordered data.",
            "math.ceil rounds up, so a partly filled final group still counts.",
        ],
    ),
    _lesson(
        "repeatable-randomness",
        "Repeatable random choices",
        "b-tools",
        "Repeat random choices without affecting other code",
        """
        import random
        def draw(items, count, seed):
            if count < 0 or (count > 0 and not items):
                raise ValueError("Invalid draw")
            rng = random.Random(seed)
            result = []
            for index in range(count):
                result.append(rng.choice(items))
            return result
        """,
        """
        import random
        def draw(items, count, seed):
            if count < 0 or (count > 0 and not items):
                raise ValueError("Invalid draw")
            random.seed(seed)
            result = []
            for index in range(count):
                result.append(random.choice(items))
            return result
        """,
        [
            _check(
                "Repeatable draws",
                "draw(['a', 'b', 'c'], 8, 12)",
                {
                    "expr": "(lambda rng: [rng.choice(['a', 'b', 'c']) for _ in range(8)])"
                    "(__import__('random').Random(12))"
                },
            ),
            _check(
                "Repeated calls restart independently",
                "[draw(['x', 'y', 'z'], 10, 4), draw(['x', 'y', 'z'], 10, 4)]",
                {
                    "expr": "(lambda values: [values, values])((lambda rng: "
                    "[rng.choice(['x', 'y', 'z']) for _ in range(10)])"
                    "(__import__('random').Random(4)))"
                },
            ),
            _check("Zero draws from empty input", "draw([], 0, 1)", []),
            _check(
                "Reject empty choices",
                "__raises_value_error__(lambda args: draw(*args), ([], 1, 1))",
                True,
            ),
            _check(
                "Reject negative count",
                "__raises_value_error__(lambda args: draw(*args), (['a'], -1, 1))",
                True,
            ),
            _check(
                "Shared random generator is unchanged",
                "(lambda before: (draw(['a', 'b'], 5, 9), "
                "__import__('random').getstate() == before)[1])(__import__('random').getstate())",
                True,
            ),
            _check(
                "Input remains unchanged",
                "(lambda xs: (draw(xs, 5, 3), xs)[1])(['b', 'a'])",
                ["b", "a"],
            ),
        ],
        [
            "Create random.Random(seed) inside each call for independent repeatable draws.",
            "Use that generator's choice method; random.seed would modify shared state.",
        ],
    ),
)
