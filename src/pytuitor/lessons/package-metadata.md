# Understand package metadata

A virtual environment gives a project its own interpreter entry point and installed packages.
It does not sandbox code or make an untrusted dependency safe.
The tutor can guide workspace environment setup; keep dependency installation deliberate and review the requested package and version first.
All exercises in this course work with the standard library after the tutor is installed.

In an external terminal, a typical project begins with `python3 -m venv .venv`.
On macOS and Linux, use `.venv/bin/python -m pip ...` to target that environment explicitly.
Avoid `sudo pip`, unknown install scripts, and copying commands you have not read.
Reproducible installations record exact versions and, when using pip requirements, verified artifact hashes with `--require-hashes`.
Dependency pins and hashes identify what you install; they are not a guarantee that its code is trustworthy.

`pyproject.toml` stores build configuration and project metadata.
The `[project]` table contains fields such as name, version, requires-python, dependencies, and scripts.
The build backend creates a wheel, an installable distribution, from source.
A package name used for installation is not always the same as its import name.

```toml
[project]
name = "small-report"
version = "0.2.0"
requires-python = ">=3.11"
dependencies = []
```

Python 3.11's `tomllib.loads(text)` parses TOML text to dictionaries and lists.
It does not install packages or evaluate arbitrary Python code.

## Build

Write `package_summary(text)`.
Input is valid TOML with a project table containing string name and version fields and an optional list of dependency strings.
Return a dictionary with exactly `name`, `version`, and `dependencies`.
Copy the name and version, and return dependencies sorted lexicographically; if absent, use an empty list.
Do not install anything or print.
The checks teach metadata inspection; an actual packaging release also requires building and installing its wheel in a clean environment.

## Repair

Repair assumes an optional field always exists and preserves arbitrary dependency order.
Apply the same contract as Build.
