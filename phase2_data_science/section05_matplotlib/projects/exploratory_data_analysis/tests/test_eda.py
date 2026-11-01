import pytest

from phase2_data_science.section04_pandas.projects.ecommerce_analysis.src.analysis import analyze
from phase2_data_science.section04_pandas.projects.ecommerce_analysis.src.cleaning import (
    clean_tables,
)
from phase2_data_science.section04_pandas.projects.ecommerce_analysis.src.data_loader import (
    load_tables,
)
from phase2_data_science.section05_matplotlib.projects.exploratory_data_analysis.src.eda import (
    generate_report,
)
from scripts.generate_datasets import ecommerce


@pytest.mark.parametrize("seed", [1, 7, 42])
def test_report(tmp_path, seed):
    ecommerce(tmp_path / "raw", seed, 20, 10, 100)
    tables, _ = clean_tables(load_tables(tmp_path / "raw"))
    figures = generate_report(tables, analyze(tables), tmp_path / "report")
    assert len(figures) == 8
    assert all(p.read_bytes().startswith(b"\x89PNG") for p in figures)
    assert (tmp_path / "report/eda_report.md").read_text().count("![") == 8
