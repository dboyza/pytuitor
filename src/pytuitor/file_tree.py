"""Compact explorer for the current stage's in-memory workspace."""

from collections.abc import Iterable

from rich.style import Style
from rich.text import Text
from textual.binding import Binding
from textual.widgets import Tree
from textual.widgets.tree import TreeNode


class FileTree(Tree[str]):
    BINDINGS = [
        Binding("left", "collapse_folder", "Collapse folder", show=False),
        Binding("right", "expand_folder", "Expand folder", show=False),
    ]

    def __init__(self) -> None:
        super().__init__("Files", id="file-tree")
        self.show_root = False
        self.show_guides = False
        self.guide_depth = 2
        self.files: dict[str, TreeNode[str]] = {}
        self.folders: dict[str, TreeNode[str]] = {}
        self.active_file = ""

    def set_files(self, paths: Iterable[str], active_file: str) -> None:
        collapsed = {path for path, node in self.folders.items() if not node.is_expanded}
        self.clear()
        self.files.clear()
        self.folders.clear()
        # Sorting each level places folders before files, like an editor explorer.
        branches = {}
        for path in paths:
            branch = branches
            parts = path.split("/")
            for part in parts[:-1]:
                branch = branch.setdefault(part, {})
            branch[parts[-1]] = path

        def populate(parent: TreeNode[str], entries: dict, prefix: str = "") -> None:
            for name, value in sorted(
                entries.items(),
                key=lambda item: (not isinstance(item[1], dict), item[0].casefold()),
            ):
                path = prefix + name
                if isinstance(value, dict):
                    node = parent.add(Text(name), data=path, expand=path not in collapsed)
                    self.folders[path] = node
                    populate(node, value, path + "/")
                else:
                    self.files[path] = parent.add_leaf(Text(name), data=path)

        populate(self.root, branches)
        self.root.expand()
        self.mark_active(active_file)

    def mark_active(self, path: str) -> None:
        self.active_file = path
        for name, node in self.files.items():
            node.set_label(
                Text(name.rsplit("/", 1)[-1], style="bold #ffd343" if name == path else "")
            )
        node = self.files[path]
        parent = node.parent
        while parent is not None:
            parent.expand()
            parent = parent.parent
        self.call_after_refresh(self.reveal_active)

    def reveal_active(self) -> None:
        self.move_cursor(self.files[self.active_file])

    def render_label(self, node: TreeNode[str], base_style: Style, style: Style) -> Text:
        label = super().render_label(node, base_style, style)
        if not node.allow_expand and node.data == self.active_file:
            label.stylize("bold #ffd343")
        return label

    def action_collapse_folder(self) -> None:
        node = self.cursor_node
        if node is None:
            return
        if node.allow_expand and node.is_expanded:
            node.collapse()
        elif node.parent is not self.root:
            self.move_cursor(node.parent)

    def action_expand_folder(self) -> None:
        node = self.cursor_node
        if node is None or not node.allow_expand:
            return
        if not node.is_expanded:
            node.expand()
        elif node.children:
            self.move_cursor(node.children[0])
