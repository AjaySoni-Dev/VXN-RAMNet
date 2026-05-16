# VXN-RAMNet Scripts

This folder contains the runnable interface for the stable Notebook 4 backtracking branch-graph pipeline.

## 1. Install dependencies

From the repository root:

```bash
pip install -r configs/requirements-src.txt
```

For the optional upload UI:

```bash
pip install -r configs/requirements-ui.txt
```

## 2. Command-line pipeline

Put videos anywhere and pass paths directly:

```bash
python scripts/run_backtracking_pipeline.py \
  --learning-video path/to/backtracking_learning_route.mp4 \
  --query-videos path/to/query_route_1.mp4 path/to/query_route_2.mp4
```

Or keep videos in a folder and use config:

```bash
python scripts/run_backtracking_pipeline.py --config configs/backtracking_default.json.example
```

## 3. Upload UI

```bash
streamlit run scripts/backtracking_upload_app.py
```

Upload:

```text
1 learning video: Root -> Junction -> First Branch -> Backtrack -> Junction -> Second Branch
1 or more query videos
```

## 4. Output

After running, open:

```text
vxn_backtracking_graph_outputs/vxn_backtracking_report.md
```

Other generated outputs include JSON, CSV, NPZ memory files, and extracted frames.
