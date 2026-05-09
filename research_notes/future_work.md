# Future Work

This document outlines planned improvements for the VXN-RAMNet research prototype.

The project is currently notebook-based and focuses on visual route memory, DTW synchronization, shared-prefix branch graph learning, and query branch classification. Future work will focus on robustness, graph expansion, object safety, and mobile deployment.

---

## 1. Improve Dataset Quality

The current experiments use a small number of route videos.

Future work should include more diverse test data:

- multiple routes
- multiple query videos per route
- different lighting conditions
- different walking speeds
- different camera angles
- indoor and outdoor routes
- repeated recordings on different days
- similar-looking branches
- unknown routes

This will help evaluate whether the system generalizes beyond the initial experiment.

---

## 2. Create a Structured Evaluation Protocol

The project needs a clear evaluation process.

Planned metrics:

| Metric | Purpose |
|---|---|
| Route classification accuracy | Measures correct route prediction |
| Branch classification accuracy | Measures LEFT/RIGHT decision quality |
| Unknown-route detection rate | Measures unknown route handling |
| False unknown rate | Checks if known routes are wrongly rejected |
| Transition detection error | Measures divergence point accuracy |
| Average inference time | Measures runtime performance |
| Memory size growth | Tracks memory scalability |

A future evaluation notebook can generate a summary report for all test routes.

---

## 3. Improve Transition Detection

Current divergence detection uses smoothed similarity drops after DTW alignment.

Future improvements:

- adaptive thresholds
- multi-window transition scoring
- confidence score for transition point
- temporal smoothing
- visual scene-change detection
- optical flow support
- transition uncertainty region instead of single index

Instead of one transition frame, the system may store a transition zone:

```text
transition_start
transition_center
transition_end
```

This may be more reliable for real-world route splits.

---

## 4. Expand Branch Graph Learning

The current graph experiment supports a simple structure:

```text
Common Path
    ↓
Junction
    ├── LEFT Branch
    └── RIGHT Branch
```

Future versions should support:

- more than two branches
- straight branch
- curved branch
- nested junctions
- route merging
- loops
- dead ends
- branch re-entry
- multi-destination graphs

Example future graph:

```text
Root
  ↓
Common Path
  ↓
Junction_A
  ├── LEFT  → Home
  ├── RIGHT → Tuition
  └── STRAIGHT → Market
```

---

## 5. Add Backtracking-Based Exploration

Current graph learning uses full videos from the root path.

Future version:

```text
Start at root
    ↓
Record LEFT branch
    ↓
Backtrack to junction
    ↓
Record RIGHT branch
```

This would reduce the need to record the full common path repeatedly.

Planned features:

- backtracking state
- visited node recognition
- return-to-junction detection
- branch completion status
- graph update after each branch

---

## 6. Add DFS-Style Graph Exploration

A later research direction is structured graph exploration inspired by DFS.

Concept:

```text
Explore LEFT first
    ↓
Go deeper if another junction exists
    ↓
Backtrack when branch ends
    ↓
Explore RIGHT branch
```

This can build a topological graph in a deterministic way.

Required components:

- traversal stack
- current node tracking
- branch completion flags
- parent-child transitions
- visited node detection
- graph consistency checks

---

## 7. Improve Unknown Route Learning

Unknown-route learning should become more structured.

Future improvements:

- detect unknown route more reliably
- prevent duplicate route memory
- merge similar unknown routes
- ask user to label new route
- connect unknown route to nearest known graph node
- create unknown branch from existing junction
- maintain memory version history

Possible future flow:

```text
UNKNOWN_BRANCH
    ↓
Save candidate memory
    ↓
Verify with repeated evidence
    ↓
Ask user for label
    ↓
Attach to graph
```

---

## 8. Improve Memory Management

As the number of routes grows, memory management becomes important.

Future memory improvements:

- route memory compression
- centroid-based search
- approximate nearest neighbor search
- memory pruning
- duplicate frame removal
- low-quality frame filtering
- route versioning
- memory confidence score

Instead of storing every frame equally, the system can store keyframes.

---

## 9. Add Object Detection Safety Layer

Object detection should be integrated as a separate safety module.

Planned models:

- YOLOv8n TFLite
- MobileNet-SSD
- EfficientDet-Lite

Planned outputs:

- object class
- confidence
- bounding box
- object position zone
- approximate danger level

The object detection layer should work even if route classification is uncertain or unknown.

---

## 10. Add Motion and Tracking

Object detection does not need to run on every frame.

Future system can use tracking between detections:

- centroid tracking
- optical flow
- bounding-box reuse
- object movement estimation
- approaching-object detection

This can reduce computation and improve real-time performance.

---

## 11. Build Risk Intelligence Engine

A risk engine should combine multiple signals.

Inputs:

- route confidence
- branch confidence
- unknown route state
- uncertain branch state
- wrong branch state
- object detection output
- motion/tracking data
- optional distance sensor

Outputs:

```text
SAFE
CAUTION
HIGH_RISK
CRITICAL / STOP
```

The risk engine should prioritize safety over route guidance.

---

## 12. Improve Guidance Engine

The guidance engine should convert system states into simple user-friendly instructions.

Planned guidance types:

- voice output
- vibration output
- wrong-branch warning
- obstacle warning
- unknown-route warning
- uncertain-route warning
- destination-aware branch instruction

Example:

```text
Take left for Home.
Wrong branch detected. Please return.
Obstacle ahead. Move carefully.
Route uncertain. Please slow down.
```

Guidance should include anti-spam logic so the system does not repeat messages too frequently.

---

## 13. Android Implementation

A future version can be implemented in Android Studio.

Recommended Android stack:

```text
Kotlin
CameraX
TensorFlow Lite / LiteRT
Room or SQLite
TextToSpeech
Vibration / Haptics
```

Mobile architecture:

```text
CameraX ImageAnalysis
    ↓
Frame Scheduler
    ↓
TFLite Visual Encoder
    ↓
Local Route Memory
    ↓
Branch Classifier
    ↓
Risk Engine
    ↓
TextToSpeech / Haptic Output
```

The Android version should separate learning mode from navigation mode.

---

## 14. TFLite / LiteRT Optimization

The current prototype uses TensorFlow/Keras in notebooks.

Future deployment should use:

- TFLite model conversion
- quantization
- GPU delegate
- NNAPI where available
- fixed input size
- preloaded route memory
- optimized FloatArray similarity search

Goal:

```text
Route / branch recognition: 2-3 FPS
Object detection: 1-2 FPS
```

---

## 15. Add Real-Time Frame Scheduler

The real-time system should not process every frame heavily.

Suggested schedule:

| Component | Target |
|---|---|
| Camera preview | 10-15 FPS |
| Route recognition | 2-3 FPS |
| Object detection | 1-2 FPS |
| Risk engine | 2-5 FPS |
| Guidance | Event-based |

This keeps the system lightweight and practical for mobile devices.

---

## 16. Add Reproducible Experiments

Future repository updates should include:

- clean sample outputs
- JSON reports
- notebook execution notes
- expected input file names
- reproducible test instructions
- sample console output
- versioned experiment folders

This will make the research easier to verify.

---

## 17. Add Better Documentation

Future documentation improvements:

- architecture diagram
- notebook walkthrough
- experiment result summary
- output file explanation
- privacy guide
- Android deployment notes
- troubleshooting guide

The goal is to make the repo understandable without needing the original chat discussion.

---

## 18. Possible Research Questions

Future research can explore:

1. Can visual route memory reliably replace GPS for repeated personal routes?
2. How much route variation can embedding memory tolerate?
3. How accurate is DTW-based common-path detection?
4. What is the best visual encoder for lightweight route memory?
5. How should unknown routes be added without creating duplicate memory?
6. Can graph memory improve wrong-turn detection?
7. How well does the system work under lighting and motion variation?
8. Can mobile hardware support route memory and object detection together?

---

## 19. Planned Development Roadmap

### Version 1

Current prototype:

- route memory baseline
- unknown route learning
- shared-prefix branch graph learning
- DTW synchronization
- query branch classification

### Version 2

Planned improvements:

- more route testing
- better transition detection
- improved unknown route handling
- cleaner modular Python code

### Version 3

Graph improvements:

- backtracking exploration
- DFS-style graph learning
- multi-branch junction support
- wrong-turn detection

### Version 4

Safety and guidance:

- object detection integration
- risk engine
- voice guidance
- haptic feedback

### Version 5

Mobile deployment:

- Android Studio implementation
- CameraX live inference
- TFLite visual encoder
- local route memory
- real-time optimization

---

## 20. Final Direction

The long-term goal of VXN-RAMNet is to move from a notebook-based research prototype toward a lightweight mobile assistive navigation system.

The current focus is not to claim production readiness, but to build and test each component carefully:

```text
visual route memory
+ shared-path detection
+ graph-based branch reasoning
+ uncertainty handling
+ safety-aware guidance
```

Each future version should improve reliability, privacy, speed, and real-world usability.
