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
    get_component,
    load_graph_memory,
)
from .similarity import component_score
from .utils import read_json, write_json


@dataclass
class QueryClassificationResult:
    reports: List[Dict]
    summary_file: Path
    query_reports_dir: Path


class BacktrackingQueryClassifier:
    """
    Classifies query videos against learned backtracking graph memory.

    This module mirrors notebook-4 Cell 4, including the multi-window branch
    evidence selection that avoids early common/root frames.
    """

    def __init__(self, config: BacktrackingPipelineConfig):
        self.config = config

    @staticmethod
    def branch_window_candidates(n: int) -> List[Tuple[int, int]]:
        """Return candidate branch-evidence windows from the later part of a query."""
        starts = sorted(list(set([
            int(0.45 * n),
            int(0.50 * n),
            int(0.55 * n),
            int(0.60 * n),
            int(0.65 * n),
            int(0.70 * n),
            int(0.75 * n),
        ])))

        windows = []

        for start in starts:
            for size_ratio in [0.20, 0.25, 0.30, 0.35]:
                size = max(12, int(size_ratio * n))
                end = min(n, start + size)

                if end - start >= 10:
                    windows.append((start, end))

        windows.append((int(0.60 * n), n))
        windows.append((int(0.65 * n), n))
        windows.append((int(0.70 * n), n))

        return sorted(list(set(windows)))

    def classify_query(
        self,
        query_name: str,
        emb_data,
        memory: Dict,
        metadata: Dict,
        query_reports_dir: Path,
    ) -> Dict:
        """Classify one query route."""
        memory_embeddings = memory["memory_embeddings"].astype(np.float32)
        memory_embeddings_flip = memory["memory_embeddings_flip"].astype(np.float32)
        memory_labels = memory["memory_labels"].astype(np.int32)
        centroids = memory["centroids"].astype(np.float32)
        component_names = memory["component_names"].tolist()

        q_emb = emb_data[f"query_embeddings__{query_name}"].astype(np.float32)
        q_flip = emb_data[f"query_embeddings_flip__{query_name}"].astype(np.float32)

        n = len(q_emb)

        first_component = get_component(
            memory_embeddings, memory_embeddings_flip, memory_labels,
            centroids, component_names, FIRST_BRANCH_LABEL,
        )
        second_component = get_component(
            memory_embeddings, memory_embeddings_flip, memory_labels,
            centroids, component_names, SECOND_BRANCH_LABEL,
        )
        common_component = get_component(
            memory_embeddings, memory_embeddings_flip, memory_labels,
            centroids, component_names, COMMON_LABEL,
        )
        junction_component = get_component(
            memory_embeddings, memory_embeddings_flip, memory_labels,
            centroids, component_names, JUNCTION_LABEL,
        )

        window_rows = []

        for start, end in self.branch_window_candidates(n):
            qe = q_emb[start:end]
            qf = q_flip[start:end]

            first_score, _ = component_score(
                qe, qf,
                first_component.embeddings,
                first_component.flipped_embeddings,
                first_component.centroid,
            )

            second_score, _ = component_score(
                qe, qf,
                second_component.embeddings,
                second_component.flipped_embeddings,
                second_component.centroid,
            )

            common_score, _ = component_score(
                qe, qf,
                common_component.embeddings,
                common_component.flipped_embeddings,
                common_component.centroid,
            )

            junction_score, _ = component_score(
                qe, qf,
                junction_component.embeddings,
                junction_component.flipped_embeddings,
                junction_component.centroid,
            )

            best_branch = max(first_score, second_score)
            branch_gap = abs(first_score - second_score)
            shared_score = max(common_score, junction_score)

            window_quality = (
                best_branch
                + 0.70 * branch_gap
                - 0.25 * shared_score
                + 0.03 * (start / max(1, n))
            )

            window_rows.append({
                "start": int(start),
                "end": int(end),
                "frame_count": int(end - start),
                "first_branch_score": float(first_score),
                "second_branch_score": float(second_score),
                "common_score": float(common_score),
                "junction_score": float(junction_score),
                "best_branch_score": float(best_branch),
                "branch_gap": float(branch_gap),
                "shared_score": float(shared_score),
                "window_quality": float(window_quality),
            })

        if not window_rows:
            raise ValueError(f"No branch evidence windows produced for query: {query_name}")

        window_rows_sorted = sorted(
            window_rows,
            key=lambda row: row["window_quality"],
            reverse=True,
        )

        best_window = window_rows_sorted[0]

        first_score = float(best_window["first_branch_score"])
        second_score = float(best_window["second_branch_score"])
        branch_gap = float(best_window["branch_gap"])
        best_branch_score = max(first_score, second_score)

        first_branch_name = first_component.name
        second_branch_name = second_component.name

        if best_branch_score < self.config.unknown_score:
            prediction = "UNKNOWN_BRANCH"
            reason = "Branch evidence is too weak for both learned branches."
        elif (
            best_branch_score >= self.config.strong_branch_score
            and branch_gap >= self.config.strong_branch_gap
        ):
            if first_score > second_score:
                prediction = first_branch_name
                reason = f"Strong evidence for {first_branch_name}."
            else:
                prediction = second_branch_name
                reason = f"Strong evidence for {second_branch_name}."
        elif branch_gap < self.config.min_branch_gap:
            prediction = "UNCERTAIN_BRANCH"
            reason = "Branch scores are too close."
        elif best_branch_score < self.config.min_branch_score:
            prediction = "UNKNOWN_BRANCH"
            reason = "Best branch score is below minimum threshold."
        elif first_score > second_score:
            prediction = first_branch_name
            reason = f"{first_branch_name} score is higher."
        else:
            prediction = second_branch_name
            reason = f"{second_branch_name} score is higher."

        report = {
            "query_name": query_name,
            "prediction": prediction,
            "reason": reason,
            "best_window": {
                "start": int(best_window["start"]),
                "end": int(best_window["end"]),
                "frame_count": int(best_window["frame_count"]),
            },
            "scores": {
                "first_branch_name": first_branch_name,
                "second_branch_name": second_branch_name,
                "first_branch_score": first_score,
                "second_branch_score": second_score,
                "branch_gap": branch_gap,
                "best_branch_score": float(best_branch_score),
                "common_score_in_selected_window": float(best_window["common_score"]),
                "junction_score_in_selected_window": float(best_window["junction_score"]),
            },
            "thresholds": {
                "MIN_BRANCH_SCORE": self.config.min_branch_score,
                "MIN_BRANCH_GAP": self.config.min_branch_gap,
                "STRONG_BRANCH_SCORE": self.config.strong_branch_score,
                "STRONG_BRANCH_GAP": self.config.strong_branch_gap,
                "UNKNOWN_SCORE": self.config.unknown_score,
            },
            "all_windows": window_rows_sorted,
            "graph_context": metadata.get("graph", {}),
            "created_at_unix": time.time(),
        }

        report_path = query_reports_dir / f"{query_name}_classification_report.json"
        write_json(report_path, report)

        return report

    def classify_all(self) -> QueryClassificationResult:
        """Classify all query embeddings saved in the embedding file."""
        output_dir = self.config.resolved_output_dir
        embeddings_file = output_dir / "vxn_backtracking_embeddings.npz"
        graph_memory_file = output_dir / "vxn_backtracking_graph_memory.npz"
        graph_metadata_file = output_dir / "vxn_backtracking_graph_metadata.json"

        if not graph_memory_file.exists():
            raise FileNotFoundError("Graph memory missing. Run graph learning first.")

        memory = load_graph_memory(graph_memory_file)
        emb_data = np.load(embeddings_file, allow_pickle=True)
        metadata = read_json(graph_metadata_file)

        query_names = emb_data["query_names"].tolist()
        query_reports_dir = output_dir / "query_reports"
        query_reports_dir.mkdir(parents=True, exist_ok=True)

        reports = []

        for query_name in query_names:
            reports.append(
                self.classify_query(
                    query_name=query_name,
                    emb_data=emb_data,
                    memory=memory,
                    metadata=metadata,
                    query_reports_dir=query_reports_dir,
                )
            )

        summary_file = output_dir / "vxn_backtracking_all_query_summary.json"
        write_json(summary_file, {"queries": reports})

        return QueryClassificationResult(
            reports=reports,
            summary_file=summary_file,
            query_reports_dir=query_reports_dir,
        )
