"""
common/file_io.py

Small helpers for loading/saving JSON test fixtures, reading the
synthetic dataset, and writing evaluation reports — keeps file-path
handling out of the actual logic modules. Used by:
  - collusion_detection/synthetic_data
  - risk_classifier/dataset
  - evaluation scripts across document_ai, risk_classifier, etc.
"""

import csv
import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> Any:
    """Load and parse a JSON file. Raises FileNotFoundError with a
    clear message if the path doesn't exist."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"JSON file not found: {p}")
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: Any, path: str | Path, indent: int = 2) -> None:
    """Write data to a JSON file, creating parent directories if needed."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, default=str)


def load_ground_truth_csv(path: str | Path) -> list[dict[str, str]]:
    """Load the ground-truth CSV (bidder_id, requirement_id,
    expected_result) as a list of row dicts, matching the format
    Gayatri's ground-truth dataset uses for accuracy scoring."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Ground-truth CSV not found: {p}")
    with p.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def save_evaluation_report(report: dict[str, Any], path: str | Path) -> None:
    """Write an evaluation report (accuracy metrics, precision/recall,
    confusion matrix, etc.) to disk as JSON, for reuse in demo slides
    or CI checks. Wraps save_json with a consistent report shape."""
    save_json(report, path)


def list_synthetic_documents(directory: str | Path, suffix: str = ".pdf") -> list[Path]:
    """List all synthetic document files of a given suffix under a
    directory — used to batch-process the test dataset."""
    d = Path(directory)
    if not d.exists():
        raise FileNotFoundError(f"Synthetic data directory not found: {d}")
    return sorted(d.glob(f"*{suffix}"))
