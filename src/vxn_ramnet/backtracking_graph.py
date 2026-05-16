from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple
import time

import numpy as np

from .config import BacktrackingPipelineConfig
from .route_memory import (
    BACKTRACK_LABEL,
    COMMON_LABEL,
    FIRST_BRANCH_LABEL,
    JUNCTION_LABEL,
    SECOND_BRANCH_LABEL,
    save_graph_memory,
)
from .similarity import (
    max_similarity_matrix,
    safe_range,
    segment_centroid,
    window_similarity_score,
)
from .utils import write_json


@dataclass
class BacktrackingGraphResult:
    graph_memory_file: Path
    graph_metadata_file: Path
    metadata: Dict


class BacktrackingGraphLearner:
    """
    Learns a simple two-branch graph from one backtracking learning video.

    Expected learning sequence:
    root -> junction -> first branch -> backtrack -> junction -> second branch
    """

    def __init__(self, config: BacktrackingPipelineConfig):
        self.config = config

    def detect_junction_pair(self, S: np.ndarray, n: int) -> Tuple[Dict, List[Dict]]:
        """Detect first and return junction indices from self-similarity matrix."""
        first_start = int(self.config.first_junction_search[0] * n)
        first_end = int(self.config.first_junction_search[1] * n)

        return_start = int(self.config.return_junction_search[0] * n)
        return_end = int(self.config.return_junction_search[1] * n)

        min_gap = int(self.config.min_junction_gap_ratio * n)
        candidates: List[Dict] = []

        for i in range(first_start, first_end):
            j_start = max(return_start, i + min_gap)

            for j in range(j_start, return_end):
                score, same_score, reverse_score = window_similarity_score(
                    S,
                    i,
                    j,
                    radius=self.config.junction_window,
                )

                i_ratio = i / n
                j_ratio = j / n

                # Notebook-4 plausibility preference:
                # first junction around 35%, return junction around 68%.
                plausibility = (
                    1.0
                    - abs(i_ratio - 0.35) * 0.20
                    - abs(j_ratio - 0.68) * 0.20
                )

                final_score = score * plausibility

                candidates.append({
                    "first_junction_index": int(i),
                    "return_junction_index": int(j),
                    "score": float(score),
                    "same_order_score": float(same_score),
                    "reverse_order_score": float(reverse_score),
                    "final_score": float(final_score),
                })

        candidates = sorted(candidates, key=lambda x: x["final_score"], reverse=True)

        if not candidates:
            raise ValueError("No junction candidates found.")

        return candidates[0], candidates[:10]

    def sequence_reverse_score(
        self,
        E: np.ndarray,
        EF: np.ndarray,
        start: int,
        mid: int,
        end: int,
        sample_count: int = 28,
    ) -> float:
        """Score whether start->mid and mid->end look like reverse traversal."""
        if mid <= start + 4 or end <= mid + 4:
            return -1.0

        a_idx = np.linspace(start, mid, sample_count, dtype=int)
        b_idx = np.linspace(mid, end, sample_count, dtype=int)[::-1]

        A = E[a_idx]
        AF = EF[a_idx]
        B = E[b_idx]
        BF = EF[b_idx]

        sim = max_similarity_matrix(A, AF, B, BF)
        diag = np.diag(sim)

        return float(np.mean(diag))

    def detect_turnaround(
        self,
        E: np.ndarray,
        EF: np.ndarray,
        first_junction_index: int,
        return_junction_index: int,
    ) -> Dict:
        """Detect endpoint of first branch / start of backtracking."""
        n = len(E)
        gap = return_junction_index - first_junction_index
        margin = max(8, int(0.08 * n))

        search_start = first_junction_index + margin
        search_end = return_junction_index - margin

        if search_end <= search_start:
            fallback = (first_junction_index + return_junction_index) // 2
            return {
                "left_endpoint_index": int(fallback),
                "score": -1.0,
                "confidence": "FALLBACK_MIDDLE",
                "method": "fallback_middle",
            }

        candidates = []

        for mid in range(search_start, search_end):
            score = self.sequence_reverse_score(
                E,
                EF,
                first_junction_index,
                mid,
                return_junction_index,
                sample_count=28,
            )

            ratio = (mid - first_junction_index) / max(1, gap)
            balance = 1.0 - abs(ratio - 0.50) * 0.18

            candidates.append({
                "left_endpoint_index": int(mid),
                "score": float(score),
                "final_score": float(score * balance),
                "ratio": float(ratio),
            })

        candidates = sorted(candidates, key=lambda x: x["final_score"], reverse=True)
        best = candidates[0]

        if best["score"] >= self.config.good_backtrack_score:
            confidence = "HIGH"
        elif best["score"] >= self.config.acceptable_backtrack_score:
            confidence = "MEDIUM_REVIEW"
        else:
            confidence = "LOW_REVIEW"

        best["confidence"] = confidence
        best["method"] = "reverse_sequence_similarity"

        return best

    def learn_from_embeddings(self, embeddings_file: str | Path) -> BacktrackingGraphResult:
        """
        Learn graph memory from saved embedding file and write graph outputs.
        """
        embeddings_file = Path(embeddings_file)
        output_dir = self.config.resolved_output_dir

        data = np.load(embeddings_file, allow_pickle=True)

        E = data["learning_embeddings"].astype(np.float32)
        EF = data["learning_embeddings_flip"].astype(np.float32)
        learning_frame_paths = data["learning_frame_paths"].tolist()

        n = len(E)
        embedding_dim = E.shape[1]

        S = max_similarity_matrix(E, EF, E, EF)

        # Remove trivial diagonal area exactly like notebook 4.
        ignore_radius = max(8, int(0.035 * n))
        for i in range(n):
            lo = max(0, i - ignore_radius)
            hi = min(n, i + ignore_radius + 1)
            S[i, lo:hi] = -1.0

        best_junction, top_junction_candidates = self.detect_junction_pair(S, n)

        first_junction_index = int(best_junction["first_junction_index"])
        return_junction_index = int(best_junction["return_junction_index"])
        junction_score = float(best_junction["score"])

        if junction_score >= self.config.good_junction_score:
            junction_confidence = "HIGH"
        elif junction_score >= self.config.acceptable_junction_score:
            junction_confidence = "MEDIUM_REVIEW"
        else:
            junction_confidence = "LOW_REVIEW"

        turnaround_info = self.detect_turnaround(
            E,
            EF,
            first_junction_index,
            return_junction_index,
        )

        turnaround_index = int(turnaround_info["left_endpoint_index"])
        backtrack_score = float(turnaround_info["score"])
        backtrack_confidence = str(turnaround_info["confidence"])

        common_start = 0
        common_end = first_junction_index

        first_branch_start = min(n - 1, first_junction_index + 1)
        first_branch_end = max(first_branch_start, turnaround_index)

        backtrack_start = min(n - 1, turnaround_index + 1)
        backtrack_end = max(backtrack_start, return_junction_index)

        second_branch_start = min(n - 1, return_junction_index + 1)
        second_branch_end = n - 1

        radius = self.config.junction_memory_radius
        junction_first_start = max(0, first_junction_index - radius)
        junction_first_end = min(n - 1, first_junction_index + radius)

        junction_return_start = max(0, return_junction_index - radius)
        junction_return_end = min(n - 1, return_junction_index + radius)

        first_branch_name = self.config.first_branch_name
        second_branch_name = self.config.second_branch_name

        segments = {
            "COMMON_PATH": [int(common_start), int(common_end)],
            "JUNCTION_A_FIRST_VISIT": [int(junction_first_start), int(junction_first_end)],
            first_branch_name: [int(first_branch_start), int(first_branch_end)],
            "BACKTRACK_TO_JUNCTION": [int(backtrack_start), int(backtrack_end)],
            "JUNCTION_A_RETURN_VISIT": [int(junction_return_start), int(junction_return_end)],
            second_branch_name: [int(second_branch_start), int(second_branch_end)],
        }

        common_idx = safe_range(common_start, common_end, n)
        junction_idx = sorted(list(set(
            safe_range(junction_first_start, junction_first_end, n)
            + safe_range(junction_return_start, junction_return_end, n)
        )))
        first_branch_idx = safe_range(first_branch_start, first_branch_end, n)
        backtrack_idx = safe_range(backtrack_start, backtrack_end, n)
        second_branch_idx = safe_range(second_branch_start, second_branch_end, n)

        memory_embeddings = np.vstack([
            E[common_idx],
            E[junction_idx],
            E[first_branch_idx],
            E[backtrack_idx],
            E[second_branch_idx],
        ]).astype(np.float32)

        memory_embeddings_flip = np.vstack([
            EF[common_idx],
            EF[junction_idx],
            EF[first_branch_idx],
            EF[backtrack_idx],
            EF[second_branch_idx],
        ]).astype(np.float32)

        memory_labels = np.concatenate([
            np.full(len(common_idx), COMMON_LABEL, dtype=np.int32),
            np.full(len(junction_idx), JUNCTION_LABEL, dtype=np.int32),
            np.full(len(first_branch_idx), FIRST_BRANCH_LABEL, dtype=np.int32),
            np.full(len(backtrack_idx), BACKTRACK_LABEL, dtype=np.int32),
            np.full(len(second_branch_idx), SECOND_BRANCH_LABEL, dtype=np.int32),
        ])

        centroids = np.vstack([
            segment_centroid(E[common_idx], embedding_dim),
            segment_centroid(E[junction_idx], embedding_dim),
            segment_centroid(E[first_branch_idx], embedding_dim),
            segment_centroid(E[backtrack_idx], embedding_dim),
            segment_centroid(E[second_branch_idx], embedding_dim),
        ]).astype(np.float32)

        component_names = np.array([
            "COMMON_PATH",
            "JUNCTION_A",
            first_branch_name,
            "BACKTRACK_TO_JUNCTION",
            second_branch_name,
        ])

        graph_memory_file = output_dir / "vxn_backtracking_graph_memory.npz"
        graph_metadata_file = output_dir / "vxn_backtracking_graph_metadata.json"

        arrays = {
            "memory_embeddings": memory_embeddings,
            "memory_embeddings_flip": memory_embeddings_flip,
            "memory_labels": memory_labels,
            "centroids": centroids,
            "component_names": component_names,
            "learning_embeddings": E,
            "learning_embeddings_flip": EF,
            "learning_frame_paths": np.array(learning_frame_paths),
            "common_indices": np.array(common_idx, dtype=np.int32),
            "junction_indices": np.array(junction_idx, dtype=np.int32),
            "first_branch_indices": np.array(first_branch_idx, dtype=np.int32),
            "backtrack_indices": np.array(backtrack_idx, dtype=np.int32),
            "second_branch_indices": np.array(second_branch_idx, dtype=np.int32),
            "first_junction_index": np.array([first_junction_index], dtype=np.int32),
            "return_junction_index": np.array([return_junction_index], dtype=np.int32),
            "turnaround_index": np.array([turnaround_index], dtype=np.int32),
        }

        if self.config.save_self_similarity_matrix:
            arrays["self_similarity_matrix"] = S.astype(np.float32)

        metadata = {
            "system": "VXN-RAMNet",
            "mode": "backtracking_branch_graph_learning",
            "stage": "graph_learning",
            "learning_path": "root -> junction -> first_branch -> backtrack -> junction -> second_branch",
            "model": "EfficientNetB0",
            "retraining_used": False,
            "flip_aware_similarity_used": True,
            "branch_label_note": (
                "Branch names are assigned by exploration order. "
                "Change first_branch_name and second_branch_name if physical labels differ."
            ),
            "graph": {
                "root": "ROOT",
                "common_path": "ROOT_TO_JUNCTION",
                "junction": "JUNCTION_A",
                "first_branch": first_branch_name,
                "second_branch": second_branch_name,
                "backtrack_segment": "BACKTRACK_TO_JUNCTION",
            },
            "detected_indices": {
                "first_junction_index": first_junction_index,
                "return_junction_index": return_junction_index,
                "turnaround_index": turnaround_index,
            },
            "confidence": {
                "junction_score": junction_score,
                "junction_confidence": junction_confidence,
                "backtrack_score": backtrack_score,
                "backtrack_confidence": backtrack_confidence,
            },
            "segments": segments,
            "component_counts": {
                "COMMON_PATH": len(common_idx),
                "JUNCTION_A": len(junction_idx),
                first_branch_name: len(first_branch_idx),
                "BACKTRACK_TO_JUNCTION": len(backtrack_idx),
                second_branch_name: len(second_branch_idx),
            },
            "top_junction_candidates": top_junction_candidates,
            "turnaround_detection": turnaround_info,
            "created_at_unix": time.time(),
        }

        save_graph_memory(graph_memory_file, graph_metadata_file, arrays, metadata)

        return BacktrackingGraphResult(
            graph_memory_file=graph_memory_file,
            graph_metadata_file=graph_metadata_file,
            metadata=metadata,
        )
