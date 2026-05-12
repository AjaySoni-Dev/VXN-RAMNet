# Future Work

This document lists the actual future work required to make VXN-RAMNet more reliable, testable, and closer to practical use.

The goal is not to overstate the project. The current repo is a notebook-based research prototype. Future work should focus on measurable improvements, better evaluation, cleaner code, and realistic deployment steps.

---

## 1. Create a Proper Evaluation Dataset

The first major future task is to test the system on more route videos.

Needed data:

- multiple root paths
- multiple junctions
- multiple left/right branch examples
- multiple backtracking videos
- query videos recorded on different days
- indoor and outdoor videos
- low-light videos
- shaky videos
- similar-looking branches
- unknown-route videos
- failure-case videos

Without a larger dataset, the system cannot claim general reliability.

---

## 2. Build an Evaluation Notebook

Add a notebook such as:

```text
notebooks/05_evaluation_summary.ipynb
```

It should measure:

| Metric | Why It Matters |
|---|---|
| Branch classification accuracy | Checks LEFT/RIGHT or first/second branch correctness |
| Unknown-route detection rate | Checks whether unseen routes are rejected |
| False unknown rate | Checks whether known routes are wrongly rejected |
| Transition detection error | Checks junction/divergence accuracy |
| Query evidence window quality | Checks whether branch frames are selected correctly |
| Average inference time | Measures speed |
| Failure cases | Shows where the system breaks |

The output should be a table, not only printed text.

---

## 3. Improve Backtracking Detection

The new backtracking notebook works experimentally, but it needs stronger validation.

Future improvements:

- better junction revisit detection
- better turnaround detection
- confidence score for each detected segment
- support for longer videos
- support for multiple backtracking points
- failure detection when junction cannot be found
- visual warning when detection confidence is low
- optional manual correction for detected junction frames

The system should not silently accept a wrong junction split.

---

## 4. Add Semi-Automatic Correction Mode

Fully automatic graph learning may fail in some videos.

A practical next step is semi-automatic correction.

Example:

```text
Detected first junction: frame 60
Detected return junction: frame 193
Detected turnaround: frame 134

User can accept or edit these values.
```

This would make experiments more reliable while automatic detection is still improving.

---

## 5. Improve Query Evidence Selection

The latest notebook improved query classification by selecting later branch windows.

Future improvements:

- compare multiple branch windows
- score branch-window stability
- reject windows that still look like common path
- use vote-based prediction across windows
- store selected evidence frames in reports
- add confidence labels such as HIGH, MEDIUM, LOW
- detect when query video does not contain enough branch evidence

This is important because wrong evidence selection can make the classifier look correct or incorrect for the wrong reason.

---

## 6. Improve Uncertainty Handling

The current uncertainty logic is threshold-based.

Future uncertainty handling should include:

- multi-window voting
- branch score stability
- confidence calibration
- repeated-frame evidence
- uncertain-state report
- automatic fallback when scores are close
- clear reason for uncertainty

Example output:

```json
{
  "prediction": "UNCERTAIN_BRANCH",
  "reason": "Branch scores are too close across multiple evidence windows",
  "left_votes": 4,
  "right_votes": 5,
  "branch_gap": 0.018
}
```

This should be implemented before using the system in any serious navigation setting.

---

## 7. Improve Unknown Route Handling

Unknown-route learning should become graph-aware.

Needed improvements:

- detect truly unknown routes more reliably
- prevent duplicate route memory
- attach unknown routes to nearest known graph node
- ask user to label new route
- create new branch memory only after confirmation
- validate memory quality before saving
- keep memory version history
- remove noisy or low-confidence memory

Future graph-aware unknown route flow:

```text
Unknown branch detected
    ↓
Save candidate route
    ↓
Verify with repeated evidence
    ↓
Ask user for label
    ↓
Attach to graph
    ↓
Re-test next time
```

---

## 8. Modularize Notebook Code

The current implementation is mostly inside notebooks.

Next engineering step:

```text
src/
├── frame_extraction.py
├── embedding_encoder.py
├── route_memory.py
├── dtw_alignment.py
├── backtracking_graph.py
├── query_classifier.py
├── evaluation.py
└── utils.py
```

This will make the project easier to test, reuse, and maintain.

The notebooks should become experiment runners, not the only place where logic exists.

---

## 9. Add a Command-Line Demo

After modularization, add:

```text
run_demo.py
```

Example command:

```bash
python run_demo.py --learning sample_data/backtracking_learning_route.mp4 --query sample_data/query_route_1.mp4
```

Expected output:

```text
Prediction: RIGHT_BRANCH
First branch score: ...
Second branch score: ...
Branch gap: ...
Report saved: ...
```

This will make the repo easier to run without opening notebooks.

---

## 10. Improve Memory Management

Current memory storage is simple.

Future work should include:

- keyframe selection
- duplicate frame removal
- low-quality frame filtering
- memory compression
- centroid-based retrieval
- approximate nearest neighbor search
- route versioning
- memory confidence scoring
- memory cleanup tools

As the number of routes grows, simple full-frame storage may become inefficient.

---

## 11. Expand Graph Support

Current graph learning is limited to simple branch structures.

Future graph support should include:

- more than two branches
- nested junctions
- route loops
- merged paths
- dead ends
- repeated corridors
- branch re-entry
- destination labels
- graph search
- graph consistency checks

A future graph may look like:

```text
Root
  ↓
Junction_A
  ├── Branch_1
  ├── Branch_2
  └── Branch_3
        ↓
      Junction_B
        ├── Branch_3A
        └── Branch_3B
```

This is a larger research task and should not be treated as already solved.

---

## 12. Add Destination-Aware Wrong-Branch Detection

Current query classification can predict a branch, but destination-aware navigation is not implemented yet.

Future logic:

```text
selected_destination = "Home"
expected_branch = "LEFT_BRANCH"
detected_branch = "RIGHT_BRANCH"

if detected_branch != expected_branch:
    state = "WRONG_BRANCH"
```

This should be implemented as a separate decision layer, not mixed directly into embedding similarity code.

---

## 13. Add Object Detection as a Separate Safety Layer

Object detection should be added separately from route memory.

First version should test:

- object detection on extracted frames
- bounding boxes
- confidence scores
- left/center/right object zones
- simple danger labels

Possible models:

- YOLOv8n TFLite
- MobileNet-SSD
- EfficientDet-Lite

This should be tested in a separate notebook before integration.

Suggested notebook:

```text
notebooks/06_object_safety_layer.ipynb
```

---

## 14. Add Motion or Tracking

Object detection does not need to run on every frame.

Future tracking options:

- centroid tracking
- optical flow
- bounding-box tracking
- object movement estimation
- approaching-object detection

Tracking can reduce compute cost and improve object warning consistency.

---

## 15. Build a Basic Risk Engine

A future risk engine should combine route and safety signals.

Inputs:

- branch prediction
- branch confidence
- unknown-route state
- uncertain-route state
- wrong-branch state
- object detection output
- object position zone
- object motion

Possible outputs:

```text
SAFE
CAUTION
HIGH_RISK
CRITICAL_STOP
```

The risk engine must prioritize safety over route guidance.

---

## 16. Add Guidance Engine

Guidance is not currently implemented.

Future work should include:

- text instruction generation
- TextToSpeech output
- haptic feedback
- message cooldown
- critical alert override
- wrong-branch warning
- uncertain-route warning
- obstacle warning

Example messages:

```text
Route uncertain. Slow down.
Wrong branch detected. Return to the junction.
Obstacle ahead. Move carefully.
Stop. Obstacle ahead.
```

This should be tested carefully because bad guidance can be dangerous.

---

## 17. Prepare for Real-Time Processing

The current system is offline and notebook-based.

Future real-time work should include:

- live frame capture
- frame scheduler
- route recognition at controlled intervals
- object detection at lower FPS
- preloaded graph memory
- no plotting during runtime
- no disk-based frame extraction
- optimized vector similarity search

Target design:

| Component | Target |
|---|---|
| Camera preview | 10-15 FPS |
| Route recognition | 2-3 FPS |
| Object detection | 1-2 FPS |
| Risk engine | 2-5 FPS |
| Guidance | Event-based |

These targets still need practical testing.

---

## 18. Convert Encoder to TFLite / LiteRT

The current notebooks use TensorFlow/Keras.

Future deployment should test:

- TFLite conversion
- float16 quantization
- int8 quantization if possible
- GPU delegate
- NNAPI delegate
- mobile latency
- memory usage
- accuracy difference after conversion

This should be measured, not assumed.

---

## 19. Android Prototype

Android work should come after the notebook and Python prototype are more stable.

Required parts:

- CameraX frame analyzer
- TFLite visual encoder
- local memory storage
- query classification loop
- object safety layer
- risk engine
- TextToSpeech
- haptic feedback
- learning mode UI
- navigation mode UI

This should be built step-by-step, not all at once.

---

## 20. Improve Documentation

Documentation should stay honest and synced with implementation.

Needed docs:

- implementation status
- notebook walkthrough
- output file explanation
- sample results explanation
- privacy guide
- troubleshooting guide
- Android deployment plan
- evaluation results summary

Documentation should clearly separate:

```text
implemented
experimental
planned
not implemented
```

---

## 21. Add Reproducibility Notes

Future repo updates should include:

- exact notebook execution order
- input file naming rules
- expected output files
- sample console outputs
- result interpretation
- known failure cases
- hardware used for testing
- approximate runtime

This will make the project easier to verify.

---

## 22. Possible Research Questions

Future research can focus on:

1. Can visual route memory reliably recognize repeated personal routes?
2. How much viewpoint change can embedding memory tolerate?
3. How accurate is DTW-based common-path detection?
4. How accurate is self-similarity-based backtracking detection?
5. What encoder works best for mobile route memory?
6. How should unknown routes be added without memory pollution?
7. Can branch graph memory support wrong-turn detection?
8. Can route memory and object detection run together on mobile hardware?
9. How often does the system fail in similar-looking environments?
10. How should uncertainty be communicated safely to users?

---

## 23. Suggested Roadmap

### Version 0.2

Current upgrade direction:

- backtracking branch graph learning
- multi-query classification
- sample output reports
- updated documentation

### Version 0.3

Next realistic upgrade:

- modular Python code
- evaluation notebook
- better uncertainty reports
- semi-automatic correction mode

### Version 0.4

Graph and decision upgrade:

- graph-aware unknown route handling
- destination-aware wrong-branch detection
- better graph memory structure

### Version 0.5

Safety upgrade:

- object detection notebook
- simple risk engine
- early guidance rules

### Version 0.6

Mobile preparation:

- TFLite encoder test
- frame scheduler design
- Android deployment plan

---

## 24. Final Direction

The future goal is to gradually move from:

```text
notebook-based visual route experiments
```

toward:

```text
tested visual route memory system
```

and eventually:

```text
mobile assistive navigation prototype
```

The next steps should focus on testing, measurement, modularization, and safety. The project should not claim production readiness until those stages are actually implemented and validated.
