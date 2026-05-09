# VXN-RAMNet Architecture

**VisionX Routine Adaptive Memory Network**

A research prototype for GPS-free visual route memory, shared-prefix branch graph learning, and assistive navigation intelligence.

---

## 1. Purpose

VXN-RAMNet explores whether a system can understand repeated visual routes using camera or video input instead of depending on GPS.

The current prototype focuses on:

- route video frame extraction
- visual embedding generation
- route memory creation
- cosine-similarity based matching
- shared-path detection
- DTW-based route synchronization
- LEFT/RIGHT branch graph learning
- query route classification
- uncertainty and unknown-route handling

This is a research prototype, not a certified navigation or mobility system.

---

## 2. Core Idea

The system uses a frozen visual encoder to convert video frames into embeddings.  
New routes are added by storing embeddings in memory, not by retraining the model.

```text
Route Video / Camera Frame
        ↓
Frame Extraction
        ↓
Frozen Visual Encoder
        ↓
Visual Embedding
        ↓
Route / Branch Memory
        ↓
Similarity-Based Decision
```

The model stays fixed. The memory grows.

---

## 3. Current Architecture Layers

```text
Input Video / Camera
        ↓
Frame Extraction
        ↓
Static Visual Encoder
        ↓
Embedding Memory
        ↓
Route Similarity
        ↓
DTW Synchronization
        ↓
Common Path Detection
        ↓
Branch Graph Builder
        ↓
Query Branch Classification
        ↓
Uncertainty / Unknown Handling
        ↓
Risk and Guidance Logic
```

---

## 4. Static Visual Encoder

The current prototype uses:

```text
EfficientNetB0
```

Purpose:

- convert frames into embeddings
- avoid route-specific model retraining
- keep the system memory-based

Current role:

```text
Frame → EfficientNetB0 → 1280-dimensional embedding
```

Planned mobile alternatives:

- EfficientNet-Lite0
- MobileNetV3Large TFLite

---

## 5. Route Memory

A route memory stores embeddings generated from route frames.

A route memory item can contain:

```text
route_id
route_name
frame_paths
embeddings
centroid_embedding
metadata
```

Prototype storage:

```text
.npz  → numerical embeddings
.json → metadata and reports
```

This keeps the notebook workflow simple and makes the memory easy to reload.

---

## 6. Baseline Route Classification

For route matching, the prototype uses similarity-based scoring.

The main score combines:

```text
0.50 × best similarity
0.30 × top-k mean similarity
0.20 × centroid similarity
```

Possible outputs:

```text
CONFIRMED_ROUTE
UNCERTAIN_ROUTE
UNKNOWN_ROUTE
```

---

## 7. Unknown Route Learning

If a query route does not match known memory strongly, it can be treated as unknown.

Experimental flow:

```text
Unknown Route
    ↓
Save Frames
    ↓
Generate Embeddings
    ↓
Add to Route Memory
    ↓
Test Again
```

No model retraining is performed. Only memory is updated.

---

## 8. Shared-Prefix Branch Graph Learning

The main current experiment is shared-prefix branch graph learning.

Two route videos are used:

```text
left_route.mp4  → common path, then LEFT branch
right_route.mp4 → common path, then RIGHT branch
```

The system tries to create this graph:

```text
Common Path
    ↓
Junction
    ├── LEFT Branch
    └── RIGHT Branch
```

Example interpretation:

```text
College
   ↓
Common Path
   ↓
Junction_A
   ├── LEFT  → Home
   └── RIGHT → Tuition
```

The current prototype assigns the branch meaning using video order:

```text
First route after divergence  = LEFT
Second route after divergence = RIGHT
```

It does not yet infer physical left/right direction automatically from camera geometry.

---

## 9. DTW Synchronization

A direct frame-index comparison is not reliable because both videos may reach the junction at different times.

Incorrect assumption:

```text
left_frame_18 == right_frame_18
```

Problem:

```text
LEFT route transition  → around 10 seconds
RIGHT route transition → around 7-8 seconds
```

The prototype uses Dynamic Time Warping-style alignment:

```text
left_frame_i ↔ right_frame_j
```

This helps align visually similar sections even when walking speed or transition timing differs.

---

## 10. Divergence Detection

After DTW alignment, the system analyzes aligned similarity.

```text
High aligned similarity
    → common path

Stable similarity drop
    → divergence / junction
```

Stored metadata includes:

```text
transition_k
divergence_k
left_transition_index
right_transition_index
left_divergence_start
right_divergence_start
```

The notebook also displays transition context frames:

```text
3 frames before transition
1 transition frame
3 frames after transition
```

for both LEFT and RIGHT route videos.

---

## 11. Query Branch Classification

A query video is classified by comparing its branch evidence against the stored LEFT and RIGHT branch memories.

Possible outputs:

```text
LEFT_BRANCH_HOME
RIGHT_BRANCH_TUITION
UNCERTAIN_BRANCH
UNKNOWN_BRANCH
UNKNOWN_OR_WEAK_COMMON_PATH
```

The classification flow:

```text
Query Video
    ↓
Frame Extraction
    ↓
Embedding Generation
    ↓
Detect Query Common-Path End
    ↓
Select Branch Evidence
    ↓
Compare with LEFT and RIGHT Memory
    ↓
Final Prediction
```

---

## 12. Strong Branch Override

During experiments, one issue appeared: the common-path score may be weak even when the branch evidence is strong.

Example:

```text
common_score = 0.5689
left_score   = 0.8168
right_score  = 0.6774
branch_gap   = 0.1395
```

In this case, the correct decision should be LEFT because branch evidence is strong.

Current rule:

```text
If branch score is strong and branch gap is clear,
classify using branch evidence even if common-path score is weak.
```

---

## 13. Object Detection Layer

Object detection is planned as a separate safety layer.

It is not the main route-memory system.

Planned models:

- YOLOv8n TFLite
- MobileNet-SSD
- EfficientDet-Lite

Expected role:

```text
Object Safety Layer
    ↓
Risk Engine
    ↓
Guidance Output
```

This layer should continue working even if route classification is uncertain or unknown.

---

## 14. Real-Time Target

The notebook is not optimized for real-time deployment yet.

Long-term runtime targets:

| Component | Target |
|---|---|
| Camera preview | 10-15 FPS |
| Route / branch classification | 2-3 FPS |
| Object detection | 1-2 FPS |
| Risk logic | 2-5 FPS |
| Guidance | Event-based |

Real-time deployment will require optimization, likely using TFLite or LiteRT.

---

## 15. Current Limitations

- The system is currently notebook-based.
- It works best when both videos start from the same root/common path.
- LEFT/RIGHT meaning is currently assigned by video order.
- Lighting, blur, camera angle, and visual similarity affect results.
- Similar-looking branches may confuse the classifier.
- Object detection is not fully integrated yet.
- Android/mobile deployment is planned but not implemented in this repo version.
- This is not a certified safety or navigation system.

---

## 16. Future Work

Planned improvements:

- test more route videos
- improve unknown-route learning
- add destination-aware wrong-branch detection
- add object detection safety layer
- move reusable code into `src/`
- convert the encoder to TFLite
- test Android CameraX + TFLite implementation
- evaluate performance under lighting and motion variation
