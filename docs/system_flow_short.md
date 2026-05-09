# VXN-RAMNet Short System Flow

A short overview of the current VXN-RAMNet research prototype.

---

## 1. Main Idea

VXN-RAMNet learns visual route memory from videos.

It does not retrain the model for each route.  
It stores route embeddings and compares new query routes against memory.

---

## 2. Inputs

For the main branch graph experiment:

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

---

## 3. Frame Extraction

```text
Video
  ↓
Use first 20 seconds
  ↓
Extract 120 frames
  ↓
Save frames
```

---

## 4. Embedding Creation

```text
Frame
  ↓
EfficientNetB0
  ↓
Visual Embedding
```

The encoder is frozen.  
No route-specific retraining is used.

---

## 5. DTW Synchronization

Two route videos may not reach the junction at the same time.

So the system uses DTW-style alignment:

```text
left_frame_i ↔ right_frame_j
```

instead of:

```text
left_frame_18 ↔ right_frame_18
```

---

## 6. Graph Creation

The system finds:

```text
Common Path
    ↓
Junction
    ├── LEFT Branch
    └── RIGHT Branch
```

Current rule:

```text
First route after divergence  = LEFT
Second route after divergence = RIGHT
```

---

## 7. Query Classification

The query video is classified as:

```text
LEFT_BRANCH
RIGHT_BRANCH
UNCERTAIN_BRANCH
UNKNOWN_BRANCH
```

The decision is based on branch evidence after the detected common path.

---

## 8. Uncertain Handling

If LEFT and RIGHT scores are close:

```text
Do not guess
Use more frames
Check stability
Return uncertain if needed
```

---

## 9. Unknown Handling

If the query does not match known memory:

```text
Mark as unknown
Save route frames
Generate embeddings
Add to memory later
```

This is experimental and requires more testing.

---

## 10. Object Safety Layer

Object detection is planned as a separate safety layer.

It should work even when route classification is uncertain or unknown.

---

## 11. Final Short Flow

```text
left video + right video
        ↓
extract frames
        ↓
create embeddings
        ↓
DTW synchronize
        ↓
find common path
        ↓
detect divergence
        ↓
build LEFT/RIGHT graph
        ↓
classify query video
        ↓
handle uncertain or unknown state
        ↓
prepare guidance
```
