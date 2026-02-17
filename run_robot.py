#!/usr/bin/env python3
"""Run Robot Framework with default output dir report/."""

import os
import sys


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    path_backup = list(sys.path)
    if root in sys.path:
        sys.path.remove(root)
    try:
        from robot.run import run_cli
    except ModuleNotFoundError as e:
        sys.path.insert(0, root)
        raise SystemExit(
            "Robot Framework not found. Install: pip install -r requirements.txt (detail: %s)" % e
        )
    sys.path = path_backup

    args = list(sys.argv[1:])
    if not any(a == "--outputdir" or a.startswith("--outputdir=") for a in args):
        args = ["--outputdir", "report"] + args
    has_suite = any(s for s in args if s.endswith(".robot") or s.endswith(".robot.txt"))
    if not has_suite:
        args = args + ["robot/bank_suite.robot"]
    return run_cli(args)


if __name__ == "__main__":
    sys.exit(main())
