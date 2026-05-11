# VXN-RAMNet

**VisionX Routine Adaptive Memory Network**

A notebook-based research prototype for GPS-free visual route memory, shared-path learning, backtracking-based branch graph learning, and assistive navigation intelligence.

![Status](https://img.shields.io/badge/status-research%20prototype-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-green)
![Workflow](https://img.shields.io/badge/workflow-jupyter%20notebook-orange)
![Domain](https://img.shields.io/badge/domain-assistive%20AI-purple)
![Model](https://img.shields.io/badge/encoder-EfficientNetB0-lightgrey)

---

## Overview

VXN-RAMNet is an experimental visual navigation project that explores how repeated routes can be learned using video input instead of relying on GPS as the main navigation brain.

The project currently focuses on:

- extracting frames from route videos
- generating visual embeddings using a frozen encoder
- comparing route memories using cosine similarity
- detecting shared route sections
- identifying where routes diverge
- building simple branch graph memory
- classifying query videos as branch routes
- handling uncertain and unknown route cases experimentally
- testing a one-video backtracking learning upgrade

This repository contains Jupyter Notebook experiments, documentation, sample reports, and console outputs used while developing the VXN-RAMNet prototype.

---

## Current Prototype Scope

This project is currently a **research prototype**, not a production navigation system.

It is not yet:

- a production Android application
- a certified assistive navigation system
- a medical or mobility safety device
- a real-time live camera product

The current implementation is based on offline video experiments in Jupyter Notebooks.

---

## Why This Project Exists

Most assistive vision systems mainly focus on object detection.

Example:

```text
Camera Frame → Object Detector → "Chair detected"
```

That is useful, but it does not answer navigation questions such as:

- Is the user on the correct route?
- Where does the route split?
- Which branch leads to the selected destination?
- Is the current path unknown?
- Can the system remember repeated routes visually?

VXN-RAMNet experiments with route memory and graph-based route reasoning instead of only detecting objects.

---

## Core Idea

The system uses a frozen visual encoder to convert route frames into embeddings.

The model is not retrained for each route. Instead, route memory grows by storing embeddings.

```text
Video Frames
    ↓
Frozen Visual Encoder
    ↓
Visual Embeddings
    ↓
Route / Branch Memory
    ↓
Similarity-Based Decision
```

Prototype encoder:

```text
EfficientNetB0
```

No route-specific model retraining is used in the current notebooks.

---

## Implemented Experiments

The repository currently contains four main notebooks.

| Notebook | Purpose |
|---|---|
| `01_route_memory_baseline.ipynb` | Baseline route-memory experiment using visual embeddings and similarity scoring |
| `02_unknown_route_auto_learning.ipynb` | Experimental unknown-route memory update without retraining |
| `03_shared_prefix_branch_graph_dtw.ipynb` | Two-video shared-prefix branch graph learning using DTW synchronization |
| `04_backtracking_branch_graph_learning.ipynb` | One-video backtracking-based branch graph learning and multi-query classification |

---

## Experiment 1: Route Memory Baseline

This notebook tests basic visual route memory.

```text
Route Videos
    ↓
Frame Extraction
    ↓
EfficientNetB0 Embeddings
    ↓
Route Memory
    ↓
Query Route Classification
```

It tests whether a query route can be matched against stored route memory using embedding similarity.

---

## Experiment 2: Unknown Route Auto-Learning

This notebook tests an early version of unknown-route learning.

```text
Known Route Memory
    ↓
Query Route
    ↓
Unknown Route Detection
    ↓
Save Unknown Route Embeddings
    ↓
Update Memory
    ↓
Test Again
```

This is still experimental and not yet fully integrated into the graph-learning system.

---

## Experiment 3: Shared-Prefix Branch Graph Learning with DTW

This notebook uses two route videos that start from a common path and later split into different branches.

Input:

```text
left_route.mp4
right_route.mp4
query_route.mp4
```

Example:

```text
left_route.mp4
Root → Common Path → Junction → LEFT Branch

right_route.mp4
Root → Common Path → Junction → RIGHT Branch
```

The notebook performs:

- frame extraction
- EfficientNetB0 embedding generation
- similarity matrix creation
- DTW-style synchronization
- common path detection
- divergence detection
- LEFT/RIGHT branch memory creation
- query route classification

Learned structure:

```text
Common Path
    ↓
Junction
    ├── LEFT Branch
    └── RIGHT Branch
```

DTW is used because two videos may reach the same junction at different times.

Instead of assuming:

```text
left_frame_18 ↔ right_frame_18
```

the system aligns visually similar sections:

```text
left_frame_i ↔ right_frame_j
```

---

## Experiment 4: Backtracking-Based Branch Graph Learning

This is the latest upgrade.

Instead of recording the common path twice, the user records one learning video.

Input:

```text
backtracking_learning_route.mp4
query_route_1.mp4
query_route_2.mp4
```

Learning video structure:

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

The notebook performs:

- frame extraction from one learning video
- EfficientNetB0 embedding generation
- flip-aware embedding comparison
- self-similarity matrix creation
- junction revisit detection
- backtracking segment detection
- graph memory creation
- multi-query branch classification
- stronger branch-evidence window selection

Learned structure:

```text
Root
  ↓
Common Path
  ↓
Junction
  ├── First Branch
  └── Second Branch
```

This upgrade fixes a key limitation of the earlier two-video method: the user does not need to re-record the same root/common path for every branch.

---

## Current Workflow

The current repo workflow is notebook-based.

```text
User records route videos
        ↓
User places videos locally
        ↓
User runs notebook cells
        ↓
System extracts frames
        ↓
System creates embeddings
        ↓
System builds memory / graph memory
        ↓
System classifies query videos
        ↓
System saves JSON and NPZ outputs
```

Raw personal videos are not included in the public repository by default.

---

## Main Outputs

The notebooks generate outputs such as:

```text
frame extraction reports
graph metadata
query classification reports
final summary reports
sample console outputs
optional graph memory NPZ files
```

Generated extracted frame folders are not included because they may contain private visual information.

---

## Repository Structure

```text
VXN-RAMNet/
│
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
│
├── notebooks/
│   ├── README.md
│   ├── 01_route_memory_baseline.ipynb
│   ├── 02_unknown_route_auto_learning.ipynb
│   ├── 03_shared_prefix_branch_graph_dtw.ipynb
│   └── 04_backtracking_branch_graph_learning.ipynb
│
├── docs/
│   ├── architecture.md
│   ├── build_manual.md
│   ├── system_flow_full.md
│   ├── system_flow_short.md
│   └── implementation_status.md
│
├── sample_data/
│   └── README.md
│
├── sample_results/
│   ├── reports/
│   │   ├── frame_extraction_report_sample.json
│   │   ├── vxn_branch_graph_metadata_dtw_sample.json
│   │   ├── vxn_branch_query_classification_report_dtw_sample.json
│   │   ├── backtracking_frame_extraction_report_sample.json
│   │   ├── backtracking_graph_metadata_sample.json
│   │   ├── backtracking_query_route_1_report_sample.json
│   │   ├── backtracking_query_route_2_report_sample.json
│   │   ├── backtracking_all_query_summary_sample.json
│   │   └── backtracking_final_summary_sample.json
│   │
│   └── memory/
│       ├── vxn_branch_graph_memory_dtw_sample.npz
│       └── vxn_backtracking_graph_memory_sample.npz
│
├── demo_outputs/
│   ├── sample_console_output.txt
│   └── backtracking_sample_console_output.txt
│
└── research_notes/
    ├── limitations.md
    └── future_work.md
```

The exact structure may change as the prototype improves.

---

## Sample Data

The `sample_data/` folder is reserved for optional anonymized sample videos.

Raw personal route videos are not included by default because route videos may contain:

- faces
- private locations
- vehicle numbers
- buildings
- personal movement patterns
- sensitive route information

The notebooks can be run with local videos placed in either:

```text
sample_data/
```

or:

```text
videos/
```

depending on notebook configuration.

---

## Sample Results

The `sample_results/` folder contains curated outputs generated from notebooks.

It may include:

- frame extraction reports
- graph metadata
- query classification reports
- final experiment summaries
- optional small graph memory files

Generated extracted frame folders and intermediate embedding files are not committed.

---

## Demo Outputs

The `demo_outputs/` folder contains clean console output examples.

Current examples:

```text
sample_console_output.txt
backtracking_sample_console_output.txt
```

These files show the important notebook output without requiring users to run the full notebooks first.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Main development language |
| Jupyter Notebook | Experimentation |
| TensorFlow / Keras | Visual encoder |
| EfficientNetB0 | Frozen frame embedding model |
| OpenCV | Video processing and frame extraction |
| NumPy | Embedding and similarity operations |
| Pandas | Result tables |
| Matplotlib | Visualization |
| Pillow | Image loading and preprocessing |

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/VXN-RAMNet.git
cd VXN-RAMNet
```

Install requirements:

```bash
pip install -r requirements.txt
```

Start Jupyter:

```bash
jupyter notebook
```

Then open the notebooks inside the `notebooks/` folder.

---

## Requirements

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

See `requirements.txt` for the full dependency list.

---

## How to Run the Main Experiments

### Run the two-video DTW experiment

Use notebook:

```text
notebooks/03_shared_prefix_branch_graph_dtw.ipynb
```

Expected local videos:

```text
left_route.mp4
right_route.mp4
query_route.mp4
```

### Run the backtracking experiment

Use notebook:

```text
notebooks/04_backtracking_branch_graph_learning.ipynb
```

Expected local videos:

```text
backtracking_learning_route.mp4
query_route_1.mp4
query_route_2.mp4
```

Recommended learning video structure:

```text
Root → Junction → First Branch → Backtrack → Junction → Second Branch
```

---

## Implementation Status

| Component | Status | Current Form |
|---|---|---|
| Video frame extraction | Implemented | Notebook |
| EfficientNetB0 frozen embedding encoder | Implemented | Notebook |
| Baseline route memory | Implemented | Notebook |
| Unknown-route memory update | Experimental | Notebook |
| Two-video DTW shared-prefix branch graph | Implemented | Notebook |
| Query LEFT/RIGHT branch classification | Implemented | Notebook |
| One-video backtracking branch graph learning | Experimental | Notebook |
| Junction revisit detection | Experimental | Self-similarity |
| Multi-query branch classification | Experimental | Notebook |
| Uncertainty handling | Partial | Threshold/evidence logic |
| Unknown branch graph insertion | Planned | Not implemented |
| Object detection safety layer | Planned | Not implemented |
| Risk engine | Planned | Not implemented |
| Voice or haptic guidance | Planned | Not implemented |
| Android app | Future work | Not implemented |
| Real-time 2-3 FPS runtime | Future work | Not implemented |

---

## Current Limitations

- The project is currently notebook-based.
- It has been tested on a limited number of route videos.
- Results depend on video quality, lighting, blur, and camera angle.
- Similar-looking branches may confuse the embedding matcher.
- Backtracking detection is experimental and should be visually verified.
- Object detection is not yet integrated.
- Live camera navigation is not implemented.
- Android deployment is future work.
- This is not a certified navigation or safety system.

See `research_notes/limitations.md` for more details.

---

## Future Work

Planned improvements:

- move reusable notebook logic into `src/` modules
- add a command-line demo script
- improve uncertainty handling
- improve unknown-route graph insertion
- add more evaluation videos
- add object detection as a separate safety layer
- build a simple risk engine
- add destination-aware wrong-branch logic
- convert the visual encoder to TensorFlow Lite
- explore Android implementation using CameraX and TFLite

See `research_notes/future_work.md` for more details.

---

## Important Safety Note

This project is a research prototype.

It is not a certified navigation system, safety device, medical device, or mobility aid.

The current goal is to test whether visual route memory and graph-based route reasoning can support personalized assistive navigation research.

Do not use this project as the only source of navigation or safety guidance.

---

## Author

**Ajay Soni**

BCA (Hons.) Data Science Student

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
