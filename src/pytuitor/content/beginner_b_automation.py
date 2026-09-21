"""Stage contracts for b-automation."""

from pytuitor.beginner_authoring import _check, _scenario_check, _stage
from pytuitor.models import code

BUILD_INSTRUCTIONS = {
    "comprehensions": (
        "Define `positive_squares(numbers)`.\nReturn the squares of the strictly po"
        "sitive integers in `numbers`, sorted from smallest to largest.\nKeep dupli"
        "cates: two occurrences of `3` produce two occurrences of `9`.\nDo not chan"
        "ge the original list.\nFor `[3, -2, 1, 3, 0]`, return `[1, 9, 9]`.\nAn emp"
        "ty list or a list with no positive numbers returns `[]`.\nA comprehension "
        "or a regular loop is acceptable."
    ),
    "counting-and-grouping": (
        "Define `summarize_visits(visits)` returning `(counts, pages)` as two dicti"
        "onaries.\n`visits` is a list of `(user, page)` string pairs.\n`counts[user"
        "]` is the total number of that user's visits.\n`pages[user]` is a list of "
        "their pages in the order they appeared in the input, including duplicates."
        '\nFor `[("ada", "home"), ("ada", "help")]`, return `({"ada": 2}, {"ada": ['
        '"home", "help"]})`.\nAn empty list returns `({}, {})`.\nEmpty strings are '
        "valid values, and only users present in the input appear in the results.\n"
        "Do not change the input or print.\nTry `Counter` and `defaultdict`; ordina"
        "ry dictionaries implementing the same behavior are accepted."
    ),
    "queues-with-deque": (
        "Define `process_queue(waiting, arrivals, limit)` returning `(served, remai"
        "ning)` as two lists.\n`waiting` and `arrivals` are lists of strings, and `"
        "limit` is a nonnegative integer.\nPlace every arrival after everyone alrea"
        "dy waiting, then serve up to `limit` entries from the front.\nPreserve ord"
        'er and duplicate entries.\nFor `(["a", "b"], ["c"], 2)`, return `(["a", "b'
        '"], ["c"])`.\nA zero limit serves nobody; a limit larger than the queue se'
        "rves everyone; two empty lists return `([], [])`.\nDo not change either in"
        "put list or print.\nTry a deque; any implementation that returns the requi"
        "red results without changing the inputs is accepted."
    ),
    "dates-and-deadlines": (
        "Define `due_date(start, days)`.\n`start` is a valid ISO date string and `d"
        "ays` is a nonnegative integer.\nReturn the ISO date exactly that many days"
        " after `start`.\nZero days returns the same date.\nHandle month ends, year"
        ' ends, and leap days by using date arithmetic.\nFor `due_date("2023-12-31"'
        ', 1)`, return `"2024-01-01"`.\nDo not use today\'s date: the supplied star'
        "t makes results predictable and easy to test."
    ),
    "date-time-formats": (
        "Define `appointment(day, clock, minutes)`.\n`day` uses `DD/MM/YYYY` and `c"
        "lock` uses `HH:MM` on a 24-hour clock.\n`minutes` is the integer number of"
        " minutes to add; a negative value moves backward and zero leaves the date "
        "and time unchanged.\nReturn the resulting date and time as `YYYY-MM-DD HH:"
        "MM`.\nReject invalid dates and clock values with `ValueError`; you may let"
        " parsing raise it.\nInputs otherwise follow the stated formats, and result"
        "s remain in Python's supported year range.\nDo not read input or print.\n`"
        "appointment('31/12/2024', '23:50', 20)` returns `'2025-01-01 00:10'`."
    ),
    "validate-boundaries": (
        "Define `valid_filename(name)` that returns a boolean.\nFor this exercise, "
        'a valid name is a nonempty string other than `"."` or `".."`, containing n'
        "either `/` nor a backslash, and with no leading or trailing whitespace.\nN"
        'ames may contain spaces between words and letters from any language.\n`"me'
        'eting notes.txt"` is valid; `"../notes.txt"` and `" notes.txt"` are not.\n'
        "The argument is always a string.\nThese are the naming rules for this exer"
        "cise; other file tools may need additional checks.\nYour function must not"
        ' create or read files.\nIn Python source, write `"\\\\"` to represent one '
        "literal backslash in a string."
    ),
    "copy-with-care": (
        "Define `copy_new(source, destination)`.\nCopy the source's bytes to the de"
        "stination and return `True` if a new destination was created.\nIf the dest"
        "ination already exists, return `False` without changing either file.\nUse "
        "exclusive creation so the overwrite rule also holds if the file appears ju"
        "st before opening it.\nThe source is an existing regular file, meaning a f"
        "ile containing data rather than a folder or symbolic link.\nThe destinatio"
        "n's parent folder exists.\nInput/output errors, often shortened to I/O err"
        "ors, report problems reading or writing data.\nLet errors other than `File"
        "ExistsError` reach the caller instead of catching them or reporting a succ"
        "essful copy."
    ),
    "notes-archiver": (
        "In `selection.py`, define `eligible(source)`.\nReturn an alphabetically so"
        "rted list of filenames for regular files directly inside `source` whose su"
        "ffix is exactly `.txt`.\nSkip directories, symbolic links, and other exten"
        "sions, including `.TXT`.\nDo not look inside subfolders.\n\nIn `lesson.py`"
        ", import `eligible` and define `archive_notes(source, destination, dry_run"
        "=True)`.\nReturn sorted filenames that can be copied because their destina"
        "tion names do not already exist.\nIn dry-run mode, create no files or dire"
        "ctories.\nWhen `dry_run=False`, create the destination directory if needed"
        " and copy each file's exact bytes using exclusive creation.\nIf another fi"
        "le already has the destination name when you try to create it, skip that f"
        "ile and leave its name out of the returned list.\nPreserve every source fi"
        "le and every existing destination file.\nAn empty source returns `[]` and "
        "need not create the destination.\nThe source directory exists; callers pro"
        "vide ordinary local directories under their control.\nLet other errors rea"
        "ding or writing files reach the caller.\n\nFor a source containing `b.txt`"
        ', `a.txt`, and `photo.png`, with no existing destination files, return `["'
        'a.txt", "b.txt"]`.\nAfter successful checks, export the workspace and try '
        "a dry run on a small folder of disposable sample notes."
    ),
}

REPAIR_STAGES = {
    "comprehensions": _stage(
        (
            "Repair a separate filter. odd_cubes(numbers) must return cubes of odd numb"
            "ers, sorted from smallest to largest, retaining duplicate inputs. Zero and"
            " negative even numbers do not qualify."
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
            "Repair a separate grouping function. group_by_first(words) must return a d"
            "ictionary whose keys are first letters and whose values list the original "
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
            "Repair a separate queue function. serve_requests(waiting, arrivals, limit)"
            " must combine arrivals and waiting, then serve up to limit entries from th"
            "e front, returning served and remaining. Priority arrivals go before the e"
            "xisting waiting list, in their original order. limit is a nonnegative inte"
            "ger. Inputs must stay unchanged."
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
            "Repair a separate timestamp formatter. format_stamp(day, clock) must parse"
            " DD/MM/YYYY and HH:MM and return YYYY-MM-DD HH:MM without changing the tim"
            "e. Invalid dates and clock values should raise ValueError."
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
            _check("Day before month", "format_stamp('03/04/2024', '09:00')", ("2024-04-03 09:00")),
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
            "Repair a separate identifier validator. valid_identifier(name) accepts a n"
            "onempty name made only of letters, digits, and underscores, with a letter "
            "as its first character. Reject spaces, punctuation, and names beginning wi"
            "th a digit or underscore. Unicode letters and digits are allowed. These ar"
            "e this exercise's naming rules, not all valid Python identifiers."
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
            "Repair a separate safe copier. backup_file(source) must copy exact bytes t"
            "o a sibling file whose name is the full source name plus .bak (notes.txt.b"
            "ak). If it already exists, return False and preserve both files. Return Tr"
            "ue for a new backup and False for an existing backup. The source is an exi"
            "sting regular file; let other I/O errors reach the caller. Never overwrite"
            " a backup, even if it appears just before you open it."
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
                    "(__import__('pathlib').Path('source.bin').write_bytes(bytes([0, 255, 97]))"
                    ", (lambda result: [result, list(__import__('pathlib').Path('source.bin.bak"
                    "').read_bytes())])(backup_file('source.bin')))[1]"
                ),
                [True, [0, 255, 97]],
            ),
            _check(
                "Existing destination",
                (
                    "(__import__('pathlib').Path('source.txt').write_text('new'), __import__('p"
                    "athlib').Path('source.txt.bak').write_text('keep'), (lambda result: [resul"
                    "t, __import__('pathlib').Path('source.txt.bak').read_text()])(backup_file("
                    "'source.txt')))[2]"
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
                (
                    "\n                from pathlib import Path\n                from unittest."
                    "mock import patch\n                import builtins\n\n                Path"
                    '("note.txt").write_text("new")\n                original_open = builtins.o'
                    'pen\n\n\n                def competing_open(path, mode="r", *args, **kwarg'
                    's):\n                    if Path(path) == Path("note.txt.bak") and mode in'
                    ' ("xb", "wb"):\n                        with original_open(path, "w") as h'
                    'andle:\n                            handle.write("keep")\n                '
                    "    return original_open(path, mode, *args, **kwargs)\n\n\n               "
                    ' with patch("builtins.open", competing_open):\n                    copied '
                    '= backup_file("note.txt")\n                result = [\n                   '
                    ' copied,\n                    Path("note.txt.bak").read_text(),\n         '
                    '           Path("note.txt").read_text(),\n                ]\n             '
                    "   "
                ),
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
            "returns sorted immediate regular filenames ending in lowercase .md, skippi"
            "ng directories and symbolic links. In lesson.py, archive_markdown(source, "
            "destination, dry_run=True) returns a dictionary with planned and skipped l"
            "ists in alphabetical order. planned contains files that can be copied; ski"
            "pped contains eligible files whose destination names are taken. Dry runs c"
            "reate nothing. Write mode creates parents as needed and copies exact bytes"
            " without overwriting, even if a destination appears during copying. Report"
            " such conflicts as skipped. Preserve sources and existing destinations; le"
            "t other I/O errors propagate. An empty source returns two empty lists. The"
            " source directory exists."
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
                    "Preview b.md and a.md with no destination: report sorted planned names and"
                    " create nothing."
                ),
                nudge="Compare the selection and report before checking which files changed.",
            ),
            _scenario_check(
                "Copy exact bytes",
                (
                    '\n                from pathlib import Path\n\n                Path("inbox"'
                    ").mkdir()\n                payload = bytes([0, 255, 97])\n                "
                    'Path("inbox/a.md").write_bytes(payload)\n                report = archive_'
                    'markdown("inbox", "nested/archive", dry_run=False)\n                result'
                    ' = [\n                    report,\n                    Path("nested/archiv'
                    'e/a.md").read_bytes() == payload,\n                    Path("inbox/a.md").'
                    "read_bytes() == payload,\n                ]\n                "
                ),
                [{"planned": ["a.md"], "skipped": []}, True, True],
                description=(
                    "Copy a.md containing bytes 0, 255, 97 into nested/archive; preserve source"
                    " and exact bytes."
                ),
                nudge="Compare the selection and report before checking which files changed.",
            ),
            _scenario_check(
                "Preview existing destination",
                (
                    '\n                from pathlib import Path\n\n                Path("inbox"'
                    ').mkdir()\n                Path("archive").mkdir()\n                Path("'
                    'inbox/a.md").write_text("new", encoding="utf-8")\n                Path("ar'
                    'chive/a.md").write_text("keep", encoding="utf-8")\n                report '
                    '= archive_markdown("inbox", "archive")\n                result = [report, '
                    'Path("archive/a.md").read_text(encoding="utf-8")]\n                '
                ),
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
                with __symlink_fixtures__({"inbox/link.md": "a.md", "inbox/broken.md": "missing"}):
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
                (
                    '\n                from pathlib import Path\n\n                Path("inbox"'
                    ').mkdir()\n                result = [archive_markdown("inbox", "archive"),'
                    ' Path("archive").exists()]\n                '
                ),
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
                with __symlink_fixtures__({"archive/a.md": "missing"}):
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
                (
                    "\n                from pathlib import Path\n                from unittest."
                    "mock import patch\n                import builtins\n\n                Path"
                    '("inbox").mkdir()\n                Path("inbox/race.md").write_text("new")'
                    "\n                original_open = builtins.open\n\n\n                def c"
                    'ompeting_open(path, mode="r", *args, **kwargs):\n                    if Pa'
                    'th(path) == Path("archive/race.md") and mode in ("xb", "wb"):\n           '
                    '             with original_open(path, "w") as handle:\n                   '
                    '         handle.write("other writer")\n                    return original'
                    '_open(path, mode, *args, **kwargs)\n\n\n                with patch("builti'
                    'ns.open", competing_open):\n                    report = archive_markdown('
                    '"inbox", "archive", dry_run=False)\n                result = [report, Path'
                    '("archive/race.md").read_text()]\n                '
                ),
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
            "lesson.py": code(
                "\n            from pathlib import Path\n            import shutil\n       "
                "     from selection import eligible_md\n\n            def archive_markdown"
                "(source, destination, dry_run=True):\n                source = Path(source"
                ")\n                destination = Path(destination)\n                planne"
                "d = []\n                skipped = []\n                for name in eligible"
                "_md(source):\n                    target = destination / name\n           "
                "         if target.exists() or target.is_symlink():\n                     "
                "   skipped.append(name)\n                        continue\n               "
                "     if dry_run:\n                        destination.mkdir(parents=True, "
                'exist_ok=True)\n                        with open(source / name, "rb") as '
                "input_file:\n                            try:\n                           "
                '     with open(target, "xb") as output_file:\n                            '
                "        shutil.copyfileobj(input_file, output_file)\n                     "
                "       except FileExistsError:\n                                skipped.ap"
                "pend(name)\n                                continue\n                    "
                'planned.append(name)\n                return {"planned": planned, "skipped'
                '": skipped}\n            '
            ),
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
            "lesson.py": code(
                "\n            from pathlib import Path\n            import shutil\n       "
                "     from selection import eligible_md\n\n            def archive_markdown"
                "(source, destination, dry_run=True):\n                source = Path(source"
                ")\n                destination = Path(destination)\n                planne"
                "d = []\n                skipped = []\n                for name in eligible"
                "_md(source):\n                    target = destination / name\n           "
                "         if target.exists() or target.is_symlink():\n                     "
                "   skipped.append(name)\n                        continue\n               "
                "     if not dry_run:\n                        destination.mkdir(parents=Tr"
                'ue, exist_ok=True)\n                        with open(source / name, "rb")'
                " as input_file:\n                            try:\n                       "
                '         with open(target, "xb") as output_file:\n                        '
                "            shutil.copyfileobj(input_file, output_file)\n                 "
                "           except FileExistsError:\n                                skippe"
                "d.append(name)\n                                continue\n                "
                '    planned.append(name)\n                return {"planned": planned, "ski'
                'pped": skipped}\n            '
            ),
            "selection.py": code(
                "\n            from pathlib import Path\n\n            def eligible_md(sour"
                "ce):\n                return sorted(\n                    path.name\n     "
                "               for path in Path(source).iterdir()\n                    if "
                'path.is_file() and not path.is_symlink() and path.suffix == ".md"\n       '
                "         )\n            "
            ),
        },
    ),
}
