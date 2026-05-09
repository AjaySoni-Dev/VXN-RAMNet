VXN-RAMNet

<div align="center">VisionX Routine Adaptive Memory Network

GPS-Free Visual Route Memory & Branch Graph Navigation Intelligence System

<img src="https://img.shields.io/badge/STATUS-Research%20Prototype-blue?style=for-the-badge"/>
<img src="https://img.shields.io/badge/DOMAIN-Assistive%20AI-success?style=for-the-badge"/>
<img src="https://img.shields.io/badge/FOCUS-Visual%20Navigation-important?style=for-the-badge"/>
<img src="https://img.shields.io/badge/ARCHITECTURE-Graph%20Memory-orange?style=for-the-badge"/>
<img src="https://img.shields.io/badge/RUNTIME-2--3%20FPS-critical?style=for-the-badge"/>
---

A Research-Oriented Route Memory and Graph Navigation Architecture for Personalized Assistive Intelligence

</div>
---

Overview

VXN-RAMNet (VisionX Routine Adaptive Memory Network) is a research-oriented visual navigation intelligence architecture designed for:

GPS-free route understanding

visual route memory learning

graph-based branch navigation

shared-path divergence reasoning

uncertainty-aware route classification

object-assisted safety guidance

destination-aware navigation intelligence


Unlike conventional assistive AI systems that only perform object detection, VXN-RAMNet attempts to understand:

repeated routes

common paths

junctions

LEFT/RIGHT route branches

unknown routes

wrong-turn situations

navigation uncertainty


using:

Visual Embeddings
+ Route Memory
+ DTW Synchronization
+ Graph Structures
+ Branch Reasoning
+ Risk Intelligence


---

Core Innovation

Traditional Assistive Pipeline

Camera Frame
    ↓
Object Detector
    ↓
Object Name
    ↓
Voice Output

Example:

"Chair detected"
"Person detected"
"Bottle detected"

This is useful for perception.

But it does not understand:

where the user is

whether the route is correct

where a junction exists

which branch leads to destination

whether the user took a wrong turn

repeated route memory

route uncertainty



---

VXN-RAMNet Pipeline

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


---

Final System Architecture

┌───────────────────────────────┐
│        Input Capture          │
│   Camera / Route Videos       │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│       Frame Extraction        │
│    120 Frames / 20 Seconds    │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│     Static Visual Encoder     │
│        EfficientNetB0         │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│      Embedding Creation       │
│      Route Memory System      │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│      DTW Synchronization      │
│  Shared Prefix Alignment      │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│   Common Path Detection       │
│ Junction / Divergence Logic   │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│      Branch Graph Builder     │
│ LEFT Branch / RIGHT Branch    │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│   Query Route Classification  │
│  Known / Uncertain / Unknown  │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│  Object Detection + Tracking  │
│       Risk Intelligence       │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│        Guidance Engine        │
│ Voice / Haptic Navigation     │
└───────────────────────────────┘


---

Research Contributions

Implemented Contributions

1. GPS-Free Route Memory

The system relies primarily on:

visual embeddings

route similarity

graph memory


instead of GPS.


---

2. Frozen Visual Encoder

The encoder is never retrained for new routes.

Current encoder:

EfficientNetB0

Planned mobile encoders:

EfficientNet-Lite0
MobileNetV3Large TFLite


---

3. Multi-Route Route-Memory Classification

Route classification uses:

0.50 × Best Similarity
0.30 × Top-3 Mean Similarity
0.20 × Centroid Similarity

Decision states:

CONFIRMED_ROUTE

UNCERTAIN_ROUTE

UNKNOWN_ROUTE



---

4. Uncertainty Evidence Collection

Instead of guessing from one frame:

Collect More Frames
→ Aggregate Evidence
→ Compute Stability
→ Re-Decide

Evidence windows:

1 Frame
3 Frames
5 Frames
7 Frames
9 Frames


---

5. Unknown Route Auto-Learning

Unknown routes can become new memory.

UNKNOWN_ROUTE
      ↓
Save Frames
      ↓
Generate Embeddings
      ↓
Update Route Memory
      ↓
Recognize Next Time

No retraining occurs.

Only memory grows.


---

Shared-Prefix Branch Graph Learning

One of the major innovations implemented in the current prototype.

Problem

Two routes may share:

same starting path

same corridor

same road section


before splitting into different destinations.

Traditional classification struggles with this.


---

Example

College
   ↓
Common Path
   ↓
Junction_A
   ├── LEFT  → Home
   └── RIGHT → Tuition


---

DTW Synchronization

Why DTW Was Needed

Old wrong assumption:

left_frame_18 ↔ right_frame_18

Problem:

walking speed differs

transition timing differs

route pacing differs


Correct solution:

Dynamic Time Warping (DTW)

DTW aligns:

left_frame_i ↔ right_frame_j

instead of using identical indices.


---

Junction & Divergence Detection

After DTW alignment:

High Similarity

→ Common Path

Stable Similarity Drop

→ Route Divergence

Detected outputs:

left_transition_index
right_transition_index
divergence_k
branch_split_metadata


---

Query Branch Classification

The query route can be classified as:

LEFT_BRANCH_HOME
RIGHT_BRANCH_TUITION
UNCERTAIN_BRANCH
UNKNOWN_BRANCH
UNKNOWN_OR_WEAK_COMMON_PATH

Classification process:

Extract Query Frames
        ↓
Generate Query Embeddings
        ↓
Detect Common Path End
        ↓
Select Branch Evidence
        ↓
Compare LEFT vs RIGHT
        ↓
Final Branch Prediction


---

Strong Branch Override

One important improvement added during experimentation:

Even if common-path similarity is weak,

Strong Branch Evidence
should dominate final classification.

Example:

Common Score = 0.56
LEFT Score = 0.81
RIGHT Score = 0.67

Correct output:

LEFT_BRANCH_HOME

because branch evidence is significantly stronger.


---

Object Detection Safety Layer

Object detection is intentionally independent from route memory.

Supported future models:

YOLOv8n TFLite

MobileNet-SSD

EfficientDet-Lite


It continues during:

confirmed routes

uncertain routes

unknown routes

wrong-turn situations



---

Risk Intelligence Engine

The Risk Engine combines:

route confidence

branch confidence

uncertainty state

object detection

wrong-branch state

motion/tracking


Outputs:

Risk Level	Meaning

SAFE	Normal navigation
CAUTION	Uncertain / unknown state
HIGH_RISK	Obstacle or wrong branch
CRITICAL / STOP	Immediate danger



---

Guidance Engine

Example outputs:

"Take left for Home"
"Take right for Tuition"
"Wrong branch detected"
"Unknown route detected"
"Obstacle ahead"
"Stop. Obstacle ahead"

Planned:

anti-spam cooldown logic

adaptive voice guidance

haptic navigation feedback



---

Current Experimental Pipeline

Implemented Notebook Stages

Stage 1 — Route Memory

frame extraction

embedding creation

route memory generation

centroid memory



---

Stage 2 — Unknown Route Learning

UNKNOWN_ROUTE detection

route saving

memory updating

re-recognition testing



---

Stage 3 — DTW Graph Learning

LEFT/RIGHT route encoding

similarity matrix creation

DTW synchronization

divergence detection

graph memory creation



---

Stage 4 — Query Classification

query embedding generation

common-path detection

branch evidence comparison

LEFT/RIGHT prediction



---

Repository Structure

VXN-RAMNet/
│
├── notebooks/
├── docs/
├── diagrams/
├── assets/
├── sample_results/
├── research_notes/
├── demo_outputs/
│
├── requirements.txt
├── LICENSE
└── README.md


---

Tech Stack

Core Technologies

Technology	Purpose

Python	Core development
TensorFlow	Deep learning
OpenCV	Video processing
NumPy	Embedding operations
Pillow	Image handling
Matplotlib	Visualization
Pandas	Result analysis
Jupyter Notebook	Research experimentation



---

Core Research Concepts

Computer Vision

Visual Embeddings

Cosine Similarity

Dynamic Time Warping (DTW)

Route Memory Systems

Graph Structures

Evidence Aggregation

Uncertainty Reasoning

Navigation Intelligence

Risk-Aware Guidance



---

Runtime Design Goals

Component	Target Runtime

Camera Preview	10–15 FPS
Route Classification	2–3 FPS
Object Detection	1–2 FPS
Risk Engine	2–5 FPS
Guidance	Event-Based


Optimization goals:

Load Encoder Once
Load Memory Once
Use .npz Memory
Single-Frame Embedding
Matrix Dot Product Similarity
TFLite Mobile Runtime


---

Current Limitations

sensitive to major lighting changes

similar-looking branches may confuse embeddings

currently assumes shared-prefix route structure

currently notebook-based prototype

real-world deployment requires large-scale testing


> This project is a research-oriented prototype and not a certified mobility/navigation system.




---

Future Research Directions

Version 2

recursive graph updates

backtracking-aware exploration

persistent junction memory


Version 3

DFS-style graph traversal

stack-based route reasoning

automatic branch expansion


Version 4

mobile deployment

TFLite optimization

real-time camera inference


Version 5

full assistive navigation integration

wrong-turn correction

adaptive guidance

real-time edge AI deployment



---

Author

Ajay Soni

BCA (Hons.) Data Science Student

Research Interests:

Reinforcement Learning

Assistive AI

Visual Navigation

Graph Intelligence

Computer Vision

Real-Time AI Systems

Edge AI



---

Final Research Statement

> VXN-RAMNet is a GPS-free, no-retraining, graph-based visual navigation intelligence architecture that combines static visual embeddings, route memory, DTW synchronization, branch-aware graph learning, uncertainty reasoning, and risk-guided assistive navigation into a unified research-oriented prototype system.




---

License

This project is licensed under the MIT License.


---

Acknowledgements

This project was developed as part of ongoing exploration in:

assistive AI systems

route-memory intelligence

graph-based navigation

visual environmental understanding

uncertainty-aware AI systems



---

Repository Topics

computer-vision
assistive-technology
deep-learning
graph-learning
navigation-system
visual-navigation
route-memory
edge-ai
dtw
dynamic-time-warping
real-time-ai
research-project
graph-based-navigation
