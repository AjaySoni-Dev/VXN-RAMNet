# VXN-RAMNet Short System Flow

A short overview of the current VXN-RAMNet research prototype.

VXN-RAMNet is currently a notebook-based prototype for GPS-free visual route memory, shared-path learning, branch graph learning, and query route classification.

---

## 1. Main Idea

VXN-RAMNet learns visual route memory from videos.

It does not retrain the model for each route.  
It stores visual embeddings and compares new query routes against saved route or branch memory.

The current repo includes two main branch-learning approaches:

```text
1. Two-video DTW shared-prefix branch graph learning
2. One-video backtracking-based branch graph learning
```

---

## 2. Core System Logic

```text
Route Video
  ↓
Frame Extraction
  ↓
Frozen Visual Encoder
  ↓
Visual Embeddings
  ↓
Route / Branch Memory
  ↓
Similarity-Based Classification
  ↓
Query Result
```

The encoder is frozen.  
No route-specific retraining is used.

Current prototype encoder:

```text
EfficientNetB0
```

---

## 3. Experiment 1: Two-Video Shared-Prefix DTW Flow

This is implemented in:

```text
notebooks/03_shared_prefix_branch_graph_dtw.ipynb
```

### Inputs

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

### Flow

```text
left_route.mp4 + right_route.mp4
        ↓
extract frames
        ↓
create EfficientNetB0 embeddings
        ↓
build LEFT/RIGHT similarity matrix
        ↓
apply DTW synchronization
        ↓
detect common path
        ↓
detect divergence / junction
        ↓
build LEFT/RIGHT branch memory
        ↓
classify query_route.mp4
```

### Why DTW Is Used

Two route videos may not reach the junction at the same time.

So the system uses DTW-style alignment:

```text
left_frame_i ↔ right_frame_j
```

instead of:

```text
left_frame_18 ↔ right_frame_18
```

This helps when walking speed or transition timing is different.

---

## 4. Experiment 2: One-Video Backtracking Branch Graph Flow

This is the latest implemented upgrade.

It is implemented in:

```text
notebooks/04_backtracking_branch_graph_learning.ipynb
```

### Inputs

```text
backtracking_learning_route.mp4
query_route_1.mp4
query_route_2.mp4
```

Meaning:

```text
backtracking_learning_route.mp4
= one learning video where the user goes:
  root → junction → first branch → backtrack → junction → second branch

query_route_1.mp4
= first query route to classify

query_route_2.mp4
= second query route to classify
```

### Backtracking Learning Flow

```text
Root / College
    ↓
Junction
    ↓
First Branch
    ↓
Backtrack to Junction
    ↓
Second Branch
```

### System Flow

```text
backtracking_learning_route.mp4
        ↓
extract frames
        ↓
create EfficientNetB0 embeddings
        ↓
build self-similarity matrix
        ↓
detect first junction visit
        ↓
detect return to junction
        ↓
detect backtracking segment
        ↓
split video into graph components
        ↓
build branch graph memory
        ↓
classify query_route_1 and query_route_2
```

### Learned Structure

```text
Root
  ↓
Common Path
  ↓
Junction
  ├── First Branch
  └── Second Branch
```

This upgrade avoids recording the same common/root path again and again.

---

## 5. Backtracking Handling

During backtracking, the camera may face the opposite direction.

The updated notebook handles this using:

```text
flip-aware embedding comparison
self-similarity matrix
junction revisit detection
multi-window branch evidence selection
```

This helps the system detect that the user has returned to the junction even when the camera direction changes.

---

## 6. Query Classification

For the two-video DTW experiment, the query video is classified as:

```text
LEFT_BRANCH
RIGHT_BRANCH
UNCERTAIN_BRANCH
UNKNOWN_BRANCH
```

For the backtracking experiment, query videos are classified against:

```text
First Branch
Second Branch
UNCERTAIN_BRANCH
UNKNOWN_BRANCH
```

The updated backtracking notebook does not select branch evidence too early from the root path.  
It checks multiple later windows and selects the strongest branch-evidence section.

---

## 7. Uncertain Handling

If branch scores are too close:

```text
Do not force a decision
Mark as uncertain
Use more evidence if needed
```

Current uncertainty handling is threshold-based and experimental.

---

## 8. Unknown Handling

If the query route does not match known memory:

```text
Mark as unknown
Save route frames
Generate embeddings
Add to memory later
```

Unknown-route learning exists as an experiment, but full graph-integrated unknown branch insertion is still future work.

---

## 9. Object Safety Layer

Object detection is planned as a separate safety layer.

It is not fully implemented in the current repo yet.

Planned purpose:

```text
Detect obstacles
Estimate risk
Work even when route classification is uncertain or unknown
```

---

## 10. Current Implemented Flow Summary

```text
User records videos
        ↓
User runs notebook
        ↓
System extracts frames
        ↓
System creates frozen visual embeddings
        ↓
System builds route or branch memory
        ↓
System detects common path / junction / branch structure
        ↓
System classifies query videos
        ↓
System saves JSON reports and optional NPZ memory
```

---

## 11. Final Short Flow

```text
Video input
    ↓
frame extraction
    ↓
EfficientNetB0 embedding
    ↓
route / branch memory
    ↓
similarity-based matching
    ↓
DTW or self-similarity alignment
    ↓
common path / junction detection
    ↓
branch graph creation
    ↓
query classification
    ↓
uncertain or unknown handling
    ↓
future safety and guidance layer
```

---

## 12. Current Status

Implemented:

```text
frame extraction
EfficientNetB0 embeddings
baseline route memory
unknown-route memory experiment
two-video DTW branch graph learning
one-video backtracking branch graph learning
query route classification
sample JSON/NPZ outputs
```

Partially implemented:

```text
uncertainty handling
unknown route learning
limited branch graph memory
```

Planned:

```text
object detection safety layer
risk engine
voice/haptic guidance
Android implementation
real-time camera deployment
```

---

## Important Note

VXN-RAMNet is currently a research prototype.

It is not a certified navigation system, safety device, medical device, or mobility aid.
