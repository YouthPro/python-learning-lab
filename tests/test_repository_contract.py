"""Static checks verify the curriculum without importing learner solutions."""

import ast
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "docs/exercise_manifest.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("section,expected", [(1, 30), (2, 9), (3, 15), (4, 15), (5, 8), (6, 8)])
def test_exercise_counts(section, expected):
    records = [r for r in MANIFEST if r["section"] == section]
    assert len(records) == expected
    assert len({r["name"] for r in records}) == expected


@pytest.mark.parametrize("record", MANIFEST, ids=lambda r: f"s{r['section']}-{r['id']}")
def test_documented_contract_and_source(record):
    section = next(ROOT.glob(f"phase*/section{record['section']:02d}_*"))
    source = section / "exercises" / f"{record['module']}.py"
    nodes = ast.parse(source.read_text(encoding="utf-8")).body
    assert any(
        isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name == record["name"]
        for node in nodes
    )
    assert record["title"] in (section / "exercise_catalog.md").read_text(encoding="utf-8")
    assert "；" in record["examples"]
    assert all(record[field] for field in ["description", "edges", "topics", "difficulty"])
    test_file = section / "tests" / f"test_{record['module']}.py"
    test_source = test_file.read_text(encoding="utf-8")
    assert record["name"] in test_source


@pytest.mark.parametrize(
    "project", sorted(ROOT.glob("phase*/section*/projects/*")), ids=lambda p: p.name
)
def test_complete_project(project):
    assert (project / "README.md").is_file()
    assert list((project / "tests").glob("test_*.py"))
    assert list((project / "src").rglob("*.py"))
    for path in (project / "src").rglob("*.py"):
        assert "NotImplementedError" not in path.read_text(encoding="utf-8")


def test_project_total():
    # Preserve the original phases' contract as the curriculum grows.
    legacy = [
        *ROOT.glob("phase1_*/section*/projects/*/README.md"),
        *ROOT.glob("phase2_*/section*/projects/*/README.md"),
    ]
    assert len(legacy) == 11


def test_local_document_links_exist():
    for document in ROOT.rglob("*.md"):
        if any(part.startswith(".") for part in document.relative_to(ROOT).parts):
            continue
        text = document.read_text(encoding="utf-8")
        for link in re.findall(r"\]\(([^)]+)\)", text):
            if "://" in link or link.startswith("#"):
                continue
            target = link.split("#", 1)[0]
            assert (document.parent / target).exists(), f"{document}: {link}"
