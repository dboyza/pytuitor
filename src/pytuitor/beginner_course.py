"""The beginner course: small programs, dependable tools, and six projects."""

from dataclasses import replace

from pytuitor.legacy import LESSONS as LEGACY
from pytuitor.models import Chapter, Check, Lesson, Review, code, lesson_text

CHAPTERS = (
    Chapter(
        "b-foundations",
        "beginner",
        "First programs",
        "Read input, calculate, and choose what happens.",
    ),
    Chapter(
        "b-collections",
        "beginner",
        "Working with collections",
        "Process lists and dictionaries without losing track of state.",
    ),
    Chapter(
        "b-functions",
        "beginner",
        "Reusable programs",
        "Organize behavior into functions and handle invalid input.",
    ),
    Chapter(
        "b-data",
        "beginner",
        "Files and structured data",
        "Read, transform, and save text, JSON, and CSV.",
    ),
    Chapter(
        "b-tools",
        "beginner",
        "Tools you can maintain",
        "Build modules, command-line interfaces, classes, and tests.",
    ),
    Chapter(
        "b-automation",
        "beginner",
        "Dependable automation",
        "Combine data, dates, validation, and safe file operations.",
    ),
)


def exercise(
    identifier,
    title,
    subtitle,
    chapter,
    solution,
    repair,
    checks,
    hints,
    *,
    project=False,
    files=None,
    entrypoint="lesson.py",
    review=None,
    stdin="",
):
    return Lesson(
        identifier,
        "beginner",
        title,
        subtitle,
        35 if project else 15,
        (title,),
        lesson_text(identifier),
        repair,
        checks,
        hints,
        "",
        (),
        0,
        "",
        solution,
        project=project,
        revision=4,
        chapter_id=chapter,
        files=tuple(files[0]) if files else ("lesson.py",),
        entrypoint=entrypoint,
        solution_files=files[0] if files else None,
        repair_files=files[1] if files else None,
        review=review,
        stdin=stdin,
    )


def case(
    label,
    expression,
    expected,
    *,
    stdin=None,
    output=None,
    nudge="Compare the result with the stated contract, including the edge cases.",
):
    return Check(label, expression, expected, nudge, stdin=stdin, expected_output=output)


_units = []


def add(*args, **kwargs):
    _units.append(exercise(*args, **kwargs))


def reuse(identifier, chapter, *, review=None, stdin=""):
    old = next(lesson for lesson in LEGACY if lesson.id == identifier)
    _units.append(replace(old, revision=4, chapter_id=chapter, review=review, stdin=stdin))


reuse("first-light", "b-foundations")
reuse("names-and-voices", "b-foundations", stdin="Ada\n")

add(
    "numbers-from-input",
    "Numbers from input",
    "Convert text and calculate whole-number results",
    "b-foundations",
    (
        code("""
            minutes = int(input("Minutes: "))
            hours = minutes // 60
            remaining = minutes % 60
            print(hours)
            print(remaining)
        """)
    ),
    (
        code("""
            minutes = int(input("Minutes: "))
            hours = minutes / 60
            remaining = minutes // 60
            print(hours)
            print(remaining)
        """)
    ),
    tuple(
        case(
            f"Convert {n} minutes", "[hours, remaining]", [h, r], stdin=f"{n}\n", output=f"{h}\n{r}"
        )
        for n, h, r in ((125, 2, 5), (0, 0, 0), (59, 0, 59), (60, 1, 0))
    ),
    (
        "Convert the answer with int(input(...)).",
        "Use // for complete hours and % for what remains after groups of 60.",
    ),
    stdin="125\n",
)

reuse("choose-a-door", "b-foundations", stdin="gold\n")

add(
    "ticket-desk",
    "Project: the ticket desk",
    "Combine input, arithmetic, and decisions",
    "b-foundations",
    (
        code("""
            age = int(input("Age: "))
            kind = input("Ticket type: ")
            if age < 12:
                price = 5
            elif age >= 65:
                price = 7
            else:
                price = 10
            if kind == "return":
                price = price * 2
            print(f"Price: {price}")
        """)
    ),
    (
        code("""
            age = int(input("Age: "))
            kind = input("Ticket type: ")
            if age <= 12:
                price = 5
            elif age > 65:
                price = 7
            else:
                price = 10
            if kind == "return":
                price = price + 2
            print(f"Price: {price}")
        """)
    ),
    tuple(
        case(
            f"Age {age}, {kind}", "price", price, stdin=f"{age}\n{kind}\n", output=f"Price: {price}"
        )
        for age, kind, price in (
            (4, "single", 5),
            (12, "return", 20),
            (65, "single", 7),
            (64, "single", 10),
            (80, "return", 14),
        )
    ),
    (
        "Write the age price chain first and test it without the return adjustment.",
        "Use age < 12, then age >= 65; after the chain multiply price by 2 only for return.",
    ),
    project=True,
    stdin=code("""
        12
        return
    """),
    review=Review(
        (lesson_text("review-ticket-desk")),
        (
            code("""
                weight = int(input("Grams: "))
                if weight <= 100:
                    cost = 3
                elif weight <= 500:
                    cost = 5
                else:
                    cost = 9
                print(cost)
            """)
        ),
        tuple(
            case(f"Weight {w}", "cost", c, stdin=f"{w}\n", output=str(c))
            for w, c in ((100, 3), (101, 5), (500, 5), (501, 9))
        ),
        stdin="101\n",
    ),
)

reuse("pack-your-bag", "b-collections", stdin="2 5 1\n")

add(
    "list-positions",
    "Finding items in a list",
    "Indexes, length, and empty collections",
    "b-collections",
    (
        code("""
            items = input("Items: ").split()
            if len(items) == 0:
                first = "empty"
                last = "empty"
            else:
                first = items[0]
                last = items[-1]
            print(first)
            print(last)
        """)
    ),
    (
        code("""
            items = input("Items: ").split()
            first = items[1]
            last = items[0]
            print(first)
            print(last)
        """)
    ),
    tuple(
        case(
            f"Words: {text or 'empty'}",
            "[first, last]",
            expected,
            stdin=text + "\n",
            output="\n".join(expected),
        )
        for text, expected in (
            ("sun moon star", ["sun", "star"]),
            ("solo", ["solo", "solo"]),
            ("", ["empty", "empty"]),
        )
    ),
    ("Check len(items) before indexing.", "The first index is 0; -1 asks for the last item."),
)

add(
    "word-counts",
    "Dictionaries and counts",
    "Associate keys with values",
    "b-collections",
    (
        code("""
            counts = {}
            for word in input("Words: ").split():
                counts[word] = counts.get(word, 0) + 1
            print(counts)
        """)
    ),
    code("""
        counts = {}
        for word in input("Words: ").split():
            counts[word] = 1
        print(counts)
    """),
    tuple(
        case(f"Count {words!r}", "counts", result, stdin=words + "\n")
        for words, result in (
            ("bee ant bee", {"bee": 2, "ant": 1}),
            ("", {}),
            ("Cat cat Cat", {"Cat": 2, "cat": 1}),
        )
    ),
    (
        "Begin with an empty dictionary outside the loop.",
        "Assign counts[word] = counts.get(word, 0) + 1 on each visit.",
    ),
)

add(
    "repeat-until-done",
    "Repeating until done",
    "While loops and stopping conditions",
    "b-collections",
    (
        code("""
            total = 0
            while True:
                number = int(input("Number (0 to finish): "))
                if number == 0:
                    break
                total = total + number
            print(total)
        """)
    ),
    (
        code("""
            total = 0
            while True:
                number = int(input("Number (0 to finish): "))
                total = total + number
                if total >= 0:
                    break
            print(total)
        """)
    ),
    tuple(
        case(label, "total", result, stdin=text, output=str(result))
        for label, text, result in (
            (
                "Several entries",
                code("""
                5
                -2
                0
            """),
                3,
            ),
            ("Stop immediately", "0\n", 0),
            (
                "Negative total",
                code("""
                -8
                2
                0
            """),
                -6,
            ),
        )
    ),
    (
        "Put total = 0 before the loop, not inside it.",
        "Read number, break if number == 0, otherwise add it to total.",
    ),
    stdin=code("""
        5
        -2
        0
    """),
)

add(
    "supply-report",
    "Project: supply report",
    "Summarize a collection without changing it",
    "b-collections",
    (
        code("""
            counts = {}
            order = []
            for word in input("Supplies: ").split():
                if word not in counts:
                    order.append(word)
                counts[word] = counts.get(word, 0) + 1
            if len(order) == 0:
                print("No supplies")
            else:
                for word in order:
                    print(f"{word}: {counts[word]}")
        """)
    ),
    (
        code("""
            counts = {}
            order = []
            for word in input("Supplies: ").split():
                order.append(word)
                counts[word] = counts.get(word, 0) + 1
            if len(order) == 0:
                print("No supplies")
            else:
                for word in order:
                    print(f"{word}: {counts[word]}")
        """)
    ),
    (
        case(
            "Repeated supplies",
            "[counts, order]",
            [{"rope": 2, "lamp": 2, "map": 1}, ["rope", "lamp", "map"]],
            stdin="rope lamp rope map lamp\n",
            output="rope: 2\nlamp: 2\nmap: 1",
        ),
        case("Empty delivery", "[counts, order]", [{}, []], stdin="\n", output="No supplies"),
    ),
    (
        "Add a word to order only when it is not already in counts.",
        "Finish counting before printing, so each output line shows the final count.",
    ),
    project=True,
    stdin="rope lamp rope map lamp\n",
    review=Review(
        (lesson_text("review-supply-report")),
        (
            code("""
                guests = []
                for name in input("Names: ").split():
                    if name not in guests:
                        guests.append(name)
                print(len(guests))
            """)
        ),
        (
            case("Repeated names", "guests", ["Ada", "Lin"], stdin="Ada Lin Ada\n", output="2"),
            case("No names", "guests", [], stdin="\n", output="0"),
        ),
        stdin="Ada Lin Ada\n",
    ),
)

reuse("small-superpowers", "b-functions")

add(
    "clean-labels",
    "Cleaning strings",
    "Methods, whitespace, and reusable transformations",
    "b-functions",
    code("""
        def slug(text):
            return "-".join(text.lower().split())
    """),
    code("""
        def slug(text):
            text.lower()
            return text.replace(" ", "-")
    """),
    tuple(
        case(f"slug({text!r})", f"slug({text!r})", result)
        for text, result in (("  Blue   Moon ", "blue-moon"), ("", ""), ("A\tB!", "a-b!"))
    ),
    (
        "lower() returns a new string, so use that result.",
        'Split without an argument, then join the words using "-".',
    ),
)

add(
    "function-options",
    "Function options",
    "Default arguments, keyword calls, and local variables",
    "b-functions",
    (
        code("""
            def subtotal(prices, discount=0):
                total = 0
                for price in prices:
                    total = total + price
                total = total - discount
                if total < 0:
                    return 0
                return total
        """)
    ),
    (
        code("""
            def subtotal(prices, discount=0):
                total = 0
                for price in prices:
                    total = total + price - discount
                return total
        """)
    ),
    (
        case("Default discount", "subtotal([6, 4])", 10),
        case("One order discount", "subtotal([6, 4], discount=3)", 7),
        case("Discount exceeds total", "subtotal([2], discount=9)", 0),
        case("Empty basket", "subtotal([])", 0),
    ),
    (
        "Add every price first, then subtract discount after the loop.",
        "If the resulting total is below zero, return zero; otherwise return total.",
    ),
)

add(
    "handle-invalid-input",
    "Handling invalid input",
    "Exceptions and deliberate recovery",
    "b-functions",
    (
        code("""
            def parse_quantity(text):
                try:
                    number = int(text)
                except ValueError:
                    return None
                if number < 0:
                    return None
                return number
        """)
    ),
    code("""
        def parse_quantity(text):
            return int(text)
    """),
    tuple(
        case(f"Parse {text!r}", f"parse_quantity({text!r})", result)
        for text, result in (
            (" +12 ", 12),
            ("0", 0),
            ("-1", None),
            ("oops", None),
            ("3.5", None),
            ("", None),
        )
    ),
    (
        "Catch ValueError around the int() conversion.",
        "After successful conversion, reject numbers smaller than zero.",
    ),
)

reuse(
    "lantern-quest",
    "b-functions",
    stdin="east take west\n",
    review=Review(
        (lesson_text("review-lantern-quest")),
        (
            code("""
                def travel(fuel, costs):
                    stops = 0
                    for cost in costs:
                        if fuel < cost:
                            break
                        fuel = fuel - cost
                        stops = stops + 1
                    return stops
            """)
        ),
        (
            case("Stop before overspending", "travel(8, [3, 4, 2])", 2),
            case("No stops", "travel(8, [])", 0),
            case("Free stop", "travel(0, [0, 1])", 1),
        ),
        stdin="",
    ),
)

add(
    "text-files",
    "Reading and writing files",
    "Use a context manager to close files reliably",
    "b-data",
    (
        code("""
            def line_total(path):
                with open(path, "r", encoding="utf-8") as handle:
                    lines = handle.read().splitlines()
                total = 0
                for line in lines:
                    if line.strip() != "":
                        total = total + int(line)
                return total
        """)
    ),
    (
        code("""
            def line_total(path):
                with open(path, "r", encoding="utf-8") as handle:
                    lines = handle.read().splitlines()
                total = 0
                for line in lines:
                    total = total + int(line)
                return total
        """)
    ),
    tuple(
        case(
            label,
            (
                f"(__import__('pathlib').Path('numbers.txt').write_text({text!r}, "
                "encoding='utf-8'), line_total('numbers.txt'))[1]"
            ),
            result,
        )
        for label, text, result in (
            (
                "Blank lines and negatives",
                "4\n \t \n-1\n",
                3,
            ),
            ("Empty file", "", 0),
            ("Single number", "7", 7),
        )
    ),
    (
        "Use a with block to read the file, then loop over splitlines().",
        "Only call int(line) when line.strip() is not empty.",
    ),
)

add(
    "paths-and-folders",
    "Paths and folders",
    "Navigate paths without fragile string concatenation",
    "b-data",
    (
        code("""
            from pathlib import Path

            def save_note(folder, text):
                directory = Path(folder)
                directory.mkdir(parents=True, exist_ok=True)
                target = directory / "note.txt"
                target.write_text(text, encoding="utf-8")
                return target
        """)
    ),
    (
        code("""
            from pathlib import Path

            def save_note(folder, text):
                target = Path(folder + "note.txt")
                target.write_text(text, encoding="utf-8")
                return target
        """)
    ),
    (
        case(
            "Create nested folder",
            (
                "(lambda p: [p.as_posix(), p.read_text(encoding='utf-8')])(save_no"
                "te('notes/deep', 'café'))"
            ),
            ["notes/deep/note.txt", "café"],
        ),
        case(
            "Replace deliberately",
            "(save_note('notes', 'old'), save_note('notes', 'new').read_text(encoding='utf-8'))[1]",
            "new",
        ),
    ),
    (
        "Create Path(folder), then call mkdir with parents=True and exist_ok=True.",
        "Join the directory and filename with / before calling write_text.",
    ),
)

add(
    "json-records",
    "Saving structured data",
    "JSON, dictionaries, and lists on disk",
    "b-data",
    (
        code("""
            import json

            def save_scores(path, scores):
                with open(path, "w", encoding="utf-8") as handle:
                    json.dump(scores, handle)
                total = 0
                for score in scores.values():
                    total = total + score
                return total
        """)
    ),
    (
        code("""
            def save_scores(path, scores):
                with open(path, "w", encoding="utf-8") as handle:
                    handle.write(str(scores))
                total = 0
                for score in scores.values():
                    total = total + score
                return total
        """)
    ),
    tuple(
        case(
            label,
            (
                "(lambda total: [total, __import__('json').loads("
                "__import__('pathlib').Path('scores.json').read_text(encoding='utf-8'))])"
                f"(save_scores('scores.json', {scores!r}))"
            ),
            [total, scores],
        )
        for label, scores, total in (
            ("Unicode names", {"Zoë": 4, "Lin": 7}, 11),
            ("Empty scores", {}, 0),
        )
    ),
    (
        "Use json.dump inside a writing with block.",
        "Loop over scores.values() to compute the returned total separately from saving.",
    ),
)

add(
    "csv-tables",
    "Working with CSV tables",
    "Read headers and quoted fields correctly",
    "b-data",
    (
        code("""
            import csv

            def csv_total(path):
                total = 0
                with open(path, newline="", encoding="utf-8") as handle:
                    for row in csv.DictReader(handle):
                        total = total + int(row["quantity"]) * int(row["price"])
                return total
        """)
    ),
    (
        code("""
            import csv

            def csv_total(path):
                total = 0
                with open(path, newline="", encoding="utf-8") as handle:
                    for row in csv.DictReader(handle):
                        total = total + int(row["quantity"]) + int(row["price"])
                return total
        """)
    ),
    tuple(
        case(
            label,
            (
                f"(__import__('pathlib').Path('table.csv').write_text({text!r}, "
                "encoding='utf-8'), csv_total('table.csv'))[1]"
            ),
            result,
        )
        for label, text, result in (
            (
                "Quoted comma",
                code("""
                item,quantity,price
                "pen, blue",2,3
                book,1,8
            """),
                14,
            ),
            ("Header only", "item,quantity,price\n", 0),
            (
                "Zero quantity",
                code("""
                item,quantity,price
                box,0,9
            """),
                0,
            ),
        )
    ),
    (
        "DictReader gives strings; convert both numeric columns with int().",
        "Accumulate quantity multiplied by price, once per row.",
    ),
)

add(
    "expense-report",
    "Project: an expense report",
    "Transform CSV records into a JSON summary",
    "b-data",
    (
        code("""
            import csv
            import json

            def summarize_expenses(source, destination):
                totals = {}
                with open(source, newline="", encoding="utf-8") as handle:
                    for row in csv.DictReader(handle):
                        category = row["category"]
                        totals[category] = totals.get(category, 0) + int(row["amount"])
                with open(destination, "w", encoding="utf-8") as handle:
                    json.dump(totals, handle)
                return totals
        """)
    ),
    (
        code("""
            import csv
            import json

            def summarize_expenses(source, destination):
                totals = {}
                with open(source, newline="", encoding="utf-8") as handle:
                    for row in csv.DictReader(handle):
                        totals[row["category"]] = int(row["amount"])
                with open(destination, "w", encoding="utf-8") as handle:
                    json.dump(totals, handle)
                return totals
        """)
    ),
    tuple(
        case(
            label,
            (
                f"(__import__('pathlib').Path('expenses.csv').write_text({text!r}, "
                "encoding='utf-8'), (lambda result: [result, __import__('json').loads("
                "__import__('pathlib').Path('summary.json').read_text()), "
                "__import__('pathlib').Path('expenses.csv').read_text()])"
                "(summarize_expenses('expenses.csv', 'summary.json')))[1]"
            ),
            [expected, expected, text],
        )
        for label, text, expected in (
            (
                "Repeated categories",
                code("""
                    category,amount
                    travel,250
                    food,600
                    travel,150
                """),
                {"travel": 400, "food": 600},
            ),
            ("Empty report", "category,amount\n", {}),
            (
                "Quoted category",
                code("""
                category,amount
                "books, used",50
            """),
                {"books, used": 50},
            ),
        )
    ),
    (
        "Read and aggregate every CSV row before writing the JSON file.",
        'Use totals.get(category, 0) + int(row["amount"]) so earlier rows are retained.',
    ),
    project=True,
    review=Review(
        (lesson_text("review-expense-report")),
        (
            code("""
                import json

                def roster(text):
                    names = []
                    for record in json.loads(text):
                        names.append(record["name"])
                    return names
            """)
        ),
        (
            case("Two people", 'roster(\'[{"name": "Mia"}, {"name": "Jo"}]\')', ["Mia", "Jo"]),
            case("Empty roster", "roster('[]')", []),
        ),
        stdin="",
    ),
)

add(
    "your-own-modules",
    "Writing your own modules",
    "Share functions across Python files",
    "b-tools",
    "from conversions import minutes_to_seconds\n",
    "from conversions import minutes_to_seconds\n",
    (
        case("One minute", "minutes_to_seconds(1)", 60),
        case("No minutes", "minutes_to_seconds(0)", 0),
        case("Imported module contract", "__import__('conversions').minutes_to_seconds(7)", 420),
        case("Imports produce no output", "__stdout__", ""),
    ),
    (
        "Put the function definition in conversions.py.",
        "In lesson.py use from conversions import minutes_to_seconds.",
    ),
    files=(
        {
            "lesson.py": "from conversions import minutes_to_seconds\n",
            "conversions.py": code("""
                def minutes_to_seconds(minutes):
                    return minutes * 60
            """),
        },
        {
            "lesson.py": "from conversions import minutes_to_seconds\n",
            "conversions.py": code("""
                def minutes_to_seconds(minutes):
                    return minutes + 60
            """),
        },
    ),
)

add(
    "command-line-options",
    "Command-line arguments",
    "Give a tool a predictable interface",
    "b-tools",
    (
        code("""
            import argparse

            def make_parser():
                parser = argparse.ArgumentParser()
                parser.add_argument("name")
                parser.add_argument("--count", type=int, default=1)
                return parser
        """)
    ),
    (
        code("""
            import argparse

            def make_parser():
                parser = argparse.ArgumentParser()
                parser.add_argument("name")
                parser.add_argument("--count", default="0")
                return parser
        """)
    ),
    (
        case("Defaults", "vars(make_parser().parse_args(['Ada']))", {"name": "Ada", "count": 1}),
        case(
            "Explicit integer",
            "vars(make_parser().parse_args(['Lin', '--count', '3']))",
            {"name": "Lin", "count": 3},
        ),
    ),
    (
        "Create the parser, add both arguments, then return the parser object.",
        "Use type=int and default=1 for --count.",
    ),
)

add(
    "your-first-class",
    "Your first class",
    "Keep state and related operations together",
    "b-tools",
    (
        code("""
            class Wallet:
                def __init__(self):
                    self.balance = 0

                def deposit(self, amount):
                    self.balance = self.balance + amount
                    return self.balance

                def spend(self, amount):
                    if amount > self.balance:
                        return False
                    self.balance = self.balance - amount
                    return True
        """)
    ),
    (
        code("""
            class Wallet:
                def __init__(self):
                    self.balance = 0

                def deposit(self, amount):
                    self.balance = self.balance + amount
                    return self.balance

                def spend(self, amount):
                    self.balance = self.balance - amount
                    return self.balance >= 0
        """)
    ),
    (
        case(
            "Successful and refused spending",
            "(lambda w: [w.deposit(8), w.spend(3), w.spend(10), w.balance])(Wallet())",
            [8, True, False, 5],
        ),
        case(
            "Independent wallets",
            "(lambda a,b: (a.deposit(5), b.balance)[1])(Wallet(), Wallet())",
            0,
        ),
        case("Spend zero", "Wallet().spend(0)", True),
        case(
            "Spend the complete balance",
            "(lambda w: [w.deposit(6), w.spend(6), w.balance])(Wallet())",
            [6, True, 0],
        ),
    ),
    (
        "Store balance in __init__ using self.balance.",
        "Check amount > self.balance before subtracting anything.",
    ),
)

add(
    "tests-for-your-code",
    "Writing automated tests",
    "Use assertions and unittest to catch regressions",
    "b-tools",
    (
        code("""
            import unittest

            def clamp(value, low, high):
                if value < low:
                    return low
                if value > high:
                    return high
                return value

            class ClampTests(unittest.TestCase):
                def test_below(self):
                    self.assertEqual(clamp(-2, 0, 10), 0)

                def test_inside(self):
                    self.assertEqual(clamp(5, 0, 10), 5)

                def test_above(self):
                    self.assertEqual(clamp(12, 0, 10), 10)
        """)
    ),
    (
        code("""
            import unittest

            def clamp(value, low, high):
                if value > low:
                    return low
                if value > high:
                    return high
                return value

            class ClampTests(unittest.TestCase):
                def test_below(self):
                    self.assertEqual(clamp(-2, 0, 10), 0)

                def test_inside(self):
                    self.assertEqual(clamp(5, 0, 10), 5)

                def test_above(self):
                    self.assertEqual(clamp(12, 0, 10), 10)
        """)
    ),
    (
        case("Lower boundary", "clamp(-2, 0, 10)", 0),
        case("Upper boundary", "clamp(12, 0, 10)", 10),
        case("Interior", "clamp(5, 0, 10)", 5),
        case("Equal boundaries", "clamp(9, 4, 4)", 4),
        case(
            "Your test suite passes",
            (
                "(lambda result: [result.testsRun >= 3, result.wasSuccessful()])(__impo"
                "rt__('unittest').defaultTestLoader.loadTestsFromTestCase(ClampTes"
                "ts).run(__import__('unittest').TestResult()))"
            ),
            [True, True],
        ),
        *tuple(
            case(
                "Your tests reject a stub returning " + stub,
                "(ClampTests.test_below.__globals__.__setitem__('clamp', "
                f"lambda value, low, high: {stub}), "
                "__import__('unittest').defaultTestLoader.loadTestsFromTestCase(ClampTests)"
                ".run(__import__('unittest').TestResult()).wasSuccessful())[1]",
                False,
                nudge="Your tests should fail when clamp is replaced with this incorrect stub.",
            )
            for stub in ("low", "value", "high")
        ),
        case(
            "Tests cover all three regions",
            "set(['test_below', 'test_inside', 'test_above']).issubset(dir(ClampTests))",
            True,
        ),
    ),
    (
        "Implement the three return cases before writing tests for each one.",
        "Use assertEqual with an input below, inside, and above a 0 to 10 range.",
    ),
)

add(
    "task-workspace",
    "Project: a task list workspace",
    "Separate a reusable model from its entry point",
    "b-tools",
    (
        code("""
            from tasks import TaskList

            def build_report(titles):
                tasks = TaskList()
                for title in titles:
                    tasks.add(title)
                return tasks.pending()
        """)
    ),
    (
        code("""
            from tasks import TaskList

            def build_report(titles):
                tasks = TaskList()
                for title in titles:
                    tasks.add(title)
                return tasks.pending()
        """)
    ),
    (
        case(
            "Clean and deduplicate",
            "build_report([' Read ', '', 'Read', 'Walk'])",
            ["Read", "Walk"],
        ),
        case("Empty input", "build_report([])", []),
        case("Case is preserved", "build_report(['Read', 'read'])", ["Read", "read"]),
        case(
            "Returned list is independent",
            (
                "(lambda t: (t.add('Read'), t.pending().append('Injected'), t.pend"
                "ing())[2])(TaskList())"
            ),
            ["Read"],
        ),
        case(
            "Instances are independent",
            "(lambda a,b: (a.add('Mine'), b.pending())[1])(TaskList(), TaskList())",
            [],
        ),
    ),
    (
        "Put all normalization and duplicate rules in TaskList.add so every caller gets them.",
        "pending() should return self.items.copy(), not the internal list itself.",
    ),
    project=True,
    files=(
        {
            ("lesson.py"): (
                code("""
                    from tasks import TaskList

                    def build_report(titles):
                        tasks = TaskList()
                        for title in titles:
                            tasks.add(title)
                        return tasks.pending()
                """)
            ),
            ("tasks.py"): (
                code("""
                    class TaskList:
                        def __init__(self):
                            self.items = []

                        def add(self, title):
                            clean = title.strip()
                            if clean != "" and clean not in self.items:
                                self.items.append(clean)

                        def pending(self):
                            return self.items.copy()
                """)
            ),
        },
        {
            ("lesson.py"): (
                code("""
                    from tasks import TaskList

                    def build_report(titles):
                        tasks = TaskList()
                        for title in titles:
                            tasks.add(title)
                        return tasks.pending()
                """)
            ),
            ("tasks.py"): (
                code("""
                    class TaskList:
                        def __init__(self):
                            self.items = []

                        def add(self, title):
                            clean = title.strip()
                            if clean != "" and clean not in self.items:
                                self.items.append(clean)

                        def pending(self):
                            return self.items
                """)
            ),
        },
    ),
    review=Review(
        (lesson_text("review-task-workspace")),
        (
            code("""
                class Counter:
                    def __init__(self, limit):
                        self.limit = limit
                        self.value = 0

                    def advance(self):
                        if self.value < self.limit:
                            self.value = self.value + 1
                        return self.value
            """)
        ),
        (
            case(
                "Stop at limit",
                "(lambda c: [c.advance(), c.advance(), c.advance()])(Counter(2))",
                [1, 2, 2],
            ),
            case("Zero limit", "Counter(0).advance()", 0),
            case(
                "Separate counters",
                "(lambda a,b: (a.advance(), b.value)[1])(Counter(3),Counter(3))",
                0,
            ),
        ),
        stdin="",
    ),
)

add(
    "comprehensions",
    "Readable comprehensions",
    "Transform and filter without hiding the intent",
    "b-automation",
    (
        code("""
            def positive_squares(numbers):
                return sorted([number * number for number in numbers if number > 0])
        """)
    ),
    (
        code("""
            def positive_squares(numbers):
                return sorted(set([number * number for number in numbers if number >= 0]))
        """)
    ),
    (
        case("Filter, order, retain duplicates", "positive_squares([3, -2, 1, 3, 0])", [1, 9, 9]),
        case("No positives", "positive_squares([-2, 0])", []),
        case("Empty collection", "positive_squares([])", []),
        case(
            "Input unchanged",
            "(lambda values: (positive_squares(values), values)[1])([3, 1])",
            [3, 1],
        ),
    ),
    (
        "Filter with number > 0, not >= 0.",
        "Use a list rather than a set so repeated inputs remain repeated outputs.",
    ),
)

add(
    "dates-and-deadlines",
    "Dates and deadlines",
    "Use date arithmetic instead of counting calendar days yourself",
    "b-automation",
    (
        code("""
            from datetime import date, timedelta

            def due_date(start, days):
                return (date.fromisoformat(start) + timedelta(days=days)).isoformat()
        """)
    ),
    (
        code("""
            from datetime import date, timedelta

            def due_date(start, days):
                return (date.fromisoformat(start) + timedelta(days=days + 1)).isoformat()
        """)
    ),
    tuple(
        case(f"{start} plus {days} days", f"due_date({start!r}, {days})", expected)
        for start, days, expected in (
            ("2023-12-31", 1, "2024-01-01"),
            ("2024-02-28", 2, "2024-03-01"),
            ("2024-05-10", 0, "2024-05-10"),
        )
    ),
    (
        "Parse the start with date.fromisoformat.",
        "Add timedelta(days=days), then call isoformat() on the resulting date.",
    ),
)

add(
    "validate-boundaries",
    "Validating a tool’s inputs",
    "State acceptable inputs before touching files",
    "b-automation",
    (
        code("""
            def valid_filename(name):
                if name == "" or name == "." or name == "..":
                    return False
                if "/" in name or "\\\\" in name:
                    return False
                return name == name.strip()
        """)
    ),
    code("""
        def valid_filename(name):
            return name != ""
    """),
    tuple(
        case(f"Validate {name!r}", f"valid_filename({name!r})", expected)
        for name, expected in (
            ("meeting notes.txt", True),
            ("café.txt", True),
            ("", False),
            (".", False),
            ("..", False),
            ("../notes.txt", False),
            ("a\\b", False),
            (" notes.txt", False),
            ("notes.txt ", False),
        )
    ),
    (
        "Reject the three special names, then either separator.",
        "The last check can compare name with name.strip() to detect outer whitespace.",
    ),
)

add(
    "copy-with-care",
    "Copying without overwriting",
    "Preview work and protect existing data",
    "b-automation",
    (
        code("""
            import shutil

            def copy_new(source, destination):
                with open(source, "rb") as input_file:
                    try:
                        with open(destination, "xb") as output_file:
                            shutil.copyfileobj(input_file, output_file)
                    except FileExistsError:
                        return False
                return True
        """)
    ),
    (
        code("""
            import shutil

            def copy_new(source, destination):
                with open(source, "rb") as input_file:
                    with open(destination, "wb") as output_file:
                        shutil.copyfileobj(input_file, output_file)
                return True
        """)
    ),
    (
        case(
            "Copy new bytes",
            (
                "(__import__('pathlib').Path('original.bin').write_bytes(bytes([0,255,97,98,99]))"
                ", (lambda result: [result, list(__import__('pathlib').Path('new.b"
                "in').read_bytes())])(copy_new('original.bin', 'new.bin')))[1]"
            ),
            [True, [0, 255, 97, 98, 99]],
        ),
        case(
            "Keep existing destination",
            (
                "(__import__('pathlib').Path('source.txt').write_text('new'), __im"
                "port__('pathlib').Path('dest.txt').write_text('keep'), (lambda re"
                "sult: [result, __import__('pathlib').Path('dest.txt').read_text()"
                ", __import__('pathlib').Path('source.txt').read_text()])(copy_new"
                "('source.txt', 'dest.txt')))[2]"
            ),
            [False, "keep", "new"],
        ),
    ),
    (
        "Open the destination with xb, not wb.",
        "Catch FileExistsError and return False; return True only after copying finishes.",
    ),
)

add(
    "notes-archiver",
    "Project: a careful notes archiver",
    "Preview a multi-file automation tool before it writes",
    "b-automation",
    (
        code("""
            from pathlib import Path
            import shutil
            from selection import eligible

            def archive_notes(source, destination, dry_run=True):
                source = Path(source)
                destination = Path(destination)
                names = []
                for name in eligible(source):
                    target = destination / name
                    if target.exists():
                        continue
                    if not dry_run:
                        destination.mkdir(parents=True, exist_ok=True)
                        with open(source / name, "rb") as input_file:
                            try:
                                with open(target, "xb") as output_file:
                                    shutil.copyfileobj(input_file, output_file)
                            except FileExistsError:
                                continue
                    names.append(name)
                return names
        """)
    ),
    (
        code("""
            from pathlib import Path
            import shutil
            from selection import eligible

            def archive_notes(source, destination, dry_run=True):
                source = Path(source)
                destination = Path(destination)
                names = []
                for name in eligible(source):
                    target = destination / name
                    if target.exists():
                        continue
                    if True:
                        destination.mkdir(parents=True, exist_ok=True)
                        with open(source / name, "rb") as input_file:
                            try:
                                with open(target, "xb") as output_file:
                                    shutil.copyfileobj(input_file, output_file)
                            except FileExistsError:
                                continue
                    names.append(name)
                return names
        """)
    ),
    (
        case(
            "Dry run creates nothing",
            (
                "(__import__('pathlib').Path('inbox').mkdir(), __import__('pathlib"
                "').Path('inbox/b.txt').write_text('B'), __import__('pathlib').Pat"
                "h('inbox/a.txt').write_text('A'), __import__('pathlib').Path('inb"
                "ox/image.png').write_text('PNG'), [archive_notes('inbox', 'archiv"
                "e'), __import__('pathlib').Path('archive').exists()])[4]"
            ),
            [["a.txt", "b.txt"], False],
        ),
        case(
            "Copy and preserve original",
            (
                "(__import__('pathlib').Path('inbox').mkdir(), __import__('pathlib"
                "').Path('inbox/a.txt').write_text('café', encoding='utf-8'), [arc"
                "hive_notes('inbox', 'archive', dry_run=False), __import__('pathli"
                "b').Path('archive/a.txt').read_text(encoding='utf-8'), __import__"
                "('pathlib').Path('inbox/a.txt').read_text(encoding='utf-8')])[2]"
            ),
            [["a.txt"], "café", "café"],
        ),
        case(
            "Existing archive file survives",
            (
                "(__import__('pathlib').Path('inbox').mkdir(), __import__('pathlib"
                "').Path('archive').mkdir(), __import__('pathlib').Path('inbox/a.t"
                "xt').write_text('new'), __import__('pathlib').Path('archive/a.txt"
                "').write_text('keep'), [archive_notes('inbox', 'archive', dry_run"
                "=False), __import__('pathlib').Path('archive/a.txt').read_text()]"
                ")[4]"
            ),
            [[], "keep"],
        ),
        case(
            "Empty source",
            "(__import__('pathlib').Path('inbox').mkdir(), archive_notes('inbox', 'archive'))[1]",
            [],
        ),
        case(
            "Select only immediate lowercase text files",
            (
                "(__import__('pathlib').Path('inbox').mkdir(), __import__('pathlib"
                "').Path('inbox/folder.txt').mkdir(), __import__('pathlib').Path('"
                "inbox/CAPS.TXT').write_text('skip'), __import__('pathlib').Path('"
                "inbox/note.txt').write_text('keep'), __import__('pathlib').Path('"
                "inbox/link.txt').symlink_to('note.txt'), eligible('inbox'))[5]"
            ),
            ["note.txt"],
        ),
    ),
    (
        (
            "Implement eligible first, then let archive_notes use that selecti"
            "on without duplicating it."
        ),
        "Keep mkdir and copying inside if not dry_run; return planned names in either mode.",
    ),
    project=True,
    files=(
        {
            ("lesson.py"): (
                code("""
                    from pathlib import Path
                    import shutil
                    from selection import eligible

                    def archive_notes(source, destination, dry_run=True):
                        source = Path(source)
                        destination = Path(destination)
                        names = []
                        for name in eligible(source):
                            target = destination / name
                            if target.exists():
                                continue
                            if not dry_run:
                                destination.mkdir(parents=True, exist_ok=True)
                                with open(source / name, "rb") as input_file:
                                    try:
                                        with open(target, "xb") as output_file:
                                            shutil.copyfileobj(input_file, output_file)
                                    except FileExistsError:
                                        continue
                            names.append(name)
                        return names
                """)
            ),
            ("selection.py"): (
                code("""
                    from pathlib import Path

                    def eligible(source):
                        paths = []
                        for path in Path(source).iterdir():
                            if path.is_file() and not path.is_symlink() and path.suffix == ".txt":
                                paths.append(path.name)
                        return sorted(paths)
                """)
            ),
        },
        {
            ("lesson.py"): (
                code("""
                    from pathlib import Path
                    import shutil
                    from selection import eligible

                    def archive_notes(source, destination, dry_run=True):
                        source = Path(source)
                        destination = Path(destination)
                        names = []
                        for name in eligible(source):
                            target = destination / name
                            if target.exists():
                                continue
                            if True:
                                destination.mkdir(parents=True, exist_ok=True)
                                with open(source / name, "rb") as input_file:
                                    try:
                                        with open(target, "xb") as output_file:
                                            shutil.copyfileobj(input_file, output_file)
                                    except FileExistsError:
                                        continue
                            names.append(name)
                        return names
                """)
            ),
            ("selection.py"): (
                code("""
                    from pathlib import Path

                    def eligible(source):
                        paths = []
                        for path in Path(source).iterdir():
                            if path.is_file() and not path.is_symlink() and path.suffix == ".txt":
                                paths.append(path.name)
                        return sorted(paths)
                """)
            ),
        },
    ),
    review=Review(
        (lesson_text("review-notes-archiver")),
        (
            code("""
                from datetime import date

                def overdue(tasks, today):
                    current = date.fromisoformat(today)
                    titles = []
                    for task in tasks:
                        if date.fromisoformat(task["due"]) < current:
                            titles.append(task["title"])
                    return sorted(titles)
            """)
        ),
        (
            case(
                "Past, today, and future",
                (
                    "overdue([{'title':'Zebra','due':'2024-02-28'},{'title':'Today','d"
                    "ue':'2024-03-01'},{'title':'Apple','due':'2024-02-29'}], '2024-03"
                    "-01')"
                ),
                ["Apple", "Zebra"],
            ),
            case("No tasks", "overdue([], '2024-03-01')", []),
        ),
        stdin="",
    ),
)

LESSONS = tuple(
    replace(
        lesson,
        prerequisites=(_units[index - 1].id,) if index else (),
        concepts=tuple(
            dict.fromkeys(
                concept
                for prerequisite in _units[index - 4 : index]
                for concept in prerequisite.concepts
            )
        )
        if lesson.project
        else lesson.concepts,
    )
    for index, lesson in enumerate(_units)
)
