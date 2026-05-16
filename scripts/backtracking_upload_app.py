"""
Optional Streamlit upload UI for the stable VXN-RAMNet backtracking pipeline.

Run from repository root:

    streamlit run apps/backtracking_upload_app.py

This app is intentionally optional. The research-grade command-line runner remains:

    python scripts/run_backtracking_pipeline.py --learning-video ... --query-videos ...
"""

from __future__ import annotations

from pathlib import Path
import shutil
import sys
import tempfile
from typing import List

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from vxn_ramnet.config import BacktrackingPipelineConfig  # noqa: E402
from vxn_ramnet.pipeline import BacktrackingPipeline  # noqa: E402


st.set_page_config(
    page_title="VXN-RAMNet Backtracking Pipeline",
    page_icon="🧭",
    layout="wide",
)

st.title("VXN-RAMNet — Backtracking Branch Graph Pipeline")
st.caption("Upload one learning video and one or more query videos. The app runs the stable Notebook 4 logic through the modular src pipeline.")

with st.expander("Expected learning video flow", expanded=True):
    st.code("Root → Junction → First Branch → Backtrack → Junction → Second Branch", language="text")

learning_file = st.file_uploader(
    "Upload learning video",
    type=["mp4", "mov", "avi", "mkv", "webm"],
    accept_multiple_files=False,
)

query_files = st.file_uploader(
    "Upload query video(s)",
    type=["mp4", "mov", "avi", "mkv", "webm"],
    accept_multiple_files=True,
)

col1, col2, col3 = st.columns(3)

with col1:
    learning_frame_count = st.number_input("Learning frames", min_value=60, max_value=600, value=270, step=10)
with col2:
    query_frame_count = st.number_input("Query frames", min_value=30, max_value=300, value=120, step=10)
with col3:
    clean_output = st.checkbox("Clean previous output folder", value=True)

first_branch_name = st.text_input("First branch name", value="LEFT_BRANCH")
second_branch_name = st.text_input("Second branch name", value="RIGHT_BRANCH")

run_button = st.button("Run Pipeline", type="primary")


def save_uploaded_file(uploaded_file, target_dir: Path) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    safe_name = Path(uploaded_file.name).name
    path = target_dir / safe_name
    with path.open("wb") as f:
        f.write(uploaded_file.getbuffer())
    return path


if run_button:
    if learning_file is None:
        st.error("Please upload a learning video.")
        st.stop()
    if not query_files:
        st.error("Please upload at least one query video.")
        st.stop()

    uploaded_dir = PROJECT_ROOT / "_uploaded_videos" / "backtracking_app"
    if uploaded_dir.exists():
        shutil.rmtree(uploaded_dir)
    uploaded_dir.mkdir(parents=True, exist_ok=True)

    learning_path = save_uploaded_file(learning_file, uploaded_dir)
    query_paths: List[Path] = [save_uploaded_file(q, uploaded_dir) for q in query_files]

    output_dir = PROJECT_ROOT / "vxn_backtracking_graph_outputs"

    config = BacktrackingPipelineConfig(
        root_dir=PROJECT_ROOT,
        videos_dir=uploaded_dir.relative_to(PROJECT_ROOT),
        output_dir=output_dir.relative_to(PROJECT_ROOT),
        learning_video_name=learning_path.name,
        query_video_names=[p.name for p in query_paths],
        learning_frame_count=int(learning_frame_count),
        query_frame_count=int(query_frame_count),
        first_branch_name=first_branch_name,
        second_branch_name=second_branch_name,
        clean_output_dir=bool(clean_output),
    )

    with st.status("Running VXN-RAMNet pipeline...", expanded=True) as status:
        try:
            result = BacktrackingPipeline(config).run()
            status.update(label="Pipeline complete", state="complete")
        except Exception as exc:  # noqa: BLE001
            status.update(label="Pipeline failed", state="error")
            st.exception(exc)
            st.stop()

    final_summary = result.final_summary
    st.success("Pipeline completed successfully.")

    st.subheader("Predictions")
    rows = []
    for report in final_summary.get("query_results", []):
        rows.append({
            "query": report.get("query"),
            "prediction": report.get("prediction"),
            "reason": report.get("reason"),
            "branch_gap": report.get("branch_gap"),
            "first_branch_score": report.get("first_branch_score"),
            "second_branch_score": report.get("second_branch_score"),
        })
    st.dataframe(rows, use_container_width=True)

    report_path = Path(final_summary["report_files"]["markdown"])
    json_path = Path(final_summary["report_files"]["json"])
    csv_path = Path(final_summary["report_files"]["csv"])

    st.subheader("Generated report files")
    st.code(f"Markdown: {report_path}\nJSON: {json_path}\nCSV: {csv_path}", language="text")

    if report_path.exists():
        st.markdown(report_path.read_text(encoding="utf-8"))
