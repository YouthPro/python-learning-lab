"""Run the documented project flows in an isolated temporary output directory.

--core runs the eight projects that need only the standard library, NumPy,
Pillow and Matplotlib. Full mode additionally runs Pandas/Scikit-learn flows.
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P1 = "phase1_python_programming"
P2 = "phase2_data_science"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--core", action="store_true")
    args = parser.parse_args(argv)
    with tempfile.TemporaryDirectory(prefix="python-lab-smoke-") as temporary:
        root = Path(temporary)
        data = root / "data"

        def run(module, *arguments):
            command = [sys.executable, "-m", module, *map(str, arguments)]
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=180)
            if result.returncode:
                raise RuntimeError(f"{module}\n{result.stdout}\n{result.stderr}")
            print(f"PASS {module}")

        run("scripts.generate_datasets", "--output", data, "--only", "core" if args.core else "all")
        text = f"{P1}.section01_data_structures.projects.text_analyzer.src.text_analyzer.cli"
        toolkit = f"{P1}.section02_python_engineering.projects.file_toolkit.src.file_toolkit.cli"
        run(
            text,
            data / "sample.txt",
            data / "sample.txt",
            "--stop-words",
            "data",
            "--output",
            root / "text",
        )
        run(toolkit, "scan", data / "ecommerce")
        run(toolkit, "hash", data / "sample.txt")
        run(toolkit, "duplicates", data / "ecommerce")
        run(toolkit, "rename", data, "--mapping", '{"sample.txt":"sample_new.txt"}')
        run(
            toolkit,
            "merge",
            data / "ecommerce/users.csv",
            data / "ecommerce/users.csv",
            "--output",
            root / "merge.csv",
        )
        run(
            toolkit,
            "merge",
            data / "ecommerce/users.csv",
            data / "ecommerce/users.csv",
            "--output",
            root / "merge.csv",
            "--apply",
        )
        run(toolkit, "normalize", data / "manifest.json", "--output", root / "normalized.json")
        run(
            toolkit,
            "normalize",
            data / "manifest.json",
            "--output",
            root / "normalized.json",
            "--apply",
        )
        run(
            "dataset_inspector",
            "--input",
            data / "ecommerce/users.csv",
            "--output",
            root / "inspection",
        )
        example = (
            ROOT
            / f"{P1}/section02_python_engineering/projects/dataset_inspector/examples/sample.json"
        )
        run(
            "dataset_inspector",
            "--input",
            example,
            "--strategy",
            "fill",
            "--output",
            root / "inspection_json",
        )
        csv_example = example.with_suffix(".csv")
        cleaning = f"{P1}.section02_python_engineering.projects.dataset_cleaning_pipeline.src.cleaning_pipeline"
        run(
            cleaning,
            "--input",
            csv_example,
            "--output",
            root / "clean.csv",
            "--fill",
            '{"salary":"0"}',
            "--types",
            '{"age":"int","salary":"float"}',
            "--columns",
            "age",
            "salary",
            "--report",
            root / "cleaning.json",
        )
        image = f"{P2}.section03_numpy.projects.image_processor.src.image_processor"
        for operation in ["grayscale", "brightness", "contrast", "normalize", "crop", "rotate"]:
            run(image, data / "sample.png", "--operation", operation, "--output", root / operation)
        run(
            f"{P2}.section03_numpy.projects.vector_similarity.src.vector_similarity",
            "--input",
            data / "vectors.npy",
            "--output",
            root / "vectors.json",
        )
        regression = f"{P2}.section03_numpy.projects.linear_regression.main"
        run(regression, "--input", data / "regression.npz", "--output", root / "regression")
        run(
            regression,
            "--input",
            data / "regression.npz",
            "--batch-size",
            "32",
            "--output",
            root / "mini",
        )
        run(
            f"{P2}.section05_matplotlib.projects.training_visualizer.src.training_visualizer",
            data / "training_log.csv",
            data / "training_log_b.csv",
            "--output",
            root / "training",
        )
        if not args.core:
            run(
                f"{P2}.section04_pandas.projects.ecommerce_analysis.main",
                "--input",
                data / "ecommerce",
                "--output",
                root / "ecommerce",
            )
            run(
                f"{P2}.section05_matplotlib.projects.exploratory_data_analysis.src.eda",
                "--input",
                data / "ecommerce",
                "--output",
                root / "eda",
            )
            import yaml

            project = ROOT / f"{P2}/section06_sklearn/projects/machine_learning_workflow"
            config = yaml.safe_load((project / "configs/config.yaml").read_text())
            for task, name in [("regression", "housing"), ("classification", "classification")]:
                config[task]["input"] = str(data / f"{name}.csv")
            config_path = root / "config.yaml"
            config_path.write_text(yaml.safe_dump(config))
            module = f"{P2}.section06_sklearn.projects.machine_learning_workflow.main"
            run(module, "--config", config_path, "--task", "all", "--output", root / "ml")
            run(
                module,
                "--predict-model",
                root / "ml/models/regression.joblib",
                "--input",
                data / "housing.csv",
                "--predictions",
                root / "predictions.csv",
            )
    print("All requested project flows passed.")


if __name__ == "__main__":
    main()
