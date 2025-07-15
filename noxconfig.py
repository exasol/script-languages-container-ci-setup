from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    root: Path = Path(__file__).parent
    doc: Path = Path(__file__).parent / "doc"
    source: Path = Path(__file__).parent / "exasol"
    version_file: Path = (
        Path(__file__).parent / "exasol" / "slc_ci_setup" / "version.py"
    )
    path_filters: Iterable[str] = (
        "dist",
        ".eggs",
        "venv",
    )

    plugins = []
    python_versions = ["3.10", "3.11", "3.12", "3.13"]
    exasol_versions = []


PROJECT_CONFIG = Config()
