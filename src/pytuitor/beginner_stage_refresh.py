"""Stage-specific exercise content for the refreshed beginner course."""

from dataclasses import replace

from pytuitor.models import Check, StageContract, code


def _check(
    label: str,
    expression: str,
    expected: object,
    *,
    stdin: str | None = None,
    output: str | None = None,
    nudge: str = "",
    description: str | None = None,
) -> Check:
    return Check(
        label,
        expression,
        expected,
        nudge,
        stdin=stdin,
        expected_output=output,
        description=description
        or (label if "lambda" in expression or "__import__" in expression else expression),
    )


def _scenario_check(
    label: str, script: str, expected: object, *, description: str, nudge: str
) -> Check:
    """Run a multi-step check and inspect result in the worker's fresh namespace."""
    return _check(
        label,
        f"(exec({code(script)!r}), result)[1]",
        expected,
        description=description,
        nudge=nudge,
    )


def _stage(
    instructions: str,
    reference: str,
    starter: str,
    checks: tuple[Check, ...],
    hints: tuple[str, ...],
    *,
    stdin: str = "",
    files: tuple[str, ...] = ("lesson.py",),
    starter_files: dict[str, str] | None = None,
    reference_files: dict[str, str] | None = None,
) -> StageContract:
    if starter_files is None:
        starter_files = {"lesson.py": code(starter)}
    if reference_files is None:
        reference_files = {"lesson.py": code(reference)}
    return StageContract(
        instructions=instructions,
        checks=tuple(check if check.nudge else replace(check, nudge=hints[0]) for check in checks),
        hints=tuple(hints),
        stdin=stdin,
        files=tuple(files),
        starter_files=starter_files,
        reference_files=reference_files,
    )


BUILD_INSTRUCTIONS = {
    ("pack-your-bag"): (
        "Read one line of space-separated integers into a list named `pouches`.\nAny "
        "input prompt is fine.\nCalculate their sum in a variable named `total`, starting "
        "at zero, and print it once after the loop.\n\nFor `2 5 1`, print `8`.\nAn empty "
        "input line prints `0`; negative integers reduce the total.\nKeep `pouches` and "
        "`total` available for checks.\nUse the input-handling pattern above, then add "
        "your total calculation."
    ),
    ("list-positions"): (
        "Read one line of space-separated words into a list called `items`.\nSet `first` "
        "to the first word and `last` to the last word.\nIf there are no words, set both "
        'variables to `"empty"`.\nPrint `first`, then `last`, on separate lines.\nA '
        "one-word input should print that word twice."
    ),
    ("tuples-and-sets"): (
        "Read two input lines; you may choose any prompts.\nThe first line contains "
        "exactly two space-separated names.\nStore them as a tuple called `pair`, then "
        "assign its first item to `first` and its second item to `second`.\nThe second "
        "line contains zero or more space-separated visitor names, possibly "
        "repeated.\nStore the distinct visitors in a set called `seen`.\nNames are "
        "case-sensitive, so `Ada` and `ada` are different.\n\nPrint three lines: whether "
        "`first` is in `seen`, whether `second` is in `seen`, and the number of distinct "
        "visitors.\nUse Python's `True` and `False` spelling for membership results.\nFor "
        "first line `Mira Sol` and second line `Sol Sol Bo`, print `False`, `True`, and "
        "`2` on separate lines.\nFor an empty second line, print `False`, `False`, and "
        "`0`.\nKeep `pair`, `first`, `second`, and `seen` available for checks; do not "
        "print the set itself, since its order is not guaranteed."
    ),
    ("comparing-sets"): (
        "Read two lines of space-separated words, with any prompts.\nEither line may be "
        "empty, and duplicate words count once.\nStore the first line's set as `required` "
        "and the second as `available`.\nCreate `shared`, `missing`, `combined`, and "
        "`exclusive` as sets representing intersection, missing requirements, union, and "
        "symmetric difference respectively.\nSet `ready` to whether every requirement is "
        "available, including when there are no requirements.\nComparisons are "
        "case-sensitive.\nFor `rope lamp` and `lamp food`, only `lamp` is shared and only "
        "`rope` is missing.\nPrinting is optional; checks inspect your result variables."
    ),
    ("loop-helpers"): (
        "Read three input lines, with any prompts you choose.\nThe first is a nonnegative "
        "whole number called `count`.\nThe second contains space-separated names; store "
        "its split result in `names`.\nThe third contains space-separated colors; store "
        "its split result in `colors`.\nEither word line may be empty.\n\nCreate these "
        "three result lists:\n\n- `slots`: integers from `1` through `count`, inclusive; "
        "use `[]` when `count` is zero.\n- `numbered`: a tuple `(number, name)` for each "
        "name, counting from `1` in input order.\n- `pairs`: a tuple `(name, color)` for "
        "each corresponding name and color, stopping at the shorter input list.\n\nStart "
        "each result as an empty list and append its values inside a loop, or use "
        "another implementation that produces the same results.\nTo append one pair, "
        "write `result.append((left, right))`; the inner parentheses create the tuple "
        "passed to `append`.\nTry `range`, `enumerate`, and `zip` for the three "
        "loops.\nChecks compare the lists and tuples, so printing is optional.\nYou may "
        "print all three lists to inspect them with Run.\n\nFor input lines `2`, `Mira "
        'Sol`, and `red`, the results are `slots = [1, 2]`, `numbered = [(1, "Mira"), '
        '(2, "Sol")]`, and `pairs = [("Mira", "red")]`.\nPreserve duplicate names and '
        "colors in their original positions.\nIf both word lines are empty, `numbered` "
        "and `pairs` are both empty regardless of `count`."
    ),
    ("nested-collections"): (
        "Read a nonnegative integer `count` on the first line, then exactly `count` "
        "lines of space-separated integers.\nEach row may be empty or a different "
        "length.\nNegative integers and repeated values are valid.\nUse any input "
        "prompts.\nBuild a list of lists named `grid` using `int()` on each word.\n\nCreate "
        "`row_totals`, with one sum per row, including zero for empty rows.\nCreate "
        "`flat`, containing every value in row order and then column order.\nCreate "
        "`positions`, containing tuples `(row_index, column_index, value)` for those "
        "values, using zero-based indexes.\nReset a row's sum before its inner loop and "
        "append the sum after that loop.\nWith rows `[2, 3]` and `[4]`, the totals are "
        "`[5, 4]`, flat values are `[2, 3, 4]`, and positions are `[(0, 0, 2), (0, 1, "
        "3), (1, 0, 4)]`.\nFor zero rows, all four lists are empty.\nPrinting is optional."
    ),
    ("word-counts"): (
        "Read space-separated words from one input line.\nCreate a dictionary called "
        "`counts` whose keys are the words and whose values are the number of times each "
        "word appears.\nTreat `Cat` and `cat` as different words.\nAn empty input produces "
        "`{}`.\nYou may print `counts` so Run shows your result.\nChecks compare the "
        "dictionary itself, so printing is optional and key order does not matter."
    ),
    ("editing-collections"): (
        "Read three lines: space-separated `items`, one word `target`, and one word "
        "`incoming`.\nOnly the first line may be empty; use any prompts.\nRemove just the "
        "first occurrence of `target` from `items`, if present.\nInsert `incoming` at the "
        "beginning, then sort `items` using Python's case-sensitive string ordering.\nFor "
        "ordinary English letters, uppercase letters come before lowercase letters: "
        '`"Z"` sorts before `"a"`.\nBuild `counts`, mapping each resulting item to its '
        "count.\nThen remove the `target` entry from `counts`, saving its former value in "
        "`removed`, or zero when absent.\nCreate `keys` as a sorted list of the remaining "
        "dictionary keys.\nDo not remove any further items from the list when deleting "
        "the dictionary entry.\nPrinting is optional.\n\nFor `pear apple pear`, `pear`, "
        "`pear`, the final list is `['apple', 'pear', 'pear']`, counts is `{'apple': "
        "1}`, removed is `2`, and keys is `['apple']`."
    ),
    ("repeat-until-done"): (
        "Keep reading one integer per input line until the user enters `0`.\nAdd all the "
        "nonzero integers into a variable called `total`, initially zero.\nStop "
        "immediately at `0` and print `total` once after the loop.\nInputs are always "
        "valid integers; negative numbers are allowed and reduce the total.\nInput lines "
        "`5`, `-2`, `0` should print `3`.\nIf the first line is `0`, print `0`.\nCheck "
        "supplies the stopping zero automatically.\nWhen using Run, remember to type it "
        "yourself."
    ),
    ("supply-report"): (
        "Read one space-separated input line.\nCreate `counts`, a dictionary counting "
        "each word, and `order`, a list containing each distinct word once in the order "
        "it first appeared.\nPrint one line per word in `order`, formatted `word: "
        "count`.\nPrint `No supplies` if the input is empty.\nFor `rope lamp rope map "
        "lamp`, print:\n\n```text\nrope: 2\nlamp: 2\nmap: 1\n```\n\nPreserve capitalization "
        "and do not alphabetize the report.\nYou do not need to define your own functions "
        "yet.\nCreate the empty list and dictionary before the loop, then decide which "
        "changes happen inside it."
    ),
    ("small-superpowers"): (
        "Write `def heal(health, potion):` and implement its body to return `health + "
        "potion`, with a maximum result of `100`.\nFor example, `heal(20, 10)` should "
        "return `30`, and `heal(90, 25)` should return `100`.\n\nUse a variable to "
        "calculate the new health, an `if` to handle values above 100, and `return` to "
        "send back the answer.\nYou may add `print(heal(90, 25))` outside the function so "
        "you can see the result when you run it.\nChecks call the function directly, so "
        "this extra print is optional."
    ),
    ("clean-labels"): (
        "A **slug** is a short text label often used in a web address or "
        "filename.\nDefine `slug(text)` that returns a lowercase label with words "
        "separated by single hyphens.\nIgnore whitespace at the beginning and end; treat "
        'repeated spaces and tabs as one separator.\nDo not remove punctuation.\n`slug("  '
        'Blue   Moon ")` returns `"blue-moon"`.\nEmpty or whitespace-only input returns '
        '`""`.\nThis function takes its argument from its caller, so it should not call '
        "`input()`.\nReturn the result instead of only printing it."
    ),
    ("function-options"): (
        "Define `subtotal(prices, discount=0)`.\n`prices` is a list of nonnegative "
        "integer prices and `discount` is a nonnegative integer amount to subtract from "
        "the total, not a percentage.\nReturn the total after subtracting the discount, "
        "with a minimum of zero.\n`subtotal([6, 4])` returns `10`; `subtotal([6, 4], "
        "discount=3)` returns `7`.\nAn empty list returns `0`, including when a positive "
        "discount is given.\nUse the loop and accumulator pattern you already know.\nDo "
        "not change the input list."
    ),
    ("recursion-basics"): (
        "Define `digit_sum(number)` for a nonnegative integer containing at most 12 "
        "digits.\nReturn the sum of its decimal digits as an integer; `digit_sum(204)` "
        "returns `6`, and `digit_sum(0)` returns `0`.\nInputs are always valid integers "
        "in this range, so no validation is needed.\n`number % 10` gives the last digit "
        "and `number // 10` removes it.\nTry a recursive solution: return a single digit "
        "directly, otherwise add the last digit to the sum of the remaining digits.\nA "
        "correct loop-based solution is also accepted.\nReturn the result without "
        "printing."
    ),
    ("recursive-collections"): (
        "Define `sum_nested(items)`.\n`items` is a finite list whose elements are "
        "integers or more lists following the same rule.\nReturn the sum of all integers "
        "at every depth.\n`sum_nested([1, [2, [3]], 4])` returns `10`.\nEmpty lists "
        "contribute zero, negative integers are allowed, and nesting is at most 20 "
        "levels deep.\nThe input never contains cycles: a list cannot contain itself, "
        "directly or through other lists.\nNo types other than lists and integers "
        "occur.\nDo not change any input list and do not print.\nTry recursion, but any "
        "implementation with the required behavior is accepted."
    ),
    ("handle-invalid-input"): (
        "To **parse** text is to read it as a value or structure your program can "
        "use.\nDefine `parse_quantity(text)`.\nConvert a string to an integer and return "
        "it if it is nonnegative.\nReturn `None` if conversion fails or the integer is "
        "negative.\nSurrounding whitespace and a leading plus sign are valid because "
        '`int()` accepts them.\n`"3.5"` and `""` are invalid.\nThe input will always be a '
        "string; no input prompts or printed output are required."
    ),
    ("lantern-quest"): (
        "Define `play(moves)` for a list of move strings.\nReturn `(place, coins)` after "
        'processing every move.\n\n- Start in `"forest"` with `0` coins.\n- `"east"` moves '
        'from the forest to the cave.\n- `"west"` moves from the cave to the forest.\n- '
        '`"take"` in the cave collects `5` coins once per game.\n- Other moves do '
        'nothing; returning to the cave does not refill the treasure.\n\nFor `["east", '
        '"take", "west"]`, return `("forest", 5)`.\nFor an empty list, return `("forest", '
        "0)`.\nChecks call your function directly.\nTo try it with Run, you may add "
        '`print(play(["east", "take", "west"]))` below the definition.'
    ),
    ("text-files"): (
        "Define `line_total(path)` that reads a UTF-8 file of integers, one per line, "
        "and returns their sum.\nIgnore blank and whitespace-only lines.\nAll nonblank "
        "lines contain valid integers, including negatives.\nAn empty file returns "
        "`0`.\nFor file contents `4`, a blank line, and `-1`, return `3`.\nRead only the "
        "supplied path and do not change its contents.\nChecks create temporary files "
        "before calling your function."
    ),
    ("paths-and-folders"): (
        "Define `save_note(folder, text)`.\nCreate the requested folder, including "
        "missing parents.\nWrite `text` exactly as given to `note.txt` inside it, using "
        "UTF-8.\nReturn the resulting `Path` object.\nThe caller supplies a folder path as "
        "a string.\nIf `note.txt` already exists, replace its contents deliberately.\nDo "
        "not add a newline unless `text` already has one."
    ),
    ("json-records"): (
        "Define `save_scores(path, scores)`.\n`scores` is a dictionary mapping names to "
        "nonnegative integer scores.\nWrite it as JSON to the supplied path and return "
        "the sum of its scores.\nA dictionary's `.values()` method gives its values for a "
        "loop.\nAn empty dictionary must save an empty JSON object and return `0`.\nKeep "
        "every name exactly as given, including names with accented letters or "
        "characters from other languages.\nThese characters are represented using "
        "Unicode, the character system Python strings use.\nFormatting and JSON key order "
        "do not matter.\nThe parent folder already exists."
    ),
    ("csv-tables"): (
        "Define `csv_total(path)` for a UTF-8 CSV with headers "
        "`item,quantity,price`.\nReturn the sum of `quantity * price` across all data "
        "rows.\nQuantities and prices are nonnegative integers; prices represent whole "
        "credits.\nA header-only file returns `0`.\nItem names may contain quoted commas "
        "and should not affect the calculation.\nRead the file without modifying it."
    ),
    ("regex-validation"): (
        "Define `valid_code(text)` returning `True` only for exactly two uppercase ASCII "
        'letters, one hyphen, and exactly three ASCII digits.\n`"AB-123"` and `"ZZ-000"` '
        "are valid.\nLowercase letters, spaces, extra characters, trailing newlines, and "
        "non-ASCII digits are invalid.\nAn empty string is invalid.\nThe input is always a "
        "string; do not remove whitespace or change its characters before checking "
        "it.\nUse `[A-Z]` for uppercase ASCII letters and `[0-9]` for ASCII "
        "digits.\nReturn a Boolean without printing."
    ),
    ("regex-transformations"): (
        "Define `redact_tags(text)` returning a tuple `(names, redacted)`.\nHere, "
        "redacting means hiding the names in the returned text.\nA valid tag is exactly "
        "`[user:name]`, where `name` contains one or more lowercase ASCII "
        "letters.\n`names` is a list of names from every valid tag, preserving order and "
        "duplicates.\n`redacted` replaces every complete valid tag with `[user:hidden]` "
        'and preserves all other text exactly.\nFor `"[user:ada] met [user:bob]"`, return '
        '`(["ada", "bob"], "[user:hidden] met [user:hidden]")`.\nInvalid tags such as '
        "`[user:Ada]`, `[user:]`, and `[user:ab2]` remain unchanged and contribute no "
        'names.\nEmpty input returns `([], "")`.\nThe input is always a string; do not '
        "print."
    ),
    ("expense-report"): (
        "Define `summarize_expenses(source, destination)`.\nRead a UTF-8 CSV file with "
        "headers `category,amount` from `source`.\nAmounts are nonnegative integer cents, "
        "so you can add them exactly without decimal rounding.\nGroup amounts by category "
        "into a dictionary, write that dictionary as JSON to `destination`, and return "
        "it.\nThe destination's parent folder already exists.\nA header-only file produces "
        "`{}`.\nPreserve category text exactly, including commas represented by CSV "
        "quoting.\nDo not change the source file.\n\nFor these CSV "
        "rows:\n\n```text\ncategory,amount\ntravel,250\nfood,600\ntravel,150\n```\n\nReturn "
        'and save `{"travel": 400, "food": 600}`.\nJSON whitespace and key order do not '
        "matter.\nThe tools you have practiced fit together here: `csv.DictReader` reads "
        "rows, a dictionary keeps each category's running total, and `json.dump` saves "
        "the result.\nThe function receives paths from its caller, so it does not need "
        "input prompts."
    ),
    ("your-own-modules"): (
        "Create `conversions.py` with a function `minutes_to_seconds(minutes)` that "
        "returns `minutes * 60`.\nInputs are nonnegative integers.\nIn `lesson.py`, import "
        "that function so it is available there under the same name.\nDo not print or "
        "request input at import time.\nBoth files are part of this exercise and both "
        "begin blank in Build."
    ),
    ("numeric-tools"): (
        "Define `summarize(values, capacity)`.\n`values` is a list of finite numbers: "
        "ordinary integers or floats, excluding infinity and the special not-a-number "
        "value `nan`.\n`capacity` is an integer representing how many readings fit into "
        "one group.\nReturn a tuple containing the mean, the median, and the number of "
        "groups needed to hold all readings.\nA partial last group counts, so four "
        "readings with capacity three need two groups.\nReject an empty values list or a "
        "capacity of zero or less with `ValueError`.\nDo not change `values`, read input, "
        "or print.\nFor `[9, 1, 5, 3]` and capacity `3`, return `(4.5, 4.0, 2)`."
    ),
    ("repeatable-randomness"): (
        "Define `draw(items, count, seed)`.\n`items` is a list, `count` is an integer, "
        "and `seed` is an integer.\nUse an independent `random.Random(seed)` and call its "
        "`choice(items)` exactly once per draw, in order.\nReturn the choices in a new "
        "list, leaving both `items` and the module's shared random generator state "
        "unchanged.\nReject negative counts, or a positive count with empty items, using "
        "`ValueError`.\nZero draws return an empty list even when items is empty.\nThe "
        "same arguments must give the same result on repeated calls.\nDo not read input "
        "or print."
    ),
    ("command-line-options"): (
        "Define `make_parser()` that returns an `argparse.ArgumentParser`.\nAdd a "
        "required positional argument `name` and an optional `--count` integer argument "
        "whose default is `1`.\nDo not parse arguments inside `make_parser()`.\nThe checks "
        'call `.parse_args(...)` on your returned parser.\nFor `["Ada", "--count", "3"]`, '
        'its attributes should be `.name == "Ada"` and `.count == 3`.\nDo not request '
        "keyboard input or print anything when this file runs."
    ),
    ("your-first-class"): (
        "Define a class `Wallet`.\n`Wallet()` starts with a `.balance` of `0`.\nIts method "
        "`deposit(amount)` adds a nonnegative integer amount to the balance and returns "
        "the new balance.\nIts method `spend(amount)` returns `True` and subtracts the "
        "amount when affordable; otherwise it returns `False` without changing the "
        "balance.\nEach wallet must have its own balance.\nAmounts are always nonnegative "
        "integers.\nSpending zero succeeds, even for an empty wallet."
    ),
    ("named-states"): (
        "Import `Enum` and define `Status(Enum)` with exactly three members in this "
        'order: `TODO = "todo"`, `DOING = "doing"`, and `DONE = "done"`.\nDefine '
        "`next_status(status)` returning the next enum member: TODO becomes DOING, DOING "
        "becomes DONE, and DONE stays DONE.\nThe argument is always a `Status` member; "
        "string conversion or invalid-input handling is not required in this "
        "function.\nReturn enum members, not their string values, and do not print."
    ),
    ("tests-for-your-code"): (
        "Define `clamp(value, low, high)` that returns `low` below the lower boundary, "
        "`high` above the upper boundary, and the original value otherwise.\nAssume `low "
        "<= high`.\nAlso define a `unittest.TestCase` subclass named `ClampTests` with at "
        "least three test methods: `test_below`, `test_inside`, and `test_above`.\nEach "
        "must call `clamp` and assert its expected result.\nUse distinct cases that would "
        "detect a clamp implementation always returning the lower bound, the original "
        "value, or the upper bound.\nDo not call `unittest.main()` outside a function or "
        "class definition because Check manages the test run."
    ),
    ("task-workspace"): (
        "In `tasks.py`, define `TaskList`.\nEach instance starts empty.\nIts `add(title)` "
        "method strips surrounding whitespace, ignores empty titles, and stores each "
        'exact cleaned title at most once.\nCapitalization matters: `"Read"` and `"read"` '
        "are different tasks.\nIts `pending()` method returns a new list of titles in the "
        "order they were first added.\nChanging that returned list must not change the "
        "task list itself.\n\nIn `lesson.py`, import `TaskList` and define "
        "`build_report(titles)`.\nCreate a fresh task list, add every supplied title, and "
        'return its pending list.\nFor `[" Read ", "", "Read", "Walk"]`, return `["Read", '
        '"Walk"]`.\nAn empty input list returns an empty list.\nDo not request input, save '
        "tasks to files, or print output for this version."
    ),
    ("comprehensions"): (
        "Define `positive_squares(numbers)`.\nReturn the squares of the strictly positive "
        "integers in `numbers`, sorted from smallest to largest.\nKeep duplicates: two "
        "occurrences of `3` produce two occurrences of `9`.\nDo not change the original "
        "list.\nFor `[3, -2, 1, 3, 0]`, return `[1, 9, 9]`.\nAn empty list or a list with "
        "no positive numbers returns `[]`.\nA comprehension or a regular loop is "
        "acceptable."
    ),
    ("counting-and-grouping"): (
        "Define `summarize_visits(visits)` returning `(counts, pages)` as two "
        "dictionaries.\n`visits` is a list of `(user, page)` string pairs.\n`counts[user]` "
        "is the total number of that user's visits.\n`pages[user]` is a list of their "
        "pages in the order they appeared in the input, including duplicates.\nFor "
        '`[("ada", "home"), ("ada", "help")]`, return `({"ada": 2}, {"ada": ["home", '
        '"help"]})`.\nAn empty list returns `({}, {})`.\nEmpty strings are valid values, '
        "and only users present in the input appear in the results.\nDo not change the "
        "input or print.\nTry `Counter` and `defaultdict`; ordinary dictionaries "
        "implementing the same behavior are accepted."
    ),
    ("queues-with-deque"): (
        "Define `process_queue(waiting, arrivals, limit)` returning `(served, "
        "remaining)` as two lists.\n`waiting` and `arrivals` are lists of strings, and "
        "`limit` is a nonnegative integer.\nPlace every arrival after everyone already "
        "waiting, then serve up to `limit` entries from the front.\nPreserve order and "
        'duplicate entries.\nFor `(["a", "b"], ["c"], 2)`, return `(["a", "b"], '
        '["c"])`.\nA zero limit serves nobody; a limit larger than the queue serves '
        "everyone; two empty lists return `([], [])`.\nDo not change either input list or "
        "print.\nTry a deque; any implementation that returns the required results "
        "without changing the inputs is accepted."
    ),
    ("dates-and-deadlines"): (
        "Define `due_date(start, days)`.\n`start` is a valid ISO date string and `days` "
        "is a nonnegative integer.\nReturn the ISO date exactly that many days after "
        "`start`.\nZero days returns the same date.\nHandle month ends, year ends, and "
        'leap days by using date arithmetic.\nFor `due_date("2023-12-31", 1)`, return '
        '`"2024-01-01"`.\nDo not use today\'s date: the supplied start makes results '
        "predictable and easy to test."
    ),
    ("date-time-formats"): (
        "Define `appointment(day, clock, minutes)`.\n`day` uses `DD/MM/YYYY` and `clock` "
        "uses `HH:MM` on a 24-hour clock.\n`minutes` is the integer number of minutes to "
        "add; a negative value moves backward and zero leaves the date and time "
        "unchanged.\nReturn the resulting date and time as `YYYY-MM-DD HH:MM`.\nReject "
        "invalid dates and clock values with `ValueError`; you may let parsing raise "
        "it.\nInputs otherwise follow the stated formats, and results remain in Python's "
        "supported year range.\nDo not read input or print.\n`appointment('31/12/2024', "
        "'23:50', 20)` returns `'2025-01-01 00:10'`."
    ),
    ("validate-boundaries"): (
        "Define `valid_filename(name)` that returns a boolean.\nFor this exercise, a "
        'valid name is a nonempty string other than `"."` or `".."`, containing neither '
        "`/` nor a backslash, and with no leading or trailing whitespace.\nNames may "
        'contain spaces between words and letters from any language.\n`"meeting '
        'notes.txt"` is valid; `"../notes.txt"` and `" notes.txt"` are not.\nThe argument '
        "is always a string.\nThese are the naming rules for this exercise; other file "
        "tools may need additional checks.\nYour function must not create or read "
        'files.\nIn Python source, write `"\\\\"` to represent one literal backslash in a '
        "string."
    ),
    ("copy-with-care"): (
        "Define `copy_new(source, destination)`.\nCopy the source's bytes to the "
        "destination and return `True` if a new destination was created.\nIf the "
        "destination already exists, return `False` without changing either file.\nUse "
        "exclusive creation so the overwrite rule also holds if the file appears just "
        "before opening it.\nThe source is an existing regular file, meaning a file "
        "containing data rather than a folder or symbolic link.\nThe destination's parent "
        "folder exists.\nInput/output errors, often shortened to I/O errors, report "
        "problems reading or writing data.\nLet errors other than `FileExistsError` reach "
        "the caller instead of catching them or reporting a successful copy."
    ),
    ("notes-archiver"): (
        "In `selection.py`, define `eligible(source)`.\nReturn an alphabetically sorted "
        "list of filenames for regular files directly inside `source` whose suffix is "
        "exactly `.txt`.\nSkip directories, symbolic links, and other extensions, "
        "including `.TXT`.\nDo not look inside subfolders.\n\nIn `lesson.py`, import "
        "`eligible` and define `archive_notes(source, destination, "
        "dry_run=True)`.\nReturn sorted filenames that can be copied because their "
        "destination names do not already exist.\nIn dry-run mode, create no files or "
        "directories.\nWhen `dry_run=False`, create the destination directory if needed "
        "and copy each file's exact bytes using exclusive creation.\nIf another file "
        "already has the destination name when you try to create it, skip that file and "
        "leave its name out of the returned list.\nPreserve every source file and every "
        "existing destination file.\nAn empty source returns `[]` and need not create the "
        "destination.\nThe source directory exists; callers provide ordinary local "
        "directories under their control.\nLet other errors reading or writing files "
        "reach the caller.\n\nFor a source containing `b.txt`, `a.txt`, and `photo.png`, "
        'with no existing destination files, return `["a.txt", "b.txt"]`.\nAfter '
        "successful checks, export the workspace and try a dry run on a small folder of "
        "disposable sample notes."
    ),
}


REPAIR_STAGES = {
    "pack-your-bag": _stage(
        (
            "Repair the snack budget. Start budget at 20 credits. Read one line of "
            "space-separated integer costs into costs, then subtract each cost from "
            "budget and print what remains. An empty line leaves 20; negative costs are "
            "refunds that increase the budget. For 2 5 1, print 12. The final budget may "
            "be negative."
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
        "Repair the route preview. Read one line of space-separated stops into stops. "
        "Store its first two entries as list preview and every later entry as list later. "
        "Print preview, then later, on two lines. Preserve order and duplicates. "
        "With fewer than two stops, preview contains all stops and later is empty. "
        "An empty input line produces two empty lists.",
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
            "Repair the checkpoint tracker. Read one line of checkpoint names into tuple "
            "route, then a second line of visited names into set visited. Build "
            "remaining as a list of route entries not yet visited, retaining route order "
            "and repeated checkpoints. Print the number of distinct visited names, then "
            "remaining, on two lines. Either input line may be empty; comparisons are "
            "case-sensitive."
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
            "Repair the release gate. Read three lines of space-separated names as sets "
            "required, installed, and blocked. Create usable containing installed names "
            "that are not blocked, and missing containing requirements not in usable. "
            "Set ready to whether no requirements are missing. All comparisons are "
            "case-sensitive; any line may be empty and duplicates count once. Blocked "
            "names must never become usable. Printing is optional."
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
            "Repair a separate packing program. Read labels and whole-number weights "
            "from two lines and create labelled as tuples numbered from 1, stopping at "
            "the shorter list. Each tuple is (number, label, weight). Empty input must "
            "produce an empty list. You may print labelled to see it in Run; printing is "
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
            "Repair a grid transformer. Read a nonnegative row count, then that many "
            "lines of space-separated integers into grid. Rows may be empty or different "
            "lengths. Create lengths with one length per row, and doubled with a "
            "separate list per row containing twice each value. Preserve empty rows. "
            "Printing is optional."
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
            "Repair the sighting index. Read one line of space-separated words. Build "
            "records as a list of (word, count) tuples, one per distinct word in first "
            "appearance order. Repeated words increase the count without adding another "
            "tuple. Names are case-sensitive; empty input gives an empty list. Printing "
            "is optional."
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
            "Repair the roster editor. Read three lines: space-separated names, one name "
            "to remove, and one name to add. Keep the list as roster. Remove only the "
            "first match if present, insert the new name at the front, then sort the "
            "list. Create frequencies counting every remaining name. Names are "
            "case-sensitive; the first line may be empty. Printing is optional."
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
            "Repair the delivery report. Read one line of space-separated items and "
            "count them in stock. Create names as the sorted list of distinct items. "
            'Print one "name: count" line per name in alphabetical order, or "No '
            'delivery" for empty input. Preserve case. Unlike Build, this report sorts '
            "the names."
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
            _check("Empty delivery", "[stock, names]", [{}, []], stdin="\n", output="No delivery"),
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
    "small-superpowers": _stage(
        (
            "Repair a separate stamina function. restore(stamina, snack) must add the "
            "snack and cap the result at 50. A snack that would exceed the cap must not "
            "produce a larger value."
        ),
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
        (
            "Repair a separate heading function. heading(text) must trim outer "
            "whitespace, collapse runs of whitespace to single spaces, and capitalize "
            "the first character of each word. Title case starts a new word after "
            "punctuation too and lowercases remaining letters: DON'T becomes Don'T. "
            "Empty or whitespace-only text returns an empty string."
        ),
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
            _check("Case and punctuation", 'heading("DON\'T stop")', "Don'T Stop"),
            _check("Whitespace only", "heading(' \\t ')", ""),
        ),
        (
            "split() returns the words and does not change text by itself.",
            "Join the cleaned words before applying the capitalization method.",
        ),
    ),
    "function-options": _stage(
        (
            "Repair a separate order function. order_total(prices, service_fee=0) must "
            "add all prices and then add one service fee for the whole order. An empty "
            "order still includes the fee, and prices must not be changed."
        ),
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
        (
            "Repair a separate recursive function. digit_product(number) must multiply "
            "the decimal digits of a nonnegative integer. The one-digit base case "
            "supplies the final digit, and larger numbers reduce with // and %."
        ),
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
        (
            "Repair a separate recursive function. count_nested(items) must count every "
            "integer at every depth in a finite nested list. Empty lists count as zero; "
            "do not count a list object as one integer."
        ),
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
            _check(
                ("Input unchanged"),
                ("(lambda x: (count_nested(x), x)[1])([1, [2, []]])"),
                [1, [2, []]],
            ),
        ),
        (
            "Use isinstance(item, list) to choose the recursive path.",
            "The recursive result is the number of integers inside the child list.",
        ),
    ),
    "handle-invalid-input": _stage(
        (
            "Repair a separate parser. parse_score(text) must return an integer from 0 "
            "through 100, or None for conversion errors and values outside that range. "
            "Whitespace and a leading plus sign are accepted by int()."
        ),
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
            _check("Zero score", "parse_score('0')", 0),
            _check("Maximum score", "parse_score('100')", 100),
            _check("Decimal rejected", "parse_score('7.5')", None),
        ),
        (
            "Catch ValueError around int(text).",
            "After conversion, reject both negative and above-cap values.",
        ),
    ),
    "lantern-quest": _stage(
        (
            "Repair a separate cave route. explore(moves) starts at camp with zero gems, "
            "moves north to the ruins and south back to camp, and collects three gems "
            "once when search is used in the ruins. Return (place, gems). Other moves do "
            "nothing."
        ),
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
            _check(
                ("Return visit"),
                ("explore(['north', 'search', 'south', 'north', 'search'])"),
                (("ruins"), 3),
            ),
            _check("No moves", "explore([])", ("camp", 0)),
        ),
        (
            "Keep a boolean found flag outside the loop.",
            "Require both the place and the move before changing state.",
        ),
    ),
    "text-files": _stage(
        (
            "Repair a separate file-reading function. nonblank_lines(path) must return "
            "the number of nonblank lines in a UTF-8 text file. Whitespace-only lines do "
            "not count, including when they appear between negative and positive numbers."
        ),
        """
        def nonblank_lines(path):
            with open(path, encoding="utf-8") as handle:
                count = 0
                for line in handle:
                    if line.strip():
                        count += 1
                return count
        """,
        """
        def nonblank_lines(path):
            with open(path, encoding="utf-8") as handle:
                count = 0
                for line in handle:
                    count += 1
                return count
        """,
        (
            _check(
                "Blank lines",
                (
                    "(__import__('pathlib').Path('lines.txt').write_text('4\\n \\n-1\\n', "
                    "encoding='utf-8'), nonblank_lines('lines.txt'))[1]"
                ),
                2,
            ),
            _check(
                "Empty file",
                (
                    "(__import__('pathlib').Path('lines.txt').write_text('', encoding='utf-8'), "
                    "nonblank_lines('lines.txt'))[1]"
                ),
                0,
            ),
            _check(
                "Whitespace only",
                (
                    "(__import__('pathlib').Path('lines.txt').write_text(' \\n\\t\\n', "
                    "encoding='utf-8'), nonblank_lines('lines.txt'))[1]"
                ),
                0,
            ),
        ),
        ("Read the file with a with block.", "Test line.strip() before counting the line."),
    ),
    "paths-and-folders": _stage(
        (
            "Repair a separate path helper. ensure_note(folder, title, text) must create "
            "missing parents, write text exactly inside folder/title.txt, and return the "
            "resulting Path. title is a nonempty filename stem without separators. Use "
            "UTF-8 and replace an existing note only at that exact path."
        ),
        """
        from pathlib import Path

        def ensure_note(folder, title, text):
            directory = Path(folder)
            directory.mkdir(parents=True, exist_ok=True)
            target = directory / (title + ".txt")
            target.write_text(text, encoding="utf-8")
            return target
        """,
        """
        from pathlib import Path

        def ensure_note(folder, title, text):
            target = Path(folder + title + ".txt")
            target.write_text(text, encoding="utf-8")
            return target
        """,
        (
            _check(
                "Nested folder",
                (
                    "(lambda path: [path.as_posix(), path.read_text(encoding='utf-8')])(ensure_no"
                    "te('notes/deep', 'draft', 'café'))"
                ),
                ["notes/deep/draft.txt", "café"],
            ),
            _check(
                "Replace note",
                (
                    "(ensure_note('notes', 'daily', 'old'), ensure_note('notes', 'daily', "
                    "'new').read_text(encoding='utf-8'))[1]"
                ),
                "new",
            ),
            _check(
                ("Exact empty note"),
                (
                    "(lambda p: [p.as_posix(), p.read_bytes() == b''])(ensure_note('empty', "
                    "'blank', ''))"
                ),
                [("empty/blank.txt"), True],
            ),
        ),
        (
            "Create Path(folder) before joining a filename.",
            "mkdir(parents=True, exist_ok=True) handles missing folders.",
        ),
    ),
    "json-records": _stage(
        (
            "Repair a separate JSON settings reader. load_preferences(path) must read a "
            "JSON object with enabled and label fields and return [enabled, label]. "
            "JSON's true and null values are valid here, so Python's display syntax is "
            "not a substitute for JSON parsing."
        ),
        """
        import json

        def load_preferences(path):
            with open(path, encoding="utf-8") as handle:
                settings = json.load(handle)
            return [settings["enabled"], settings["label"]]
        """,
        """
        import json

        def load_preferences(path):
            with open(path, encoding="utf-8") as handle:
                settings = json.loads(handle)
            return [settings["enabled"], settings["label"]]
        """,
        (
            _check(
                "JSON boolean and null",
                (
                    "(__import__('pathlib').Path('settings.json').write_text('{\"enabled\": "
                    "true, \"label\": null}', encoding='utf-8'), "
                    "load_preferences('settings.json'))[1]"
                ),
                [True, None],
            ),
            _check(
                "Unicode label",
                (
                    "(__import__('pathlib').Path('settings.json').write_text('{\"enabled\": "
                    'false, "label": "café"}\', encoding=\'utf-8\'), '
                    "load_preferences('settings.json'))[1]"
                ),
                [False, "café"],
            ),
        ),
        (
            "Open the file with a with block and call json.load.",
            "JSON uses true, false, and null spellings that are not Python literals.",
        ),
    ),
    "csv-tables": _stage(
        (
            "Repair a separate CSV function. total_quantities(path) must add the "
            "quantity column from every data row, including rows whose item name "
            "contains a quoted comma. A header only file returns zero."
        ),
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
                (
                    "(__import__('pathlib').Path('table.csv').write_text('item,quantity,price\\n"
                    "\"pen, blue\",2,3\\nbook,1,8\\n', encoding='utf-8'), "
                    "total_quantities('table.csv'))[1]"
                ),
                3,
            ),
            _check(
                "Header only",
                (
                    "(__import__('pathlib').Path('table.csv').write_text('item,quantity,price\\n'"
                    ", encoding='utf-8'), total_quantities('table.csv'))[1]"
                ),
                0,
            ),
            _check(
                "Zero quantity",
                (
                    "(__import__('pathlib').Path('table.csv').write_text('item,quantity,price\\nb"
                    "ox,0,9\\n', encoding='utf-8'), total_quantities('table.csv'))[1]"
                ),
                0,
            ),
        ),
        (
            "DictReader names the columns for you.",
            "Convert row['quantity'] to int and add that field, not price.",
        ),
    ),
    "regex-validation": _stage(
        (
            "Repair a separate text validator. valid_ticket(text) must accept exactly "
            "three lowercase ASCII letters, a colon, and two ASCII digits. Reject "
            "matching fragments, extra text, spaces, and non-ASCII digits."
        ),
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
            _check("Trailing newline", "valid_ticket('abc:12\\n')", False),
            _check("Empty text", "valid_ticket('')", False),
            _check("Wrong digit count", "valid_ticket('abc:1')", False),
        ),
        (
            "Use fullmatch so the complete string is checked.",
            "Use [0-9] when the contract calls for ASCII digits.",
        ),
    ),
    "regex-transformations": _stage(
        (
            "Repair the chat masker. mask_mentions(text) replaces every complete <@name> "
            "marker with <@hidden>, where name is one or more lowercase ASCII letters. "
            "Preserve all other text exactly. For '<@ada> met <@bob>', return '<@hidden> "
            "met <@hidden>'. Invalid markers such as <@Ada>, <@bob2>, and <@> remain "
            "unchanged. Empty text stays empty."
        ),
        """
        import re

        def mask_mentions(text):
            return re.sub(r"<@[a-z]+>", "<@hidden>", text)
        """,
        """
        import re

        def mask_mentions(text):
            return re.sub(r"<@[a-z]+>", "<@hidden>", text, count=1)
        """,
        (
            _check("Two mentions", "mask_mentions('<@ada> met <@bob>')", "<@hidden> met <@hidden>"),
            _check(
                ("Repeated mention"),
                ("mask_mentions('<@ada> and <@ada>')"),
                ("<@hidden> and <@hidden>"),
            ),
            _check("Invalid mentions", "mask_mentions('<@Ada> <@bob2> <@>')", "<@Ada> <@bob2> <@>"),
            _check("Incomplete marker", "mask_mentions('<@ada')", "<@ada"),
            _check("Adjacent mentions", "mask_mentions('<@ada><@bob>')", "<@hidden><@hidden>"),
            _check("Empty text", "mask_mentions('')", ""),
        ),
        (
            "Trace how many matches the replacement call changes.",
            "re.sub replaces every match by default; count=1 limits it to the first match.",
        ),
    ),
    "expense-report": _stage(
        (
            "Repair a separate expense counter. category_counts(source, destination) "
            "must count the number of rows in each category, save that dictionary as "
            "JSON, and return it. Repeated categories must increase their existing count."
        ),
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
                (
                    "(__import__('pathlib').Path('expenses.csv').write_text('category,amount\\ntr"
                    "avel,250\\nfood,600\\ntravel,150\\n', encoding='utf-8'), "
                    "category_counts('expenses.csv', 'counts.json'))[1]"
                ),
                {"travel": 2, "food": 1},
            ),
            _check(
                "Empty report",
                (
                    "(__import__('pathlib').Path('expenses.csv').write_text('category,amount\\n',"
                    " encoding='utf-8'), category_counts('expenses.csv', 'counts.json'))[1]"
                ),
                {},
            ),
            _scenario_check(
                "Saved JSON and original CSV",
                """
                import json
                from pathlib import Path

                text = 'category,amount\\n"café, snacks",20\\ntravel,7\\n"café, snacks",30\\n'
                Path("expenses.csv").write_text(text, encoding="utf-8")
                report = category_counts("expenses.csv", "counts.json")
                saved = json.loads(Path("counts.json").read_text(encoding="utf-8"))
                result = [
                    report,
                    saved,
                    Path("expenses.csv").read_text(encoding="utf-8") == text,
                ]
                """,
                [{"café, snacks": 2, "travel": 1}, {"café, snacks": 2, "travel": 1}, True],
                description="C"
                "o"
                "u"
                "n"
                "t"
                " "
                "r"
                "e"
                "p"
                "e"
                "a"
                "t"
                "e"
                "d"
                " "
                "q"
                "u"
                "o"
                "t"
                "e"
                "d"
                " "
                "U"
                "n"
                "i"
                "c"
                "o"
                "d"
                "e"
                " "
                "c"
                "a"
                "t"
                "e"
                "g"
                "o"
                "r"
                "i"
                "e"
                "s"
                ";"
                " "
                "s"
                "a"
                "v"
                "e"
                " "
                "m"
                "a"
                "t"
                "c"
                "h"
                "i"
                "n"
                "g"
                " "
                "J"
                "S"
                "O"
                "N"
                " "
                "a"
                "n"
                "d"
                " "
                "p"
                "r"
                "e"
                "s"
                "e"
                "r"
                "v"
                "e"
                " "
                "t"
                "h"
                "e"
                " "
                "C"
                "S"
                "V"
                ".",
                nudge="Check both the returned mapping and the file written to destination.",
            ),
        ),
        (
            "Read each row before writing JSON.",
            "Use get(category, 0) + 1 so earlier rows are retained.",
        ),
    ),
    "your-own-modules": _stage(
        (
            "Repair a separate conversion module. Create conversions.py with "
            "hours_to_minutes(hours, minutes=0) returning hours times 60 plus minutes, "
            "then import it in lesson.py under the same name. Both arguments are "
            "nonnegative integers; minutes defaults to zero. Both files must remain "
            "quiet when imported."
        ),
        "",
        "",
        (
            _check("One hour", "hours_to_minutes(1)", 60),
            _check("No hours", "hours_to_minutes(0)", 0),
            _check("Several hours", "__import__('conversions').hours_to_minutes(7)", 420),
            _check("Extra minutes", "hours_to_minutes(2, minutes=15)", 135),
            _check("Only minutes", "hours_to_minutes(0, 20)", 20),
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
                def hours_to_minutes(hours, minutes=0):
                    return (hours + minutes) * 60
            """),
        },
        reference_files={
            "lesson.py": "from conversions import hours_to_minutes\n",
            "conversions.py": code("""
                def hours_to_minutes(hours, minutes=0):
                    return hours * 60 + minutes
            """),
        },
    ),
    "numeric-tools": _stage(
        (
            "Repair a separate score summary. score_summary(values) must return "
            "(minimum, maximum, mean) for a nonempty list of numbers without changing "
            "it. A one-value list has the same minimum, maximum, and mean."
        ),
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
            _check("One value", "score_summary([7])", (7, 7, 7)),
            _check("Input unchanged", "(lambda x: (score_summary(x), x)[1])([9, 1, 5])", [9, 1, 5]),
        ),
        (
            "min and max each inspect the whole collection.",
            "The order of the returned tuple is minimum, maximum, then mean.",
        ),
    ),
    "repeatable-randomness": _stage(
        (
            "Repair a separate seeded picker. pick_sequence(items, count, seed) must use "
            "a fresh Random(seed) for each call and return count choices in order. "
            "Repeated calls with the same inputs must match, and shared random state "
            "must remain unchanged. count and seed are integers. Reject negative counts "
            "or a positive count with empty items using ValueError. Zero draws return "
            "[]; leave items unchanged."
        ),
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
                (
                    "pick_sequence(['red', 'blue', 'green'], 4, 7) == pick_sequence(['red', "
                    "'blue', 'green'], 4, 7)"
                ),
                True,
            ),
            _check(
                "Shared state unchanged",
                (
                    "(lambda module: (module.seed(123), (lambda before: (pick_sequence(['red'], "
                    "1, 7), module.getstate() == before)[1])(module.getstate())))(__import__('ran"
                    "dom'))"
                ),
                (None, True),
            ),
            _check("Zero draws", "pick_sequence([], 0, 7)", []),
            _check(
                ("Negative count"),
                ("__raises_value_error__(lambda args: pick_sequence(*args), (['a'], -1, 7))"),
                True,
            ),
            _check(
                ("Empty choices"),
                ("__raises_value_error__(lambda args: pick_sequence(*args), ([], 1, 7))"),
                True,
            ),
            _check(
                ("Input unchanged"),
                ("(lambda x: (pick_sequence(x, 4, 7), x)[1])(['b', 'a'])"),
                [("b"), ("a")],
            ),
        ),
        (
            "Create random.Random(seed), not a shared seeded generator.",
            "Call choice once for each requested draw.",
        ),
    ),
    "command-line-options": _stage(
        (
            "Repair a separate command-line parser. make_tool_parser() must require a "
            "positional path and provide an integer --limit option defaulting to 10. "
            "Return the parser without parsing arguments in the function."
        ),
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
            _scenario_check(
                "Invalid arguments",
                """
                import contextlib
                import io

                result = []
                for args in ([], ["notes", "--limit", "many"]):
                    with contextlib.redirect_stderr(io.StringIO()):
                        try:
                            make_tool_parser().parse_args(args)
                        except SystemExit as error:
                            result.append(error.code)
                        else:
                            result.append(None)
                """,
                [2, 2],
                description=(
                    "Parsing must reject a missing path and a non-integer --limit with "
                    "argparse's usage error. "
                ),
                nudge=("Keep the path required and use type=int on the optional limit. "),
            ),
        ),
        ("Add the positional path first.", "Use type=int and default=10 for --limit."),
    ),
    "your-first-class": _stage(
        (
            "Repair a separate Ledger class. Ledger starts with balance zero, "
            "add(amount) returns the new balance, and withdraw(amount) returns True only "
            "when it can afford the amount. An unsuccessful withdrawal must not change "
            "balance. transfer_to(other, amount) moves money to another Ledger and "
            "returns True only when affordable; otherwise return False and leave both "
            "balances unchanged. Amounts are nonnegative integers; other is a different "
            "Ledger."
        ),
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

            def transfer_to(self, other, amount):
                if self.withdraw(amount):
                    other.add(amount)
                    return True
                return False
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

            def transfer_to(self, other, amount):
                if self.withdraw(amount):
                    other.add(amount)
                    return True
                return False
        """,
        (
            _check(
                "Transfer and refusal",
                "(lambda a, b: [a.add(10), a.transfer_to(b, 4), a.transfer_to(b, 20), "
                "a.balance, b.balance])(Ledger(), Ledger())",
                [10, True, False, 6, 4],
                description="Transfer 4 from a ledger holding 10, then refuse 20; "
                "balances remain 6 and 4.",
            ),
            _check(
                "Successful and refused",
                (
                    "(lambda account: [account.add(8), account.withdraw(3), "
                    "account.withdraw(10), account.balance])(Ledger())"
                ),
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
            _check(
                ("Zero withdrawal"), ("(lambda x: [x.withdraw(0), x.balance])(Ledger())"), [True, 0]
            ),
        ),
        (
            "Check affordability before subtracting.",
            "A failed withdrawal returns False and leaves the balance unchanged.",
        ),
    ),
    "named-states": _stage(
        (
            'Repair a separate Priority enum. Define Priority with LOW = "low", MEDIUM = '
            '"medium", and HIGH = "high", in that order, and raise_priority(priority) so '
            "LOW becomes MEDIUM, MEDIUM becomes HIGH, and HIGH stays HIGH."
        ),
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
        (
            "Repair the range validator and its tests. between(value, low, high) returns "
            "a boolean: True inside the inclusive range, False outside. Assume low <= "
            "high. Keep RangeTests as a unittest.TestCase with test_below, test_inside, "
            "and test_above. Add boundary tests that would catch a function accepting or "
            "rejecting everything. Check runs your tests; do not call unittest.main()."
        ),
        """
        import unittest

        def between(value, low, high):
            return low <= value <= high

        class RangeTests(unittest.TestCase):
            def test_below(self):
                self.assertEqual(between(-2, 0, 10), False)

            def test_inside(self):
                self.assertEqual(between(5, 0, 10), True)

            def test_above(self):
                self.assertEqual(between(12, 0, 10), False)

            def test_boundaries(self):
                self.assertEqual(between(0, 0, 10), True)
                self.assertEqual(between(10, 0, 10), True)
        """,
        """
        import unittest

        def between(value, low, high):
            return low < value < high

        class RangeTests(unittest.TestCase):
            def test_below(self):
                self.assertEqual(between(-2, 0, 10), False)

            def test_inside(self):
                self.assertEqual(between(5, 0, 10), True)

            def test_above(self):
                self.assertEqual(between(12, 0, 10), False)
        """,
        (
            _check("Below", "between(-2, 0, 10) is False", True),
            _check("Inside", "between(5, 0, 10) is True", True),
            _check("Above", "between(12, 0, 10) is False", True),
            _check("Inclusive lower bound", "between(0, 0, 10) is True", True),
            _check("Inclusive upper bound", "between(10, 0, 10) is True", True),
            _check("Equal boundaries", "between(4, 4, 4) is True", True),
            _check(
                "Tests pass",
                (
                    "(lambda result: [result.testsRun >= 3, result.wasSuccessful()])(__import__('"
                    "unittest').defaultTestLoader.loadTestsFromTestCase(RangeTests).run(__import_"
                    "_('unittest').TestResult()))"
                ),
                [True, True],
                description="Run RangeTests: at least three tests must pass.",
            ),
            _check(
                ("Named cases"),
                ("{'test_below', 'test_inside', 'test_above'} <= set(dir(RangeTests))"),
                True,
            ),
            *tuple(
                _check(
                    "Tests reject " + label,
                    "(RangeTests.test_inside.__globals__.__setitem__('between', "
                    f"lambda value, low, high: {stub}), "
                    "__import__('unittest').defaultTestLoader.loadTestsFromTestCase(RangeTests)"
                    ".run(__import__('unittest').TestResult()).wasSuccessful())[1]",
                    False,
                    nudge="Include an assertion whose expected result differs from this defect.",
                    description="Run your tests with between replaced by " + label + ".",
                )
                for label, stub in (
                    ("always True", "True"),
                    ("always False", "False"),
                    ("exclusive lower bound", "low < value <= high"),
                    ("exclusive upper bound", "low <= value < high"),
                )
            ),
        ),
        (
            "The supplied tests miss values exactly on the boundary. Add those cases first.",
            "An inclusive range includes low and high: compare with <= at both ends.",
        ),
    ),
    "task-workspace": _stage(
        (
            "Repair a separate notebook application. Keep Notebook in notes.py and make "
            "lesson.py return a copy of its note titles from list_notes(titles). "
            "Notebook.add(title) strips outer whitespace, skips empty titles and exact "
            "duplicates, and preserves case and insertion order. Each instance starts empty. "
            "A caller editing the returned list must not edit the Notebook's stored list. "
            "Also repair Notebook.rename(old, new): strip new, replace an existing exact old "
            "title in its original position, and return True. Return False without changing "
            "the list if old is missing, new is empty, or the cleaned new title belongs to "
            "another note. Renaming to the same cleaned title succeeds."
        ),
        "",
        "",
        (
            _check(
                "Rename in place",
                "(lambda b: (b.add('Read'), b.add('Walk'), b.rename('Read', ' Write '), "
                "b.list_notes())[2:])(Notebook())",
                (True, ["Write", "Walk"]),
            ),
            _check(
                "Refuse a duplicate title",
                "(lambda b: (b.add('Read'), b.add('Walk'), b.rename('Read', 'Walk'), "
                "b.list_notes())[2:])(Notebook())",
                (False, ["Read", "Walk"]),
            ),
            _check(
                "Missing and empty names",
                "(lambda b: (b.add('Read'), b.rename('Missing', 'Write'), "
                "b.rename('Read', ' '), b.list_notes())[1:])(Notebook())",
                (False, False, ["Read"]),
            ),
            _check(
                "Same title succeeds",
                "(lambda b: (b.add('Read'), b.rename('Read', ' Read '), b.list_notes())[1:])"
                "(Notebook())",
                (True, ["Read"]),
            ),
            _check(
                "Independent notebooks",
                "(lambda a, b: (a.add('Mine'), b.list_notes())[1])(Notebook(), Notebook())",
                [],
            ),
            _check("Clean notes", "list_notes([' Read ', '', 'Read', 'Walk'])", ["Read", "Walk"]),
            _check("Empty input", "list_notes([])", []),
            _check(
                "Returned list is independent",
                (
                    "(lambda book: (book.add('Read'), book.list_notes().append('Injected'), "
                    "book.list_notes())[2])(Notebook())"
                ),
                ["Read"],
            ),
        ),
        (
            "Trace both renaming and editing a returned list: can either corrupt stored titles?",
            "Validate the new title before replacing the old one; return a copy from list_notes.",
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


                    def rename(self, old, new):
                        clean = new.strip()
                        if not clean:
                            return False
                        for index, title in enumerate(self.items):
                            if title == old:
                                self.items[index] = clean
                                return True
                        return False

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


                    def rename(self, old, new):
                        clean = new.strip()
                        if not clean or (clean != old and clean in self.items):
                            return False
                        for index, title in enumerate(self.items):
                            if title == old:
                                self.items[index] = clean
                                return True
                        return False

                    def list_notes(self):
                        return self.items.copy()
            """),
        },
    ),
    "comprehensions": _stage(
        (
            "Repair a separate filter. odd_cubes(numbers) must return cubes of odd "
            "numbers, sorted from smallest to largest, retaining duplicate inputs. Zero "
            "and negative even numbers do not qualify."
        ),
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
            _check("Negative odds", "odd_cubes([-3, -1, 2, -3])", [-27, -27, -1]),
            _check("Empty list", "odd_cubes([])", []),
        ),
        (
            "Filter with number % 2 != 0.",
            "Use a list so duplicate inputs remain duplicate outputs.",
        ),
    ),
    "counting-and-grouping": _stage(
        (
            "Repair a separate grouping function. group_by_first(words) must return a "
            "dictionary whose keys are first letters and whose values list the original "
            "words in order. Repeated words remain repeated and empty input returns an "
            "empty dictionary. Each word is a nonempty string; preserve case and leave "
            "the input unchanged."
        ),
        """
        def group_by_first(words):
            groups = {}
            for word in words:
                key = word[0]
                if key not in groups:
                    groups[key] = []
                groups[key].append(word)
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
            _check(
                ("Case-sensitive groups"),
                ("group_by_first(['Ada', 'ant', 'Ada'])"),
                {("A"): [("Ada"), ("Ada")], ("a"): [("ant")]},
            ),
            _check(
                ("Input unchanged"),
                ("(lambda x: (group_by_first(x), x)[1])(['bee', 'ant'])"),
                [("bee"), ("ant")],
            ),
        ),
        (
            "Create a new list only for a new key.",
            "Append later words to the existing list instead of replacing it.",
        ),
    ),
    "queues-with-deque": _stage(
        (
            "Repair a separate queue function. serve_requests(waiting, arrivals, limit) "
            "must combine arrivals and waiting, then serve up to limit entries from the "
            "front, returning served and remaining. Priority arrivals go before the "
            "existing waiting list, in their original order. limit is a nonnegative "
            "integer. Inputs must stay unchanged."
        ),
        """
        from collections import deque

        def serve_requests(waiting, arrivals, limit):
            queue = deque(arrivals)
            queue.extend(waiting)
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
                served.append(queue.popleft())
            return served, list(queue)
        """,
        (
            _check("Arrival order", "serve_requests(['a', 'b'], ['c'], 2)", (["c", "a"], ["b"])),
            _check("No capacity", "serve_requests(['a'], ['b'], 0)", ([], ["b", "a"])),
            _check("More capacity", "serve_requests([], ['a', 'b'], 8)", (["a", "b"], [])),
            _check(
                ("Input lists unchanged"),
                ("(lambda a, b: (serve_requests(a, b, 2), a, b)[1:])(['a', 'a'], ['b'])"),
                ([("a"), ("a")], [("b")]),
            ),
            _check("Empty queue", "serve_requests([], [], 3)", ([], [])),
            _check(
                ("Duplicate priority requests"),
                ("serve_requests(['a'], ['b', 'b'], 2)"),
                ([("b"), ("b")], [("a")]),
            ),
        ),
        (
            "Which group belongs at the front before serving starts?",
            "Start with deque(arrivals), then extend it with waiting; serve with popleft.",
        ),
    ),
    "dates-and-deadlines": _stage(
        (
            "Repair a separate calendar helper. days_until(start, end) must return the "
            "number of days from the ISO start date to the ISO end date. The same date "
            "is zero days apart, and the result may be negative when end comes first."
        ),
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
        (
            "Repair a separate timestamp formatter. format_stamp(day, clock) must parse "
            "DD/MM/YYYY and HH:MM and return YYYY-MM-DD HH:MM without changing the time. "
            "Invalid dates and clock values should raise ValueError."
        ),
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
            _check(
                ("Invalid date"),
                (
                    "__raises_value_error__(lambda args: format_stamp(*args), ('31/02/2024', "
                    "'09:00'))"
                ),
                True,
            ),
            _check(
                ("Invalid clock"),
                (
                    "__raises_value_error__(lambda args: format_stamp(*args), ('01/01/2024', "
                    "'25:00'))"
                ),
                True,
            ),
        ),
        ("The input directive is %d/%m/%Y.", "The output directive is %Y-%m-%d %H:%M."),
    ),
    "validate-boundaries": _stage(
        (
            "Repair a separate identifier validator. valid_identifier(name) accepts a "
            "nonempty name made only of letters, digits, and underscores, with a letter "
            "as its first character. Reject spaces, punctuation, and names beginning "
            "with a digit or underscore. Unicode letters and digits are allowed. These "
            "are this exercise's naming rules, not all valid Python identifiers."
        ),
        """
        def valid_identifier(name):
            if not name or not name[0].isalpha():
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
            _check("Leading underscore", "valid_identifier('_task')", False),
            _check("Unicode letters and digits", "valid_identifier('café_٢')", True),
            _check("Single letter", "valid_identifier('A')", True),
        ),
        (
            "Check empty text and the first character before the rest.",
            "Every later character must be alphanumeric or underscore.",
        ),
    ),
    "copy-with-care": _stage(
        (
            "Repair a separate safe copier. backup_file(source) must copy exact bytes to "
            "a sibling file whose name is the full source name plus .bak "
            "(notes.txt.bak). If it already exists, return False and preserve both "
            "files. Return True for a new backup and False for an existing backup. The "
            "source is an existing regular file; let other I/O errors reach the caller. "
            "Never overwrite a backup, even if it appears just before you open it."
        ),
        """
        import shutil
        from pathlib import Path

        def backup_file(source):
            source = Path(source)
            destination = source.parent / (source.name + ".bak")
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
        from pathlib import Path

        def backup_file(source):
            source = Path(source)
            destination = source.parent / (source.name + ".bak")
            with open(source, "rb") as input_file:
                with open(destination, "wb") as output_file:
                    shutil.copyfileobj(input_file, output_file)
            return True
        """,
        (
            _check(
                "New destination",
                (
                    "(__import__('pathlib').Path('source.bin').write_bytes(bytes([0, 255, 97])), "
                    "(lambda result: [result, list(__import__('pathlib').Path('source.bin.bak').r"
                    "ead_bytes())])(backup_file('source.bin')))[1]"
                ),
                [True, [0, 255, 97]],
            ),
            _check(
                "Existing destination",
                (
                    "(__import__('pathlib').Path('source.txt').write_text('new'), "
                    "__import__('pathlib').Path('source.txt.bak').write_text('keep'), (lambda "
                    "result: [result, __import__('pathlib').Path('source.txt.bak').read_text()])("
                    "backup_file('source.txt')))[2]"
                ),
                [False, "keep"],
            ),
            _scenario_check(
                "Backup beside source",
                """
                from pathlib import Path

                Path("nested").mkdir()
                Path("nested/note.txt").write_bytes(b"original")
                result = [
                    backup_file("nested/note.txt"),
                    Path("nested/note.txt.bak").read_bytes() == b"original",
                    Path("nested/note.txt").read_bytes() == b"original",
                ]
                """,
                [True, True, True],
                description=(
                    "Back up nested/note.txt beside itself, preserving the .txt suffix and "
                    "original bytes. "
                ),
                nudge=("Build the destination from the source parent and complete filename. "),
            ),
            _scenario_check(
                "Competing backup",
                """
                from pathlib import Path
                from unittest.mock import patch
                import builtins

                Path("note.txt").write_text("new")
                original_open = builtins.open


                def competing_open(path, mode="r", *args, **kwargs):
                    if Path(path) == Path("note.txt.bak") and mode in ("xb", "wb"):
                        with original_open(path, "w") as handle:
                            handle.write("keep")
                    return original_open(path, mode, *args, **kwargs)


                with patch("builtins.open", competing_open):
                    copied = backup_file("note.txt")
                result = [
                    copied,
                    Path("note.txt.bak").read_text(),
                    Path("note.txt").read_text(),
                ]
                """,
                [False, "keep", "new"],
                description=(
                    "Another writer creates note.txt.bak just before opening: return False "
                    "and preserve both files. "
                ),
                nudge=(
                    "The no-overwrite rule must hold when opening the file, even after an "
                    "earlier existence check. "
                ),
            ),
        ),
        (
            "Build the backup path beside the source, keeping its complete filename.",
            "Catch FileExistsError and return False without reporting success.",
        ),
    ),
    "notes-archiver": _stage(
        (
            "Repair the Markdown archive planner. In selection.py, eligible_md(source) "
            "returns sorted immediate regular filenames ending in lowercase .md, "
            "skipping directories and symbolic links. In lesson.py, "
            "archive_markdown(source, destination, dry_run=True) returns a dictionary "
            "with planned and skipped lists in alphabetical order. planned contains "
            "files that can be copied; skipped contains eligible files whose destination "
            "names are taken. Dry runs create nothing. Write mode creates parents as "
            "needed and copies exact bytes without overwriting, even if a destination "
            "appears during copying. Report such conflicts as skipped. Preserve sources "
            "and existing destinations; let other I/O errors propagate. An empty source "
            "returns two empty lists. The source directory exists."
        ),
        "",
        "",
        (
            _scenario_check(
                "Preview new files",
                """
                from pathlib import Path

                Path("inbox").mkdir()
                Path("inbox/b.md").write_bytes(b"B")
                Path("inbox/a.md").write_bytes(b"A")
                report = archive_markdown("inbox", "archive")
                result = [report, Path("archive").exists()]
                """,
                [{"planned": ["a.md", "b.md"], "skipped": []}, False],
                description=(
                    "Preview b.md and a.md with no destination: report sorted planned names and "
                    "create nothing."
                ),
                nudge="Compare the selection and report before checking which files changed.",
            ),
            _scenario_check(
                "Copy exact bytes",
                """
                from pathlib import Path

                Path("inbox").mkdir()
                payload = bytes([0, 255, 97])
                Path("inbox/a.md").write_bytes(payload)
                report = archive_markdown("inbox", "nested/archive", dry_run=False)
                result = [
                    report,
                    Path("nested/archive/a.md").read_bytes() == payload,
                    Path("inbox/a.md").read_bytes() == payload,
                ]
                """,
                [{"planned": ["a.md"], "skipped": []}, True, True],
                description=(
                    "Copy a.md containing bytes 0, 255, 97 into nested/archive; preserve source "
                    "and exact bytes."
                ),
                nudge="Compare the selection and report before checking which files changed.",
            ),
            _scenario_check(
                "Preview existing destination",
                """
                from pathlib import Path

                Path("inbox").mkdir()
                Path("archive").mkdir()
                Path("inbox/a.md").write_text("new", encoding="utf-8")
                Path("archive/a.md").write_text("keep", encoding="utf-8")
                report = archive_markdown("inbox", "archive")
                result = [report, Path("archive/a.md").read_text(encoding="utf-8")]
                """,
                [{"planned": [], "skipped": ["a.md"]}, "keep"],
                description="Preview a.md "
                "already in "
                "archive: report it "
                "as skipped and "
                "keep its contents.",
                nudge="Compare the selection and report before checking which files changed.",
            ),
            _scenario_check(
                "Write around conflicts",
                """
                from pathlib import Path

                Path("inbox").mkdir()
                Path("archive").mkdir()
                Path("inbox/a.md").write_text("new", encoding="utf-8")
                Path("inbox/b.md").write_text("B", encoding="utf-8")
                Path("archive/a.md").write_text("keep", encoding="utf-8")
                report = archive_markdown("inbox", "archive", dry_run=False)
                result = [
                    report,
                    Path("archive/a.md").read_text(encoding="utf-8"),
                    Path("archive/b.md").read_text(encoding="utf-8"),
                ]
                """,
                [{"planned": ["b.md"], "skipped": ["a.md"]}, "keep", "B"],
                description=(
                    "Write a.md and b.md when a.md already exists: skip a.md, copy b.md, "
                    "preserve existing data."
                ),
                nudge="Compare the selection and report before checking which files changed.",
            ),
            _scenario_check(
                "Selection rules",
                """
                from pathlib import Path

                Path("inbox").mkdir()
                Path("inbox/nested.md").mkdir()
                Path("inbox/nested.md/child.md").write_text("skip")
                Path("inbox/Z.MD").write_text("skip")
                Path("inbox/note.txt").write_text("skip")
                Path("inbox/b.md").write_text("B")
                Path("inbox/a.md").write_text("A")
                Path("inbox/link.md").symlink_to("a.md")
                Path("inbox/broken.md").symlink_to("missing")
                result = [
                    eligible_md("inbox"),
                    archive_markdown("inbox", "archive"),
                    Path("archive").exists(),
                ]
                """,
                [["a.md", "b.md"], {"planned": ["a.md", "b.md"], "skipped": []}, False],
                description=(
                    "Select only immediate regular lowercase .md files, sorted; skip folders, "
                    "uppercase suffixes and links."
                ),
                nudge="Compare the selection and report before checking which files changed.",
            ),
            _scenario_check(
                "Empty source",
                """
                from pathlib import Path

                Path("inbox").mkdir()
                result = [archive_markdown("inbox", "archive"), Path("archive").exists()]
                """,
                [{"planned": [], "skipped": []}, False],
                description="Preview an empty source: "
                "both lists are empty and "
                "no destination is created.",
                nudge="Compare the selection and report before checking which files changed.",
            ),
            _scenario_check(
                "Dangling destination link",
                """
                from pathlib import Path

                Path("inbox").mkdir()
                Path("archive").mkdir()
                Path("inbox/a.md").write_text("new")
                Path("archive/a.md").symlink_to("missing")
                result = [
                    archive_markdown("inbox", "archive", dry_run=False),
                    Path("archive/a.md").is_symlink(),
                    Path("archive/missing").exists(),
                ]
                """,
                [{"planned": [], "skipped": ["a.md"]}, True, False],
                description=(
                    "A destination symbolic link occupies its name even if its target is "
                    "missing; skip it."
                ),
                nudge="Compare the selection and report before checking which files changed.",
            ),
            _scenario_check(
                "Destination appears during copy",
                """
                from pathlib import Path
                from unittest.mock import patch
                import builtins

                Path("inbox").mkdir()
                Path("inbox/race.md").write_text("new")
                original_open = builtins.open


                def competing_open(path, mode="r", *args, **kwargs):
                    if Path(path) == Path("archive/race.md") and mode in ("xb", "wb"):
                        with original_open(path, "w") as handle:
                            handle.write("other writer")
                    return original_open(path, mode, *args, **kwargs)


                with patch("builtins.open", competing_open):
                    report = archive_markdown("inbox", "archive", dry_run=False)
                result = [report, Path("archive/race.md").read_text()]
                """,
                [{"planned": [], "skipped": ["race.md"]}, "other writer"],
                description=(
                    "A destination appears after the initial check: skip it without "
                    "changing the other writer's bytes. "
                ),
                nudge=(
                    "Exclusive creation detects a conflict at opening time, not just during "
                    "preview. "
                ),
            ),
        ),
        (
            (
                "Compare a preview with a write run. Which statements should be allowed to "
                "create files?"
            ),
            (
                "Guard directory creation and copying with not dry_run; append conflicts to "
                "skipped, and exclude symbolic links in eligible_md."
            ),
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
                planned = []
                skipped = []
                for name in eligible_md(source):
                    target = destination / name
                    if target.exists() or target.is_symlink():
                        skipped.append(name)
                        continue
                    if dry_run:
                        destination.mkdir(parents=True, exist_ok=True)
                        with open(source / name, "rb") as input_file:
                            try:
                                with open(target, "xb") as output_file:
                                    shutil.copyfileobj(input_file, output_file)
                            except FileExistsError:
                                skipped.append(name)
                                continue
                    planned.append(name)
                return {"planned": planned, "skipped": skipped}
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
                planned = []
                skipped = []
                for name in eligible_md(source):
                    target = destination / name
                    if target.exists() or target.is_symlink():
                        skipped.append(name)
                        continue
                    if not dry_run:
                        destination.mkdir(parents=True, exist_ok=True)
                        with open(source / name, "rb") as input_file:
                            try:
                                with open(target, "xb") as output_file:
                                    shutil.copyfileobj(input_file, output_file)
                            except FileExistsError:
                                skipped.append(name)
                                continue
                    planned.append(name)
                return {"planned": planned, "skipped": skipped}
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
