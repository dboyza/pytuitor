"""Author-side integration of every optional feature, never a learner source merger."""

from pytuitor.content.lantern.authoring import api_import, public_names
from pytuitor.project_catalog import MILESTONES


def reference_history():
    """Yield complete authored states while preserving all previously added features."""
    previous = {}
    for index, milestone in enumerate(MILESTONES):
        canonical = milestone.lesson.solution_files
        if index < 11:
            current = dict(canonical)
        elif milestone.lesson.id == "reach-package":
            current = dict(canonical)
            modules = {
                name.removesuffix(".py")
                for name in previous
                if name.endswith(".py") and name != "game.py" and not name.startswith("test_")
            }
            for name, source in previous.items():
                if not name.endswith(".py") or name.startswith("test_"):
                    current[name] = source
                    continue
                if name == "game.py":
                    continue
                for module in modules:
                    source = source.replace(f"from {module} import ", f"from .{module} import ")
                current[f"lantern_reach/{name}"] = source
                names = public_names(source, modules)
                current[name] = api_import(f"lantern_reach.{name.removesuffix('.py')}", names)
            names = public_names(current["lantern_reach/engine.py"], modules)
            current["game.py"] = (
                api_import("lantern_reach.engine", tuple(name for name in names if name != "main"))
                + "from lantern_reach.cli import main\n\n"
                + 'if __name__ == "__main__":\n    main()\n'
            )
        else:
            current = dict(previous)
            base = milestone.base_files
            assert canonical["engine.py"].startswith(base["engine.py"])
            addition = canonical["engine.py"][len(base["engine.py"]) :]
            packaged = "lantern_reach/engine.py" in current
            target = "lantern_reach/engine.py" if packaged else "engine.py"
            new_modules = []
            for name, source in canonical.items():
                if name in ("engine.py", "game.py") or base.get(name) == source:
                    continue
                if packaged and name.endswith(".py") and not name.startswith("test_"):
                    current[f"lantern_reach/{name}"] = source
                    current[name] = api_import(
                        f"lantern_reach.{name.removesuffix('.py')}", public_names(source)
                    )
                    new_modules.append(name.removesuffix(".py"))
                else:
                    current[name] = source
            if packaged:
                for module in new_modules:
                    addition = addition.replace(f"from {module} import ", f"from .{module} import ")
            current[target] += addition
            modules = {
                name.removesuffix(".py").split("/")[-1] for name in current if name.endswith(".py")
            }
            names = public_names(current[target], modules)
            if packaged:
                current["engine.py"] = api_import("lantern_reach.engine", names)
                current["game.py"] = (
                    api_import(
                        "lantern_reach.engine", tuple(name for name in names if name != "main")
                    )
                    + "from lantern_reach.cli import main\n\n"
                    + 'if __name__ == "__main__":\n    main()\n'
                )
            else:
                current["game.py"] = (
                    api_import("engine", names) + '\nif __name__ == "__main__":\n    main()\n'
                )
        current["my-trail.txt"] = "A personal detail carried through the whole expedition.\n"
        yield milestone, current
        previous = current
