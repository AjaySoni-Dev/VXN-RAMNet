# Sample Data

This folder is reserved for sample videos or anonymized test data for the VXN-RAMNet research prototype.

VXN-RAMNet uses route videos to test:

- visual route memory
- shared-path detection
- DTW-based synchronization
- LEFT/RIGHT branch classification
- one-video backtracking branch graph learning

Raw personal route videos are not included by default for privacy reasons.

---

## Purpose of This Folder

The `sample_data/` folder is used for optional input videos that can be tested with the notebooks.

The repository can be understood without public videos because it already includes:

- notebooks
- documentation
- sample results
- JSON reports
- console output samples

If videos are added later, they should be short, anonymized, and safe for public sharing.

---

## Supported Notebook Experiments

### 1. Two-Video Shared-Prefix DTW Experiment

Notebook:

```text
notebooks/03_shared_prefix_branch_graph_dtw.ipynb
```

Expected video files:

```text
left_route.mp4
right_route.mp4
query_route.mp4
```

Meaning:

| File Name | Purpose |
|---|---|
| `left_route.mp4` | First route video. It starts from the common path and later moves into the LEFT branch. |
| `right_route.mp4` | Second route video. It starts from the same common path and later moves into the RIGHT branch. |
| `query_route.mp4` | Test route video. The system tries to classify it as LEFT, RIGHT, uncertain, or unknown. |

Example route structure:

```text
left_route.mp4
College → Common Path → Junction → LEFT branch → Home

right_route.mp4
College → Common Path → Junction → RIGHT branch → Tuition

query_route.mp4
College → Common Path → Junction → either LEFT or RIGHT
```

The notebook tries to learn:

```text
Common Path
    ↓
Junction
    ├── LEFT Branch
    └── RIGHT Branch
```

---

### 2. One-Video Backtracking Branch Graph Experiment

Notebook:

```text
notebooks/04_backtracking_branch_graph_learning.ipynb
```

Expected video files:

```text
backtracking_learning_route.mp4
query_route_1.mp4
query_route_2.mp4
```

Meaning:

| File Name | Purpose |
|---|---|
| `backtracking_learning_route.mp4` | One learning video where the user goes from root to junction, takes the first branch, backtracks to the junction, and then takes the second branch. |
| `query_route_1.mp4` | First query route video to classify. |
| `query_route_2.mp4` | Second query route video to classify. |

Example learning route:

```text
backtracking_learning_route.mp4
College → Junction → First Branch → Backtrack → Junction → Second Branch
```

The notebook tries to learn:

```text
Root / College
    ↓
Common Path
    ↓
Junction
    ├── First Branch
    └── Second Branch
```

Important note:

In the backtracking experiment, branch names are assigned by exploration order.

```text
First branch visited before backtracking  = first branch memory
Second branch visited after backtracking  = second branch memory
```

If your recording order is different, update the branch label variables inside the notebook.

---

## Recommended Folder Usage

You can place videos directly inside `sample_data/`:

```text
VXN-RAMNet/
│
├── sample_data/
│   ├── left_route.mp4
│   ├── right_route.mp4
│   ├── query_route.mp4
│   ├── backtracking_learning_route.mp4
│   ├── query_route_1.mp4
│   └── query_route_2.mp4
│
└── notebooks/
    ├── 03_shared_prefix_branch_graph_dtw.ipynb
    └── 04_backtracking_branch_graph_learning.ipynb
```

Some notebook versions may expect videos inside a local `videos/` folder:

```text
VXN-RAMNet/
│
├── videos/
│   ├── left_route.mp4
│   ├── right_route.mp4
│   ├── query_route.mp4
│   ├── backtracking_learning_route.mp4
│   ├── query_route_1.mp4
│   └── query_route_2.mp4
│
└── notebooks/
    ├── 03_shared_prefix_branch_graph_dtw.ipynb
    └── 04_backtracking_branch_graph_learning.ipynb
```

If needed, update the video path variables inside the notebook.

---

## Current Notebook Input Names

### For `03_shared_prefix_branch_graph_dtw.ipynb`

```python
LEFT_ROUTE_VIDEO_NAME = "left_route.mp4"
RIGHT_ROUTE_VIDEO_NAME = "right_route.mp4"
QUERY_ROUTE_VIDEO_NAME = "query_route.mp4"
```

### For `04_backtracking_branch_graph_learning.ipynb`

```python
LEARNING_VIDEO_NAME = "backtracking_learning_route.mp4"

QUERY_VIDEO_NAMES = [
    "query_route_1.mp4",
    "query_route_2.mp4",
]
```

If your files have different names, either rename the files or update the notebook variables.

---

## Video Recording Guidelines

For better results, record videos carefully.

Recommended practices:

- walk slowly
- keep the camera stable
- avoid sudden turns
- avoid heavy blur
- record in good lighting
- keep the camera facing forward as much as possible
- pause briefly near important junctions
- avoid recording faces, number plates, or private places

For the backtracking experiment, the learning video should follow this structure:

```text
start/root
    ↓
junction
    ↓
first branch
    ↓
backtrack to junction
    ↓
second branch
```

Recommended learning video length:

```text
45 seconds or less
```

Recommended query video length:

```text
20 seconds or less
```

The notebooks use only the configured duration from each video.

---

## Important Privacy Note

Raw personal route videos may contain sensitive information such as:

- faces
- vehicle numbers
- home locations
- college locations
- street views
- building names
- personal movement patterns
- private route patterns

For this reason, raw personal videos are not included in this repository by default.

Only upload videos if they are safe for public sharing.

---

## Guidelines for Adding Public Sample Videos

If you add sample videos to this folder, make sure they are:

- short
- anonymized
- safe for public upload
- free from private faces
- free from addresses or house locations
- free from vehicle number plates
- free from sensitive location details
- recorded only for demonstration or testing

Do not upload private real route videos unless they have been reviewed and are safe to share.

---

## Generated Outputs

When the notebooks run, they may generate output folders and files.

### Outputs from `03_shared_prefix_branch_graph_dtw.ipynb`

```text
vxn_branch_frames_dtw/
vxn_branch_graph_memory_dtw.npz
vxn_branch_graph_metadata_dtw.json
vxn_branch_query_classification_report_dtw.json
```

### Outputs from `04_backtracking_branch_graph_learning.ipynb`

```text
vxn_backtracking_graph_outputs/
├── frames/
├── frame_extraction_report.json
├── vxn_backtracking_embeddings.npz
├── vxn_backtracking_graph_memory.npz
├── vxn_backtracking_graph_metadata.json
├── query_reports/
├── vxn_backtracking_all_query_summary.json
└── vxn_backtracking_final_summary.json
```

These are generated experiment outputs.

Generated frame folders should usually not be committed to GitHub because they can be large and may contain private visual information.

---

## What Should Be Uploaded

Safe to upload:

```text
sample_data/README.md
```

Optional, only if privacy-safe:

```text
sample_data/left_route.mp4
sample_data/right_route.mp4
sample_data/query_route.mp4
sample_data/backtracking_learning_route.mp4
sample_data/query_route_1.mp4
sample_data/query_route_2.mp4
```

Not recommended for public upload:

```text
private route videos
raw personal route recordings
generated frame folders
large extracted image datasets
video files showing faces, homes, number plates, or private locations
```

---

## Recommended `.gitignore` Rules

If you do not want to upload videos publicly, add this to `.gitignore`:

```text
sample_data/*.mp4
sample_data/*.mov
sample_data/*.avi
sample_data/*.mkv
videos/
raw_videos/
```

Also ignore generated experiment outputs:

```text
vxn_branch_frames_dtw/
vxn_backtracking_graph_outputs/
extracted_frames/
vxn_extracted_frames/
```

If you decide to upload safe demo videos, remove or modify the video ignore rules.

---

## Current Repository Status

At the current stage, this folder is mainly a placeholder for safe sample data.

The main project can still be understood through:

- notebooks
- documentation
- sample results
- JSON reports
- console output samples
- research notes

Public route videos are optional and should only be included after privacy review.

---

## Disclaimer

The videos used with VXN-RAMNet are for research and experimentation only.

This project is not a certified navigation system, mobility aid, medical device, or safety product.
