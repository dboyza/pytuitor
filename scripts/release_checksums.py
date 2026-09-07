"""Generate a checksum manifest for locally built release artifacts."""

import hashlib
from pathlib import Path


def main():
    artifacts = sorted([*Path("dist").glob("*.whl"), *Path("dist").glob("*.tar.gz")])
    if not artifacts:
        raise SystemExit("Run uv build first.")
    lines = [f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}" for path in artifacts]
    Path("dist/SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Generated dist/SHA256SUMS")


if __name__ == "__main__":
    main()
