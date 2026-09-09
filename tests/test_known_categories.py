from copy import deepcopy

import pytest
from textual.widgets import SelectionList

from pytuitor.app import TutorApp
from pytuitor.curriculum import SECTIONS
from pytuitor.state import Store


@pytest.mark.parametrize("size", [(80, 24), (140, 44)])
async def test_category_toggle_partial_selection_save_and_resume(tmp_path, size):
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, last_lesson="first-light")
    async with app.run_test(size=size) as pilot:
        await pilot.press("p")
        await pilot.pause()
        screen = app.screen
        listing = screen.query_one("#onboarding-concepts", SelectionList)
        assert listing.region.height > 8
        assert screen.query_one("#begin").region.bottom < size[1]
        for section in SECTIONS:
            category = f"category:{section.id}"
            topics = screen.category_topics[category]
            listing.highlighted = next(
                i
                for i in range(listing.option_count)
                if listing.get_option_at_index(i).value == category
            )
            await pilot.press("space")
            await pilot.pause()
            assert set(topics) <= set(listing.selected)
            assert category in listing.selected
            listing.deselect(topics[0])
            await pilot.pause()
            assert category not in listing.selected
            await pilot.press("space")
            await pilot.pause()
            assert set(topics) <= set(listing.selected)
            await pilot.press("space")
            await pilot.pause()
            assert not set(topics) & set(listing.selected)
        listing.highlighted = 0
        await pilot.press("space", "f5")
        await pilot.pause()
        assert set(app.store.data["familiar"]) == set(
            screen.category_topics["category:foundations"]
        )
        assert app.store.data["last_lesson"] == "first-light"
    restored = Store(tmp_path)
    assert set(restored.data["familiar"]) == set(screen.category_topics["category:foundations"])
    restored.close()


async def test_cancel_discards_bulk_selection(tmp_path):
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    before = deepcopy(app.store.data)
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("p")
        await pilot.click("#onboarding-concepts", offset=(6, 1))
        await pilot.pause()
        assert (
            "category:foundations"
            in app.screen.query_one("#onboarding-concepts", SelectionList).selected
        )
        await pilot.press("escape")
        await pilot.pause()
        assert app.store.data == before
