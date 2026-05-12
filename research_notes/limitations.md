# Limitations

This document lists the current limitations of the VXN-RAMNet research prototype.

The goal is to keep the project technically honest. VXN-RAMNet is currently a notebook-based research prototype. It is not a production navigation product, not a certified assistive device, and not a safety-critical system.

---

## 1. Current Prototype Status

VXN-RAMNet is currently implemented through Jupyter Notebook experiments.

Current implementation includes:

- video frame extraction
- EfficientNetB0-based visual embeddings
- baseline route memory
- unknown-route memory update experiment
- two-video DTW shared-prefix branch graph learning
- one-video backtracking branch graph learning
- query route classification
- JSON and NPZ sample output generation

Current implementation does not yet include:

- production Android application
- live camera navigation
- certified safety layer
- fully integrated object detection
- risk engine
- voice or haptic guidance
- large-scale dataset evaluation
- real-world assistive deployment

The current system should be treated as an experimental research base, not a finished product.

---

## 2. Small Dataset Limitation

The current experiments use a small number of personally recorded route videos.

This creates major limitations:

- limited route diversity
- limited lighting variation
- limited camera angle variation
- limited walking speed variation
- limited route complexity
- limited number of query videos
- limited unknown-route testing
- no benchmark dataset
- no large public validation set

Because of this, current results cannot prove real-world reliability. They only show that the idea works under controlled prototype conditions.

---

## 3. Notebook-Based Workflow Limitation

The current workflow is not production-like.

The notebooks:

- read videos from disk
- extract frames into folders
- process batches offline
- display plots and frame previews
- save intermediate JSON and NPZ files
- require manual inspection

This is useful for research, but it is not the same as a live assistive system.

A real system would need:

- live camera frame processing
- frame scheduling
- low-latency inference
- background processing
- optimized memory search
- user-safe error handling
- no manual notebook inspection

---

## 4. Frozen Encoder Limitation

The current prototype uses EfficientNetB0 as a frozen visual encoder.

This is practical for early experiments, but it has limitations:

- it was not trained specifically for visual navigation
- it may confuse visually similar places
- it may fail under strong lighting changes
- it may be affected by motion blur
- it may not handle large viewpoint changes well
- it may miss small but important route differences
- it may not generalize to all indoor/outdoor environments

The encoder is useful for prototype testing, but it is not proven as the final best model for this system.

---

## 5. Two-Video Shared-Prefix Method Limitation

The two-video DTW notebook assumes this structure:

```text
left_route.mp4  = root/common path → LEFT branch
right_route.mp4 = root/common path → RIGHT branch
query_route.mp4 = route to classify
```

This works for testing shared-path branch learning, but it has limitations:

- the common path must be recorded twice
- both videos should start from a similar root point
- both videos should share a visually recognizable path
- large camera differences can break alignment
- the system currently supports a simple two-branch case
- complex multi-junction environments are not fully handled

This method is useful, but it is not efficient for learning larger environments.

---

## 6. Backtracking Learning Limitation

The new backtracking notebook improves the workflow by using one learning video:

```text
root → junction → first branch → backtrack → junction → second branch
```

However, it is still experimental.

Limitations:

- the system must detect the first junction and return junction correctly
- backtracking changes camera direction, which can reduce similarity quality
- the detected turnaround point may be wrong if the video is shaky
- long pauses or sudden turns can confuse the split logic
- visually repetitive corridors may create false junction matches
- the learning video must follow the expected structure
- it currently supports a limited one-junction, two-branch scenario

The backtracking notebook is a major upgrade, but it still requires visual verification.

---

## 7. Branch Label Limitation

In the current implementation, branch labels are assigned by recording order or notebook configuration.

For the two-video DTW notebook:

```text
first route after divergence  = LEFT
second route after divergence = RIGHT
```

For the backtracking notebook:

```text
first branch visited before backtracking  = first branch memory
second branch visited after backtracking  = second branch memory
```

The system does not yet infer real physical left/right direction automatically from camera geometry.

This means:

- branch labels depend on how the user records the videos
- wrong naming can cause wrong interpretation
- physical left/right is not automatically verified
- inertial sensor support is not yet used

Future versions may use IMU, compass, optical flow, or visual odometry to improve physical direction understanding.

---

## 8. DTW Alignment Limitation

DTW-style alignment helps when two videos have different walking speeds or transition times.

However, DTW can fail when:

- videos start from different places
- one video skips part of the common path
- one video has long pauses
- one video has heavy camera shake
- the common path is too short
- the scene contains repeated similar visual patterns
- embeddings are weak or noisy

DTW improves synchronization, but it does not guarantee correct route alignment.

---

## 9. Self-Similarity Limitation

The backtracking notebook uses a self-similarity matrix to detect when the user returns to the junction.

This can fail if:

- the junction looks similar to other places
- the route has repeated corridors
- the camera angle is very different on return
- lighting changes during recording
- the user turns too quickly
- the return path is visually unclear
- there is no clear pause or visual landmark at the junction

Self-similarity is useful, but it is not yet a complete visual localization solution.

---

## 10. Query Classification Limitation

Query classification depends on:

- video quality
- branch visibility
- selected evidence window
- camera direction
- lighting
- frame stability
- visual difference between branches
- strength of saved branch memory

The classifier can misclassify if:

- the query video starts too late
- the query video does not contain enough branch frames
- the branch looks similar to another branch
- the camera angle is different from learning
- the path is partially blocked
- motion blur affects important frames
- the selected branch evidence window is not representative

The latest backtracking notebook improves branch evidence selection, but query classification still needs more testing.

---

## 11. Uncertainty Handling Limitation

Uncertainty handling currently exists mainly as threshold-based logic.

The current system can return uncertain states, but it does not yet have a complete robust uncertainty engine.

Missing parts include:

- multi-window vote stability
- repeated evidence collection over time
- temporal confidence smoothing
- confidence calibration
- false-positive control
- explainable uncertainty reports
- automatic request for more frames in real time

The current uncertainty logic is useful for experiments, but it is not strong enough for safety-critical navigation.

---

## 12. Unknown Route Learning Limitation

Unknown-route learning exists as an experiment, but it is not fully integrated into graph memory.

Current limitations:

- unknown routes are not automatically attached to the correct junction
- duplicate unknown routes may be created
- noisy route memories may grow over time
- route naming is not automated
- user confirmation is not implemented
- unknown route quality is not validated
- graph consistency is not enforced

Full unknown-route graph insertion is still future work.

---

## 13. Graph Memory Limitation

The current graph memory is limited.

Implemented graph structures are mainly:

```text
common path → junction → LEFT/RIGHT branch
```

and:

```text
root → junction → first branch → backtrack → junction → second branch
```

The system does not yet fully support:

- many junctions
- loops
- route merging
- recursive graph expansion
- multiple destinations
- route planning
- shortest path selection
- graph repair
- graph versioning
- automatic graph consistency checks

Current graph memory is a prototype, not a complete navigation graph engine.

---

## 14. Object Detection Limitation

Object detection is planned as a separate safety layer, but it is not fully implemented in the current repo.

The current notebooks focus mainly on:

- visual embeddings
- route memory
- branch graph learning
- query classification

Object detection still needs:

- lightweight detector integration
- detection zones
- tracking
- risk scoring
- false warning control
- real-time performance testing
- voice/haptic warning connection

Until this is implemented, the system cannot provide real obstacle safety support.

---

## 15. Risk Engine Limitation

The risk engine is not implemented yet.

The current system does not yet combine:

- branch confidence
- unknown-route state
- uncertain-route state
- object detection
- motion tracking
- wrong-branch state
- distance information
- user guidance priority

Risk levels such as:

```text
SAFE
CAUTION
HIGH_RISK
CRITICAL / STOP
```

are planned concepts, not complete working runtime logic.

---

## 16. Guidance Limitation

Voice or haptic guidance is not implemented in the current repo.

There is no working system yet for:

- TextToSpeech output
- haptic feedback
- cooldown between messages
- critical alert priority
- wrong-branch warning
- live user instruction
- accessibility testing

Current guidance examples are design plans, not deployed features.

---

## 17. Real-Time Limitation

The current system is not optimized for real-time deployment.

Current notebooks include:

- batch inference
- frame extraction to disk
- plotting
- visualization
- JSON/NPZ saving
- manual verification

A real-time system would need:

- encoder loaded once
- graph memory loaded once
- live frame scheduler
- fast similarity search
- no runtime plotting
- no repeated disk reads
- mobile inference optimization
- strict latency measurement

The target of 2-3 FPS route recognition is a future engineering goal, not a proven mobile result yet.

---

## 18. Android Deployment Limitation

The architecture may be possible to deploy on Android, but no Android app is currently implemented.

Android implementation would require:

- CameraX pipeline
- TensorFlow Lite or LiteRT encoder
- local memory storage
- optimized embedding comparison
- background threading
- battery testing
- thermal testing
- TextToSpeech
- haptics
- UI/UX for learning and navigation modes

The current repo is a research base for Android work, not an Android application.

---

## 19. Privacy Limitation

Route videos can contain sensitive information.

Possible privacy risks:

- faces
- homes
- number plates
- college buildings
- street signs
- personal routes
- repeated movement patterns
- location context

For this reason:

- raw videos should not be uploaded publicly unless anonymized
- extracted frames should not be committed
- generated frame folders should remain local
- public sample data should be privacy-reviewed

Privacy is a serious limitation for this kind of project.

---

## 20. Safety Limitation

VXN-RAMNet is not a certified navigation, medical, mobility, or safety product.

It should not be used as the only source of navigation guidance.

Current outputs can be wrong.

Before real assistive use, the system would need:

- larger testing
- controlled evaluation
- field trials
- accessibility testing
- failure-mode handling
- safety validation
- human review
- legal and ethical review

---

## 21. Summary

The current VXN-RAMNet prototype demonstrates an experimental direction:

```text
visual route memory
+ DTW synchronization
+ backtracking graph learning
+ branch classification
```

However, it remains early-stage.

The main limitations are:

```text
small dataset
not real-time
not mobile-ready
not safety-certified
limited graph complexity
experimental backtracking detection
no integrated object detection
no risk/guidance engine
```

These limitations should be treated as active research and engineering problems, not solved features.
