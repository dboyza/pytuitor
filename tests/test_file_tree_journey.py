"""Navigate and edit the compact explorer through learner controls."""

import pytest
from textual.widgets import Input, TextArea

from pytuitor.app import TutorApp
from pytuitor.curriculum import BY_ID
from pytuitor.file_tree import FileTree


@pytest.mark.parametrize("size", [(80, 24), (140, 44)], ids=["compact", "wide"])
async def test_explorer_files_folders_and_drafts(tmp_path, size):
    app = TutorApp(tmp_path)
    lesson = BY_ID["first-light"]
    app.store.data.update(onboarded=True, last_lesson=lesson.id)
    async with app.run_test(size=size) as pilot:
        await pilot.press("c", "ctrl+t")
        screen = app.screen
        editor = screen.query_one(TextArea)
        tree = screen.query_one(FileTree)
        sidebar = screen.query_one("#file-sidebar")
        assert sidebar.region.width == 20
        assert editor.region.width >= 50
        assert editor.region.height >= 5
        await pilot.press("#", "a")
        await pilot.click("#add-file")
        await pilot.click("#new-file")
        app.screen.query_one(Input).value = "notes/résumé.txt"
        await pilot.press("enter")
        await pilot.pause()
        assert screen.active_file == "notes/résumé.txt"
        assert editor.language is None
        await pilot.press("h", "i")
        await pilot.press("ctrl+e", "left")
        assert tree.cursor_node == tree.folders["notes"]
        await pilot.press("left")
        assert not tree.folders["notes"].is_expanded
        await pilot.press("right", "right", "enter")
        assert editor.has_focus
        assert editor.text == "hi"
        await pilot.press("ctrl+e", "down", "enter")
        assert screen.active_file == lesson.entrypoint
        assert editor.text == "#a"
        assert editor.language == "python"
        assert screen.project_files()["notes/résumé.txt"] == "hi"

        await pilot.click("#toggle-files")
        await pilot.pause()
        assert not sidebar.display
        wider = editor.region.width
        await pilot.press("ctrl+e")
        await pilot.pause()
        assert tree.has_focus
        assert sidebar.display
        assert editor.region.width < wider
        await pilot.press("up", "enter")
        assert editor.text == "hi"
        screen.action_remove_file()
        await pilot.pause()
        await pilot.click("#remove-file-confirm")
        await pilot.pause()
        assert "notes/résumé.txt" not in tree.files
        assert "notes" not in tree.folders
        assert screen.active_file == lesson.entrypoint
        assert editor.text == "#a"
        assert editor.language == "python"


async def test_explorer_mouse_selection_resizing_and_hidden_focus(tmp_path):
    app = TutorApp(tmp_path)
    lesson = BY_ID["first-light"]
    app.store.data.update(onboarded=True, last_lesson=lesson.id)
    app.store.entry(lesson)["files"] = {lesson.entrypoint: "# saved", "notes.txt": "notes"}
    async with app.run_test(size=(140, 44)) as pilot:
        await pilot.press("c")
        screen = app.screen
        tree = screen.query_one(FileTree)
        await pilot.click(tree, offset=(3, 2))
        assert screen.active_file == "notes.txt"
        assert screen.query_one(TextArea).text == "notes"
        await pilot.resize_terminal(80, 24)
        await pilot.pause()
        assert screen.query_one("#file-sidebar").display
        await pilot.press("ctrl+t")
        assert screen.active_pane == "console"
        assert not screen.query_one("#file-sidebar").display
        await pilot.click("#toggle-files")
        await pilot.pause()
        assert tree.has_focus
        assert screen.query_one("#file-sidebar").display
        screen.action_toggle_files()
        await pilot.pause()
        assert screen.query_one(TextArea).has_focus
        await pilot.resize_terminal(140, 44)
        await pilot.press("ctrl+e")
        await pilot.pause()
        assert tree.has_focus
        assert tree.cursor_node.data == "notes.txt"
