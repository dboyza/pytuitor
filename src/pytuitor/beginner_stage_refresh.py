"""Stage-specific exercise content for the refreshed beginner course."""

from pytuitor.models import Check, StageContract, code


def _check(
    label,
    expression,
    expected,
    *,
    stdin=None,
    output=None,
    nudge="Inspect the value at the point where this stage's behavior changes.",
):
    return Check(label, expression, expected, nudge, stdin=stdin, expected_output=output)


def _stage(
    instructions,
    reference,
    starter,
    checks,
    hints,
    *,
    stdin="",
    files=("lesson.py",),
    starter_files=None,
    reference_files=None,
):
    if starter_files is None:
        starter_files = {"lesson.py": code(starter)}
    if reference_files is None:
        reference_files = {"lesson.py": code(reference)}
    return StageContract(
        instructions=instructions,
        checks=tuple(checks),
        hints=tuple(hints),
        stdin=stdin,
        files=tuple(files),
        starter_files=starter_files,
        reference_files=reference_files,
    )


BUILD_INSTRUCTIONS = {
    "pack-your-bag": (
        "Read one line of whole-number pouch amounts. Build a list named pouches, "
        "add every amount into total starting at zero, and leave total available for checks. "
        "An empty line must produce total 0."
    ),
    "list-positions": (
        "Read one line into items. Set first and last to the first and last item, or to "
        "'empty' for an empty list, and leave both names available for checks."
    ),
    "tuples-and-sets": (
        "Read two names into a tuple named pair and unpack first and second in input order. "
        "Store distinct visitor names in the set seen, then leave the four named values "
        "available for checks."
    ),
    "comparing-sets": (
        "Read required and available word groups as sets. Create shared, missing, combined, "
        "exclusive, and ready using their usual set relationships, including equal and empty "
        "sets."
    ),
    "loop-helpers": (
        "Read count, names, and colors. Build slots from 1 through count, number names from 1, "
        "and pair names with colors until the shorter list ends. Keep the three result lists "
        "named slots, numbered, and pairs."
    ),
    "nested-collections": (
        "Read a number of integer rows into grid, allowing empty and different-length rows. "
        "Create row_totals, flat, and positions with zero-based row and column indexes."
    ),
    "word-counts": (
        "Read one line of words and create counts, a dictionary mapping each case-sensitive word "
        "to its number of occurrences. An empty line produces an empty dictionary."
    ),
    "editing-collections": (
        "Read items, target, and incoming. Remove only the first target, insert incoming at the "
        "front, sort items, count the resulting values, remove target from counts into removed, "
        "and leave sorted remaining keys in keys."
    ),
    "repeat-until-done": (
        "Read integers until a zero is entered. Add every nonzero value to total, starting at "
        "zero, and print total once after the loop. Negative values count normally."
    ),
    "supply-report": (
        "Read one line of supplies. Count each word in counts and keep each distinct word once "
        "in first_seen order, then print word: count lines or No supplies for an empty input."
    ),
    "small-superpowers": (
        "Define heal(health, potion). Return health plus potion, capped at 100. Use a local value "
        "and return it; checks call the function directly."
    ),
    "clean-labels": (
        "Define slug(text) to return lowercase words joined by one hyphen. Ignore leading, "
        "trailing, and repeated whitespace, preserve punctuation, and return rather than print."
    ),
    "function-options": (
        "Define subtotal(prices, discount=0). Add all nonnegative prices, subtract one discount "
        "from the order total, and never return less than zero. Do not change prices."
    ),
    "recursion-basics": (
        "Define digit_sum(number) for a nonnegative integer. Return the sum of its decimal digits; "
        "a one-digit number is the base case and larger numbers use the remaining prefix."
    ),
    "recursive-collections": (
        "Define sum_nested(items) for finite lists containing integers or more lists. Recursively "
        "add every integer at every depth, treating empty lists as zero and preserving the input."
    ),
    "handle-invalid-input": (
        "Define parse_quantity(text). Return a nonnegative integer when conversion succeeds, and "
        "return None for invalid text or negative numbers. Catch conversion errors deliberately."
    ),
    "lantern-quest": (
        "Define play(moves) for a forest-and-cave adventure. Start in forest with zero coins, "
        "move east or west, and collect five cave coins only once when the move is take. Return "
        "the final place and coin count as a tuple."
    ),
    "text-files": (
        "Define line_total(path) to read UTF-8 integer lines, ignore blank lines, and return their "
        "sum. The file may contain negatives and must not be changed."
    ),
    "paths-and-folders": (
        "Define save_note(folder, text). Create missing parent folders, write text exactly to "
        "note.txt in the requested folder using UTF-8, and return its Path."
    ),
    "json-records": (
        "Define save_scores(path, scores). Save the dictionary as JSON and return the sum of its "
        "integer values. Preserve every key, including Unicode names."
    ),
    "csv-tables": (
        "Define csv_total(path) for a CSV with item, quantity, and price headers. Add quantity "
        "times price for every data row, including quoted item names, and return the total."
    ),
    "regex-validation": (
        "Define valid_code(text) returning True only for exactly two uppercase ASCII letters, "
        "a hyphen, and three ASCII digits. Reject extra characters and other digit types."
    ),
    "regex-transformations": (
        "Define redact_tags(text) returning (names, redacted). Extract every lowercase name from "
        "complete [user:name] tags in order and replace every such tag with [user:hidden]."
    ),
    "expense-report": (
        "Define summarize_expenses(source, destination). Read category and amount CSV rows, add "
        "repeated category amounts, save the dictionary as JSON, and return it."
    ),
    "your-own-modules": (
        "Create conversions.py with minutes_to_seconds(minutes) returning minutes times 60. "
        "Import that function in lesson.py without printing or reading input at import time."
    ),
    "numeric-tools": (
        "Define summarize(values, capacity). Return mean, median, and the number of capacity-sized "
        "groups needed. Reject empty values or nonpositive capacity with ValueError and preserve "
        "the input list."
    ),
    "repeatable-randomness": (
        "Define draw(items, count, seed). Use an independent seeded Random object, choose exactly "
        "count times, and return a new list. Reject invalid counts without changing shared state."
    ),
    "command-line-options": (
        "Define make_parser() returning an ArgumentParser with required name and optional integer "
        "--count, defaulting to 1. Do not parse arguments or print during definition."
    ),
    "your-first-class": (
        "Define Wallet with an independent balance starting at zero. deposit adds and returns the "
        "new balance; spend subtracts only when affordable and returns whether it succeeded."
    ),
    "named-states": (
        "Define Status(Enum) with TODO, DOING, and DONE values in that order. Define next_status "
        "so TODO advances, DOING finishes, and DONE remains DONE."
    ),
    "tests-for-your-code": (
        "Define clamp(value, low, high), then a ClampTests unittest.TestCase with below, inside, "
        "and above tests. Check manages the test run, so do not call unittest.main()."
    ),
    "task-workspace": (
        "Create tasks.py with TaskList that cleans, deduplicates, and returns independent pending "
        "lists. In lesson.py import it and define build_report(titles) using a fresh TaskList."
    ),
    "comprehensions": (
        "Define positive_squares(numbers) returning sorted squares of strictly positive integers. "
        "Keep duplicates, leave the input unchanged, and use a comprehension or loop."
    ),
    "counting-and-grouping": (
        "Define summarize_visits(visits) returning counts and ordered pages dictionaries. Count "
        "every visit and append every page for its user, including duplicates."
    ),
    "queues-with-deque": (
        "Define process_queue(waiting, arrivals, limit). Append arrivals after waiting, serve up "
        "to limit from the front, and return served and remaining lists without changing inputs."
    ),
    "dates-and-deadlines": (
        "Define due_date(start, days) using date arithmetic. Return the ISO date exactly "
        "days after "
        "start, including month ends, year ends, and leap days."
    ),
    "date-time-formats": (
        "Define appointment(day, clock, minutes) for DD/MM/YYYY and HH:MM input. Add signed "
        "minutes "
        "and return YYYY-MM-DD HH:MM, letting invalid values raise ValueError."
    ),
    "validate-boundaries": (
        "Define valid_filename(name). Accept nonempty names except . and .., with no slash, "
        "backslash, leading whitespace, or trailing whitespace. Do not touch the filesystem."
    ),
    "copy-with-care": (
        "Define copy_new(source, destination). Copy bytes only when destination is new, return "
        "True "
        "after a successful copy, and return False without changes when the destination exists."
    ),
    "notes-archiver": (
        "Create selection.py with eligible(source) returning sorted immediate lowercase .txt "
        "files. "
        "In lesson.py define archive_notes with a dry-run default and exclusive copying when "
        "enabled."
    ),
}


REPAIR_STAGES = {
    "pack-your-bag": _stage(
        "Repair a separate snack-budget program. Its total should add each whole-number cost "
        "in costs and return 0 for an empty list. Investigate the accumulator before changing it.",
        """
        def snack_budget(costs):
            total = 0
            for cost in costs:
                total += cost
            return total
        """,
        """
        def snack_budget(costs):
            total = 0
            for cost in costs:
                total = cost
            return total
        """,
        (
            _check(
                "Several costs", "snack_budget([2, 5, 1])", 8, nudge="Trace total after each cost."
            ),
            _check(
                "Empty costs",
                "snack_budget([])",
                0,
                nudge="Check the value returned when the loop has no iterations.",
            ),
            _check(
                "Negative adjustment",
                "snack_budget([10, -3, 2])",
                9,
                nudge="Each item contributes to the running total.",
            ),
        ),
        ("Start total at zero.", "Add each cost to the existing total instead of replacing it."),
    ),
    "list-positions": _stage(
        "Repair a separate edge-summary function. describe_edges(items) must return a tuple "
        "of the first item, last item, and item count, using 'empty' for both item positions "
        "when the list is empty.",
        """
        def describe_edges(items):
            if not items:
                return "empty", "empty", 0
            return items[0], items[-1], len(items)
        """,
        """
        def describe_edges(items):
            if not items:
                return "empty", "empty", 0
            return items[1], items[0], len(items)
        """,
        (
            _check("Several items", "describe_edges(['sun', 'moon', 'star'])", ("sun", "star", 3)),
            _check("One item", "describe_edges(['solo'])", ("solo", "solo", 1)),
            _check("Empty items", "describe_edges([])", ("empty", "empty", 0)),
        ),
        (
            "Handle the empty list before indexing.",
            "Index zero is the first item and -1 is the last item.",
        ),
    ),
    "tuples-and-sets": _stage(
        "Repair a separate guest-summary program. guest_summary(names, visitors) must return "
        "the original two-name tuple and a set of distinct visitor names. Preserve name order "
        "and case sensitivity.",
        """
        def guest_summary(names, visitors):
            pair = tuple(names)
            first, second = pair
            seen = set(visitors)
            return pair, first, second, seen
        """,
        """
        def guest_summary(names, visitors):
            pair = tuple(names)
            first, second = pair[::-1]
            seen = list(visitors)
            return pair, first, second, seen
        """,
        (
            _check(
                "Repeated visitors",
                "(lambda result: (result[0], result[1], result[2], sorted(result[3])))"
                "(guest_summary(['Ada', 'Lin'], ['Ada', 'Ada', 'Bo']))",
                (("Ada", "Lin"), "Ada", "Lin", ["Ada", "Bo"]),
            ),
            _check(
                "No visitors",
                "(lambda result: (result[0], result[1], result[2], sorted(result[3])))"
                "(guest_summary(['Ada', 'Lin'], []))",
                (("Ada", "Lin"), "Ada", "Lin", []),
            ),
            _check(
                "Case matters",
                "(lambda result: (result[0], result[1], result[2], sorted(result[3])))"
                "(guest_summary(['Ada', 'ada'], ['ada', 'Bo']))",
                (("Ada", "ada"), "Ada", "ada", ["Bo", "ada"]),
            ),
        ),
        (
            "Use tuple(names) and unpack it without reversing it.",
            "Use set(visitors) so repeated visits appear once.",
        ),
    ),
    "comparing-sets": _stage(
        "Repair a separate availability report. availability_report(required, available) must "
        "return a dictionary with shared, missing, combined, exclusive, and ready results. "
        "Equal sets count as ready.",
        """
        def availability_report(required, available):
            required = set(required)
            available = set(available)
            return {
                "shared": required & available,
                "missing": required - available,
                "combined": required | available,
                "exclusive": required ^ available,
                "ready": required <= available,
            }
        """,
        """
        def availability_report(required, available):
            required = set(required)
            available = set(available)
            return {
                "shared": required | available,
                "missing": available - required,
                "combined": required & available,
                "exclusive": required | available,
                "ready": required < available,
            }
        """,
        (
            _check(
                "Partial overlap",
                "(lambda r: {key: sorted(value) if isinstance(value, set) else value "
                "for key, value in r.items()})(availability_report("
                "{'rope', 'lamp'}, {'lamp', 'food'}))",
                {
                    "shared": ["lamp"],
                    "missing": ["rope"],
                    "combined": ["food", "lamp", "rope"],
                    "exclusive": ["food", "rope"],
                    "ready": False,
                },
            ),
            _check(
                "Equal sets",
                "(lambda r: {key: sorted(value) if isinstance(value, set) else value "
                "for key, value in r.items()})(availability_report({'rope'}, {'rope'}))",
                {
                    "shared": ["rope"],
                    "missing": [],
                    "combined": ["rope"],
                    "exclusive": [],
                    "ready": True,
                },
            ),
            _check(
                "No requirements",
                "(lambda r: {key: sorted(value) if isinstance(value, set) else value "
                "for key, value in r.items()})(availability_report(set(), {'lamp'}))",
                {
                    "shared": [],
                    "missing": [],
                    "combined": ["lamp"],
                    "exclusive": ["lamp"],
                    "ready": True,
                },
            ),
        ),
        (
            "Intersection finds shared values; difference keeps values in only one direction.",
            "Subset comparison <= includes equality, unlike <.",
        ),
    ),
    "loop-helpers": _stage(
        "Repair a separate packing program. Read labels and whole-number weights from two lines "
        "and create labelled as tuples numbered from 1, stopping at the shorter list. Empty input "
        "must produce an empty list. Keep the work at module level as in the lessons so Run can "
        "show the result.",
        """
        labels = input("Labels: ").split()
        weights = []
        for text in input("Weights: ").split():
            weights.append(int(text))
        labelled = []
        for index in range(len(labels)):
            if index < len(weights):
                labelled.append((index + 1, labels[index], weights[index]))
        """,
        """
        labels = input("Labels: ").split()
        weights = []
        for text in input("Weights: ").split():
            weights.append(int(text))
        labelled = []
        for index in range(len(labels)):
            if index < len(weights):
                labelled.append((index, weights[index], labels[index]))
        """,
        (
            _check(
                "Matched labels",
                "labelled",
                [(1, "Mira", 3), (2, "Sol", 5)],
                stdin="Mira Sol\n3 5\n",
            ),
            _check("Numbering starts at one", "labelled[0][0]", 1, stdin="Mira Sol\n3 5\n"),
            _check("Pair order", "labelled[0][1:]", ("Mira", 3), stdin="Mira Sol\n3 5\n"),
        ),
        (
            "zip stops at the shorter input.",
            "Use a one-based number and keep the label before its weight in each tuple.",
        ),
        stdin="Mira Sol\n3 5\n",
    ),
    "nested-collections": _stage(
        "Repair a separate matrix summary. matrix_summary(grid) must return row lengths and "
        "column totals as (lengths, totals), preserving empty rows and columns that have no "
        "values. The provided program loses the row boundary while accumulating.",
        """
        def matrix_summary(grid):
            lengths = []
            totals = {}
            for row in grid:
                lengths.append(len(row))
                for column, value in enumerate(row):
                    totals[column] = totals.get(column, 0) + value
            return lengths, totals
        """,
        """
        def matrix_summary(grid):
            lengths = []
            totals = {}
            running = 0
            for row in grid:
                lengths.append(len(row))
                for column, value in enumerate(row):
                    running += value
                    totals[column] = running
            return lengths, totals
        """,
        (
            _check("Unequal rows", "matrix_summary([[2, 3], [4]])", ([2, 1], {0: 6, 1: 3})),
            _check(
                "Empty middle row", "matrix_summary([[1], [], [5, 5]])", ([1, 0, 2], {0: 6, 1: 5})
            ),
            _check("No rows", "matrix_summary([])", ([], {})),
        ),
        (
            "Keep one length for each row.",
            "A column total is independent from totals in earlier columns or rows.",
        ),
    ),
    "word-counts": _stage(
        "Repair a separate frequency function. first_seen_counts(words) must return a list of "
        "(word, count) pairs in first-seen order. Repeated words increase their existing count "
        "without creating another pair.",
        """
        def first_seen_counts(words):
            counts = {}
            order = []
            for word in words:
                if word not in counts:
                    order.append(word)
                    counts[word] = 0
                counts[word] += 1
            return [(word, counts[word]) for word in order]
        """,
        """
        def first_seen_counts(words):
            counts = {}
            order = []
            for word in words:
                if word not in counts:
                    order.append(word)
                    counts[word] = 0
                counts[word] = 1
            return [(word, counts[word]) for word in order]
        """,
        (
            _check(
                "Repeated words",
                "first_seen_counts(['bee', 'ant', 'bee'])",
                [("bee", 2), ("ant", 1)],
            ),
            _check("Empty words", "first_seen_counts([])", []),
            _check(
                "Case-sensitive words",
                "first_seen_counts(['Cat', 'cat', 'Cat'])",
                [("Cat", 2), ("cat", 1)],
            ),
        ),
        (
            "Keep a separate order list for first appearances.",
            "Increase the stored count instead of resetting it to one.",
        ),
    ),
    "editing-collections": _stage(
        "Repair a separate roster editor. edit_roster(items, target, incoming) must remove one "
        "matching item, add incoming at the front, sort the final list, and return the list plus "
        "a count dictionary. The broken code removes every match and loses duplicate counts.",
        """
        def edit_roster(items, target, incoming):
            items = list(items)
            if target in items:
                items.remove(target)
            items.insert(0, incoming)
            items.sort()
            counts = {}
            for item in items:
                counts[item] = counts.get(item, 0) + 1
            return items, counts
        """,
        """
        def edit_roster(items, target, incoming):
            items = list(items)
            while target in items:
                items.remove(target)
            items.insert(0, incoming)
            counts = {}
            for item in items:
                counts[item] = 1
            return items, counts
        """,
        (
            _check(
                "Remove one duplicate",
                "edit_roster(['pear', 'apple', 'pear'], 'pear', 'pear')",
                (["apple", "pear", "pear"], {"apple": 1, "pear": 2}),
            ),
            _check(
                "Absent target",
                "edit_roster(['pear'], 'plum', 'apple')",
                (["apple", "pear"], {"apple": 1, "pear": 1}),
            ),
            _check("Empty list", "edit_roster([], 'x', 'z')", (["z"], {"z": 1})),
        ),
        (
            "list.remove removes only the first matching item.",
            "Use get(item, 0) + 1 so repeated items retain their counts.",
        ),
    ),
    "repeat-until-done": _stage(
        "Repair a separate sentinel collector. sum_before_stop(values) must add values until the "
        "first zero and ignore the zero and everything after it. Negative values are valid. The "
        "bug checks the running total instead of the current value.",
        """
        def sum_before_stop(values):
            total = 0
            for value in values:
                if value == 0:
                    break
                total += value
            return total
        """,
        """
        def sum_before_stop(values):
            total = 0
            for value in values:
                total += value
                if total == 0:
                    break
            return total
        """,
        (
            _check("Several values", "sum_before_stop([5, -2, 0, 20])", 3),
            _check("Stop immediately", "sum_before_stop([0, 9])", 0),
            _check("Negative running total", "sum_before_stop([-8, 2, 0])", -6),
        ),
        (
            "Inspect each input value before adding it.",
            "The sentinel is zero, not a particular running total.",
        ),
    ),
    "supply-report": _stage(
        "Repair a separate supply index. index_supplies(items) must return (counts, first_seen), "
        "where counts records every frequency and first_seen lists each word once in its first "
        "appearance order. Empty input returns ({}, []).",
        """
        def index_supplies(items):
            counts = {}
            first_seen = []
            for item in items:
                if item not in counts:
                    first_seen.append(item)
                counts[item] = counts.get(item, 0) + 1
            return counts, first_seen
        """,
        """
        def index_supplies(items):
            counts = {}
            first_seen = []
            for item in items:
                first_seen.append(item)
                counts[item] = counts.get(item, 0) + 1
            return counts, first_seen
        """,
        (
            _check(
                "Repeated supplies",
                "index_supplies(['rope', 'lamp', 'rope', 'map', 'lamp'])",
                ({"rope": 2, "lamp": 2, "map": 1}, ["rope", "lamp", "map"]),
            ),
            _check("Empty delivery", "index_supplies([])", ({}, [])),
            _check(
                "Case-sensitive names",
                "index_supplies(['Ada', 'ada', 'Ada'])",
                ({"Ada": 2, "ada": 1}, ["Ada", "ada"]),
            ),
        ),
        (
            "Append to first_seen only when the item has no count yet.",
            "Counting and first appearance order are separate pieces of state.",
        ),
    ),
    "small-superpowers": _stage(
        "Repair a separate stamina function. restore(stamina, snack) must add the snack and cap "
        "the result at 50. A snack that would exceed the cap must not produce a larger value.",
        """
        def restore(stamina, snack):
            amount = stamina + snack
            if amount > 50:
                amount = 50
            return amount
        """,
        """
        def restore(stamina, snack):
            amount = stamina + snack
            if amount > 50:
                amount = 50
            return stamina
        """,
        (
            _check("Below cap", "restore(20, 10)", 30),
            _check("At cap", "restore(45, 5)", 50),
            _check("Over cap", "restore(45, 20)", 50),
        ),
        (
            "Calculate the new amount before applying the cap.",
            "Return the capped amount, not the original stamina.",
        ),
    ),
    "clean-labels": _stage(
        "Repair a separate heading function. heading(text) must trim outer whitespace, collapse "
        "runs of whitespace to single spaces, and capitalize the first character of each word. "
        "Punctuation remains part of its word.",
        """
        def heading(text):
            return " ".join(text.split()).title()
        """,
        """
        def heading(text):
            text.split()
            return text.title()
        """,
        (
            _check("Repeated spaces", "heading('  blue   moon  ')", "Blue Moon"),
            _check("Tabs", "heading('red\\tplanet')", "Red Planet"),
            _check("Punctuation", "heading('version 2.0!')", "Version 2.0!"),
            _check("Empty text", "heading('')", ""),
        ),
        (
            "split() returns the words and does not change text by itself.",
            "Join the cleaned words before applying the capitalization method.",
        ),
    ),
    "function-options": _stage(
        "Repair a separate order function. order_total(prices, service_fee=0) must add all prices "
        "and then add one service fee for the whole order. An empty order still includes the fee, "
        "and prices must not be changed.",
        """
        def order_total(prices, service_fee=0):
            total = 0
            for price in prices:
                total += price
            return total + service_fee
        """,
        """
        def order_total(prices, service_fee=0):
            total = 0
            for price in prices:
                total += price + service_fee
            return total
        """,
        (
            _check("Default fee", "order_total([6, 4])", 10),
            _check("One fee", "order_total([6, 4], service_fee=3)", 13),
            _check("Empty order fee", "order_total([], service_fee=3)", 3),
            _check(
                "Input unchanged",
                "(lambda values: (order_total(values, 2), values))([1, 2])",
                (5, [1, 2]),
            ),
        ),
        ("Add every price first.", "Apply service_fee once after the loop, not once per item."),
    ),
    "recursion-basics": _stage(
        "Repair a separate recursive function. digit_product(number) must multiply the decimal "
        "digits of a nonnegative integer. The one-digit base case supplies the final digit, and "
        "larger numbers reduce with // and %.",
        """
        def digit_product(number):
            if number < 10:
                return number
            return number % 10 * digit_product(number // 10)
        """,
        """
        def digit_product(number):
            if number < 10:
                return 1
            return number % 10 * digit_product(number // 10)
        """,
        (
            _check("Zero", "digit_product(0)", 0),
            _check("One digit", "digit_product(7)", 7),
            _check("Several digits", "digit_product(204)", 0),
            _check("Nonzero digits", "digit_product(234)", 24),
        ),
        (
            "The base case is reached for every one-digit number.",
            "Return that digit so it participates in the multiplication.",
        ),
    ),
    "recursive-collections": _stage(
        "Repair a separate recursive function. count_nested(items) must count every integer at "
        "every depth in a finite nested list. Empty lists count as zero; do not count a list "
        "object as one integer.",
        """
        def count_nested(items):
            total = 0
            for item in items:
                if isinstance(item, list):
                    total += count_nested(item)
                else:
                    total += 1
            return total
        """,
        """
        def count_nested(items):
            total = 0
            for item in items:
                if isinstance(item, list):
                    total += len(item)
                else:
                    total += 1
            return total
        """,
        (
            _check("Empty", "count_nested([])", 0),
            _check("Flat", "count_nested([3, -2])", 2),
            _check("Nested", "count_nested([1, [2, [3]], 4])", 4),
            _check("Empty inner lists", "count_nested([[[], []]])", 0),
        ),
        (
            "Use isinstance(item, list) to choose the recursive path.",
            "The recursive result is the number of integers inside the child list.",
        ),
    ),
    "handle-invalid-input": _stage(
        "Repair a separate parser. parse_score(text) must return an integer from 0 through 100, "
        "or None for conversion errors and values outside that range. Whitespace and a leading "
        "plus sign are accepted by int().",
        """
        def parse_score(text):
            try:
                score = int(text)
            except ValueError:
                return None
            if score < 0 or score > 100:
                return None
            return score
        """,
        """
        def parse_score(text):
            score = int(text)
            if score < 0:
                return None
            return score
        """,
        (
            _check("Ordinary score", "parse_score('82')", 82),
            _check("Whitespace", "parse_score(' +7 ')", 7),
            _check("Negative", "parse_score('-1')", None),
            _check("Too high", "parse_score('101')", None),
            _check("Not a number", "parse_score('oops')", None),
        ),
        (
            "Catch ValueError around int(text).",
            "After conversion, reject both negative and above-cap values.",
        ),
    ),
    "lantern-quest": _stage(
        "Repair a separate cave route. explore(moves) starts at camp with zero gems, moves north "
        "to the ruins and south back to camp, and collects three gems once when search is used "
        "in the ruins. Return (place, gems). Other moves do nothing.",
        """
        def explore(moves):
            place = "camp"
            gems = 0
            found = False
            for move in moves:
                if place == "camp" and move == "north":
                    place = "ruins"
                elif place == "ruins" and move == "south":
                    place = "camp"
                elif place == "ruins" and move == "search" and not found:
                    gems += 3
                    found = True
            return place, gems
        """,
        """
        def explore(moves):
            place = "camp"
            gems = 0
            found = False
            for move in moves:
                if place == "camp" and move == "north":
                    place = "ruins"
                elif place == "ruins" and move == "south":
                    place = "camp"
                elif place == "ruins" and move == "search":
                    gems += 3
                    found = True
            return place, gems
        """,
        (
            _check("Find gems", "explore(['north', 'search', 'south'])", ("camp", 3)),
            _check("One search", "explore(['north', 'search', 'search'])", ("ruins", 3)),
            _check("Stay put", "explore(['search'])", ("camp", 0)),
            _check("Unknown move", "explore(['north', 'wait'])", ("ruins", 0)),
        ),
        (
            "Keep a boolean found flag outside the loop.",
            "Require both the place and the move before changing state.",
        ),
    ),
    "text-files": _stage(
        "Repair a separate file-reading function. nonblank_lines(path) must return the number "
        "of nonblank lines in a UTF-8 text file. Whitespace-only lines do not count, including "
        "when they appear between negative and positive numbers.",
        """
        def nonblank_lines(path):
            with open(path, encoding="utf-8") as handle:
                return sum(1 for line in handle if line.strip())
        """,
        """
        def nonblank_lines(path):
            with open(path, encoding="utf-8") as handle:
                return sum(1 for line in handle)
        """,
        (
            _check(
                "Blank lines",
                "(__import__('pathlib').Path('lines.txt').write_text("
                "'4\\n \\n-1\\n', encoding='utf-8'), nonblank_lines('lines.txt'))[1]",
                2,
            ),
            _check(
                "Empty file",
                "(__import__('pathlib').Path('lines.txt').write_text('', encoding='utf-8'), "
                "nonblank_lines('lines.txt'))[1]",
                0,
            ),
            _check(
                "Whitespace only",
                "(__import__('pathlib').Path('lines.txt').write_text(' \\n\\t\\n', "
                "encoding='utf-8'), nonblank_lines('lines.txt'))[1]",
                0,
            ),
        ),
        ("Read the file with a with block.", "Test line.strip() before counting the line."),
    ),
    "paths-and-folders": _stage(
        "Repair a separate path helper. ensure_note(folder, text) must create missing parents, "
        "write text exactly inside folder/note.txt, and return the resulting Path. Joining the "
        "filename to the folder string by hand is the defect to diagnose.",
        """
        from pathlib import Path

        def ensure_note(folder, text):
            directory = Path(folder)
            directory.mkdir(parents=True, exist_ok=True)
            target = directory / "note.txt"
            target.write_text(text, encoding="utf-8")
            return target
        """,
        """
        from pathlib import Path

        def ensure_note(folder, text):
            target = Path(folder + "note.txt")
            target.write_text(text, encoding="utf-8")
            return target
        """,
        (
            _check(
                "Nested folder",
                "(lambda path: [path.as_posix(), path.read_text(encoding='utf-8')])"
                "(ensure_note('notes/deep', 'café'))",
                ["notes/deep/note.txt", "café"],
            ),
            _check(
                "Replace note",
                "(ensure_note('notes', 'old'), "
                "ensure_note('notes', 'new').read_text(encoding='utf-8'))[1]",
                "new",
            ),
        ),
        (
            "Create Path(folder) before joining a filename.",
            "mkdir(parents=True, exist_ok=True) handles missing folders.",
        ),
    ),
    "json-records": _stage(
        "Repair a separate JSON settings reader. load_preferences(path) must read a JSON object "
        "with enabled and label fields and return [enabled, label]. JSON's true and null values "
        "are valid here, so Python's display syntax is not a substitute for JSON parsing.",
        """
        import json

        def load_preferences(path):
            with open(path, encoding="utf-8") as handle:
                settings = json.load(handle)
            return [settings["enabled"], settings["label"]]
        """,
        """
        import ast

        def load_preferences(path):
            with open(path, encoding="utf-8") as handle:
                settings = ast.literal_eval(handle.read())
            return [settings["enabled"], settings["label"]]
        """,
        (
            _check(
                "JSON boolean and null",
                "(__import__('pathlib').Path('settings.json').write_text("
                "'{\"enabled\": true, \"label\": null}', encoding='utf-8'), "
                "load_preferences('settings.json'))[1]",
                [True, None],
            ),
            _check(
                "Unicode label",
                "(__import__('pathlib').Path('settings.json').write_text("
                '\'{"enabled": false, "label": "café"}\', encoding=\'utf-8\'), '
                "load_preferences('settings.json'))[1]",
                [False, "café"],
            ),
        ),
        (
            "Open the file with a with block and call json.load.",
            "JSON uses true, false, and null spellings that are not Python literals.",
        ),
    ),
    "csv-tables": _stage(
        "Repair a separate CSV function. total_quantities(path) must add the quantity column "
        "from every data row, including rows whose item name contains a quoted comma. A header "
        "only file returns zero.",
        """
        import csv

        def total_quantities(path):
            total = 0
            with open(path, newline="", encoding="utf-8") as handle:
                for row in csv.DictReader(handle):
                    total += int(row["quantity"])
            return total
        """,
        """
        import csv

        def total_quantities(path):
            total = 0
            with open(path, newline="", encoding="utf-8") as handle:
                for row in csv.DictReader(handle):
                    total += int(row["price"])
            return total
        """,
        (
            _check(
                "Quoted item",
                "(__import__('pathlib').Path('table.csv').write_text("
                "'item,quantity,price\\n\"pen, blue\",2,3\\nbook,1,8\\n', "
                "encoding='utf-8'), total_quantities('table.csv'))[1]",
                3,
            ),
            _check(
                "Header only",
                "(__import__('pathlib').Path('table.csv').write_text("
                "'item,quantity,price\\n', encoding='utf-8'), total_quantities('table.csv'))[1]",
                0,
            ),
            _check(
                "Zero quantity",
                "(__import__('pathlib').Path('table.csv').write_text("
                "'item,quantity,price\\nbox,0,9\\n', encoding='utf-8'), "
                "total_quantities('table.csv'))[1]",
                0,
            ),
        ),
        (
            "DictReader names the columns for you.",
            "Convert row['quantity'] to int and add that field, not price.",
        ),
    ),
    "regex-validation": _stage(
        "Repair a separate text validator. valid_ticket(text) must accept exactly three lowercase "
        "ASCII letters, a colon, and two ASCII digits. Reject matching fragments, extra text, "
        "spaces, and non-ASCII digits.",
        """
        import re

        def valid_ticket(text):
            return re.fullmatch(r"[a-z]{3}:[0-9]{2}", text) is not None
        """,
        """
        import re

        def valid_ticket(text):
            return re.search(r"[a-z]{3}:[0-9]{2}", text) is not None
        """,
        (
            _check("Valid ticket", "valid_ticket('abc:12')", True),
            _check("Extra text", "valid_ticket('xabc:12y')", False),
            _check("Uppercase", "valid_ticket('ABC:12')", False),
            _check("Unicode digit", "valid_ticket('abc:１２')", False),
        ),
        (
            "Use fullmatch so the complete string is checked.",
            "Use [0-9] when the contract calls for ASCII digits.",
        ),
    ),
    "regex-transformations": _stage(
        "Repair a separate text masker. mask_mentions(text) must replace every complete @name "
        "mention, where name contains lowercase ASCII letters, with @hidden. Return the changed "
        "text and leave invalid mentions untouched.",
        """
        import re

        def mask_mentions(text):
            return re.sub(r"@[a-z]+", "@hidden", text)
        """,
        """
        import re

        def mask_mentions(text):
            return re.sub(r"@[a-z]+", "@hidden", text, count=1)
        """,
        (
            _check("Two mentions", "mask_mentions('@ada met @bob')", "@hidden met @hidden"),
            _check("Repeated mention", "mask_mentions('@ada and @ada')", "@hidden and @hidden"),
            _check("Invalid mention", "mask_mentions('@Ada @bob2')", "@Ada @hidden2"),
        ),
        (
            "re.sub replaces every match by default.",
            "A count of one limits replacement to the first match, which is the defect.",
        ),
    ),
    "expense-report": _stage(
        "Repair a separate expense counter. category_counts(source, destination) must count the "
        "number of rows in each category, save that dictionary as JSON, and return it. Repeated "
        "categories must increase their existing count.",
        """
        import csv
        import json

        def category_counts(source, destination):
            counts = {}
            with open(source, newline="", encoding="utf-8") as handle:
                for row in csv.DictReader(handle):
                    category = row["category"]
                    counts[category] = counts.get(category, 0) + 1
            with open(destination, "w", encoding="utf-8") as handle:
                json.dump(counts, handle)
            return counts
        """,
        """
        import csv
        import json

        def category_counts(source, destination):
            counts = {}
            with open(source, newline="", encoding="utf-8") as handle:
                for row in csv.DictReader(handle):
                    counts[row["category"]] = 1
            with open(destination, "w", encoding="utf-8") as handle:
                json.dump(counts, handle)
            return counts
        """,
        (
            _check(
                "Repeated categories",
                "(__import__('pathlib').Path('expenses.csv').write_text("
                "'category,amount\\ntravel,250\\nfood,600\\ntravel,150\\n', "
                "encoding='utf-8'), category_counts('expenses.csv', 'counts.json'))[1]",
                {"travel": 2, "food": 1},
            ),
            _check(
                "Empty report",
                "(__import__('pathlib').Path('expenses.csv').write_text("
                "'category,amount\\n', encoding='utf-8'), "
                "category_counts('expenses.csv', 'counts.json'))[1]",
                {},
            ),
        ),
        (
            "Read each row before writing JSON.",
            "Use get(category, 0) + 1 so earlier rows are retained.",
        ),
    ),
    "your-own-modules": _stage(
        "Repair a separate conversion module. Create conversions.py with hours_to_minutes(hours) "
        "returning hours times 60, then import it in lesson.py under the same name. Both files "
        "must remain quiet when imported.",
        "",
        "",
        (
            _check("One hour", "hours_to_minutes(1)", 60),
            _check("No hours", "hours_to_minutes(0)", 0),
            _check("Several hours", "__import__('conversions').hours_to_minutes(7)", 420),
            _check("Imports are quiet", "__stdout__", ""),
        ),
        (
            "Put the function definition in conversions.py.",
            "Import it from lesson.py without calling it at module load time.",
        ),
        files=("lesson.py", "conversions.py"),
        starter_files={
            "lesson.py": "from conversions import hours_to_minutes\n",
            "conversions.py": code("""
                def hours_to_minutes(hours):
                    return hours + 60
            """),
        },
        reference_files={
            "lesson.py": "from conversions import hours_to_minutes\n",
            "conversions.py": code("""
                def hours_to_minutes(hours):
                    return hours * 60
            """),
        },
    ),
    "numeric-tools": _stage(
        "Repair a separate score summary. score_summary(values) must return (minimum, maximum, "
        "mean) for a nonempty list of numbers without changing it. The supplied program confuses "
        "the minimum and maximum positions.",
        """
        from statistics import mean

        def score_summary(values):
            return min(values), max(values), mean(values)
        """,
        """
        from statistics import mean

        def score_summary(values):
            return max(values), min(values), mean(values)
        """,
        (
            _check("Mixed values", "score_summary([9, 1, 5, 3])", (1, 9, 4.5)),
            _check("Repeated values", "score_summary([2, 2, 8])", (2, 8, 4)),
            _check("Negative values", "score_summary([-3, 0, 6])", (-3, 6, 1)),
        ),
        (
            "min and max each inspect the whole collection.",
            "The order of the returned tuple is minimum, maximum, then mean.",
        ),
    ),
    "repeatable-randomness": _stage(
        "Repair a separate seeded picker. pick_sequence(items, count, seed) must use a fresh "
        "Random(seed) for each call and return count choices in order. Repeated calls with the "
        "same inputs must match, and shared random state must not be reseeded.",
        """
        import random

        def pick_sequence(items, count, seed):
            if count < 0 or (count and not items):
                raise ValueError("invalid draw")
            generator = random.Random(seed)
            return [generator.choice(items) for _ in range(count)]
        """,
        """
        import random

        def pick_sequence(items, count, seed):
            if count < 0 or (count and not items):
                raise ValueError("invalid draw")
            random.seed(seed)
            return [random.choice(items) for _ in range(count)]
        """,
        (
            _check(
                "Seeded sequence",
                "pick_sequence(['red', 'blue', 'green'], 4, 7)",
                ["blue", "red", "blue", "green"],
            ),
            _check(
                "Repeat call",
                "pick_sequence(['red', 'blue', 'green'], 4, 7) == "
                "pick_sequence(['red', 'blue', 'green'], 4, 7)",
                True,
            ),
            _check(
                "Shared state unchanged",
                "(lambda module: (module.seed(123), (lambda before: "
                "(pick_sequence(['red'], 1, 7), module.getstate() == before)[1])"
                "(module.getstate())))(__import__('random'))",
                (None, True),
            ),
            _check("Zero draws", "pick_sequence([], 0, 7)", []),
        ),
        (
            "Create random.Random(seed), not a shared seeded generator.",
            "Call choice once for each requested draw.",
        ),
    ),
    "command-line-options": _stage(
        "Repair a separate command-line parser. make_tool_parser() must require a positional path "
        "and provide an integer --limit option defaulting to 10. Return the parser without parsing "
        "arguments in the function.",
        """
        import argparse

        def make_tool_parser():
            parser = argparse.ArgumentParser()
            parser.add_argument("path")
            parser.add_argument("--limit", type=int, default=10)
            return parser
        """,
        """
        import argparse

        def make_tool_parser():
            parser = argparse.ArgumentParser()
            parser.add_argument("path")
            parser.add_argument("--limit", default="0")
            return parser
        """,
        (
            _check(
                "Default",
                "vars(make_tool_parser().parse_args(['notes']))",
                {"path": "notes", "limit": 10},
            ),
            _check(
                "Explicit integer",
                "vars(make_tool_parser().parse_args(['notes', '--limit', '3']))",
                {"path": "notes", "limit": 3},
            ),
        ),
        ("Add the positional path first.", "Use type=int and default=10 for --limit."),
    ),
    "your-first-class": _stage(
        "Repair a separate Ledger class. Ledger starts with balance zero, add(amount) returns the "
        "new balance, and withdraw(amount) returns True only when it can afford the amount. An "
        "unsuccessful withdrawal must not change balance.",
        """
        class Ledger:
            def __init__(self):
                self.balance = 0

            def add(self, amount):
                self.balance += amount
                return self.balance

            def withdraw(self, amount):
                if amount > self.balance:
                    return False
                self.balance -= amount
                return True
        """,
        """
        class Ledger:
            def __init__(self):
                self.balance = 0

            def add(self, amount):
                self.balance += amount
                return self.balance

            def withdraw(self, amount):
                self.balance -= amount
                return self.balance >= 0
        """,
        (
            _check(
                "Successful and refused",
                "(lambda account: [account.add(8), account.withdraw(3), "
                "account.withdraw(10), account.balance])(Ledger())",
                [8, True, False, 5],
            ),
            _check(
                "Independent ledgers",
                "(lambda a, b: (a.add(5), b.balance)[1])(Ledger(), Ledger())",
                0,
            ),
            _check(
                "Exact withdrawal",
                "(lambda account: [account.add(6), account.withdraw(6), "
                "account.balance])(Ledger())",
                [6, True, 0],
            ),
        ),
        (
            "Check affordability before subtracting.",
            "A failed withdrawal returns False and leaves the balance unchanged.",
        ),
    ),
    "named-states": _stage(
        "Repair a separate Priority enum. Define Priority with LOW, MEDIUM, and HIGH values, and "
        "raise_priority(priority) so LOW becomes MEDIUM, MEDIUM becomes HIGH, and HIGH stays HIGH.",
        """
        from enum import Enum

        class Priority(Enum):
            LOW = "low"
            MEDIUM = "medium"
            HIGH = "high"

        def raise_priority(priority):
            if priority is Priority.LOW:
                return Priority.MEDIUM
            if priority is Priority.MEDIUM:
                return Priority.HIGH
            return Priority.HIGH
        """,
        """
        from enum import Enum

        class Priority(Enum):
            LOW = "low"
            MEDIUM = "medium"
            HIGH = "high"

        def raise_priority(priority):
            if priority is Priority.LOW:
                return Priority.MEDIUM
            return Priority.LOW
        """,
        (
            _check(
                "Members",
                "[(item.name, item.value) for item in Priority]",
                [("LOW", "low"), ("MEDIUM", "medium"), ("HIGH", "high")],
            ),
            _check("Raise low", "raise_priority(Priority.LOW) is Priority.MEDIUM", True),
            _check("Raise medium", "raise_priority(Priority.MEDIUM) is Priority.HIGH", True),
            _check("High is final", "raise_priority(Priority.HIGH) is Priority.HIGH", True),
        ),
        (
            "Give the three members their fixed string values.",
            "Handle LOW, MEDIUM, and HIGH separately so the final state does not go backward.",
        ),
    ),
    "tests-for-your-code": _stage(
        "Repair a separate range function. Define between(value, low, high), then a RangeTests "
        "TestCase with test_below, test_inside, and test_above. The provided function has a "
        "reversed lower-bound comparison.",
        """
        import unittest

        def between(value, low, high):
            if value < low:
                return low
            if value > high:
                return high
            return value

        class RangeTests(unittest.TestCase):
            def test_below(self):
                self.assertEqual(between(-2, 0, 10), 0)

            def test_inside(self):
                self.assertEqual(between(5, 0, 10), 5)

            def test_above(self):
                self.assertEqual(between(12, 0, 10), 10)
        """,
        """
        import unittest

        def between(value, low, high):
            if value > low:
                return low
            if value > high:
                return high
            return value

        class RangeTests(unittest.TestCase):
            def test_below(self):
                self.assertEqual(between(-2, 0, 10), 0)

            def test_inside(self):
                self.assertEqual(between(5, 0, 10), 5)

            def test_above(self):
                self.assertEqual(between(12, 0, 10), 10)
        """,
        (
            _check("Lower bound", "between(-2, 0, 10)", 0),
            _check("Inside range", "between(5, 0, 10)", 5),
            _check("Upper bound", "between(12, 0, 10)", 10),
            _check(
                "Tests pass",
                "(lambda result: [result.testsRun >= 3, result.wasSuccessful()])"
                "(__import__('unittest').defaultTestLoader.loadTestsFromTestCase("
                "RangeTests).run(__import__('unittest').TestResult()))",
                [True, True],
            ),
        ),
        (
            "A value below low should return low.",
            "Use the test names to identify which boundary comparison is reversed.",
        ),
    ),
    "task-workspace": _stage(
        "Repair a separate notebook application. Keep Notebook in notes.py and make lesson.py "
        "return a copy of its note titles from list_notes(titles). A caller editing the returned "
        "list must not edit the Notebook's stored list.",
        "",
        "",
        (
            _check("Clean notes", "list_notes([' Read ', '', 'Read', 'Walk'])", ["Read", "Walk"]),
            _check("Empty input", "list_notes([])", []),
            _check(
                "Returned list is independent",
                "(lambda book: (book.add('Read'), book.list_notes().append('Injected'), "
                "book.list_notes())[2])(Notebook())",
                ["Read"],
            ),
        ),
        (
            "Put cleanup and duplicate checks in Notebook.add.",
            "Return a copy of the stored titles so callers can edit their result safely.",
        ),
        files=("lesson.py", "notes.py"),
        starter_files={
            "lesson.py": code("""
                from notes import Notebook

                def list_notes(titles):
                    book = Notebook()
                    for title in titles:
                        book.add(title)
                    return book.list_notes()
            """),
            "notes.py": code("""
                class Notebook:
                    def __init__(self):
                        self.items = []

                    def add(self, title):
                        clean = title.strip()
                        if clean and clean not in self.items:
                            self.items.append(clean)

                    def list_notes(self):
                        return self.items
            """),
        },
        reference_files={
            "lesson.py": code("""
                from notes import Notebook

                def list_notes(titles):
                    book = Notebook()
                    for title in titles:
                        book.add(title)
                    return book.list_notes()
            """),
            "notes.py": code("""
                class Notebook:
                    def __init__(self):
                        self.items = []

                    def add(self, title):
                        clean = title.strip()
                        if clean and clean not in self.items:
                            self.items.append(clean)

                    def list_notes(self):
                        return self.items.copy()
            """),
        },
    ),
    "comprehensions": _stage(
        "Repair a separate filter. odd_cubes(numbers) must return cubes of odd numbers, sorted "
        "from smallest to largest, retaining duplicate inputs. Zero and negative even numbers "
        "do not qualify.",
        """
        def odd_cubes(numbers):
            return sorted([number ** 3 for number in numbers if number % 2 != 0])
        """,
        """
        def odd_cubes(numbers):
            return sorted(set([number ** 3 for number in numbers if number % 2 == 0]))
        """,
        (
            _check("Odd values", "odd_cubes([3, -2, 1, 3, 0])", [1, 27, 27]),
            _check("No odd values", "odd_cubes([-2, 0])", []),
            _check(
                "Input unchanged", "(lambda values: (odd_cubes(values), values)[1])([3, 1])", [3, 1]
            ),
        ),
        (
            "Filter with number % 2 != 0.",
            "Use a list so duplicate inputs remain duplicate outputs.",
        ),
    ),
    "counting-and-grouping": _stage(
        "Repair a separate grouping function. group_by_first(words) must return a dictionary "
        "whose keys are first letters and whose values list the original words in order. Repeated "
        "words remain repeated and empty input returns an empty dictionary.",
        """
        def group_by_first(words):
            groups = {}
            for word in words:
                key = word[0]
                groups.setdefault(key, []).append(word)
            return groups
        """,
        """
        def group_by_first(words):
            groups = {}
            for word in words:
                key = word[0]
                groups[key] = [word]
            return groups
        """,
        (
            _check(
                "Grouped words",
                "group_by_first(['apple', 'ant', 'berry'])",
                {"a": ["apple", "ant"], "b": ["berry"]},
            ),
            _check("Repeated word", "group_by_first(['ada', 'ada'])", {"a": ["ada", "ada"]}),
            _check("Empty words", "group_by_first([])", {}),
        ),
        (
            "Create a new list only for a new key.",
            "Append later words to the existing list instead of replacing it.",
        ),
    ),
    "queues-with-deque": _stage(
        "Repair a separate queue function. serve_requests(waiting, arrivals, limit) must append "
        "arrivals and serve up to limit entries from the front, returning served and remaining. "
        "Inputs must stay unchanged.",
        """
        from collections import deque

        def serve_requests(waiting, arrivals, limit):
            queue = deque(waiting)
            queue.extend(arrivals)
            served = []
            while queue and len(served) < limit:
                served.append(queue.popleft())
            return served, list(queue)
        """,
        """
        from collections import deque

        def serve_requests(waiting, arrivals, limit):
            queue = deque(waiting)
            queue.extend(arrivals)
            served = []
            while queue and len(served) < limit:
                served.append(queue.pop())
            return served, list(queue)
        """,
        (
            _check("Arrival order", "serve_requests(['a', 'b'], ['c'], 2)", (["a", "b"], ["c"])),
            _check("No capacity", "serve_requests(['a'], ['b'], 0)", ([], ["a", "b"])),
            _check("More capacity", "serve_requests([], ['a', 'b'], 8)", (["a", "b"], [])),
        ),
        (
            "append adds arrivals at the right.",
            "popleft serves the oldest item; pop serves the newest item.",
        ),
    ),
    "dates-and-deadlines": _stage(
        "Repair a separate calendar helper. days_until(start, end) must return the number of days "
        "from the ISO start date to the ISO end date. The same date is zero days apart, and the "
        "result may be negative when end comes first.",
        """
        from datetime import date

        def days_until(start, end):
            return (date.fromisoformat(end) - date.fromisoformat(start)).days
        """,
        """
        from datetime import date

        def days_until(start, end):
            return (date.fromisoformat(end) - date.fromisoformat(start)).days + 1
        """,
        (
            _check("Year boundary", "days_until('2023-12-31', '2024-01-01')", 1),
            _check("Same day", "days_until('2024-05-10', '2024-05-10')", 0),
            _check("Leap day", "days_until('2024-02-28', '2024-03-01')", 2),
            _check("Backwards", "days_until('2024-05-10', '2024-05-08')", -2),
        ),
        (
            "Parse both strings with date.fromisoformat.",
            "Subtract start from end; do not count the starting day as elapsed.",
        ),
    ),
    "date-time-formats": _stage(
        "Repair a separate timestamp formatter. format_stamp(day, clock) must parse DD/MM/YYYY "
        "and HH:MM and return YYYY-MM-DD HH:MM without changing the time. The broken version "
        "swaps the day and month directives.",
        """
        from datetime import datetime

        def format_stamp(day, clock):
            value = datetime.strptime(day + " " + clock, "%d/%m/%Y %H:%M")
            return value.strftime("%Y-%m-%d %H:%M")
        """,
        """
        from datetime import datetime

        def format_stamp(day, clock):
            value = datetime.strptime(day + " " + clock, "%m/%d/%Y %H:%M")
            return value.strftime("%Y-%m-%d %H:%M")
        """,
        (
            _check("Day before month", "format_stamp('03/04/2024', '09:00')", "2024-04-03 09:00"),
            _check("Leap day", "format_stamp('29/02/2024', '23:30')", "2024-02-29 23:30"),
            _check("New year", "format_stamp('01/01/2025', '00:05')", "2025-01-01 00:05"),
        ),
        ("The input directive is %d/%m/%Y.", "The output directive is %Y-%m-%d %H:%M."),
    ),
    "validate-boundaries": _stage(
        "Repair a separate identifier validator. valid_identifier(name) accepts a nonempty name "
        "made only of letters, digits, and underscores, with a letter as its first character. "
        "Reject spaces, punctuation, and names beginning with a digit.",
        """
        def valid_identifier(name):
            if not name or not (name[0].isalpha() or name[0] == "_"):
                return False
            return all(character.isalnum() or character == "_" for character in name)
        """,
        """
        def valid_identifier(name):
            return name != ""
        """,
        (
            _check("Ordinary name", "valid_identifier('task_2')", True),
            _check("Empty", "valid_identifier('')", False),
            _check("Starts with digit", "valid_identifier('2task')", False),
            _check("Space", "valid_identifier('task name')", False),
            _check("Punctuation", "valid_identifier('task-name')", False),
        ),
        (
            "Check empty text and the first character before the rest.",
            "Every later character must be alphanumeric or underscore.",
        ),
    ),
    "copy-with-care": _stage(
        "Repair a separate safe copier. copy_if_missing(source, destination) must copy exact bytes "
        "only when destination is new. If it already exists, return False and preserve both files. "
        "Use exclusive creation and catch FileExistsError.",
        """
        import shutil

        def copy_if_missing(source, destination):
            with open(source, "rb") as input_file:
                try:
                    with open(destination, "xb") as output_file:
                        shutil.copyfileobj(input_file, output_file)
                except FileExistsError:
                    return False
            return True
        """,
        """
        import shutil

        def copy_if_missing(source, destination):
            with open(source, "rb") as input_file:
                with open(destination, "wb") as output_file:
                    shutil.copyfileobj(input_file, output_file)
            return True
        """,
        (
            _check(
                "New destination",
                "(__import__('pathlib').Path('source.bin').write_bytes(bytes([0, 255, 97])), "
                "(lambda result: [result, list(__import__('pathlib').Path("
                "'new.bin').read_bytes())])"
                "(copy_if_missing('source.bin', 'new.bin')))[1]",
                [True, [0, 255, 97]],
            ),
            _check(
                "Existing destination",
                "(__import__('pathlib').Path('source.txt').write_text('new'), "
                "__import__('pathlib').Path('dest.txt').write_text('keep'), "
                "(lambda result: [result, __import__('pathlib').Path('dest.txt').read_text()])"
                "(copy_if_missing('source.txt', 'dest.txt')))[2]",
                [False, "keep"],
            ),
        ),
        (
            "Open a new destination with xb, not wb.",
            "Catch FileExistsError and return False without reporting success.",
        ),
    ),
    "notes-archiver": _stage(
        "Repair a separate archive preview tool. In selection.py define eligible_md(source) for "
        "immediate lowercase .md files. In lesson.py define archive_markdown(source, destination, "
        "dry_run=True) that reports planned files without writing in dry-run mode and copies only "
        "when explicitly enabled.",
        "",
        "",
        (
            _check(
                "Dry run",
                "(__import__('pathlib').Path('inbox').mkdir(), "
                "__import__('pathlib').Path('inbox/a.md').write_text('A'), "
                "[archive_markdown('inbox', 'archive'), "
                "__import__('pathlib').Path('archive').exists()])[2]",
                [["a.md"], False],
            ),
            _check(
                "Write mode",
                "(__import__('pathlib').Path('inbox').mkdir(), "
                "__import__('pathlib').Path('inbox/a.md').write_text('A'), "
                "[archive_markdown('inbox', 'archive', dry_run=False), "
                "__import__('pathlib').Path('archive/a.md').read_text()])[2]",
                [["a.md"], "A"],
            ),
            _check(
                "Skip other suffix",
                "(__import__('pathlib').Path('inbox').mkdir(), "
                "__import__('pathlib').Path('inbox/a.txt').write_text('A'), "
                "archive_markdown('inbox', 'archive'))[2]",
                [],
            ),
        ),
        (
            "Keep mkdir and copying inside if not dry_run.",
            "Use eligible_md so selection and archiving share the same file rules.",
        ),
        files=("lesson.py", "selection.py"),
        starter_files={
            "lesson.py": code("""
                from pathlib import Path
                import shutil
                from selection import eligible_md

                def archive_markdown(source, destination, dry_run=True):
                    source = Path(source)
                    destination = Path(destination)
                    names = eligible_md(source)
                    if True:
                        destination.mkdir(parents=True, exist_ok=True)
                        for name in names:
                            with open(source / name, "rb") as input_file:
                                with open(destination / name, "xb") as output_file:
                                    shutil.copyfileobj(input_file, output_file)
                    return names
            """),
            "selection.py": code("""
                from pathlib import Path

                def eligible_md(source):
                    return sorted(
                        path.name
                        for path in Path(source).iterdir()
                        if path.is_file() and path.suffix == ".md"
                    )
            """),
        },
        reference_files={
            "lesson.py": code("""
                from pathlib import Path
                import shutil
                from selection import eligible_md

                def archive_markdown(source, destination, dry_run=True):
                    source = Path(source)
                    destination = Path(destination)
                    names = eligible_md(source)
                    if not dry_run:
                        destination.mkdir(parents=True, exist_ok=True)
                        for name in names:
                            with open(source / name, "rb") as input_file:
                                try:
                                    with open(destination / name, "xb") as output_file:
                                        shutil.copyfileobj(input_file, output_file)
                                except FileExistsError:
                                    continue
                    return names
            """),
            "selection.py": code("""
                from pathlib import Path

                def eligible_md(source):
                    return sorted(
                        path.name
                        for path in Path(source).iterdir()
                        if path.is_file() and not path.is_symlink() and path.suffix == ".md"
                    )
            """),
        },
    ),
}
