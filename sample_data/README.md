# Sample Data

This folder is reserved for sample videos or anonymized test data for the VXN-RAMNet research prototype.

VXN-RAMNet uses route videos to test visual route memory, shared-path detection, DTW-based synchronization, and LEFT/RIGHT branch classification.

---

## Purpose of This Folder

The `sample_data/` folder is used for input videos that can be tested with the notebooks.

The current main experiment expects three route videos:

```text
left_route.mp4
right_route.mp4
query_route.mp4
```

These videos are used by the notebook:

```text
notebooks/03_shared_prefix_branch_graph_dtw.ipynb
```

---

## Expected Video Files

| File Name | Purpose |
|---|---|
| `left_route.mp4` | First route video. It starts from the common path and later moves into the LEFT branch. |
| `right_route.mp4` | Second route video. It starts from the same common path and later moves into the RIGHT branch. |
| `query_route.mp4` | Test video. The system tries to classify it as LEFT branch, RIGHT branch, uncertain, or unknown. |

---

## Example Route Meaning

A typical experiment may look like this:

```text
left_route.mp4
College → Common Path → Junction → LEFT branch → Home

right_route.mp4
College → Common Path → Junction → RIGHT branch → Tuition

query_route.mp4
College → Common Path → Junction → either LEFT or RIGHT
```

The system tries to learn this structure:

```text
Common Path
    ↓
Junction
    ├── LEFT Branch
    └── RIGHT Branch
```

---

## Important Privacy Note

Raw personal route videos are not included in this repository by default.

Route videos may contain private or sensitive information such as:

- faces
- vehicle numbers
- home locations
- college locations
- street views
- building names
- personal movement patterns

For this reason, public sample videos should only be added if they are safe to share.

---

## Guidelines for Adding Sample Videos

If you add sample videos to this folder, make sure they are:

- short
- anonymized
- safe for public upload
- free from private faces
- free from addresses or house locations
- free from vehicle number plates
- free from sensitive location details
- recorded only for demonstration or testing

Recommended video length:

```text
20 seconds or less
```

The notebooks use only the first 20 seconds of each video.

---

## How to Use This Folder

Place the videos inside this folder or copy them into a local `videos/` folder before running the notebooks.

Recommended local structure:

```text
VXN-RAMNet/
│
├── sample_data/
│   ├── left_route.mp4
│   ├── right_route.mp4
│   └── query_route.mp4
│
└── notebooks/
    └── 03_shared_prefix_branch_graph_dtw.ipynb
```

Some notebook versions may expect this structure instead:

```text
VXN-RAMNet/
│
├── videos/
│   ├── left_route.mp4
│   ├── right_route.mp4
│   └── query_route.mp4
│
└── notebooks/
    └── 03_shared_prefix_branch_graph_dtw.ipynb
```

If needed, update the video path variables inside the notebook.

---

## Current Notebook Input Names

The main DTW branch graph notebook uses these expected names:

```python
LEFT_ROUTE_VIDEO_NAME = "left_route.mp4"
RIGHT_ROUTE_VIDEO_NAME = "right_route.mp4"
QUERY_ROUTE_VIDEO_NAME = "query_route.mp4"
```

If your files have different names, either rename them or update the notebook variables.

---

## Generated Outputs

When the notebook runs, it can generate output folders and files such as:

```text
vxn_branch_frames_dtw/
vxn_branch_graph_memory_dtw.npz
vxn_branch_graph_metadata_dtw.json
vxn_branch_query_classification_report_dtw.json
```

These are generated experiment outputs.

In most cases, generated frame folders should not be committed to GitHub because they can be large and may contain private visual information.

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
```

Not recommended for public upload:

```text
private route videos
raw personal route recordings
generated frame folders
large extracted image datasets
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

If you decide to upload safe demo videos, remove or modify those rules.

---

## Current Repository Status

At the current stage, this folder is mainly a placeholder for safe sample data.

The main project can still be understood through:

- notebooks
- documentation
- sample results
- JSON reports
- console output samples

Public route videos are optional and should only be included after privacy review.

---

## Disclaimer

The videos used with VXN-RAMNet are for research and experimentation only.

This project is not a certified navigation system, mobility aid, medical device, or safety product.
