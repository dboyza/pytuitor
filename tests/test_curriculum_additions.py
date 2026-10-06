"""Regressions for the built-in, object-principle, depth, and online lessons."""

import pytest
from textual.widgets import TextArea

from pytuitor.app import TutorApp
from pytuitor.curriculum import BY_ID, default_input
from pytuitor.file_tree import FileTree
from pytuitor.models import code
from pytuitor.runner import execute

ADDED = (
    "summary-builtins",
    "dictionary-pairs",
    "object-principles",
    "pattern-matching",
    "logging-basics",
    "sqlite-records",
    "installing-packages",
    "pytest-basics",
    "web-requests",
)

# Each mutant restores exactly one defect of a two-defect Repair, so fixing half is not enough.
PARTIAL_REPAIRS = [
    ("summary-builtins", "lesson.py", "temperature <= 0", "temperature < 0"),
    ("summary-builtins", "lesson.py", "any(freezing)", "all(freezing)"),
    ("dictionary-pairs", "lesson.py", "max(points.values())", "max(points)"),
    (
        "dictionary-pairs",
        "lesson.py",
        "for name, value in points.items():\n    print",
        "for name, value in points:\n    print",
    ),
    (
        "object-principles",
        "lesson.py",
        "def area(self):\n        return self.width",
        "def area_of(self):\n        return self.width",
    ),
    ("object-principles", "lesson.py", "super().__init__(side, side)", "self.side = side"),
    ("pattern-matching", "lesson.py", '        case _:\n            return "Ignored"\n', ""),
    (
        "pattern-matching",
        "lesson.py",
        '        case {"kind": "move", "to": place}:\n'
        '            return f"Moving to {place}"\n'
        '        case {"kind": "move"}:\n'
        '            return "Where to?"\n',
        '        case {"kind": "move"}:\n'
        '            return "Where to?"\n'
        '        case {"kind": "move", "to": place}:\n'
        '            return f"Moving to {place}"\n',
    ),
    ("logging-basics", "lesson.py", "logger.exception(", "logger.error("),
    ("logging-basics", "lesson.py", 'getLogger("payments")', 'getLogger("money")'),
    (
        "sqlite-records",
        "lesson.py",
        "    with connection:\n        connection",
        "    if True:\n        connection",
    ),
    (
        "sqlite-records",
        "lesson.py",
        '"INSERT INTO visits (visitor, place) VALUES (?, ?)", (visitor, place)',
        "f\"INSERT INTO visits (visitor, place) VALUES ('{visitor}', '{place}')\"",
    ),
    (
        "installing-packages",
        "lesson.py",
        "version(name)\n        except PackageNotFoundError:",
        "__import__(name)\n        except ImportError:",
    ),
    ("pytest-basics", "test_shop.py", "def test_empty_cart", "def check_empty_cart"),
    ("pytest-basics", "test_shop.py", "    assert total([1.5", "    total([1.5"),
    ("pytest-basics", "test_shop.py", "        total([-1])", "        pass\n    total([-1])"),
    ("web-requests", "lesson.py", ", timeout=5)", ")"),
    ("web-requests", "lesson.py", "    response.raise_for_status()\n", ""),
    ("reach-ranger", "game.py", '    if response.status_code == 503:\n        return "busy"\n', ""),
    (
        "reach-ranger",
        "game.py",
        '    response.raise_for_status()\n    return "online"',
        "    try:\n        response.raise_for_status()\n    except Exception:\n"
        '        return "offline"\n    return "online"',
    ),
]


@pytest.mark.parametrize(
    "identifier,filename,before,after",
    PARTIAL_REPAIRS,
    ids=[f"{row[0]}-{index}" for index, row in enumerate(PARTIAL_REPAIRS)],
)
async def test_half_fixed_repairs_still_fail(identifier, filename, before, after):
    lesson = BY_ID[identifier]
    stage = lesson.stage_contract("repair")
    files = dict(stage.reference_files)
    assert files[filename].count(before) == 1
    files[filename] = files[filename].replace(before, after)
    result = await execute(
        lesson, files[lesson.entrypoint], default_input(lesson, "repair"), files=files, stage=stage
    )
    assert not result.passed, identifier
    assert not result.error, "This should fail for behavior, not syntax or startup."


ALTERNATIVES = {
    "summary-builtins": {
        "lesson.py": """
            scores = [int(word) for word in input().split()]
            total = 0
            for score in scores:
                total += score
            passes = [score >= 50 for score in scores]
            anyone_passed = True in passes
            everyone_passed = False not in passes
            if not scores:
                print("No scores")
            else:
                ordered = sorted(scores)
                highest, lowest = ordered[-1], ordered[0]
                print("Total:", total)
                print("Highest:", highest)
                print("Lowest:", lowest)
                print("Anyone passed:", anyone_passed)
                print("Everyone passed:", everyone_passed)
        """
    },
    "dictionary-pairs": {
        "lesson.py": """
            stock = {}
            for name, amount in zip(input().split(), input().split()):
                if name in stock:
                    stock[name] += int(amount)
                else:
                    stock[name] = int(amount)
            low = [name for name in stock.keys() if stock[name] < 3]
            for name in stock:
                print(name + ": " + str(stock[name]))
            total = 0
            for amount in stock.values():
                total += amount
            print("Total: " + str(total))
        """
    },
    "object-principles": {
        "lesson.py": """
            class Ticket:
                def __init__(self, price):
                    if price < 0:
                        raise ValueError(price)
                    self.base = price

                def cost(self):
                    return self.base

                def label(self):
                    return "Ticket: " + str(self.cost())


            class ChildTicket(Ticket):
                def cost(self):
                    return super().cost() // 2


            class GroupTicket(Ticket):
                def __init__(self, price, people):
                    if people < 1:
                        raise ValueError(people)
                    super().__init__(price)
                    self.people = people

                def cost(self):
                    return super().cost() * self.people

                def label(self):
                    return f"Group of {self.people}: {self.cost()}"


            def total_cost(tickets):
                return sum(ticket.cost() for ticket in tickets)
        """
    },
    "pattern-matching": {
        "lesson.py": """
            def handle(command):
                words = list(command)
                if not words:
                    return "Say something"
                if words == ["look"]:
                    return "You look around"
                if len(words) == 2 and words[0] == "go":
                    if words[1] in {"north", "south", "east", "west"}:
                        return "You go " + words[1]
                    return "You can't go that way"
                if words[0] == "take":
                    return "Take what?" if len(words) == 1 else "Taken: " + ", ".join(words[1:])
                if words in (["quit"], ["exit"]):
                    return "Goodbye"
                return "Unknown command"
        """
    },
    "logging-basics": {
        "lesson.py": """
            import logging


            def load_counts(lines):
                log = logging.getLogger("inventory")
                counts = {}
                for number, line in enumerate(lines, 1):
                    if line.strip() == "":
                        continue
                    pieces = line.split(",", 1)
                    text = pieces[1].strip() if len(pieces) == 2 else ""
                    try:
                        counts[pieces[0].strip()] = int(text)
                    except ValueError:
                        log.warning(f"Skipping line {number}: bad count {text!r}")
                log.info(f"Loaded {len(counts)} items")
                return counts
        """
    },
    "sqlite-records": {
        "lesson.py": """
            import sqlite3


            def open_store(path):
                connection = sqlite3.connect(path)
                connection.execute(
                    "CREATE TABLE IF NOT EXISTS supplies "
                    "(name TEXT UNIQUE NOT NULL, amount INTEGER)"
                )
                connection.commit()
                return connection


            def supply_amount(connection, name):
                for (amount,) in connection.execute(
                    "SELECT amount FROM supplies WHERE name = ?", (name,)
                ):
                    return amount
                return None


            def add_supply(connection, name, amount):
                if amount < 0 or supply_amount(connection, name) is not None:
                    raise ValueError(name)
                insert = "INSERT INTO supplies (name, amount) VALUES (?, ?)"
                connection.execute(insert, (name, amount))
                connection.commit()


            def low_supplies(connection, limit):
                rows = connection.execute("SELECT name, amount FROM supplies").fetchall()
                return sorted(name for name, amount in rows if amount < limit)
        """
    },
    "installing-packages": {
        "lesson.py": """
            import re
            import importlib.metadata


            def parse_requirement(line):
                text = line.partition("#")[0].strip()
                if not text:
                    return None
                match = re.match(r"([^=<>!~]*)(.*)", text)
                return (match.group(1).strip(), re.sub(r"\\s+", "", match.group(2)))


            def installed_version(name):
                try:
                    return importlib.metadata.distribution(name).version
                except importlib.metadata.PackageNotFoundError:
                    return None


            def requirement_report(lines):
                parsed = [parse_requirement(line) for line in lines]
                return [
                    f"{name}: {installed_version(name) or 'missing'}"
                    for name, _ in filter(None, parsed)
                ]
        """
    },
    "pytest-basics": {
        "shop.py": """
            def apply_discount(price, percent):
                if price < 0 or percent < 0 or percent > 100:
                    raise ValueError("invalid discount")
                return round(price - price * percent / 100, 2)
        """,
        "test_shop.py": """
            import pytest

            import shop


            @pytest.mark.parametrize(
                "price, percent, expected",
                [(19.99, 10, 17.99), (40, 50, 20), (8, 0, 8), (8, 100, 0)],
            )
            def test_discounts(price, percent, expected):
                assert shop.apply_discount(price, percent) == pytest.approx(expected, abs=0.001)


            def test_too_large_percent():
                with pytest.raises(ValueError, match="invalid"):
                    shop.apply_discount(10, 101)
        """,
    },
    "web-requests": {
        "lesson.py": """
            import requests


            def fetch_forecast(base_url, city):
                with requests.Session() as session:
                    reply = session.get(
                        base_url + "/forecast", params={"city": city}, timeout=(3, 7)
                    )
                if reply.status_code == 404:
                    return None
                if not reply.ok:
                    reply.raise_for_status()
                body = reply.json()
                return "{}: {} to {}".format(body["city"], body["low"], body["high"])


            def post_sighting(base_url, animal, count):
                reply = requests.request(
                    "POST",
                    base_url + "/sightings",
                    json=dict(animal=animal, count=count),
                    timeout=9,
                )
                reply.raise_for_status()
                return reply.json()["id"]
        """
    },
}


@pytest.mark.parametrize("identifier", ALTERNATIVES)
async def test_build_accepts_alternative_implementations(identifier):
    lesson = BY_ID[identifier]
    stage = lesson.stage_contract("build")
    files = {name: code(source) for name, source in ALTERNATIVES[identifier].items()}
    result = await execute(
        lesson, files[lesson.entrypoint], default_input(lesson, "build"), files=files, stage=stage
    )
    assert result.passed, (identifier, result.error, result.checks)


WEAK_SUITES = {
    "no rounding case": """
        import pytest
        from shop import apply_discount

        @pytest.mark.parametrize("price, percent, expected", [(80, 25, 60), (5, 0, 5), (5, 100, 0)])
        def test_discount(price, percent, expected):
            assert apply_discount(price, percent) == expected

        def test_rejects_large_percent():
            with pytest.raises(ValueError):
                apply_discount(10, 150)
    """,
    "no upper bound test": """
        import pytest
        from shop import apply_discount

        @pytest.mark.parametrize(
            "price, percent, expected", [(80, 25, 60), (19.99, 10, 17.99), (5, 0, 5), (5, 100, 0)]
        )
        def test_discount(price, percent, expected):
            assert apply_discount(price, percent) == expected
    """,
    "no discount that changes the price": """
        import pytest
        from shop import apply_discount

        @pytest.mark.parametrize("price, percent, expected", [(5, 0, 5), (8, 0, 8), (9, 0, 9)])
        def test_discount(price, percent, expected):
            assert apply_discount(price, percent) == expected

        def test_rejects_large_percent():
            with pytest.raises(ValueError):
                apply_discount(10, 150)
    """,
}


@pytest.mark.parametrize("gap", WEAK_SUITES)
async def test_build_rejects_learner_tests_that_miss_a_behavior(gap):
    lesson = BY_ID["pytest-basics"]
    stage = lesson.stage_contract("build")
    files = dict(stage.reference_files)
    files["test_shop.py"] = code(WEAK_SUITES[gap])
    result = await execute(lesson, files["shop.py"], "", files=files, stage=stage)
    assert not result.passed, gap
    assert not result.error


def test_every_chapter_has_repair_guidance():
    from pytuitor.curriculum import CHAPTERS
    from pytuitor.repair_pacing import CHAPTER_FOCUS

    assert {chapter.id for chapter in CHAPTERS} == set(CHAPTER_FOCUS)


@pytest.mark.parametrize("identifier", ADDED)
async def test_empty_builds_fail(identifier):
    lesson = BY_ID[identifier]
    stage = lesson.stage_contract("build")
    files = {name: "" for name in stage.files}
    result = await execute(lesson, "", default_input(lesson, "build"), files=files, stage=stage)
    assert not result.passed


@pytest.mark.parametrize(
    ("identifier", "size"),
    [
        ("object-principles", (80, 24)),
        ("pytest-basics", (80, 24)),
        ("web-requests", (140, 44)),
    ],
)
async def test_added_lessons_complete_both_stages_in_the_workbench(tmp_path, identifier, size):
    lesson = BY_ID[identifier]
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    async with app.run_test(size=size) as pilot:
        app.screen.open_lesson(lesson)
        await pilot.pause()
        screen = app.screen
        for stage in ("build", "repair"):
            assert screen.stage == stage
            for name, source in lesson.stage_contract(stage).reference_files.items():
                if screen.query(FileTree):
                    tree = screen.query_one(FileTree)
                    tree.select_node(tree.files[name])
                    await pilot.pause()
                screen.query_one("#editor", TextArea).load_text(source)
                await pilot.pause()
            await pilot.press("f5")
            await app.workers.wait_for_complete()
            assert screen.stage_passed(stage), screen.check_results
            if stage == "build":
                await pilot.press("ctrl+n")
                await pilot.pause()
        assert app.store.status(lesson) == "completed"
