"""Curriculum inventory without requiring learners to leave their TODOs empty."""

import ast
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "docs/phase3_exercise_manifest.json").read_text())


@pytest.mark.parametrize("section,count", [(7, 18), (8, 15), (9, 10)])
def test_phase3_problem_counts(section, count):
    rows = [r for r in MANIFEST if r["section"] == section]
    assert len(rows) == count and {r["id"] for r in rows} == set(range(1, count + 1))


@pytest.mark.parametrize("record", MANIFEST, ids=lambda r: f"s{r['section']}-{r['id']}")
def test_problem_contract_and_three_cases(record):
    folder = next((ROOT / "phase3_deep_learning").glob(f"section{record['section']:02d}_*"))
    tree = ast.parse((folder / "exercises" / (record["module"] + ".py")).read_text())
    node = next(
        n
        for n in tree.body
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == record["name"]
    )
    doc = ast.get_docstring(node)
    for field in ["Input Shape", "Output Shape", "Expected dtype", "computation graph", "Hint"]:
        assert field in doc
    test_tree = ast.parse((folder / "tests" / ("test_" + record["module"] + ".py")).read_text())
    test = next(
        n
        for n in test_tree.body
        if isinstance(n, ast.FunctionDef) and n.name == "test_" + record["name"]
    )
    parametrizations = [
        d
        for d in test.decorator_list
        if isinstance(d, ast.Call)
        and isinstance(d.func, ast.Attribute)
        and d.func.attr == "parametrize"
    ]
    assert any(
        isinstance(p.args[1], (ast.List, ast.Tuple)) and len(p.args[1].elts) >= 3
        for p in parametrizations
    )
    assert any(isinstance(n, ast.Assert) for n in ast.walk(test))


def test_phase3_project_count_and_no_exercise_imports():
    projects = list((ROOT / "phase3_deep_learning").glob("section*/projects/*"))
    assert len(projects) == 6
    for project in projects:
        assert (project / "README.md").is_file()
        assert list((project / "tests").glob("test_*.py"))
        for path in (project / "src").rglob("*.py"):
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, ast.ImportFrom):
                    assert "exercises" not in (node.module or "").split(".")
