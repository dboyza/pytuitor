"""Launch resizing is optional, local, and never reduces either dimension."""

import io
import os

import pytest

from pytuitor import terminal_size


class TerminalOutput(io.StringIO):
    def isatty(self):
        return True

    def fileno(self):
        return 1


@pytest.fixture
def terminal(monkeypatch):
    output = TerminalOutput()
    monkeypatch.setattr(terminal_size.sys, "stdin", output)
    monkeypatch.setattr(terminal_size.sys, "stdout", output)
    monkeypatch.setenv("TERM_PROGRAM", "Apple_Terminal")
    monkeypatch.setenv("TERM", "xterm-256color")
    for name in ("CI", "SSH_CONNECTION", "SSH_TTY", "TMUX", "STY"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(
        terminal_size.os, "get_terminal_size", lambda fd: os.terminal_size((80, 24))
    )
    return output


@pytest.mark.parametrize(
    "name,value",
    [
        ("TERM_PROGRAM", "vscode"),
        ("TERM_PROGRAM", ""),
        ("TERM", "dumb"),
        ("CI", "true"),
        ("SSH_CONNECTION", "remote"),
        ("SSH_TTY", "/dev/pts/1"),
        ("TMUX", "/tmp/tmux/session"),
        ("STY", "session"),
    ],
)
def test_resize_skips_unsupported_or_managed_sessions(monkeypatch, terminal, name, value):
    monkeypatch.setenv(name, value)
    terminal_size.resize_terminal_if_needed()
    assert terminal.getvalue() == ""


@pytest.mark.parametrize("stream", ["stdin", "stdout"])
def test_redirected_streams_never_receive_window_commands(monkeypatch, terminal, stream):
    redirected = io.StringIO()
    monkeypatch.setattr(terminal_size.sys, stream, redirected)
    terminal_size.resize_terminal_if_needed()
    assert terminal.getvalue() == redirected.getvalue() == ""


@pytest.mark.parametrize("size", [(0, 0), (0, 30), (120, 0)])
def test_unknown_size_does_not_request_maximization(monkeypatch, terminal, size):
    monkeypatch.setattr(terminal_size.os, "get_terminal_size", lambda fd: os.terminal_size(size))
    terminal_size.resize_terminal_if_needed()
    assert terminal.getvalue() == ""


def test_size_lookup_failure_does_not_prevent_launch(monkeypatch, terminal):
    def unavailable(fd):
        raise OSError("No terminal size available")

    monkeypatch.setattr(terminal_size.os, "get_terminal_size", unavailable)
    terminal_size.resize_terminal_if_needed()
    assert terminal.getvalue() == ""


def test_failed_resize_request_does_not_prevent_launch(monkeypatch, terminal):
    def rejected(text):
        raise OSError("Terminal disconnected")

    monkeypatch.setattr(terminal, "write", rejected)
    terminal_size.resize_terminal_if_needed()
