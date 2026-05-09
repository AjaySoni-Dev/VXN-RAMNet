# Limitations

This document lists the current limitations of the VXN-RAMNet research prototype.

The goal of this file is to keep the project honest and technically reliable. VXN-RAMNet is currently a notebook-based research prototype, not a production-ready assistive navigation product.

---

## 1. Prototype Status

VXN-RAMNet is currently implemented as a research prototype using Jupyter Notebooks.

Current implementation includes:

- video frame extraction
- EfficientNetB0-based visual embeddings
- route memory creation
- unknown-route learning experiments
- DTW-based shared-prefix branch graph learning
- LEFT/RIGHT branch classification
- JSON and NPZ output generation

Current implementation does not yet include:

- production Android application
- real-time camera pipeline
- certified navigation safety layer
- fully integrated object detection
- large-scale public dataset evaluation
- field-tested assistive deployment

---

## 2. Dataset and Testing Limitations

The current experiments are based on a small number of personally recorded route videos.

This creates several limitations:

- limited route diversity
- limited lighting variation
- limited camera angle variation
- limited walking speed variation
- limited environmental variation
- limited number of query routes
- no large benchmark dataset yet

Because of this, current results should be treated as early experimental evidence, not final proof of reliability.

---

## 3. Route Structure Assumption

The current shared-prefix branch graph experiment assumes a specific route pattern:

```text
Common Path
    ↓
Junction
    ├── LEFT Branch
    └── RIGHT Branch
```

The system currently expects:

```text
left_route.mp4  = common path, then LEFT branch
right_route.mp4 = common path, then RIGHT branch
query_route.mp4 = route to classify
```

This works well for testing the idea, but real environments may include:

- multiple branches
- loops
- stairs
- repeated corridors
- visually similar paths
- curved paths
- overlapping routes
- routes that merge again later

These cases need further testing and architecture refinement.

---

## 4. Branch Direction Limitation

In the current prototype, LEFT and RIGHT branch labels are assigned by video order.

Current rule:

```text
First route after divergence  = LEFT
Second route after divergence = RIGHT
```

The system does not yet infer real physical left or right direction from the camera scene.

This means:

- physical direction is user-defined
- branch labels depend on how videos are provided
- automatic geometric direction understanding is not implemented yet

Future versions may combine visual memory with inertial sensor data, device orientation, optical flow, or visual odometry to estimate direction more automatically.

---

## 5. Visual Embedding Limitations

The current prototype uses EfficientNetB0 as a frozen visual encoder.

This is useful for feature extraction, but it has limitations:

- it was not trained specifically for route navigation
- it may confuse visually similar locations
- lighting changes can reduce similarity accuracy
- motion blur can reduce embedding quality
- large viewpoint changes can affect matching
- seasonal or environmental changes may reduce reliability
- small but important route differences may be missed

The encoder is strong enough for prototype testing, but further model evaluation is needed.

---

## 6. Similar-Looking Branches

If the LEFT and RIGHT branches look very similar, the system may produce weak separation.

Example cases:

- two similar corridors
- similar staircases
- similar building entrances
- repeated wall patterns
- similar road sections
- low-texture environments

In these cases, branch scores may become close and the system may return:

```text
UNCERTAIN_BRANCH
```

This is safer than forcing a wrong prediction, but it shows that more robust evidence collection is needed.

---

## 7. DTW Synchronization Limitations

Dynamic Time Warping-style alignment helps when two videos have different walking speeds or transition timings.

However, DTW may still fail when:

- videos start from different places
- one route has long pauses
- one video has large camera shake
- one video contains missing route sections
- two paths have repetitive visual patterns
- the common path is too short
- the visual encoder produces weak features

DTW improves synchronization, but it does not fully solve all route alignment problems.

---

## 8. Common Path Detection Limitation

The system detects a common path using embedding similarity.

This can fail when:

- the common path is visually inconsistent
- lighting changes heavily between recordings
- camera orientation changes too much
- the user records the same route from different sides
- frames are blurry or occluded
- the common path is too short

Because of this, transition detection should be visually verified using the displayed context frames.

---

## 9. Transition Detection Limitation

The notebook displays:

```text
3 frames before transition
1 transition frame
3 frames after transition
```

This is useful for human verification.

However, the detected transition is still based on similarity thresholds and smoothed similarity drops.

It may be inaccurate if:

- similarity drops too early
- similarity drops too late
- the junction is visually gradual
- the branch starts before the visual scene changes
- the camera turns slowly
- multiple environmental changes happen near the same time

The current transition detection is experimental and should be checked visually.

---

## 10. Query Classification Limitation

The query route classification depends on:

- query video quality
- common-path match
- branch evidence quality
- LEFT/RIGHT branch score gap
- embedding separation

The system may misclassify if:

- the query video starts late
- the query video misses the common path
- the query branch is recorded from a different angle
- the route is partially blocked
- the query route contains unusual motion
- the query branch looks similar to the other branch

The strong branch override helps when branch evidence is clear, but it can also be risky if branch memory is not diverse enough.

---

## 11. Unknown Route Learning Limitation

Unknown-route learning is currently experimental.

The system can save unknown route frames and generate new memory, but several issues remain:

- deciding when a route is truly unknown
- avoiding duplicate memory for the same route
- merging similar routes
- naming new routes
- connecting unknown routes into an existing graph
- verifying new route quality
- preventing noisy memory growth

Future versions need better memory management and graph update logic.

---

## 12. Object Detection Integration Limitation

Object detection is described as a planned safety layer.

It is not yet fully integrated into the current VXN-RAMNet branch graph pipeline.

Current route-memory experiments focus mainly on:

- visual route embeddings
- route matching
- DTW alignment
- branch classification

Future object detection integration will need:

- lightweight object detector
- mobile-compatible inference
- object tracking
- risk scoring
- warning priority logic
- anti-spam voice output

---

## 13. Real-Time Limitation

The current implementation is notebook-based and not optimized for real-time deployment.

The target is:

```text
Route / branch recognition: 2-3 FPS
Object detection: 1-2 FPS
Camera preview: 10-15 FPS
```

However, the notebook workflow includes:

- plotting
- displaying frames
- reading images from disk
- running full batch inference
- saving intermediate files

These are useful for research but not suitable for real-time mobile deployment.

A production-style version would require:

- CameraX or live camera pipeline
- TFLite / LiteRT model conversion
- optimized memory search
- preloaded embeddings
- background processing
- careful frame scheduling

---

## 14. Mobile Deployment Limitation

The architecture is mobile-implementable, but the current repo version is not an Android app.

Android implementation would require:

- Kotlin or Java app structure
- CameraX frame analysis
- TensorFlow Lite model
- local memory storage
- optimized embedding comparison
- background threading
- TextToSpeech
- haptic feedback
- battery and thermal testing

The current notebooks are a research base for this future work.

---

## 15. Privacy Limitation

Route videos may contain sensitive information such as:

- faces
- houses
- vehicle numbers
- road signs
- college buildings
- personal movement patterns
- location context

For this reason, raw personal videos and extracted frame folders should not be uploaded publicly unless anonymized.

The repository should include only safe sample data or placeholder instructions.

---

## 16. Safety Limitation

VXN-RAMNet is not a certified navigation, medical, or mobility-assistance product.

It should not be used as the only source of navigation or safety guidance.

Current outputs are experimental and may be wrong.

The system requires:

- more testing
- safety validation
- failure handling
- user studies
- accessibility review
- real-world evaluation

before any assistive deployment.

---

## 17. Summary

The current VXN-RAMNet prototype demonstrates a promising research direction:

```text
visual route memory
+ DTW synchronization
+ branch graph learning
+ uncertainty-aware classification
```

However, the system is still early-stage and needs more validation before it can be considered reliable for real-world assistive use.

The limitations in this document should be treated as active research challenges, not final failures.
