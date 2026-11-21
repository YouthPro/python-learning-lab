"""Print correctness, time/required time and memory/required memory for Section 01."""

import sys
from pathlib import Path


def cli():
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root))

    from phase1_python_programming.section01_data_structures.assessment.grader import main

    return main()


if __name__ == "__main__":
    raise SystemExit(cli())
