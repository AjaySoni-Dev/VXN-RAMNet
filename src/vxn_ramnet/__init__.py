"""
VXN-RAMNet production-grade modular package.

This package modularizes the stable notebook:
04_backtracking_branch_graph_learning.ipynb

Main flow:
learning video + query videos
-> frame extraction
-> EfficientNetB0 embeddings
-> backtracking graph learning
-> query branch classification
-> JSON / CSV / Markdown reports
"""

from .config import BacktrackingPipelineConfig
from .pipeline import BacktrackingPipeline, run_backtracking_pipeline

__all__ = [
    "BacktrackingPipelineConfig",
    "BacktrackingPipeline",
    "run_backtracking_pipeline",
]
__version__ = "0.2.0"
