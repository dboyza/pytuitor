"""Build and Repair contracts for python-semantics."""

from pytuitor.experienced_authoring import (
    _check,
    _exec,
    _probe,
    _repair,
    check,
    legacy,
    probe,
    unit,
)

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
        [
            check(
                "Index records",
                "index_records([{'id': 'a', 'tags': ['cli']}, {'id': 'b', 'tags': []}])",
                {"a": {"id": "a", "tags": ["cli"]}, "b": {"id": "b", "tags": []}},
            ),
            check(
                "Nested copy is independent",
                ("(lambda r: index_records([r])['a']['tags'] is r['tags'])({'id':'a','tags':[]})"),
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
)

BUILD_INSTRUCTIONS = {
    "python-expressions": (
        "\nWrite `display_name(value)`.\nIts argument is either `None` or a string."
        '\nReturn `"Anonymous"` for `None` or a string containing only whitespace.'
        "\nOtherwise return the string with surrounding whitespace removed, preserv"
        'ing its case and internal spaces.\nFor example, `display_name("  Ravi Shah'
        '  ")` returns `"Ravi Shah"`.\nThe string `"0"` must remain `"0"`.\nDefine '
        "the function without asking for input or printing.\nChecks call it with se"
        "veral arguments; Run can be used with your own temporary print calls.\n"
    ).strip(),
    "objects-not-boxes": (
        "\nWrite `def add_tag(record, tag):` so it returns an independent copy with"
        ' `tag` appended to its `"tags"` list.\nPreserve every other field, and do '
        "not change the original record or its nested contents.\nAssume the record "
        "contains ordinary dictionaries, lists, strings, and numbers.\n\nAdd a smal"
        "l example below your function and use Run to inspect both the original and"
        " the returned value.\nCheck also tests nested metadata, so copying only th"
        "e tags list is not sufficient for this contract.\n"
    ).strip(),
    "call-contracts": (
        "\nDefine `quote(price, quantity=1, *, discount=0)`.\nArguments are finite "
        "numbers; quantity is a nonnegative integer.\nReject a negative price, nega"
        "tive quantity, or discount outside the inclusive range zero through one wi"
        "th `ValueError`.\nReturn the price times quantity after applying the fract"
        "ional discount, rounded to two decimal places.\nFor example, `quote(8, 4, "
        "discount=0.25)` returns `24.0`.\nZero quantity and a discount of one are v"
        "alid and return zero.\nDo not print or read input.\n"
    ).strip(),
    "collection-idioms": (
        "\nWrite `group_names(pairs)`.\nEach pair contains a group string and a nam"
        "e string.\nReturn a dictionary mapping each group to its distinct names in"
        " first-seen order.\nKeep groups in their first-seen order too.\nNames are "
        "case-sensitive and already cleaned; preserve each supplied string exactly."
        "\nFor example, `[('team', 'Mina'), ('team', 'Sol'), ('team', 'Mina')]` bec"
        "omes `{'team': ['Mina', 'Sol']}`.\nAccept an empty iterable and a one-pass"
        " iterator.\nDo not mutate the input or print.\n"
    ).strip(),
    "index-records": (
        "\nWrite `index_records(records)`.\nThe input is a finite iterable of dicti"
        'onaries.\nEvery record has an `"id"` key with a string value; all remainin'
        "g fields contain values supported by `copy.deepcopy`.\nReturn a dictionary"
        " mapping each identifier to a deeply independent copy of its record, inclu"
        "ding its identifier.\nPreserve identifier insertion order.\nIf an identifi"
        "er occurs twice, raise `ValueError`, even when both records have equal con"
        "tents.\nDo not mutate any input record.\nAn empty iterable returns `{}`.\n"
        "No input prompts or printed output are required.\n\nFor example, `[{'id': "
        "'r7', 'tags': ['urgent']}]` produces `{'r7': {'id': 'r7', 'tags': ['urgent"
        "']}}`.\nAppending a tag to that result must not change the source list.\nU"
        "se `from copy import deepcopy` to access the copying function.\nA dictiona"
        "ry comprehension alone would silently overwrite duplicate identifiers, so "
        "consider where validation belongs.\n"
    ).strip(),
}

REPAIR_STAGES = {
    "python-expressions": _repair(
        (
            "Write format_label(name, count). Use 'Anonymous' for a missing or blank na"
            "me and return '<name>: <count>' with the count converted to text. Preserve"
            " zero and do not print. Assume name is None or a string and count is an in"
            "teger. Strip only surrounding whitespace from names and preserve case and "
            "internal spaces."
        ),
        """
        def format_label(name, count):
            name = name.strip() if name is not None else ""
            return f"{name or 'Anonymous'}: {count}"
        """,
        """
        def format_label(name, count):
            return f"{name.strip()}: {count}"
        """,
        [
            _check(
                "Missing label",
                "format_label(None, 0)",
                "Anonymous: 0",
                "Handle None before using a string method.",
            ),
            _check(
                "Trim label",
                "format_label('  Ada  ', 3)",
                "Ada: 3",
                "Trim only the name and preserve the count.",
            ),
            _probe(
                "Blank, zero, and internal spaces",
                """
                result = [format_label(" \\t", 0), format_label("  A  B  ", -2)]
                """,
                ["Anonymous: 0", "A  B: -2"],
                "Handle whitespace-only names without losing zero or internal spaces.",
            ),
        ],
        [
            "Treat None and blank text as the same fallback case.",
            "An f-string can format the numeric count without changing its value.",
        ],
    ),
    "objects-not-boxes": _repair(
        (
            "Write merge_settings(base, overrides). Return a deep independent copy of b"
            "ase with override values applied, leaving base and its nested values uncha"
            "nged. Both arguments are dictionaries of ordinary nested containers and sc"
            "alar values. Overrides replace whole values, without recursive merging. Th"
            "e result must share no mutable nested containers with either argument."
        ),
        """
        from copy import deepcopy

        def merge_settings(base, overrides):
            result = deepcopy(base)
            result.update(deepcopy(overrides))
            return result
        """,
        """
        def merge_settings(base, overrides):
            base.update(overrides)
            return base
        """,
        [
            _check(
                "Apply overrides",
                "merge_settings({'a': 1}, {'b': 2})",
                {"a": 1, "b": 2},
                "Copy before updating.",
            ),
            _check(
                "Keep nested input independent",
                "(lambda x: (merge_settings(x, {}) is x, "
                "merge_settings(x, {})['meta'] is x['meta']))({'meta': []})",
                (False, False),
                "A shallow or in-place copy still aliases nested data.",
            ),
            _probe(
                "Overrides are independent too",
                (
                    """
                base = {"meta": {"tags": ["old"]}, "keep": []}
                overrides = {"meta": {"tags": ["new"]}}
                merged = merge_settings(base, overrides)
                merged["meta"]["tags"].append("changed")
                merged["keep"].append(1)
                result = (base, overrides)
                """
                ),
                ({"meta": {"tags": ["old"]}, "keep": []}, {"meta": {"tags": ["new"]}}),
                "Copy override values as well as the base before sharing the result.",
            ),
        ],
        ["Use deepcopy for nested independence.", "Update the copy, not the caller's mapping."],
    ),
    "call-contracts": _repair(
        (
            "Define label(text, /, prefix='item', *, upper=False). Return prefix plus '"
            ": ' plus text, uppercased only when requested, and preserve the positional"
            "-only and keyword-only contract. Both text and prefix are strings. Upperca"
            "se the whole result only when upper is true. Passing text by keyword or up"
            "per positionally must raise TypeError."
        ),
        """
        def label(text, /, prefix="item", *, upper=False):
            result = f"{prefix}: {text}"
            return result.upper() if upper else result
        """,
        """
        def label(text, prefix="item", upper=False):
            return f"{text}: {prefix}".upper() if upper else f"{text}: {prefix}"
        """,
        [
            _check(
                "Default label",
                "label('report')",
                "item: report",
                "Put the default prefix before the text.",
            ),
            _check(
                "Upper option",
                "label('report', prefix='file', upper=True)",
                "FILE: REPORT",
                "Uppercase the completed label only when requested.",
            ),
            _check(
                "Call contract",
                _exec(
                    """
                    try:
                        label(text="x")
                    except TypeError:
                        result = True
                    else:
                        result = False
                    """
                ),
                True,
                "A slash makes text positional-only.",
            ),
            _probe(
                "Reject a positional option",
                (
                    """
                try:
                    label("x", "tag", True)
                except TypeError:
                    result = True
                else:
                    result = False
                """
                ),
                True,
                "A bare star makes upper keyword-only.",
            ),
        ],
        [
            "Use a slash for positional-only text and a bare star before upper.",
            "Build the normal label first, then conditionally uppercase it.",
        ],
    ),
    "collection-idioms": _repair(
        (
            "Define count_words(words). Return a first-seen-order dictionary of word co"
            "unts for a one-pass iterable. Preserve case and do not mutate input. Words"
            " are strings. Empty input returns {}. Keep words such as A and a separate "
            "and preserve first insertion order."
        ),
        """
        def count_words(words):
            counts = {}
            for word in words:
                counts[word] = counts.get(word, 0) + 1
            return counts
        """,
        """
        def count_words(words):
            return {word: 1 for word in words}
        """,
        [
            _check(
                "Count repeats",
                "count_words(['red', 'blue', 'red'])",
                {"red": 2, "blue": 1},
                "Increment an existing count instead of replacing it.",
            ),
            _check(
                "One-pass words",
                "count_words(iter(['a', 'a']))",
                {"a": 2},
                "Iterate once and build the dictionary as you go.",
            ),
            _probe(
                "Empty, case, and insertion order",
                (
                    """
                result = [
                    list(count_words(iter(["b", "A", "a", "b"])).items()),
                    count_words([]),
                ]
                """
                ),
                [[("b", 2), ("A", 1), ("a", 1)], {}],
                (
                    "Counts are case-sensitive and dictionary insertion order follows the first"
                    " occurrence."
                ),
            ),
        ],
        [
            "Use get(word, 0) for a missing count.",
            "Dictionary assignment preserves the first insertion order.",
        ],
    ),
    "index-records": _repair(
        (
            "Define first_by_key(records, key). Return a new dictionary containing the "
            "first record for each key, deep-copied so later caller changes cannot alte"
            "r the result. Accept a finite one-pass iterable of dictionaries. Call key "
            "exactly once per record; its result is hashable. Keep first-seen key order"
            " and return {} for empty input."
        ),
        """
        from copy import deepcopy

        def first_by_key(records, key):
            result = {}
            for record in records:
                value = key(record)
                if value not in result:
                    result[value] = deepcopy(record)
            return result
        """,
        """
        def first_by_key(records, key):
            return {key(record): record for record in records}
        """,
        [
            _check(
                "Keep first record",
                "first_by_key([{'id': 'a', 'n': 1}, {'id': 'a', 'n': 2}], lambda r: r['id'])",
                {"a": {"id": "a", "n": 1}},
                "Only store a key the first time it appears.",
            ),
            _check(
                "Copy records",
                "(lambda r: first_by_key([r], lambda x: x['id'])['a'] is r)({'id': 'a'})",
                False,
                "Copy each selected record before storing it.",
            ),
            _probe(
                "Copy nested records and call key once",
                (
                    """
                records = [
                    {"id": 2, "nested": []},
                    {"id": 2, "nested": [1]},
                    {"id": 1, "nested": []},
                ]
                calls = []


                def identify(record):
                    calls.append(record["id"])
                    return record["id"]


                selected = first_by_key(iter(records), identify)
                selected[2]["nested"].append(7)
                result = (
                    list(selected),
                    calls,
                    records[0]["nested"],
                    first_by_key([], identify),
                )
                """
                ),
                ([2, 1], [2, 2, 1], [], {}),
                "Copy nested values and evaluate the key once even for duplicates.",
            ),
        ],
        ["Check membership before assignment.", "deepcopy protects nested record data too."],
    ),
}

EXTRA_CHECKS = {
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
}
