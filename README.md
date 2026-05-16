<h1 align="center">VXN-RAMNet</h1>

<p align="center">
  <strong>VisionX Routine Adaptive Memory Network</strong><br>
  GPS-free visual route memory, backtracking branch-graph learning, and assistive navigation research.
</p>

<p align="center">
  <img alt="Status" src="https://img.shields.io/badge/status-research%20prototype-blue">
  <img alt="Python" src="https://img.shields.io/badge/python-3.10%2B-3776AB">
  <img alt="Core" src="https://img.shields.io/badge/core-visual%20route%20memory-purple">
  <img alt="Pipeline" src="https://img.shields.io/badge/pipeline-src%20%2B%20scripts-success">
  <img alt="Encoder" src="https://img.shields.io/badge/encoder-EfficientNetB0-lightgrey">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green">
</p>

<p align="center">
  <a href="#overview">Overview</a> ·
  <a href="#what-is-implemented">Implemented</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="#repository-structure">Structure</a> ·
  <a href="#current-limitations">Limitations</a>
</p>

---

## Overview

**VXN-RAMNet** is a research prototype that explores whether repeated routes can be learned through **visual memory** instead of relying on GPS as the main navigation signal.

The system processes route videos, extracts frames, converts those frames into visual embeddings using a frozen encoder, stores route/branch memory, and classifies future query routes using similarity-based evidence.

The main research direction is:

```text
Teach a route visually
        ↓
Store route embeddings as memory
        ↓
Compare future query routes against memory
        ↓
Detect common path, junction, branch, and route identity
```

> [!IMPORTANT]
> This repository is a **research prototype**, not a certified navigation product, medical device, or mobility safety system.

---

## Core Idea

Most assistive vision systems mainly answer object-level questions:

```text
Camera frame → Object detector → "Chair detected"
```

VXN-RAMNet focuses on route-level questions:

```text
Is this a known route?
Where does the route split?
Which branch is the user taking?
Did the user return to the same junction?
Can a route be remembered without retraining the model?
```

The core design principle is:

```text
The visual encoder stays fixed.
The route memory grows.
```

This means VXN-RAMNet does **not** retrain a model for every route. It stores embeddings and compares new route evidence against those memories.

---

## Current Research Scope

VXN-RAMNet currently supports offline video-based experiments and a modular Python pipeline.

It currently includes:

- frame extraction from route videos
- EfficientNetB0 frozen visual embedding generation
- cosine-similarity based route/branch matching
- baseline visual route memory
- unknown-route memory update experiment
- two-video DTW shared-prefix branch graph learning
- stable one-video backtracking branch graph learning
- query branch classification
- JSON, CSV, NPZ, and Markdown result reports

It does **not** currently provide:

- certified real-world navigation safety
- Android production deployment
- live camera guidance
- object detection safety layer
- validated large-scale user testing
- medical or mobility-aid certification

---

## What Is Implemented

| Area | Status | Current Form |
|---|---:|---|
| Visual frame extraction | ✅ Implemented | `src/` + experiments |
| EfficientNetB0 frozen encoder | ✅ Implemented | `src/` + experiments |
| Baseline route-memory classification | ✅ Implemented | experiment notebook |
| Unknown-route memory update | 🧪 Experimental | experiment notebook |
| Two-video DTW branch graph | ✅ Stable baseline | experiment notebook |
| One-video backtracking branch graph | ✅ Stable advanced | `src/` + experiment notebook |
| Query branch classification | ✅ Implemented | `src/` + experiment notebook |
| Report generation | ✅ Implemented | `src/` pipeline |
| Modular CLI pipeline | ✅ Implemented | `scripts/` |
| Upload-based local UI | ✅ Implemented if Streamlit deps are installed | `scripts/` |
| Multi-junction graph memory | 🚧 Planned | not implemented |
| Graph-aware unknown branch insertion | 🚧 Planned | not implemented |
| Object detection safety layer | 🚧 Planned | not implemented |
| Android/TFLite runtime | 🚧 Planned | not implemented |

---

## Main Experiments

The notebook experiments are stored in the `experiments/` folder.

| Experiment | Status | Purpose |
|---|---:|---|
| `01_route_memory_baseline.ipynb` | ✅ Stable | Baseline visual route-memory recognition |
| `02_unknown_route_auto_learning.ipynb` | 🧪 Experimental | Unknown-route detection and memory update |
| `03_shared_prefix_branch_graph_dtw.ipynb` | ✅ Stable baseline | Two-video shared-prefix branch graph learning using DTW |
| `04_backtracking_branch_graph_learning.ipynb` | ✅ Stable advanced | One-video backtracking-based branch graph learning and query classification |

> [!NOTE]
> `04_backtracking_branch_graph_learning.ipynb` is the main advanced method in the current repository. `03_shared_prefix_branch_graph_dtw.ipynb` remains useful as the stable two-video baseline.

---

## Production SRC Pipeline

The notebook 4 logic has been modularized into `src/` and can now be run without opening Jupyter.

```text
Learning video + query videos
        ↓
Frame extraction
        ↓
Original + flipped embedding generation
        ↓
Flip-aware self-similarity
        ↓
Junction revisit detection
        ↓
Backtracking graph construction
        ↓
Multi-window query classification
        ↓
Result reports
```

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/AjaySoni-Dev/VXN-RAMNet.git
cd VXN-RAMNet
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install pipeline dependencies

```bash
pip install -r configs/requirements-src.txt
```

### 4. Run the backtracking pipeline

Windows PowerShell:

```powershell
python scripts/run_backtracking_pipeline.py `
  --learning-video "path\to\backtracking_learning_route.mp4" `
  --query-videos "path\to\query_route_1.mp4" "path\to\query_route_2.mp4"
```

macOS/Linux:

```bash
python scripts/run_backtracking_pipeline.py \
  --learning-video "path/to/backtracking_learning_route.mp4" \
  --query-videos "path/to/query_route_1.mp4" "path/to/query_route_2.mp4"
```

### 5. Open the generated report

```text
vxn_backtracking_graph_outputs/vxn_backtracking_report.md
```

---

## Optional Upload App

For users who prefer uploading videos through a local browser UI:

```bash
pip install -r configs/requirements-ui.txt
streamlit run scripts/backtracking_upload_app.py
```

Then upload:

```text
1 learning video
1 or more query videos
```

The app runs the same backtracking pipeline and writes the same output reports.

---

## Expected Input for the Stable Backtracking Pipeline

### Learning video

```text
backtracking_learning_route.mp4
```

Recommended structure:

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

### Query videos

```text
query_route_1.mp4
query_route_2.mp4
...
```

Each query video should show a route that belongs to one of the learned branches.

---

## Output Files

The pipeline generates:

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

| File | Purpose |
|---|---|
| `frame_extraction_report.json` | Records frame counts and extracted video metadata |
| `vxn_backtracking_embeddings.npz` | Stores original/flipped embeddings |
| `vxn_backtracking_graph_memory.npz` | Stores learned graph component embeddings |
| `vxn_backtracking_graph_metadata.json` | Stores detected junction, return, and segment information |
| `query_reports/` | Per-query classification reports |
| `vxn_backtracking_all_query_summary.json` | Combined query prediction summary |
| `vxn_backtracking_query_results.csv` | Table-friendly query result file |
| `vxn_backtracking_report.md` | Human-readable final report |

---

## Repository Structure

```text
VXN-RAMNet/
├── configs/          # Configuration files and pipeline-specific requirements
├── demo_outputs/     # Clean console output examples from experiments
├── docs/             # Architecture, build manual, and system flow documentation
├── experiments/      # Jupyter notebooks used for research experiments
├── research_notes/   # Limitations, future work, and research notes
├── sample_data/      # Sample-data instructions; raw private videos are not committed
├── sample_results/   # Curated sample outputs and reports
├── scripts/          # User-facing runnable scripts and optional upload app
├── src/              # Modular Python source code for the reusable pipeline
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## What Each New Production Folder Does

| Folder | Role |
|---|---|
| `src/` | Reusable Python engine converted from the stable backtracking notebook |
| `scripts/` | Entry points users run from terminal or local upload UI |
| `configs/` | Pipeline config and dependency files |

<details>
<summary><strong>src/ module responsibilities</strong></summary>

```text
src/vxn_ramnet/config.py
Stores pipeline settings and thresholds.

src/vxn_ramnet/frame_extraction.py
Extracts frames from learning and query videos.

src/vxn_ramnet/encoder.py
Loads EfficientNetB0 and generates original/flipped embeddings.

src/vxn_ramnet/similarity.py
Contains normalization, cosine similarity, top-k, and self-similarity helpers.

src/vxn_ramnet/route_memory.py
Stores and saves graph memory components.

src/vxn_ramnet/backtracking_graph.py
Builds the backtracking graph using flip-aware self-similarity.

src/vxn_ramnet/query_classifier.py
Classifies query videos using branch evidence windows.

src/vxn_ramnet/reports.py
Writes JSON, CSV, and Markdown reports.

src/vxn_ramnet/pipeline.py
Runs the complete end-to-end flow.

src/vxn_ramnet/cli.py
Connects the pipeline to terminal commands.

src/vxn_ramnet/utils.py
Common filesystem and JSON helpers.
```

</details>

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Main programming language |
| Jupyter Notebook | Research experiments |
| TensorFlow/Keras | EfficientNetB0 encoder |
| OpenCV | Video processing and frame extraction |
| NumPy | Embeddings, similarity, matrix operations |
| Pandas | CSV and tabular reports |
| Pillow | Image loading and preprocessing |
| Matplotlib | Experiment visualization |
| Streamlit | Optional local upload UI |

---

## Research Notes

The current research contribution is strongest around:

```text
Single-demonstration backtracking branch graph learning
```

Instead of recording:

```text
common path → left branch
common path → right branch
```

the user can record:

```text
common path → first branch → backtrack → second branch
```

This reduces repeated teaching effort and makes the route-learning process more natural.

---

## Current Limitations

This project is not overclaimed. Current limitations include:

- the dataset is still small
- the pipeline needs broader evaluation across more routes
- the system is currently offline video-based
- similar-looking corridors or branches can confuse similarity matching
- physical left/right direction is not inferred geometrically
- object detection safety is not integrated yet
- unknown-route insertion is not fully graph-aware yet
- live camera navigation is not implemented
- Android deployment is future work
- this is not certified as a safety-critical assistive navigation system

> [!WARNING]
> Do not use this repository as the only source of navigation or safety guidance. It is a research prototype.

---

## Research Roadmap

Immediate next step:

```text
VXN-RAMNet v0.2
Stable Backtracking Branch Graph Evaluation
```

Minimum evaluation target:

```text
5 backtracking route graphs
20 query videos
manual labels for junction and branch ground truth
accuracy table
failure analysis
sample reports
```

Planned improvements:

- add `05_backtracking_evaluation_summary.ipynb`
- evaluate notebook 4 across multiple route graphs
- add graph-aware unknown branch insertion
- add multi-junction graph support
- add destination-aware wrong-branch detection
- improve uncertainty handling
- add edge/mobile feasibility tests
- explore object detection as a separate safety layer
- prepare TFLite/Android deployment experiments

---

## When to Use What

| Use case | Recommended path |
|---|---|
| Understand the research idea | Read `docs/` and `experiments/` |
| Reproduce the original experiments | Run notebooks in `experiments/` |
| Run the stable modular pipeline | Use `scripts/run_backtracking_pipeline.py` |
| Use a browser upload UI | Use `scripts/backtracking_upload_app.py` |
| Inspect output without running videos | Open `demo_outputs/` and `sample_results/` |
| Study current limitations | Read `research_notes/limitations.md` |
| Study roadmap | Read `research_notes/future_work.md` |

---

## Privacy

Raw route videos are not committed by default because they may contain:

- faces
- vehicle numbers
- building names
- private locations
- home routes
- personal movement patterns
- sensitive route information

Use local videos for testing and commit only curated, anonymized reports.

---

## Author

**Ajay Soni**

Research interests:

- Assistive AI
- Computer Vision
- Visual Navigation
- Graph-Based Navigation
- Edge AI
- Real-Time AI Systems

---

## License

This project is licensed under the MIT License.
