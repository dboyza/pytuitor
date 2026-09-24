"""Request a comfortable launch size from supported local terminal windows."""

import os
import sys


def resize_terminal_if_needed() -> None:
    """Send one grow-only request; terminals may ignore it or limit it to the display."""
    if os.environ.get("TERM_PROGRAM") not in {"Apple_Terminal", "iTerm.app"}:
        return
    if os.environ.get("TERM", "dumb") in {"", "dumb", "unknown"}:
        return
    if any(os.environ.get(name) for name in ("CI", "SSH_CONNECTION", "SSH_TTY", "TMUX", "STY")):
        return
    try:
        if not sys.stdin.isatty() or not sys.stdout.isatty():
            return
        columns, rows = os.get_terminal_size(sys.stdout.fileno())
        if columns <= 0 or rows <= 0 or (columns >= 120 and rows >= 30):
            return
        # XTWINOPS: resize the text area in rows and columns. Preserve larger dimensions.
        sys.stdout.write(f"\x1b[8;{max(rows, 30)};{max(columns, 120)}t")
        sys.stdout.flush()
    except (OSError, ValueError):
        # Sizing is optional; startup and the responsive layout must still work.
        return
