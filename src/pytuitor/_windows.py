"""Standard-library Win32 operations, imported only on Windows.

The launcher joins a kill-on-close job before starting any requested program.
Its non-inheritable job handle also closes when the launcher is forcibly stopped.
"""

import ctypes
import json
import os
import subprocess
import sys
from contextlib import contextmanager
from ctypes import wintypes
from pathlib import Path

kernel = ctypes.WinDLL("kernel32", use_last_error=True)
SIZE_T = ctypes.c_size_t


def _function(name, arguments, result=wintypes.BOOL):
    function = getattr(kernel, name)
    function.argtypes = arguments
    function.restype = result
    return function


_close = _function("CloseHandle", [wintypes.HANDLE])
_create_job = _function("CreateJobObjectW", [ctypes.c_void_p, wintypes.LPCWSTR], wintypes.HANDLE)
_set_job = _function(
    "SetInformationJobObject", [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
)
_assign_job = _function("AssignProcessToJobObject", [wintypes.HANDLE, wintypes.HANDLE])
_current_process = _function("GetCurrentProcess", [], wintypes.HANDLE)
_move = _function("MoveFileExW", [wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.DWORD])
_create_file = _function(
    "CreateFileW",
    [
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        ctypes.c_void_p,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.HANDLE,
    ],
    wintypes.HANDLE,
)
_file_info = _function("GetFileInformationByHandle", [wintypes.HANDLE, ctypes.c_void_p])


class BasicLimits(ctypes.Structure):
    _fields_ = [
        ("process_time", ctypes.c_int64),
        ("job_time", ctypes.c_int64),
        ("flags", wintypes.DWORD),
        ("minimum_working_set", SIZE_T),
        ("maximum_working_set", SIZE_T),
        ("active_processes", wintypes.DWORD),
        ("affinity", SIZE_T),
        ("priority", wintypes.DWORD),
        ("scheduling", wintypes.DWORD),
    ]


class ExtendedLimits(ctypes.Structure):
    _fields_ = [
        ("basic", BasicLimits),
        ("io_counters", ctypes.c_uint64 * 6),
        ("process_memory", SIZE_T),
        ("job_memory", SIZE_T),
        ("peak_process_memory", SIZE_T),
        ("peak_job_memory", SIZE_T),
    ]


class FileInformation(ctypes.Structure):
    _fields_ = [
        ("attributes", wintypes.DWORD),
        ("creation", wintypes.FILETIME),
        ("access", wintypes.FILETIME),
        ("write", wintypes.FILETIME),
        ("volume", wintypes.DWORD),
        ("size_high", wintypes.DWORD),
        ("size_low", wintypes.DWORD),
        ("links", wintypes.DWORD),
        ("index_high", wintypes.DWORD),
        ("index_low", wintypes.DWORD),
    ]


def replace_profile(source: str, destination: Path) -> None:
    # Same-volume replacement, with write-through rather than Unix directory fsync.
    if not _move(str(source), str(destination), 0x1 | 0x8):
        raise ctypes.WinError(ctypes.get_last_error())


@contextmanager
def open_path(path: Path, *, directory: bool = False):
    """Pin an entry against rename, refuse reparse points, and own its handle."""
    import msvcrt

    handle = _create_file(
        str(path),
        0 if directory else 0x80000000,
        0x1 | 0x2,
        None,
        3,
        0x00200000 | 0x02000000,
        None,
    )
    if handle == wintypes.HANDLE(-1).value:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        information = FileInformation()
        if not _file_info(handle, ctypes.byref(information)):
            raise ctypes.WinError(ctypes.get_last_error())
        if information.attributes & 0x400:
            raise OSError("Symbolic links and reparse points are not run files")
        if bool(information.attributes & 0x10) != directory:
            raise OSError("The run-file entry changed type")
        if directory:
            yield None
        else:
            descriptor = msvcrt.open_osfhandle(handle, os.O_RDONLY | os.O_BINARY)
            handle = None  # The file descriptor now owns it.
            with os.fdopen(descriptor, "rb") as stream:
                yield stream
    finally:
        if handle is not None:
            _close(handle)


def launch() -> None:
    limits = json.loads(sys.argv[1])
    job = _create_job(None, None)
    if not job:
        raise ctypes.WinError(ctypes.get_last_error())
    information = ExtendedLimits()
    information.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
    if limits:
        information.basic.flags |= 0x2 | 0x200  # Per-process CPU and total job memory.
        information.basic.process_time = limits["cpu_seconds"] * 10_000_000
        information.job_memory = limits["memory_bytes"]
    if not _set_job(job, 9, ctypes.byref(information), ctypes.sizeof(information)):
        error = ctypes.get_last_error()
        _close(job)
        raise ctypes.WinError(error)
    if not _assign_job(job, _current_process()):
        error = ctypes.get_last_error()
        _close(job)
        raise ctypes.WinError(error)
    # Keep job alive until process exit. Closing it explicitly would kill this
    # launcher too, before it could return the child's exit status.
    code = subprocess.call(sys.argv[2:])
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(code)


if __name__ == "__main__":
    launch()
