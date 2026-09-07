import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Your offline Python apprenticeship")
    parser.add_argument("--data-dir", type=Path, help="Use a separate local learning profile")
    from pytuitor.release import check_upgrade, installed_version

    parser.add_argument("--version", action="version", version=installed_version())
    parser.add_argument(
        "--check-upgrade",
        action="store_true",
        help="Explicitly contact PyPI to compare release versions; installs nothing",
    )
    args = parser.parse_args()
    if args.check_upgrade:
        try:
            print(check_upgrade())
        except (OSError, ValueError, KeyError) as exc:
            parser.exit(1, f"Could not check releases: {exc}\n")
        return
    from pytuitor.app import TutorApp
    from pytuitor.state import ProfileError

    try:
        app = TutorApp(data_dir=args.data_dir)
    except (ProfileError, OSError) as exc:
        parser.exit(1, f"pytuitor: {exc}\n")
    try:
        app.run()
    finally:
        app.store.close()


if __name__ == "__main__":
    main()
