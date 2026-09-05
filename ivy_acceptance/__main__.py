"""Read-only CLI entry point. Provider execution belongs to the next build stage."""
import argparse
import json
import sys
from pathlib import Path
from .canonical import InvalidManifest, read_json
from .planning import compile_plan


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    plan = sub.add_parser("plan", help="hash inputs and print a plan; never execute")
    plan.add_argument("config", type=Path)
    plan.add_argument("--root", type=Path, default=Path.cwd(), help="root of explicitly referenced inputs")
    args = parser.parse_args(argv)
    try:
        result = compile_plan(read_json(args.config), args.root)
    except (InvalidManifest, OSError, UnicodeError) as exc:
        print(json.dumps({"error": str(exc), "execution_started": False}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
