from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import json
import logging
import time


def setup_logger(name: str = "vxn_ramnet", level: int = logging.INFO) -> logging.Logger:
    """Create a simple console logger."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


def ensure_dir(path: str | Path) -> Path:
    """Create a directory if it does not exist."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: str | Path, payload: Dict[str, Any]) -> None:
    """Write JSON with UTF-8 and indentation."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def read_json(path: str | Path) -> Dict[str, Any]:
    """Read JSON file."""
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8"))


def unix_time() -> float:
    """Return current UNIX timestamp."""
    return time.time()


def to_posix(path: str | Path) -> str:
    """Return a stable POSIX-like path string for JSON reports."""
    return Path(path).as_posix()


def round_float(value: float, digits: int = 4) -> float:
    """Safely round numeric values for reports."""
    return round(float(value), digits)
