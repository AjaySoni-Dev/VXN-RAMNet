# VXN-RAMNet Source Package

This folder converts the stable `04_backtracking_branch_graph_learning.ipynb` logic into reusable research-grade Python modules.

## Package

```text
src/vxn_ramnet/
├── config.py
├── frame_extraction.py
├── encoder.py
├── similarity.py
├── route_memory.py
├── backtracking_graph.py
├── query_classifier.py
├── reports.py
├── pipeline.py
├── cli.py
└── utils.py
```

## Flow

```text
Learning video + query videos
        ↓
Frame extraction
        ↓
EfficientNetB0 embeddings
        ↓
Original + flipped embeddings
        ↓
Flip-aware self-similarity
        ↓
Junction revisit detection
        ↓
Backtracking graph memory
        ↓
Query branch classification
        ↓
JSON + CSV + Markdown reports
```

This is additive. It does not require deleting or modifying existing notebooks, docs, sample data, or sample results.
