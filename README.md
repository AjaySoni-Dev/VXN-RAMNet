<div align="center">

# VXN-RAMNet

### VisionX Routine Adaptive Memory Network

**GPS-Free Visual Route Memory and Branch Graph Navigation Intelligence System**

<br/>

![Status](https://img.shields.io/badge/Status-Research%20Prototype-blue?style=for-the-badge)
![Domain](https://img.shields.io/badge/Domain-Assistive%20AI-success?style=for-the-badge)
![Focus](https://img.shields.io/badge/Focus-Visual%20Navigation-important?style=for-the-badge)
![Architecture](https://img.shields.io/badge/Architecture-Graph%20Memory-orange?style=for-the-badge)
![Runtime](https://img.shields.io/badge/Runtime-2--3%20FPS-critical?style=for-the-badge)

<br/>

**A research-oriented route memory and graph navigation architecture for personalized assistive intelligence.**

</div>

---

## Overview

**VXN-RAMNet** is a GPS-free visual navigation intelligence architecture designed to help assistive systems understand repeated routes, shared paths, route branches, and navigation uncertainty.

Unlike conventional assistive vision systems that mainly detect objects, VXN-RAMNet focuses on route understanding through:

- Visual embeddings
- Route memory
- Dynamic Time Warping synchronization
- Shared-prefix graph learning
- LEFT/RIGHT branch reasoning
- Unknown-route learning
- Risk-aware guidance

The system is designed as a research prototype for assistive AI, visual navigation, graph-based route memory, and edge AI deployment.

---

## Problem Statement

Most assistive AI pipelines follow this structure:

```text
Camera Frame
    ↓
Object Detector
    ↓
Object Name
    ↓
Voice Output
```

This is useful for perception, but it does not answer important navigation questions:

- Where is the user currently?
- Is the user on the correct route?
- Where does the route split?
- Which branch leads to the selected destination?
- Has the user taken a wrong turn?
- Is the route known, uncertain, or unknown?

VXN-RAMNet extends assistive perception into route-memory intelligence.

---

## Core Idea

```text
Camera / Route Video
        ↓
Frame Extraction
        ↓
Static Visual Encoder
        ↓
Visual Embeddings
        ↓
Route Memory
        ↓
DTW Synchronization
        ↓
Shared-Path Graph Learning
        ↓
LEFT / RIGHT Branch Intelligence
        ↓
Uncertainty Handling
        ↓
Object Safety Layer
        ↓
Risk Engine
        ↓
Guidance Engine
```

---

## Final System Architecture

```text
┌──────────────────────────────────────┐
│            Input Capture             │
│        Camera / Route Videos         │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│           Frame Extraction           │
│       120 Frames / 20 Seconds        │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│        Static Visual Encoder         │
│            EfficientNetB0            │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│         Embedding Creation           │
│         Route Memory System          │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│          DTW Synchronization         │
│       Shared-Prefix Alignment        │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│        Common Path Detection         │
│     Junction / Divergence Logic      │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│          Branch Graph Builder        │
│       LEFT Branch / RIGHT Branch     │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│       Query Route Classification     │
│      Known / Uncertain / Unknown     │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│      Object Detection and Tracking   │
│          Risk Intelligence           │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│            Guidance Engine           │
│       Voice / Haptic Navigation      │
└──────────────────────────────────────┘
```

---

## Research Contributions

### 1. GPS-Free Route Memory

The system primarily relies on visual route memory instead of GPS. Routes are represented using visual embeddings and similarity-based matching.

### 2. Frozen Visual Encoder

The visual encoder is not retrained for every new route. It is used only for embedding generation.

Current prototype encoder:

```text
EfficientNetB0
```

Planned mobile encoders:

```text
EfficientNet-Lite0
MobileNetV3Large TFLite
```

### 3. Multi-Route Classification

Route scoring is based on three similarity signals:

```text
Final Route Score =
    0.50 × Best Similarity
  + 0.30 × Top-3 Mean Similarity
  + 0.20 × Centroid Similarity
```

Decision states:

```text
CONFIRMED_ROUTE
UNCERTAIN_ROUTE
UNKNOWN_ROUTE
```

### 4. Evidence-Based Uncertainty Handling

Instead of making a decision from one frame, the system collects more evidence when route confidence is unclear.

```text
1 frame → 3 frames → 5 frames → 7 frames → 9 frames
```

The final decision uses average score, vote stability, and confidence gap.

### 5. Unknown Route Auto-Learning

Unknown routes can be saved as new memory without retraining the model.

```text
UNKNOWN_ROUTE
      ↓
Save Frames
      ↓
Generate Embeddings
      ↓
Update Route Memory
      ↓
Recognize Next Time
```

---

## Shared-Prefix Branch Graph Learning

One of the major components of VXN-RAMNet is **Shared-Prefix Branch Graph Learning**.

Many real routes share the same starting path before splitting into different destinations.

Example:

```text
College
   ↓
Common Path
   ↓
Junction_A
   ├── LEFT  → Home
   └── RIGHT → Tuition
```

Instead of storing both full routes separately, VXN-RAMNet detects the common path, identifies the divergence point, and builds a graph structure.

---

## DTW Synchronization

A major issue in route video comparison is that two route videos may not reach the transition point at the same time.

Incorrect assumption:

```text
left_frame_18 ↔ right_frame_18
```

This fails when:

- walking speed differs
- transition timing differs
- camera pacing differs

VXN-RAMNet uses Dynamic Time Warping-style alignment:

```text
left_frame_i ↔ right_frame_j
```

This allows the system to synchronize visually similar route sections even when the transition occurs at different timestamps.

---

## Divergence and Junction Detection

After DTW synchronization:

```text
High Similarity
    → Common Path

Stable Similarity Drop
    → Route Divergence
```

Detected metadata includes:

```text
left_transition_index
right_transition_index
divergence_k
left_divergence_start
right_divergence_start
branch_split_metadata
```

For validation, the system displays:

```text
3 frames before transition
1 transition frame
3 frames after transition
```

for both LEFT and RIGHT route videos.

---

## Branch Classification

A query route can be classified as:

```text
LEFT_BRANCH_HOME
RIGHT_BRANCH_TUITION
UNCERTAIN_BRANCH
UNKNOWN_BRANCH
UNKNOWN_OR_WEAK_COMMON_PATH
```

Classification flow:

```text
Extract Query Frames
        ↓
Generate Query Embeddings
        ↓
Detect Query Common-Path End
        ↓
Select Branch Evidence
        ↓
Compare LEFT vs RIGHT Branch Memory
        ↓
Final Branch Prediction
```

### Strong Branch Override

If the branch evidence is strong, the system does not reject the result only because the common path score is weak.

Example:

```text
Common Score = 0.56
LEFT Score   = 0.81
RIGHT Score  = 0.67
```

Correct output:

```text
LEFT_BRANCH_HOME
```

Reason: the branch evidence is significantly stronger.

---

## Object Safety Layer

Object detection is intentionally independent from route memory.

It continues during:

- confirmed routes
- uncertain routes
- unknown routes
- wrong-branch situations

Planned object detection models:

```text
YOLOv8n TFLite
MobileNet-SSD
EfficientDet-Lite
```

This keeps safety warnings active even when route memory is uncertain.

---

## Risk Intelligence Engine

The risk engine combines:

- route confidence
- branch confidence
- uncertainty state
- unknown-route state
- wrong-branch state
- object detection output
- motion or tracking information

| Risk Level | Meaning |
|---|---|
| SAFE | Normal navigation |
| CAUTION | Uncertain or unknown state |
| HIGH_RISK | Obstacle or wrong branch |
| CRITICAL / STOP | Immediate danger |

---

## Guidance Engine

Example outputs:

```text
Take left for Home.
Take right for Tuition.
Wrong branch detected.
Unknown route detected.
Obstacle ahead.
Stop. Obstacle ahead.
```

Planned guidance features:

- anti-spam cooldown
- adaptive voice guidance
- haptic navigation feedback
- priority-based warning system

---

## Current Experimental Pipeline

| Stage | Description |
|---|---|
| Stage 1 | Route frame extraction and embedding creation |
| Stage 2 | Route memory generation and centroid storage |
| Stage 3 | Unknown-route detection and memory update |
| Stage 4 | DTW-based shared-prefix graph learning |
| Stage 5 | LEFT/RIGHT query branch classification |
| Stage 6 | Transition-frame verification |
| Stage 7 | Risk and guidance logic design |

---

## Repository Structure

```text
VXN-RAMNet/
│
├── notebooks/
│   ├── route_memory_experiments.ipynb
│   ├── unknown_route_learning.ipynb
│   └── dtw_branch_graph_learning.ipynb
│
├── docs/
│   ├── architecture.md
│   ├── build_manual.md
│   └── system_flow.md
│
├── diagrams/
│   └── architecture_flow.png
│
├── assets/
│   └── sample_frames/
│
├── sample_results/
│   ├── classification_reports/
│   └── transition_outputs/
│
├── research_notes/
│
├── demo_outputs/
│
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core research development |
| TensorFlow | Visual encoder and model inference |
| OpenCV | Video processing and frame extraction |
| NumPy | Embedding operations and similarity search |
| Pandas | Result tables and analysis |
| Pillow | Image processing |
| Matplotlib | Visual verification and plots |
| Jupyter Notebook | Research experimentation |

---

## Core Research Concepts

- Computer Vision
- Visual Embeddings
- Cosine Similarity
- Dynamic Time Warping
- Route Memory Systems
- Graph-Based Navigation
- Shared-Prefix Learning
- Evidence Aggregation
- Uncertainty Reasoning
- Risk-Aware Guidance
- Edge AI Deployment

---

## Runtime Design Goals

| Component | Target Runtime |
|---|---|
| Camera Preview | 10–15 FPS |
| Route Classification | 2–3 FPS |
| Object Detection | 1–2 FPS |
| Risk Engine | 2–5 FPS |
| Guidance | Event-Based |

Optimization principles:

```text
Load encoder once
Load memory once
Use .npz memory files
Use single-frame embeddings
Use matrix dot-product similarity
Avoid runtime plotting
Use TFLite for mobile deployment
```

---

## Android Deployment Direction

The research prototype is notebook-based, but the architecture is mobile-implementable.

Recommended Android stack:

```text
Kotlin
CameraX
TensorFlow Lite / LiteRT
Room or SQLite
TextToSpeech
Vibration / Haptics
```

Mobile design split:

```text
Learning Mode
    Frame extraction
    DTW synchronization
    Graph memory creation

Navigation Mode
    Live frame embedding
    Branch classification
    Object safety layer
    Risk engine
    Guidance output
```

---

## Current Limitations

- Sensitive to major lighting changes
- Similar-looking branches may confuse embeddings
- Assumes shared-prefix structure for branch graph learning
- Requires more real-world testing
- Currently implemented as a research notebook prototype
- Not a certified mobility or medical navigation system

> This project is a research-oriented prototype and should not be used as a certified navigation or safety device.

---

## Future Research Directions

| Version | Planned Upgrade |
|---|---|
| Version 2 | Recursive graph updates and persistent junction memory |
| Version 3 | DFS-style graph traversal and stack-based route reasoning |
| Version 4 | Mobile deployment with TFLite optimization |
| Version 5 | Real-time assistive navigation with adaptive guidance |
| Version 6 | Larger-scale environment graph learning and evaluation |

---

## Author

**Ajay Soni**

BCA (Hons.) Data Science Student

Research interests:

- Assistive AI
- Visual Navigation
- Graph Intelligence
- Computer Vision
- Real-Time AI Systems
- Edge AI
- Reinforcement Learning

---

## Final Research Statement

> VXN-RAMNet is a GPS-free, no-retraining, graph-based visual navigation intelligence architecture that combines static visual embeddings, route memory, DTW synchronization, branch-aware graph learning, uncertainty reasoning, and risk-guided assistive navigation into a unified research-oriented prototype system.

---

## Repository Topics

```text
computer-vision
assistive-technology
deep-learning
graph-learning
navigation-system
visual-navigation
route-memory
edge-ai
dynamic-time-warping
real-time-ai
research-project
graph-based-navigation
```

---

## License

This project is licensed under the MIT License.
