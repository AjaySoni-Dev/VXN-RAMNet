# VXN-RAMNet Full System Flow

This document describes the complete current system flow for the VXN-RAMNet research prototype.

---

## 1. High-Level Flow 

```text
Route Video / Camera Input
        ↓
Frame Extraction
        ↓
Visual Embedding Generation
        ↓
Route Memory
        ↓
DTW Alignment
        ↓
Common Path Detection
        ↓
Junction / Divergence Detection
        ↓
Branch Graph Memory
        ↓
Query Classification
        ↓
Uncertainty / Unknown Handling
        ↓
Risk and Guidance Logic
```

---

## 2. Core Purpose

The system is designed to test whether a route can be remembered visually.

Current goals:

- learn repeated route videos
- compare route similarity
- identify common route sections
- detect route divergence
- classify query routes as LEFT or RIGHT
- handle uncertain or unknown routes
- prepare for future assistive navigation logic

---

## 3. Input Stage

Current expected input for the branch graph experiment:

```text
left_route.mp4
right_route.mp4
query_route.mp4
```

Meaning:

```text
left_route.mp4  = common path, then LEFT branch
right_route.mp4 = common path, then RIGHT branch
query_route.mp4 = route to classify
```

The current prototype assumes both LEFT and RIGHT route videos begin from the same or visually similar root path.

---

## 4. Frame Extraction

Each video is processed as follows:

```text
Use first 20 seconds
Extract 120 evenly spaced frames
Save frames into folders
```

Output:

```text
vxn_branch_frames_dtw/
  left_route/
  right_route/
  query_route/
```

This folder is generated output and should usually not be uploaded to GitHub.

---

## 5. Embedding Stage

Each frame is passed through a frozen encoder.

```text
Frame
  ↓
EfficientNetB0
  ↓
Embedding
```

The model is not retrained.

The same encoder is used for:

- LEFT route frames
- RIGHT route frames
- query route frames
- unknown route frames

---

## 6. Shared-Prefix Branch Graph Learning

The system compares LEFT and RIGHT route videos.

```text
LEFT Route Embeddings
        ↓
Similarity Matrix
        ↑
RIGHT Route Embeddings
```

Then it performs DTW-style synchronization.

```text
left_frame_i ↔ right_frame_j
```

This solves different walking speeds and different transition times.

---

## 7. Common Path Detection

After DTW alignment:

```text
High aligned similarity
    → common path

Stable similarity drop
    → route divergence
```

The common section becomes shared graph memory.

---

## 8. Junction and Branch Creation

After divergence detection, the system creates:

```text
Common Path
    ↓
Junction_A
    ├── LEFT_BRANCH
    └── RIGHT_BRANCH
```

Current branch assignment rule:

```text
First route after divergence  = LEFT
Second route after divergence = RIGHT
```

This is a deterministic prototype rule. It does not yet infer physical direction automatically.

---

## 9. Transition Verification

The notebook displays transition context frames:

```text
3 frames before transition
1 transition frame
3 frames after transition
```

for both LEFT and RIGHT videos.

This step is important because transition detection is experimental and should be visually checked.

---

## 10. Query Classification

The query video goes through the same embedding process.

```text
Query Video
    ↓
Query Frames
    ↓
Query Embeddings
    ↓
Common Path End Detection
    ↓
Branch Evidence Selection
    ↓
LEFT vs RIGHT Scoring
    ↓
Prediction
```

Possible predictions:

```text
LEFT_BRANCH_HOME
RIGHT_BRANCH_TUITION
UNCERTAIN_BRANCH
UNKNOWN_BRANCH
UNKNOWN_OR_WEAK_COMMON_PATH
```

---

## 11. Strong Branch Rule

If common path score is weak but branch evidence is clearly strong, the system can classify using branch evidence.

Example:

```text
common_score = 0.5689
left_score   = 0.8168
right_score  = 0.6774
```

Expected output:

```text
LEFT_BRANCH_HOME
```

Reason:

```text
LEFT branch evidence is significantly stronger than RIGHT.
```

---

## 12. Uncertain Branch Handling

If LEFT and RIGHT scores are too close, the system should not guess.

It should:

- use more frames
- expand the evidence window
- average scores
- check stability
- output uncertain if still unclear

Output:

```text
UNCERTAIN_BRANCH
```

---

## 13. Unknown Route Handling

If the query does not match the learned graph, it can be marked unknown.

Possible outputs:

```text
UNKNOWN_BRANCH
UNKNOWN_OR_WEAK_COMMON_PATH
```

Future handling:

```text
Save unknown frames
Generate embeddings
Add new route or branch memory
Test again
```

---

## 14. Navigation Logic Planned

After graph memory exists, the system can support destination-based logic.

Example:

```text
Destination = Home
Expected branch = LEFT

Destination = Tuition
Expected branch = RIGHT
```

If the user takes the wrong branch:

```text
Expected = LEFT
Detected = RIGHT
```

Output:

```text
WRONG_BRANCH
```

Guidance:

```text
Wrong branch detected. Please return to the junction.
```

This part is planned and partially represented in the architecture, but not fully production-tested.

---

## 15. Object Safety Layer

Object detection is planned as an independent layer.

It should run during:

- known route
- uncertain route
- unknown route
- wrong branch
- navigation mode

It should not depend on route classification being correct.

Planned models:

- YOLOv8n TFLite
- MobileNet-SSD
- EfficientDet-Lite

---

## 16. Risk and Guidance

The future risk engine will combine:

- branch prediction
- confidence score
- unknown or uncertain state
- wrong-branch state
- object detection output
- motion or tracking data

Risk outputs:

```text
SAFE
CAUTION
HIGH_RISK
CRITICAL / STOP
```

Guidance examples:

```text
Take left for Home.
Take right for Tuition.
Wrong branch detected.
Unknown route detected.
Route uncertain.
Obstacle ahead.
Stop.
```

---

## 17. Real-Time Target

Long-term target:

| Component | Target |
|---|---|
| Camera preview | 10-15 FPS |
| Route / branch recognition | 2-3 FPS |
| Object detection | 1-2 FPS |
| Risk logic | 2-5 FPS |
| Guidance | Event-based |

The notebook version is not optimized for real-time mobile deployment yet.

---

## 18. Complete Flow Summary

```text
Record LEFT and RIGHT route videos
        ↓
Extract frames
        ↓
Generate embeddings
        ↓
Synchronize with DTW
        ↓
Detect common path
        ↓
Detect divergence
        ↓
Build LEFT/RIGHT graph memory
        ↓
Classify query video
        ↓
Handle uncertain or unknown result
        ↓
Prepare risk and guidance output
```
