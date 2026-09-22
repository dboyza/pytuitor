"""Learner journeys and plausible wrong answers missed by the original refresh."""

import ast

import pytest
from textual.widgets import Button, Static, TextArea

from pytuitor.app import TutorApp
from pytuitor.curriculum import BY_ID, default_input
from pytuitor.file_tree import FileTree
from pytuitor.runner import execute


@pytest.mark.parametrize(
    "identifier",
    [
        "pack-your-bag",
        "task-workspace",
        "comparing-sets",
        "first-light",
        "typed-contracts",
        "plugin-system",
    ],
)
async def test_old_passes_are_invalidated_without_losing_drafts(tmp_path, identifier):
    lesson = BY_ID[identifier]
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, last_lesson=identifier)
    old_revision = 3 if identifier == "comparing-sets" else 4
    entry = app.store.entry(lesson)
    entry.update(
        revision=old_revision,
        code="# my original Build\n",
        checked_code="# my original Build\n",
        checked_revision=old_revision,
        stage="repair",
        repair={
            "revision": old_revision,
            "code": "# my original Repair\n",
            "files": {"lesson.py": "# my original Repair\n", "notes.txt": "Keep my notes"},
            "checked_code": "# my original Repair\n",
            "checked_revision": old_revision,
        },
    )
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("c")
        screen = app.screen
        assert screen.stage == "build"
        assert not screen.stage_passed("build")
        assert not screen.stage_passed("repair")
        assert screen.query_one("#stage-repair", Button).disabled
        assert screen.query("#updated-notice")
        assert screen.query_one("#editor", TextArea).text == "# my original Build\n"
        assert entry["repair"]["files"]["notes.txt"] == "Keep my notes"
        assert entry["repair"]["code"] == "# my original Repair\n"


@pytest.mark.parametrize("size", [(80, 24), (140, 44)])
@pytest.mark.parametrize("identifier", ["supply-report", "task-workspace", "notes-archiver"])
async def test_refreshed_projects_through_both_editors_and_saved_stages(tmp_path, size, identifier):
    lesson = BY_ID[identifier]
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, last_lesson=identifier)
    async with app.run_test(size=size) as pilot:
        await pilot.press("c")
        screen = app.screen
        for name in ("build", "repair"):
            assert screen.stage == name
            contract = lesson.stage_contract(name)
            assert set(screen.project_files()) == set(contract.files)
            assert name.upper() in str(screen.query_one("#stage-heading", Static).content)
            if name == "repair":
                await pilot.press("f5")
                await app.workers.wait_for_complete()
                assert not screen.stage_passed(name)
            for filename, source in contract.reference_files.items():
                tree = screen.query_one(FileTree)
                tree.select_node(tree.files[filename])
                await pilot.pause()
                screen.query_one("#editor", TextArea).load_text(source)
            await pilot.press("f5")
            await app.workers.wait_for_complete()
            assert screen.stage_passed(name)
            if name == "build":
                assert app.store.status(lesson) != "completed"
                await pilot.press("ctrl+n")
                await pilot.pause()
        assert app.store.status(lesson) == "completed"
        screen.switch_stage("build")
        await pilot.pause()
        assert screen.project_files() == lesson.stage_contract("build").reference_files
        screen.switch_stage("repair")
        await pilot.pause()
        assert screen.project_files() == lesson.stage_contract("repair").reference_files
        await pilot.press("ctrl+b")
        app.screen.open_lesson(lesson)
        await pilot.pause()
        assert app.screen.stage == "repair"
        assert app.screen.project_files() == lesson.stage_contract("repair").reference_files


def test_collection_repairs_use_only_the_syntax_taught_so_far():
    for identifier in (
        "pack-your-bag",
        "list-positions",
        "tuples-and-sets",
        "comparing-sets",
        "loop-helpers",
        "nested-collections",
        "word-counts",
        "editing-collections",
        "repeat-until-done",
        "supply-report",
    ):
        stage = BY_ID[identifier].stage_contract("repair")
        for sources in (stage.starter_files, stage.reference_files):
            nodes = tuple(ast.walk(ast.parse(sources["lesson.py"])))
            assert not any(
                isinstance(
                    node,
                    (
                        ast.FunctionDef,
                        ast.Lambda,
                        ast.ListComp,
                        ast.DictComp,
                        ast.SetComp,
                        ast.GeneratorExp,
                    ),
                )
                for node in nodes
            ), identifier
            if identifier in (
                "pack-your-bag",
                "list-positions",
                "tuples-and-sets",
                "comparing-sets",
                "loop-helpers",
                "nested-collections",
            ):
                assert not any(isinstance(node, ast.Dict) for node in nodes), identifier


MUTANTS = [
    ("loop-helpers", "lesson.py", "index < len(weights)", "index <= len(weights)"),
    ("loop-helpers", "lesson.py", "range(len(labels))", "range(len(weights))"),
    ("handle-invalid-input", "lesson.py", "score > 100", "score >= 100"),
    (
        "clean-labels",
        "lesson.py",
        '" ".join(text.split()).title()',
        '" ".join(word.capitalize() for word in text.split())',
    ),
    (
        "recursive-collections",
        "lesson.py",
        "for item in items:",
        "items.reverse()\n    for item in items:",
    ),
    ("expense-report", "lesson.py", "json.dump(counts, handle)", "pass"),
    ("numeric-tools", "lesson.py", "return min(values)", "values.sort()\n    return min(values)"),
    ("repeatable-randomness", "lesson.py", 'raise ValueError("invalid draw")', "return []"),
    (
        "validate-boundaries",
        "lesson.py",
        "not name[0].isalpha()",
        "not (name[0].isalpha() or name[0] == '_')",
    ),
    ("regex-transformations", "lesson.py", 'r"<@[a-z]+>"', 'r"<@[a-z]+"'),
    (
        "queues-with-deque",
        "lesson.py",
        "queue = deque(arrivals)\n    queue.extend(waiting)",
        "queue = deque(waiting)\n    queue.extend(arrivals)",
    ),
    ("notes-archiver", "selection.py", " and not path.is_symlink()", ""),
    ("notes-archiver", "lesson.py", "skipped.append(name)", "planned.append(name)"),
    ("notes-archiver", "lesson.py", 'open(target, "xb")', 'open(target, "wb")'),
    (
        "tests-for-your-code",
        "lesson.py",
        "self.assertEqual(between(0, 0, 10), True)",
        "self.assertTrue(True)",
    ),
]


@pytest.mark.parametrize(
    "identifier,filename,before,after",
    MUTANTS,
    ids=[f"{item[0]}-{index}" for index, item in enumerate(MUTANTS)],
)
async def test_checks_reject_plausible_incomplete_repairs(identifier, filename, before, after):
    lesson = BY_ID[identifier]
    stage = lesson.stage_contract("repair")
    files = dict(stage.reference_files)
    assert before in files[filename]
    files[filename] = files[filename].replace(before, after)
    result = await execute(
        lesson, files[lesson.entrypoint], default_input(lesson, "repair"), files=files, stage=stage
    )
    assert not result.passed, identifier
    assert not result.error, "This should fail for behavior, not syntax or startup."


@pytest.mark.parametrize(
    "identifier,source",
    [
        (
            "pack-your-bag",
            "costs = list(map(int, input().split()))\nbudget = 20 - sum(costs)\nprint(budget)\n",
        ),
        (
            "word-counts",
            "from collections import Counter\nrecords = list(Counter(input().split()).items())\n",
        ),
        ("clean-labels", 'def heading(text):\n    return " ".join(text.title().split())\n'),
        (
            "recursive-collections",
            "def count_nested(items):\n"
            "    return sum(count_nested(x) if isinstance(x, list) else 1 for x in items)\n",
        ),
        (
            "queues-with-deque",
            "def serve_requests(waiting, arrivals, limit):\n"
            "    queue = arrivals + waiting\n    return queue[:limit], queue[limit:]\n",
        ),
        (
            "validate-boundaries",
            "def valid_identifier(name):\n    return bool(name) and name[0].isalpha() "
            'and all(c.isalnum() or c == "_" for c in name)\n',
        ),
    ],
)
async def test_checks_accept_alternative_implementations(identifier, source):
    lesson = BY_ID[identifier]
    stage = lesson.stage_contract("repair")
    result = await execute(
        lesson, source, default_input(lesson, "repair"), files={"lesson.py": source}, stage=stage
    )
    assert result.passed, (identifier, result.error, result.checks)
