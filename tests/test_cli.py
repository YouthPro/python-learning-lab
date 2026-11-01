"""Every documented project exposes a real argparse entry point."""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULES = [
    "phase1_python_programming.section01_data_structures.projects.text_analyzer.src.text_analyzer.cli",
    "phase1_python_programming.section02_python_engineering.projects.file_toolkit.src.file_toolkit.cli",
    "dataset_inspector",
    "phase1_python_programming.section02_python_engineering.projects.dataset_cleaning_pipeline.src.cleaning_pipeline",
    "phase2_data_science.section03_numpy.projects.image_processor.src.image_processor",
    "phase2_data_science.section03_numpy.projects.vector_similarity.src.vector_similarity",
    "phase2_data_science.section03_numpy.projects.linear_regression.main",
    "phase2_data_science.section04_pandas.projects.ecommerce_analysis.main",
    "phase2_data_science.section05_matplotlib.projects.exploratory_data_analysis.src.eda",
    "phase2_data_science.section05_matplotlib.projects.training_visualizer.src.training_visualizer",
    "phase2_data_science.section06_sklearn.projects.machine_learning_workflow.main",
]


@pytest.mark.parametrize("module", MODULES, ids=lambda name: name.split("projects.")[-1])
def test_module_help(module):
    result = subprocess.run(
        [sys.executable, "-m", module, "--help"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert "usage:" in result.stdout
