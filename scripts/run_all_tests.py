"""Use the active interpreter and return pytest's exact exit status."""

import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    arguments = sys.argv[1:]
    if "--core" in arguments:
        arguments.remove("--core")
        # Explicit subset, never an automatic dependency-based skip.
        suite = [
            "phase1_python_programming",
            "phase2_data_science/section03_numpy",
            "phase2_data_science/section05_matplotlib/tests/test_basic_plots.py",
            "phase2_data_science/section05_matplotlib/projects/training_visualizer",
            "tests",
            "--deselect=tests/test_datasets.py::test_classification_generation",
            "--deselect=tests/test_cli.py::test_module_help[ecommerce_analysis.main]",
            "--deselect=tests/test_cli.py::test_module_help[exploratory_data_analysis.src.eda]",
            "--deselect=tests/test_cli.py::test_module_help[machine_learning_workflow.main]",
        ]
        arguments = [*suite, *arguments]
    return subprocess.call([sys.executable, "-m", "pytest", *arguments], cwd=root)


if __name__ == "__main__":
    raise SystemExit(main())
