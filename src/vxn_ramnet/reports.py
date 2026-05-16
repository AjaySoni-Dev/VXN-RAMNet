from __future__ import annotations

from pathlib import Path
from typing import Dict, List
import csv

from .config import BacktrackingPipelineConfig
from .utils import read_json, round_float, write_json


def build_final_summary(config: BacktrackingPipelineConfig, query_reports: List[Dict]) -> Dict:
    """Build final JSON summary for the whole backtracking run."""
    output_dir = config.resolved_output_dir
    graph_meta = read_json(output_dir / "vxn_backtracking_graph_metadata.json")

    rows = []
    for report in query_reports:
        rows.append({
            "query": report["query_name"],
            "prediction": report["prediction"],
            "reason": report["reason"],
            "evidence_start": report["best_window"]["start"],
            "evidence_end": report["best_window"]["end"],
            "first_branch_name": report["scores"]["first_branch_name"],
            "first_branch_score": round_float(report["scores"]["first_branch_score"]),
            "second_branch_name": report["scores"]["second_branch_name"],
            "second_branch_score": round_float(report["scores"]["second_branch_score"]),
            "branch_gap": round_float(report["scores"]["branch_gap"]),
            "common_score_selected_window": round_float(
                report["scores"]["common_score_in_selected_window"]
            ),
            "junction_score_selected_window": round_float(
                report["scores"]["junction_score_in_selected_window"]
            ),
        })

    final_summary = {
        "system": "VXN-RAMNet",
        "mode": "backtracking_branch_graph_learning",
        "graph": graph_meta["graph"],
        "detected_indices": graph_meta["detected_indices"],
        "confidence": graph_meta["confidence"],
        "segments": graph_meta["segments"],
        "query_results": rows,
        "important_note": (
            "This modular production-grade pipeline mirrors the stable notebook-4 logic. "
            "It uses one learning video with backtracking, learns graph memory, then "
            "classifies query videos using multiple late branch-evidence windows."
        ),
    }

    return final_summary


def write_csv_summary(path: Path, query_results: List[Dict]) -> None:
    """Write query result rows to CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "query",
        "prediction",
        "reason",
        "evidence_start",
        "evidence_end",
        "first_branch_name",
        "first_branch_score",
        "second_branch_name",
        "second_branch_score",
        "branch_gap",
        "common_score_selected_window",
        "junction_score_selected_window",
    ]

    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(query_results)


def write_markdown_report(path: Path, final_summary: Dict) -> None:
    """Write human-readable Markdown report."""
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append("# VXN-RAMNet Backtracking Graph Report")
    lines.append("")
    lines.append("## Detected Graph")
    lines.append("")
    graph = final_summary["graph"]
    lines.append(f"- Root: `{graph['root']}`")
    lines.append(f"- Common path: `{graph['common_path']}`")
    lines.append(f"- Junction: `{graph['junction']}`")
    lines.append(f"- First branch: `{graph['first_branch']}`")
    lines.append(f"- Second branch: `{graph['second_branch']}`")
    lines.append(f"- Backtrack segment: `{graph['backtrack_segment']}`")
    lines.append("")
    lines.append("## Detected Indices")
    lines.append("")
    for key, value in final_summary["detected_indices"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    lines.append("## Confidence")
    lines.append("")
    for key, value in final_summary["confidence"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    lines.append("## Segments")
    lines.append("")
    for name, span in final_summary["segments"].items():
        lines.append(f"- {name}: `{span[0]} -> {span[1]}`")
    lines.append("")
    lines.append("## Query Results")
    lines.append("")
    lines.append("| Query | Prediction | Branch Gap | First Score | Second Score | Reason |")
    lines.append("|---|---:|---:|---:|---:|---|")

    for row in final_summary["query_results"]:
        lines.append(
            f"| {row['query']} | {row['prediction']} | {row['branch_gap']} | "
            f"{row['first_branch_score']} | {row['second_branch_score']} | {row['reason']} |"
        )

    lines.append("")
    lines.append("## Important Note")
    lines.append("")
    lines.append(final_summary["important_note"])
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def write_final_reports(config: BacktrackingPipelineConfig, query_reports: List[Dict]) -> Dict:
    """Write final JSON, CSV, and Markdown reports."""
    output_dir = config.resolved_output_dir
    final_summary = build_final_summary(config, query_reports)

    final_json = output_dir / "vxn_backtracking_final_summary.json"
    final_csv = output_dir / "vxn_backtracking_query_results.csv"
    final_md = output_dir / "vxn_backtracking_report.md"

    write_json(final_json, final_summary)
    write_csv_summary(final_csv, final_summary["query_results"])
    write_markdown_report(final_md, final_summary)

    final_summary["report_files"] = {
        "json": str(final_json),
        "csv": str(final_csv),
        "markdown": str(final_md),
    }

    return final_summary
