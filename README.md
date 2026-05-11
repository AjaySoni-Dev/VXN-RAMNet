# VXN-RAMNet

**VisionX Routine Adaptive Memory Network**

A research prototype for GPS-free visual route memory, shared-path branch graph learning, and assistive navigation intelligence.

![Status](https://img.shields.io/badge/status-research%20prototype-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-green)
![Notebook](https://img.shields.io/badge/workflow-jupyter%20notebook-orange)
![Domain](https://img.shields.io/badge/domain-assistive%20AI-purple)

---

## Overview

VXN-RAMNet is an experimental visual navigation system that explores how repeated routes can be learned using camera/video input instead of GPS.

The project focuses on:

- extracting frames from route videos
- generating visual embeddings using a frozen encoder
- comparing routes using cosine similarity
- detecting shared route sections
- identifying where two routes diverge
- creating a simple LEFT/RIGHT branch memory
- classifying a query route video as LEFT or RIGHT
- handling uncertain and unknown route cases

This repository contains the research prototype, Jupyter Notebook experiments, documentation, and sample outputs used while developing the architecture.

---

## Current Prototype Scope

This project is currently a **notebook-based research prototype**.

It is not yet a production Android/mobile application and it is not a certified navigation or mobility system.

The current implementation mainly tests:

```text
Route Video
    ↓
Frame Extraction
    ↓
Visual Embedding
    ↓
Route Similarity
    ↓
DTW Alignment
    ↓
Common Path Detection
    ↓
Branch Classification
```

---

## Why This Project Exists

Most assistive vision systems focus mainly on object detection.

Example:

```text
Camera Frame → Object Detector → "Chair detected"
```

That is useful, but it does not understand whether the user is on the correct route.

VXN-RAMNet experiments with a different idea:

```text
Can a system remember repeated visual routes
and understand where two paths share a common section
before splitting into different branches?
```

Example:

```text
College
   ↓
Common Path
   ↓
Junction
   ├── LEFT  → Home
   └── RIGHT → Tuition
```

---

## Core Idea

The system uses a frozen visual encoder to convert route frames into embeddings.

The model is not retrained for each route. Instead, the route memory grows by storing embeddings.

```text
Video Frames
    ↓
Frozen Visual Encoder
    ↓
Embeddings
    ↓
Route / Branch Memory
    ↓
Similarity-Based Decision
```

---

## Main Features Implemented

### 1. Route Frame Extraction

Route videos are clipped logically to the first 20 seconds and sampled into evenly spaced frames.

Current experiment setting:

```text
120 frames per video
```

This helps capture the route from start to end.

---

### 2. Visual Embedding Generation

Frames are converted into embeddings using a frozen CNN encoder.

Current prototype model:

```text
EfficientNetB0
```

The encoder is used only for feature extraction.

No route-specific model retraining is performed.

---

### 3. Route Similarity Matching

The prototype uses cosine similarity between normalized embeddings.

Earlier experiments tested simple route matching using:

- best similarity
- top-k similarity
- centroid similarity
- average route score

---

### 4. Unknown Route Handling

If a route does not match existing memory strongly, the system can mark it as an unknown route.

The unknown route can later be saved as a new route memory by storing its embeddings.

This is still experimental and needs more testing.

---

### 5. Shared-Prefix Branch Graph Learning

This is the main current experiment.

Two route videos are used:

```text
left_route.mp4   → common path, then LEFT branch
right_route.mp4  → common path, then RIGHT branch
```

The system tries to detect:

- the shared route section
- the divergence point
- the LEFT branch memory
- the RIGHT branch memory

Final learned structure:

```text
Common Path
    ↓
Junction
    ├── LEFT Branch
    └── RIGHT Branch
```

---

### 6. DTW-Based Video Synchronization

A major issue in route videos is that the transition point may occur at different times.

Example:

```text
LEFT route transition  → around 10 seconds
RIGHT route transition → around 7-8 seconds
```

So direct frame-to-frame matching is not reliable.

Instead of comparing:

```text
left_frame_18 ↔ right_frame_18
```

the updated prototype uses Dynamic Time Warping style alignment:

```text
left_frame_i ↔ right_frame_j
```

This helps synchronize route videos even when walking speed is different.

---

### 7. Query Branch Classification

A third video is used as a query route:

```text
query_route.mp4
```

The system classifies it as:

```text
LEFT_BRANCH
RIGHT_BRANCH
UNCERTAIN_BRANCH
UNKNOWN_BRANCH
```

The query classification uses branch evidence after the detected common path.

---

## Current Workflow

The current notebook workflow is split into three main cells.

### Cell 1: Frame Extraction

Input:

```text
videos/
  left_route.mp4
  right_route.mp4
  query_route.mp4
```

Output:

```text
vxn_branch_frames_dtw/
  left_route/
  right_route/
  query_route/
```

---

### Cell 2: Graph Memory Creation

This cell:

- loads extracted frames
- creates embeddings
- builds a similarity matrix
- applies DTW alignment
- detects the divergence point
- creates common path, LEFT branch, and RIGHT branch memory
- saves graph memory

Output files:

```text
vxn_branch_graph_memory_dtw.npz
vxn_branch_graph_metadata_dtw.json
```

---

### Cell 3: Query Classification

This cell:

- loads the query video frames
- creates query embeddings
- detects the query common-path end
- compares branch evidence with LEFT and RIGHT memories
- outputs the predicted branch

Output file:

```text
vxn_branch_query_classification_report_dtw.json
```

---

## Repository Structure

```text
VXN-RAMNet/
│
├── notebooks/
│   └── experimental notebooks
│
├── docs/
│   └── architecture and build notes
│
├── sample_results/
│   └── reports and output examples
│
├── assets/
│   └── sample frames or diagrams
│
├── requirements.txt
├── README.md
└── LICENSE
```

The exact structure may change as the prototype improves.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Main development language |
| Jupyter Notebook | Experimentation |
| TensorFlow / Keras | Visual encoder |
| EfficientNetB0 | Frame embedding model |
| OpenCV | Video and frame processing |
| NumPy | Embedding and similarity operations |
| Pandas | Result tables |
| Matplotlib | Visualization |
| Pillow | Image handling |

---

## Example Outputs

The system generates outputs such as:

```text
Detected transition index
LEFT branch score
RIGHT branch score
Query classification result
Common path similarity curve
DTW alignment visualization
Transition context frames
```

Transition context frames are displayed for verification:

```text
3 frames before transition
1 transition frame
3 frames after transition
```

This helps check whether the detected divergence point is visually meaningful.

---

## Runtime Target

The long-term target is to make the system lightweight enough for assistive use.

Planned runtime goal:

| Component | Target |
|---|---|
| Camera preview | 10-15 FPS |
| Route / branch classification | 2-3 FPS |
| Object detection | 1-2 FPS |
| Risk and guidance logic | event-based |

The notebook version is not optimized for mobile runtime yet.

---

## Future Work

Planned improvements:

- improve branch classification robustness
- test on more real-world route videos
- add better unknown-route learning
- add wrong-branch detection using destination selection
- integrate object detection as a safety layer
- optimize the encoder using TensorFlow Lite
- explore Android implementation using CameraX and TFLite
- evaluate performance across lighting, blur, and route variation

---

## Important Note

This project is a research prototype.

It is not a certified navigation system, safety device, or medical assistive product.

The current goal is to test whether visual route memory and graph-based route reasoning can support personalized assistive navigation.

---

## Author

**Ajay Soni** 

BCA (Hons.) Data Science Student at Chandigarh University, Unnao

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
