# VXN-RAMNet Local Usage Guide

This guide explains how to download the repository, install dependencies, provide learning/query videos, run the modular `src/` pipeline, use the optional upload app, and inspect generated results.

---

## 1. What This Guide Covers

This guide is for users who want to run VXN-RAMNet on their own machine.

It covers:

- downloading the repository
- understanding the folders
- installing dependencies
- running the command-line pipeline
- using the optional upload-based local app
- understanding input videos
- understanding output files
- troubleshooting common errors

> [!IMPORTANT]
> The modular pipeline is based on the stable advanced backtracking branch-graph method.

---

## 2. Repository Folders

After downloading the repository, the important folders are:

```text
VXN-RAMNet/
├── configs/
├── experiments/
├── scripts/
├── src/
├── sample_results/
├── demo_outputs/
└── docs/
```

## 2.1 `src/`

`src/` contains the actual reusable Python source code.

Think of it as:

```text
src/ = the engine
```

It contains modules such as:

```text
frame extraction
video preprocessing
EfficientNetB0 encoding
similarity calculation
backtracking graph construction
query classification
report generation
```

Users normally do not directly run files inside `src/`.

## 2.2 `scripts/`

`scripts/` contains user-facing runnable files.

Think of it as:

```text
scripts/ = the start button
```

Main scripts:

```text
scripts/run_backtracking_pipeline.py
scripts/backtracking_upload_app.py
```

## 2.3 `configs/`

`configs/` contains configuration and dependency files.

Typical files:

```text
configs/backtracking_default.json
configs/requirements-src.txt
configs/requirements-ui.txt
```

If you have `backtracking_default.json.example`, copy it first:

```bash
cp configs/backtracking_default.json.example configs/backtracking_default.json
```

Windows PowerShell:

```powershell
Copy-Item configs/backtracking_default.json.example configs/backtracking_default.json
```

## 2.4 `experiments/`

`experiments/` contains the original Jupyter notebooks.

Use this folder if you want to study the research process step by step.

Main advanced notebook:

```text
experiments/04_backtracking_branch_graph_learning.ipynb
```

## 2.5 `sample_results/`

This contains curated sample outputs.

Use it to inspect the kind of reports produced by the system.

---

## 3. Download the Repository

You can download the project in two ways.

---

## Method A: Download ZIP from GitHub

1. Open the GitHub repository.
2. Click the green **Code** button.
3. Click **Download ZIP**.
4. Extract the ZIP.
5. Open the extracted folder in VS Code, PyCharm, or terminal.

---

## Method B: Clone with Git

```bash
git clone https://github.com/AjaySoni-Dev/VXN-RAMNet.git
cd VXN-RAMNet
```

---

## 4. Create a Virtual Environment

Creating a virtual environment is recommended.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

After activation, your terminal usually shows:

```text
(.venv)
```

---

## 5. Install Dependencies

For the command-line pipeline:

```bash
pip install -r configs/requirements-src.txt
```

For the optional upload app:

```bash
pip install -r configs/requirements-ui.txt
```

If TensorFlow installation fails, check your Python version. Python 3.10 or 3.11 is usually safer than using the newest Python release.

---

## 6. Prepare Input Videos

The stable backtracking pipeline needs:

```text
1 learning video
1 or more query videos
```

### Learning video structure

The learning video should follow this path pattern:

```text
Root
  ↓
Junction
  ↓
First Branch
  ↓
Backtrack to Junction
  ↓
Second Branch
```

Recommended filename:

```text
backtracking_learning_route.mp4
```

### Query videos

Query videos should show a route that belongs to one of the learned branches.

Recommended filenames:

```text
query_route_1.mp4
query_route_2.mp4
```

### Good recording practices

- walk slowly
- avoid sudden camera rotation
- avoid heavy blur
- keep the camera mostly forward-facing
- record in reasonable lighting
- keep the route structure clear
- pause slightly near the junction if possible
- avoid recording private faces, number plates, or sensitive locations

---

## 7. Run the CLI Pipeline

### Windows PowerShell

```powershell
python scripts/run_backtracking_pipeline.py `
  --learning-video "C:\path\to\backtracking_learning_route.mp4" `
  --query-videos "C:\path\to\query_route_1.mp4" "C:\path\to\query_route_2.mp4"
```

### macOS/Linux

```bash
python scripts/run_backtracking_pipeline.py \
  --learning-video "/path/to/backtracking_learning_route.mp4" \
  --query-videos "/path/to/query_route_1.mp4" "/path/to/query_route_2.mp4"
```

### With an output directory

```bash
python scripts/run_backtracking_pipeline.py \
  --learning-video "path/to/backtracking_learning_route.mp4" \
  --query-videos "path/to/query_route_1.mp4" "path/to/query_route_2.mp4" \
  --output-dir "vxn_backtracking_graph_outputs"
```

---

## 8. Run with Config File

If your script supports config-based execution:

```bash
python scripts/run_backtracking_pipeline.py --config configs/backtracking_default.json
```

A config file may define:

```text
learning video path
query video paths
output directory
frame counts
image size
thresholds
window sizes
```

---

## 9. Use the Upload App

The upload app is useful for users who do not want to type file paths.

Install UI dependencies:

```bash
pip install -r configs/requirements-ui.txt
```

Run:

```bash
streamlit run scripts/backtracking_upload_app.py
```

A local browser page will open.

Upload:

```text
1 learning video
1 or more query videos
```

Then run the pipeline from the page.

The output folder will be generated locally.

---

## 10. Output Folder

By default, the pipeline writes outputs to:

```text
vxn_backtracking_graph_outputs/
```

Expected files:

```text
vxn_backtracking_graph_outputs/
├── frame_extraction_report.json
├── vxn_backtracking_embeddings.npz
├── vxn_backtracking_graph_memory.npz
├── vxn_backtracking_graph_metadata.json
├── query_reports/
├── vxn_backtracking_all_query_summary.json
├── vxn_backtracking_final_summary.json
├── vxn_backtracking_query_results.csv
└── vxn_backtracking_report.md
```

---

## 11. Which Output File Should You Open?

Open this first:

```text
vxn_backtracking_graph_outputs/vxn_backtracking_report.md
```

This is the human-readable final report.

It should explain:

```text
how many frames were extracted
which graph segments were detected
where the junction was detected
where the return junction was detected
which query was classified as which branch
branch score
branch gap
final prediction
```

For table-based inspection, open:

```text
vxn_backtracking_graph_outputs/vxn_backtracking_query_results.csv
```

For raw metadata, open:

```text
vxn_backtracking_graph_outputs/vxn_backtracking_graph_metadata.json
```

---

## 12. How the Pipeline Works Internally

The pipeline follows this flow:

```text
Learning video
        ↓
Frame extraction
        ↓
Original and flipped frame encoding
        ↓
Flip-aware self-similarity matrix
        ↓
First junction detection
        ↓
Return junction detection
        ↓
Turnaround/backtracking detection
        ↓
Graph segment split
        ↓
Graph memory creation
        ↓
Query video classification
        ↓
Report generation
```

---

## 13. What Each `src/` File Does

| File | Purpose |
|---|---|
| `config.py` | Stores pipeline settings and thresholds |
| `frame_extraction.py` | Extracts frames from videos |
| `encoder.py` | Loads EfficientNetB0 and creates embeddings |
| `similarity.py` | Computes cosine similarity, top-k scores, and self-similarity |
| `route_memory.py` | Stores and saves route/graph memory |
| `backtracking_graph.py` | Detects junction revisit and builds the backtracking branch graph |
| `query_classifier.py` | Classifies query videos into learned branches |
| `reports.py` | Generates JSON, CSV, and Markdown reports |
| `pipeline.py` | Runs the full end-to-end pipeline |
| `cli.py` | Handles terminal arguments |
| `utils.py` | Common filesystem and JSON helpers |

---

## 14. What Each `scripts/` File Does

| File | Purpose |
|---|---|
| `run_backtracking_pipeline.py` | Runs the full pipeline from terminal |
| `backtracking_upload_app.py` | Starts the optional Streamlit upload UI |

---

## 15. Recommended Local Working Style

Keep raw videos outside GitHub.

Good local structure:

```text
local_videos/
├── backtracking_learning_route.mp4
├── query_route_1.mp4
└── query_route_2.mp4
```

Then run:

```bash
python scripts/run_backtracking_pipeline.py \
  --learning-video "local_videos/backtracking_learning_route.mp4" \
  --query-videos "local_videos/query_route_1.mp4" "local_videos/query_route_2.mp4"
```

Do not commit raw private videos unless they are intentionally anonymized sample data.

---

## 16. Common Problems and Fixes

### Problem: `ModuleNotFoundError: No module named 'vxn_ramnet'`

Run the script from the repository root:

```bash
cd VXN-RAMNet
python scripts/run_backtracking_pipeline.py --help
```

Or install the package in editable mode if supported:

```bash
pip install -e .
```

### Problem: TensorFlow does not install

Use Python 3.10 or 3.11 and upgrade pip:

```bash
python -m pip install --upgrade pip
```

Then reinstall:

```bash
pip install -r configs/requirements-src.txt
```

### Problem: Video path not found

Use quotes around paths:

```bash
--learning-video "C:\Users\Ajay\Videos\backtracking_learning_route.mp4"
```

### Problem: Query result is uncertain

Possible causes:

```text
query video is too short
branch looks visually similar to another branch
camera angle changed heavily
lighting is very different
frames are blurry
junction is not visually clear
```

Fixes:

```text
record slower
avoid sudden camera turns
improve lighting
record longer query videos
keep camera forward-facing
```

### Problem: Wrong branch detected

Possible causes:

```text
branches look visually similar
not enough branch-specific evidence
query contains mostly common-path frames
learning video segmentation is not clear
```

Fixes:

```text
record clearer branch sections
pause near junction
increase query length
inspect generated graph metadata
compare report with actual route video
```

---

## 17. What to Commit and What Not to Commit

### Safe to commit

```text
src/
scripts/
configs/
experiments/
docs/
research_notes/
sample_results/reports/
demo_outputs/
README.md
LICENSE
requirements.txt
```

### Avoid committing

```text
raw private videos
generated extracted frame folders
large temporary embeddings
private location data
faces or vehicle numbers
personal route recordings
```

---

## 18. For Researchers

For serious evaluation, create a route dataset like:

```text
VXN-BacktrackingSet-1/
├── route_01/
│   ├── backtracking_learning_route.mp4
│   ├── query_left_1.mp4
│   ├── query_left_2.mp4
│   ├── query_right_1.mp4
│   ├── query_right_2.mp4
│   └── labels.json
├── route_02/
├── route_03/
├── route_04/
└── route_05/
```

Minimum research target:

```text
5 route graphs
20 query videos
manual junction labels
manual branch labels
accuracy table
failure analysis
```

Recommended metrics:

```text
branch accuracy
precision
recall
F1-score
average branch gap
junction frame error
return-junction frame error
unknown-route false accept rate
embedding time per frame
memory size
```

---

## 19. Safety Note

> [!WARNING]
> VXN-RAMNet is a research prototype. It is not a certified navigation system, safety device, medical device, or mobility aid. Do not use it as the only source of navigation or safety guidance.

---

## 20. Quick Command Summary

```bash
git clone https://github.com/AjaySoni-Dev/VXN-RAMNet.git
cd VXN-RAMNet
python -m venv .venv
pip install -r configs/requirements-src.txt
python scripts/run_backtracking_pipeline.py --learning-video path/to/backtracking_learning_route.mp4 --query-videos path/to/query_route_1.mp4 path/to/query_route_2.mp4
```

Open:

```text
vxn_backtracking_graph_outputs/vxn_backtracking_report.md
```
