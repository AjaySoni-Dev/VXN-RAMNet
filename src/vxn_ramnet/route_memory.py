from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List
import numpy as np

from .utils import write_json


COMMON_LABEL = 0
JUNCTION_LABEL = 1
FIRST_BRANCH_LABEL = 2
BACKTRACK_LABEL = 3
SECOND_BRANCH_LABEL = 4


@dataclass
class GraphMemoryPaths:
    graph_memory_file: Path
    graph_metadata_file: Path


@dataclass
class ComponentMemory:
    name: str
    label: int
    embeddings: np.ndarray
    flipped_embeddings: np.ndarray
    centroid: np.ndarray


def save_graph_memory(
    graph_memory_file: Path,
    graph_metadata_file: Path,
    arrays: Dict,
    metadata: Dict,
) -> GraphMemoryPaths:
    """Save graph memory arrays and metadata."""
    graph_memory_file.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(graph_memory_file, **arrays)
    write_json(graph_metadata_file, metadata)

    return GraphMemoryPaths(
        graph_memory_file=graph_memory_file,
        graph_metadata_file=graph_metadata_file,
    )


def load_graph_memory(graph_memory_file: str | Path) -> Dict:
    """Load graph memory NPZ as a dictionary of arrays."""
    data = np.load(graph_memory_file, allow_pickle=True)
    return {key: data[key] for key in data.files}


def get_component(
    memory_embeddings: np.ndarray,
    memory_embeddings_flip: np.ndarray,
    memory_labels: np.ndarray,
    centroids: np.ndarray,
    component_names: List[str],
    label: int,
) -> ComponentMemory:
    """Extract one component memory by label."""
    return ComponentMemory(
        name=str(component_names[label]),
        label=label,
        embeddings=memory_embeddings[memory_labels == label],
        flipped_embeddings=memory_embeddings_flip[memory_labels == label],
        centroid=centroids[label],
    )
