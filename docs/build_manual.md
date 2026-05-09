# VXN-RAMNet Build Manual

This document explains how to run the current VXN-RAMNet research prototype.

The current implementation is notebook-based and uses route videos, frame extraction, visual embeddings, similarity matching, DTW alignment, and branch classification.

---

## 1. Recommended Repository Layout

```text
VXN-RAMNet/
│
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
│
├── notebooks/
│   ├── 01_route_memory_baseline.ipynb
│   ├── 02_unknown_route_auto_learning.ipynb
│   └── 03_shared_prefix_branch_graph_dtw.ipynb
│
├── docs/
│   ├── architecture.md
│   ├── build_manual.md
│   ├── system_flow_full.md
│   └── system_flow_short.md
│
├── sample_results/
│   ├── reports/
│   └── memory/
│
├── sample_data/
│   └── README.md
│
└── research_notes/
    ├── limitations.md
    └── future_work.md
```

---

## 2. Environment Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Main dependencies:

```text
opencv-python
numpy
pandas
pillow
matplotlib
tensorflow
scikit-learn
jupyter
ipykernel
tqdm
```

---

## 3. Notebook Order

Run the notebooks in this order:

```text
01_route_memory_baseline.ipynb
02_unknown_route_auto_learning.ipynb
03_shared_prefix_branch_graph_dtw.ipynb
```

The third notebook is the main current experiment.

---

## 4. Notebook 1: Route Memory Baseline

File:

```text
notebooks/01_route_memory_baseline.ipynb
```

Purpose:

- extract frames from route videos
- create route embeddings
- save route memory
- classify a query video using evidence-based scoring

Typical outputs:

```text
extracted_frames/
vxn_video_route_memory.npz
vxn_video_route_metadata.json
vxn_query_video_classification_report.json
```

This notebook is useful as the baseline experiment before graph learning.

---

## 5. Notebook 2: Unknown Route Auto-Learning

File:

```text
notebooks/02_unknown_route_auto_learning.ipynb
```

Purpose:

- build known route memory
- classify a query route
- detect unknown route
- save unknown route as new memory
- test recognition after memory update

Typical outputs:

```text
vxn_extracted_frames/
vxn_route_memory.npz
vxn_route_metadata.json
vxn_unknown_route_decision.json
vxn_route_memory_updated.npz
vxn_route_metadata_updated.json
```

This notebook demonstrates memory growth without retraining the model.

---

## 6. Notebook 3: Shared-Prefix Branch Graph with DTW

File:

```text
notebooks/03_shared_prefix_branch_graph_dtw.ipynb
```

Purpose:

- extract frames from LEFT, RIGHT, and query videos
- generate embeddings using EfficientNetB0
- align LEFT and RIGHT route videos using DTW
- detect shared common path
- detect route divergence
- build LEFT/RIGHT branch graph memory
- classify a query route as LEFT or RIGHT

Expected input videos:

```text
videos/
  left_route.mp4
  right_route.mp4
  query_route.mp4
```

Generated outputs:

```text
vxn_branch_frames_dtw/
vxn_branch_graph_memory_dtw.npz
vxn_branch_graph_metadata_dtw.json
vxn_branch_query_classification_report_dtw.json
```

---

## 7. Frame Extraction

Current setting:

```text
Use first 20 seconds
Extract 120 frames per video
```

Reason:

- enough frames to represent the route
- improves DTW synchronization
- keeps notebook runtime manageable

The generated frame folder is useful locally, but should not usually be uploaded to GitHub.

Do not upload:

```text
vxn_branch_frames_dtw/
```

unless it contains a small anonymized sample.

---

## 8. Embedding Generation

The current prototype uses:

```text
EfficientNetB0
```

Configuration:

```text
include_top=False
weights="imagenet"
pooling="avg"
input size = 224 × 224
```

Each frame is converted into a 1280-dimensional embedding.

---

## 9. DTW Graph Creation

The third notebook creates a similarity matrix:

```text
left_embeddings @ right_embeddings.T
```

Then it applies DTW-style alignment to match visually similar sections.

The output includes:

```text
left_transition_index
right_transition_index
left_divergence_start
right_divergence_start
```

This fixes the issue where the LEFT route and RIGHT route reach the transition at different times.

---

## 10. Query Classification

The query route is classified using branch evidence.

Possible outputs:

```text
LEFT_BRANCH_HOME
RIGHT_BRANCH_TUITION
UNCERTAIN_BRANCH
UNKNOWN_BRANCH
UNKNOWN_OR_WEAK_COMMON_PATH
```

Important rule:

```text
If branch evidence is strong and the LEFT/RIGHT gap is clear,
use branch evidence even if common-path score is weak.
```

---

## 11. What to Upload to GitHub

Upload:

```text
notebooks/
docs/
sample_results/reports/
README.md
requirements.txt
LICENSE
.gitignore
```

Optional:

```text
sample_results/memory/vxn_branch_graph_memory_dtw_sample.npz
```

Do not upload:

```text
.ipynb_checkpoints/
vxn_branch_frames_dtw/
raw videos with private locations
large generated frame folders
temporary files
```

---

## 12. Testing Checklist

Before uploading or presenting the repo, check:

- notebooks open correctly
- notebook names are clean
- no checkpoint files are included
- requirements.txt is present
- README explains current scope honestly
- sample reports are included
- raw private videos are not included
- generated frames are not uploaded as main repo content

---

## 13. Current Status

The project currently works as a research notebook prototype.

It is useful for:

- route memory experimentation
- unknown-route learning tests
- DTW-based shared-path branch graph experiments
- query branch classification

It is not yet:

- a production Android app
- a certified assistive device
- a fully real-time navigation system
