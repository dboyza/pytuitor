"""Stage contracts for b-collections."""

from pytuitor.beginner_authoring import _check, _stage

BUILD_INSTRUCTIONS = {
    "pack-your-bag": (
        "Read one line of space-separated integers into a list named `pouches`.\nAn"
        "y input prompt is fine.\nCalculate their sum in a variable named `total`, "
        "starting at zero, and print it once after the loop.\n\nFor `2 5 1`, print "
        "`8`.\nAn empty input line prints `0`; negative integers reduce the total."
        "\nKeep `pouches` and `total` available for checks.\nUse the input-handling"
        " pattern above, then add your total calculation."
    ),
    "list-positions": (
        "Read one line of space-separated words into a list called `items`.\nSet `f"
        "irst` to the first word and `last` to the last word.\nIf there are no word"
        's, set both variables to `"empty"`.\nPrint `first`, then `last`, on separa'
        "te lines.\nA one-word input should print that word twice."
    ),
    "tuples-and-sets": (
        "Read two input lines; you may choose any prompts.\nThe first line contains"
        " exactly two space-separated names.\nStore them as a tuple called `pair`, "
        "then assign its first item to `first` and its second item to `second`.\nTh"
        "e second line contains zero or more space-separated visitor names, possibl"
        "y repeated.\nStore the distinct visitors in a set called `seen`.\nNames ar"
        "e case-sensitive, so `Ada` and `ada` are different.\n\nPrint three lines: "
        "whether `first` is in `seen`, whether `second` is in `seen`, and the numbe"
        "r of distinct visitors.\nUse Python's `True` and `False` spelling for memb"
        "ership results.\nFor first line `Mira Sol` and second line `Sol Sol Bo`, p"
        "rint `False`, `True`, and `2` on separate lines.\nFor an empty second line"
        ", print `False`, `False`, and `0`.\nKeep `pair`, `first`, `second`, and `s"
        "een` available for checks; do not print the set itself, since its order is"
        " not guaranteed."
    ),
    "comparing-sets": (
        "Read two lines of space-separated words, with any prompts.\nEither line ma"
        "y be empty, and duplicate words count once.\nStore the first line's set as"
        " `required` and the second as `available`.\nCreate `shared`, `missing`, `c"
        "ombined`, and `exclusive` as sets representing intersection, missing requi"
        "rements, union, and symmetric difference respectively.\nSet `ready` to whe"
        "ther every requirement is available, including when there are no requireme"
        "nts.\nComparisons are case-sensitive.\nFor `rope lamp` and `lamp food`, on"
        "ly `lamp` is shared and only `rope` is missing.\nPrinting is optional; che"
        "cks inspect your result variables."
    ),
    "loop-helpers": (
        "Read three input lines, with any prompts you choose.\nThe first is a nonne"
        "gative whole number called `count`.\nThe second contains space-separated n"
        "ames; store its split result in `names`.\nThe third contains space-separat"
        "ed colors; store its split result in `colors`.\nEither word line may be em"
        "pty.\n\nCreate these three result lists:\n\n- `slots`: integers from `1` t"
        "hrough `count`, inclusive; use `[]` when `count` is zero.\n- `numbered`: a"
        " tuple `(number, name)` for each name, counting from `1` in input order.\n"
        "- `pairs`: a tuple `(name, color)` for each corresponding name and color, "
        "stopping at the shorter input list.\n\nStart each result as an empty list "
        "and append its values inside a loop, or use another implementation that pr"
        "oduces the same results.\nTo append one pair, write `result.append((left, "
        "right))`; the inner parentheses create the tuple passed to `append`.\nTry "
        "`range`, `enumerate`, and `zip` for the three loops.\nChecks compare the l"
        "ists and tuples, so printing is optional.\nYou may print all three lists t"
        "o inspect them with Run.\n\nFor input lines `2`, `Mira Sol`, and `red`, th"
        'e results are `slots = [1, 2]`, `numbered = [(1, "Mira"), (2, "Sol")]`, an'
        'd `pairs = [("Mira", "red")]`.\nPreserve duplicate names and colors in the'
        "ir original positions.\nIf both word lines are empty, `numbered` and `pair"
        "s` are both empty regardless of `count`."
    ),
    "nested-collections": (
        "Read a nonnegative integer `count` on the first line, then exactly `count`"
        " lines of space-separated integers.\nEach row may be empty or a different "
        "length.\nNegative integers and repeated values are valid.\nUse any input p"
        "rompts.\nBuild a list of lists named `grid` using `int()` on each word.\n"
        "\nCreate `row_totals`, with one sum per row, including zero for empty rows"
        ".\nCreate `flat`, containing every value in row order and then column orde"
        "r.\nCreate `positions`, containing tuples `(row_index, column_index, value"
        ")` for those values, using zero-based indexes.\nReset a row's sum before i"
        "ts inner loop and append the sum after that loop.\nWith rows `[2, 3]` and "
        "`[4]`, the totals are `[5, 4]`, flat values are `[2, 3, 4]`, and positions"
        " are `[(0, 0, 2), (0, 1, 3), (1, 0, 4)]`.\nFor zero rows, all four lists a"
        "re empty.\nPrinting is optional."
    ),
    "word-counts": (
        "Read space-separated words from one input line.\nCreate a dictionary calle"
        "d `counts` whose keys are the words and whose values are the number of tim"
        "es each word appears.\nTreat `Cat` and `cat` as different words.\nAn empty"
        " input produces `{}`.\nYou may print `counts` so Run shows your result.\nC"
        "hecks compare the dictionary itself, so printing is optional and key order"
        " does not matter."
    ),
    "editing-collections": (
        "Read three lines: space-separated `items`, one word `target`, and one word"
        " `incoming`.\nOnly the first line may be empty; use any prompts.\nRemove j"
        "ust the first occurrence of `target` from `items`, if present.\nInsert `in"
        "coming` at the beginning, then sort `items` using Python's case-sensitive "
        "string ordering.\nFor ordinary English letters, uppercase letters come bef"
        'ore lowercase letters: `"Z"` sorts before `"a"`.\nBuild `counts`, mapping '
        "each resulting item to its count.\nThen remove the `target` entry from `co"
        "unts`, saving its former value in `removed`, or zero when absent.\nCreate "
        "`keys` as a sorted list of the remaining dictionary keys.\nDo not remove a"
        "ny further items from the list when deleting the dictionary entry.\nPrinti"
        "ng is optional.\n\nFor `pear apple pear`, `pear`, `pear`, the final list i"
        "s `['apple', 'pear', 'pear']`, counts is `{'apple': 1}`, removed is `2`, a"
        "nd keys is `['apple']`."
    ),
    "repeat-until-done": (
        "Keep reading one integer per input line until the user enters `0`.\nAdd al"
        "l the nonzero integers into a variable called `total`, initially zero.\nSt"
        "op immediately at `0` and print `total` once after the loop.\nInputs are a"
        "lways valid integers; negative numbers are allowed and reduce the total.\n"
        "Input lines `5`, `-2`, `0` should print `3`.\nIf the first line is `0`, pr"
        "int `0`.\nCheck supplies the stopping zero automatically.\nWhen using Run,"
        " remember to type it yourself."
    ),
    "supply-report": (
        "Read one space-separated input line.\nCreate `counts`, a dictionary counti"
        "ng each word, and `order`, a list containing each distinct word once in th"
        "e order it first appeared.\nPrint one line per word in `order`, formatted "
        "`word: count`.\nPrint `No supplies` if the input is empty.\nFor `rope lamp"
        " rope map lamp`, print:\n\n```text\nrope: 2\nlamp: 2\nmap: 1\n```\n\nPrese"
        "rve capitalization and do not alphabetize the report.\nYou do not need to "
        "define your own functions yet.\nCreate the empty list and dictionary befor"
        "e the loop, then decide which changes happen inside it."
    ),
}

REPAIR_STAGES = {
    "pack-your-bag": _stage(
        (
            "Repair the snack budget. Start budget at 20 credits. Read one line of spac"
            "e-separated integer costs into costs, then subtract each cost from budget "
            "and print what remains. An empty line leaves 20; negative costs are refund"
            "s that increase the budget. For 2 5 1, print 12. The final budget may be n"
            "egative."
        ),
        """
        costs = []
        for text in input("Snack costs: ").split():
            costs.append(int(text))
        budget = 20
        for cost in costs:
            budget -= cost
        print(budget)
        """,
        """
        costs = []
        for text in input("Snack costs: ").split():
            costs.append(int(text))
        budget = 20
        for cost in costs:
            budget = 20 - cost
        print(budget)
        """,
        (
            _check(
                "Several costs",
                ("budget"),
                12,
                stdin="2 5 1\n",
                output="12",
            ),
            _check(
                "Empty costs",
                ("budget"),
                20,
                stdin="\n",
                output="20",
            ),
            _check(
                "Refund",
                ("budget"),
                11,
                stdin="10 -3 2\n",
                output="11",
            ),
            _check(
                "Over budget",
                ("budget"),
                -5,
                stdin="10 15\n",
                output="-5",
            ),
        ),
        (
            ("Trace the remaining budget after each purchase."),
            ("Subtract each cost from the current budget, rather than starting from 20 again."),
        ),
        stdin="2 5 1\n",
    ),
    "list-positions": _stage(
        (
            "Repair the route preview. Read one line of space-separated stops into stop"
            "s. Store its first two entries as list preview and every later entry as li"
            "st later. Print preview, then later, on two lines. Preserve order and dupl"
            "icates. With fewer than two stops, preview contains all stops and later is"
            " empty. An empty input line produces two empty lists."
        ),
        """
        stops = input("Route stops: ").split()
        preview = stops[:2]
        later = stops[2:]
        print(preview)
        print(later)
        """,
        """
        stops = input("Route stops: ").split()
        preview = stops[1:3]
        later = stops[1:]
        print(preview)
        print(later)
        """,
        (
            _check(
                "Long route",
                "[preview, later]",
                [["port", "hill"], ["lake", "home"]],
                stdin="port hill lake home\n",
                output="['port', 'hill']\n['lake', 'home']",
            ),
            _check(
                "Two stops",
                "[preview, later]",
                [["port", "hill"], []],
                stdin="port hill\n",
                output="['port', 'hill']\n[]",
            ),
            _check(
                "One stop",
                "[preview, later]",
                [["home"], []],
                stdin="home\n",
                output="['home']\n[]",
            ),
            _check("No stops", "[preview, later]", [[], []], stdin="\n", output="[]\n[]"),
            _check(
                "Repeated stops",
                "[preview, later]",
                [["port", "port"], ["port"]],
                stdin="port port port\n",
                output="['port', 'port']\n['port']",
            ),
        ),
        (
            "A slice starts at its first index and stops before its second index.",
            "The first two positions are 0 and 1: use [:2] for preview and [2:] for later.",
        ),
        stdin="port hill lake home\n",
    ),
    "tuples-and-sets": _stage(
        (
            "Repair the checkpoint tracker. Read one line of checkpoint names into tupl"
            "e route, then a second line of visited names into set visited. Build remai"
            "ning as a list of route entries not yet visited, retaining route order and"
            " repeated checkpoints. Print the number of distinct visited names, then re"
            "maining, on two lines. Either input line may be empty; comparisons are cas"
            "e-sensitive."
        ),
        """
        route = tuple(input("Route: ").split())
        visited = set(input("Visited: ").split())
        remaining = []
        for checkpoint in route:
            if checkpoint not in visited:
                remaining.append(checkpoint)
        print(len(visited))
        print(remaining)
        """,
        """
        route = tuple(input("Route: ").split())
        visited = list(input("Visited: ").split())
        remaining = []
        for checkpoint in route:
            if checkpoint in visited:
                remaining.append(checkpoint)
        print(len(visited))
        print(remaining)
        """,
        (
            _check(
                "Repeated visits",
                (
                    "[list(route), sorted(visited), remaining, isinstance(route, tuple), "
                    "isinstance(visited, set)]"
                ),
                [["port", "hill", "lake", "hill"], ["lake", "port"], ["hill", "hill"], True, True],
                stdin="port hill lake hill\nport port lake\n",
                output="2\n['hill', 'hill']",
            ),
            _check(
                "No visits",
                ("remaining"),
                ["port", "hill"],
                stdin="port hill\n\n",
                output="0\n['port', 'hill']",
            ),
            _check(
                "Empty route",
                ("remaining"),
                [],
                stdin="\nport\n",
                output="1\n[]",
            ),
            _check(
                "Case matters",
                ("remaining"),
                ["Port"],
                stdin="Port port\nport\n",
                output="1\n['Port']",
            ),
            _check(
                "Both empty",
                ("remaining"),
                [],
                stdin="\n\n",
                output="0\n[]",
            ),
        ),
        (
            ("A checkpoint belongs in remaining only when it has not been visited."),
            ("Use a set to count distinct visits and not in to select unvisited checkpoints."),
        ),
        stdin="port hill lake hill\nport port lake\n",
    ),
    "comparing-sets": _stage(
        (
            "Repair the release gate. Read three lines of space-separated names as sets"
            " required, installed, and blocked. Create usable containing installed name"
            "s that are not blocked, and missing containing requirements not in usable."
            " Set ready to whether no requirements are missing. All comparisons are cas"
            "e-sensitive; any line may be empty and duplicates count once. Blocked name"
            "s must never become usable. Printing is optional."
        ),
        """
        required = set(input("Required: ").split())
        installed = set(input("Installed: ").split())
        blocked = set(input("Blocked: ").split())
        usable = installed - blocked
        missing = required - usable
        ready = required <= usable
        """,
        """
        required = set(input("Required: ").split())
        installed = set(input("Installed: ").split())
        blocked = set(input("Blocked: ").split())
        usable = installed | blocked
        missing = required - usable
        ready = required <= usable
        """,
        (
            _check(
                "Blocked requirement",
                ("[sorted(usable), sorted(missing), ready]"),
                [["core"], ["plugin"], False],
                stdin="core plugin\ncore plugin\nplugin\n",
                output=None,
            ),
            _check(
                "Everything available",
                ("[sorted(usable), sorted(missing), ready]"),
                [["core", "plugin"], [], True],
                stdin="core plugin\nplugin core core\n\n",
                output=None,
            ),
            _check(
                "Blocked is not installed",
                ("[sorted(usable), sorted(missing), ready]"),
                [["core"], ["plugin"], False],
                stdin="plugin\ncore\nplugin\n",
                output=None,
            ),
            _check(
                "No requirements",
                ("[sorted(usable), sorted(missing), ready]"),
                [[], [], True],
                stdin="\ncore\ncore\n",
                output=None,
            ),
            _check(
                "Case matters",
                ("[sorted(usable), sorted(missing), ready]"),
                [["Core"], [], True],
                stdin="Core\nCore core\ncore\n",
                output=None,
            ),
            _check(
                "All empty",
                ("[sorted(usable), sorted(missing), ready]"),
                [[], [], True],
                stdin="\n\n\n",
                output=None,
            ),
        ),
        (
            ("Trace how blocked names affect usable before inspecting missing."),
            ("Set difference removes blocked names; union adds them."),
        ),
        stdin="core plugin\ncore plugin\nplugin\n",
    ),
    "loop-helpers": _stage(
        (
            "Repair a separate packing program. Read labels and whole-number weights fr"
            "om two lines and create labelled as tuples numbered from 1, stopping at th"
            "e shorter list. Each tuple is (number, label, weight). Empty input must pr"
            "oduce an empty list. You may print labelled to see it in Run; printing is "
            "optional."
        ),
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
            _check("Empty input", "labelled", [], stdin="\n\n"),
            _check("Fewer weights", "labelled", [(1, "a", 4)], stdin="a b\n4\n"),
            _check("Fewer labels", "labelled", [(1, "a", 4)], stdin="a\n4 7\n"),
        ),
        (
            "zip stops at the shorter input.",
            "Use a one-based number and keep the label before its weight in each tuple.",
        ),
        stdin="Mira Sol\n3 5\n",
    ),
    "nested-collections": _stage(
        (
            "Repair a grid transformer. Read a nonnegative row count, then that many li"
            "nes of space-separated integers into grid. Rows may be empty or different "
            "lengths. Create lengths with one length per row, and doubled with a separa"
            "te list per row containing twice each value. Preserve empty rows. Printing"
            " is optional."
        ),
        """
        count = int(input("Rows: "))
        grid = []
        for number in range(count):
            row = []
            for text in input("Row: ").split():
                row.append(int(text))
            grid.append(row)
        lengths = []
        doubled = []
        for row in grid:
            lengths.append(len(row))
            changed = []
            for value in row:
                changed.append(value * 2)
            doubled.append(changed)
        """,
        """
        count = int(input("Rows: "))
        grid = []
        for number in range(count):
            row = []
            for text in input("Row: ").split():
                row.append(int(text))
            grid.append(row)
        lengths = []
        doubled = []
        changed = []
        for row in grid:
            lengths.append(len(row))
            for value in row:
                changed.append(value * 2)
            doubled.append(changed)
        """,
        (
            _check(
                "Unequal rows",
                "[lengths, doubled]",
                [[2, 1], [[4, 6], [8]]],
                stdin="2\n2 3\n4\n",
                output=None,
            ),
            _check(
                "Empty middle row",
                "[lengths, doubled]",
                [[1, 0, 2], [[2], [], [-10, 10]]],
                stdin="3\n1\n\n-5 5\n",
                output=None,
            ),
            _check("No rows", "[lengths, doubled]", [[], []], stdin="0\n", output=None),
        ),
        (
            "Each row needs its own output list.",
            "Create changed inside the outer loop, before the inner loop.",
        ),
        stdin="2\n2 3\n4\n",
    ),
    "word-counts": _stage(
        (
            "Repair the sighting index. Read one line of space-separated words. Build r"
            "ecords as a list of (word, count) tuples, one per distinct word in first a"
            "ppearance order. Repeated words increase the count without adding another "
            "tuple. Names are case-sensitive; empty input gives an empty list. Printing"
            " is optional."
        ),
        """
        frequencies = {}
        first_seen = []
        for word in input("Sightings: ").split():
            if word not in frequencies:
                first_seen.append(word)
                frequencies[word] = 0
            frequencies[word] += 1
        records = []
        for word in first_seen:
            records.append((word, frequencies[word]))
        """,
        """
        frequencies = {}
        first_seen = []
        for word in input("Sightings: ").split():
            if word not in frequencies:
                first_seen.append(word)
                frequencies[word] = 0
            frequencies[word] = 1
        records = []
        for word in first_seen:
            records.append((word, frequencies[word]))
        """,
        (
            _check(
                "Repeated words",
                "records",
                [("bee", 2), ("ant", 1)],
                stdin="bee ant bee\n",
                output=None,
            ),
            _check("Empty words", "records", [], stdin="\n", output=None),
            _check(
                "Case-sensitive words",
                "records",
                [("Cat", 2), ("cat", 1)],
                stdin="Cat cat Cat\n",
                output=None,
            ),
        ),
        (
            "Remember first appearances separately from frequencies.",
            "Increase the existing frequency instead of resetting it.",
        ),
        stdin="bee ant bee\n",
    ),
    "editing-collections": _stage(
        (
            "Repair the roster editor. Read three lines: space-separated names, one nam"
            "e to remove, and one name to add. Keep the list as roster. Remove only the"
            " first match if present, insert the new name at the front, then sort the l"
            "ist. Create frequencies counting every remaining name. Names are case-sens"
            "itive; the first line may be empty. Printing is optional."
        ),
        """
        roster = input("Roster: ").split()
        remove = input("Remove: ")
        addition = input("Add: ")
        if remove in roster:
            roster.remove(remove)
        roster.insert(0, addition)
        roster.sort()
        frequencies = {}
        for name in roster:
            frequencies[name] = frequencies.get(name, 0) + 1
        """,
        """
        roster = input("Roster: ").split()
        remove = input("Remove: ")
        addition = input("Add: ")
        if remove in roster:
            roster.remove(remove)
        roster.insert(0, addition)
        frequencies = {}
        for name in roster:
            frequencies[name] = 1
        """,
        (
            _check(
                "Keep duplicates",
                "[roster, frequencies]",
                [["apple", "pear", "pear"], {"apple": 1, "pear": 2}],
                stdin="pear apple pear\npear\npear\n",
                output=None,
            ),
            _check(
                "Absent target",
                "[roster, frequencies]",
                [["apple", "pear"], {"apple": 1, "pear": 1}],
                stdin="pear\nplum\napple\n",
                output=None,
            ),
            _check(
                "Empty roster",
                "[roster, frequencies]",
                [["z"], {"z": 1}],
                stdin="\nx\nz\n",
                output=None,
            ),
        ),
        (
            "Sort roster after inserting the new name.",
            "Increase a previous count when a name repeats.",
        ),
        stdin="pear apple pear\npear\npear\n",
    ),
    "repeat-until-done": _stage(
        (
            "Repair the adjustment log. Read one integer per line until 99, which is a "
            "stopping signal and must not be added. Add all earlier integers into "
            "balance, initially zero, and print balance once. Zero and negative "
            "adjustments are valid. Check supplies 99; type it yourself in Run."
        ),
        """
        balance = 0
        while True:
            adjustment = int(input("Adjustment (99 to finish): "))
            if adjustment == 99:
                break
            balance += adjustment
        print(balance)
        """,
        """
        balance = 0
        while True:
            adjustment = int(input("Adjustment (99 to finish): "))
            if balance >= 0:
                break
            balance += adjustment
        print(balance)
        """,
        (
            _check("Several adjustments", "balance", 3, stdin="5\n-2\n99\n", output="3"),
            _check("Stop immediately", "balance", 0, stdin="99\n", output="0"),
            _check("Zero is not the stop", "balance", 4, stdin="0\n4\n99\n", output="4"),
            _check("Total crosses zero", "balance", 3, stdin="-2\n2\n3\n99\n", output="3"),
        ),
        (
            "Check the latest adjustment before adding it.",
            "Only the input value 99 stops this loop.",
        ),
        stdin="5\n-2\n99\n",
    ),
    "supply-report": _stage(
        (
            "Repair the delivery report. Read one line of space-separated items and cou"
            "nt them in stock. Create names as the sorted list of distinct items. Print"
            ' one "name: count" line per name in alphabetical order, or "No delivery" f'
            "or empty input. Preserve case. Unlike Build, this report sorts the names."
        ),
        """
        stock = {}
        for item in input("Delivery: ").split():
            stock[item] = stock.get(item, 0) + 1
        names = sorted(stock.keys())
        if len(names) == 0:
            print("No delivery")
        else:
            for name in names:
                print(f"{name}: {stock[name]}")
        """,
        """
        stock = {}
        for item in input("Delivery: ").split():
            stock[item] = 1
        names = list(stock.keys())
        if len(names) == 0:
            print("No delivery")
        else:
            for name in names:
                print(f"{name}: {stock[name]}")
        """,
        (
            _check(
                "Repeated delivery",
                "[stock, names]",
                [{"rope": 2, "lamp": 2, "map": 1}, ["lamp", "map", "rope"]],
                stdin="rope lamp rope map lamp\n",
                output="lamp: 2\nmap: 1\nrope: 2",
            ),
            _check(
                "Empty delivery", "[stock, names]", [{}, []], stdin="\n", output=("No delivery")
            ),
            _check(
                "Case matters",
                "[stock, names]",
                [{"ada": 2, "Ada": 1}, ["Ada", "ada"]],
                stdin="ada Ada ada\n",
                output="Ada: 1\nada: 2",
            ),
        ),
        (
            "Count every occurrence before printing.",
            "Sort the distinct names, then look up their final counts.",
        ),
        stdin="rope lamp rope map lamp\n",
    ),
}
