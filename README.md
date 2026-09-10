<h1 align="center">VXN-RAMNet</h1>

<p align="center">
  <strong>VisionX Routine Adaptive Memory Network</strong><br>
  A GPS-free visual route-memory research prototype for learning and recognizing a constrained common-path → junction → branch → turnaround → revisit → second-branch pattern.
</p>

<p align="center">
  <img alt="Status" src="https://img.shields.io/badge/status-research%20prototype-blue">
  <img alt="Language" src="https://img.shields.io/badge/language-Python-yellow">
  <img alt="Vision" src="https://img.shields.io/badge/vision-EfficientNetB0-purple">
  <img alt="Interface" src="https://img.shields.io/badge/interface-CLI%20%2F%20Streamlit-success">
  <img alt="Tests" src="https://img.shields.io/badge/tests-pytest-lightgrey">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green">
</p>

<p align="center">
  <a href="#overview">Overview</a> ·
  <a href="#what-this-repo-contains">Contents</a> ·
  <a href="#implemented-pages">Pages</a> ·
  <a href="#features">Features</a> ·
  <a href="#deployment">Deployment</a>
</p>

---

## Overview

**VXN-RAMNet** is an offline research baseline for constrained visual route memory without GPS. It learns and recognizes the traversal pattern:

```text
Common path → Junction → Branch A → Turnaround → Junction revisit → Branch B
```

The immediate objective is reproducible, measurable camera-only research before adding validated IMU fusion, Android streaming, wearable hardware, ultrasonic supervision, or assistive guidance.

---

## What This Repo Contains

| Area | What is included |
|---|---|
| Vision encoder | Frozen EfficientNetB0 embedding adapters and preprocessing. |
| Similarity analysis | Flip-aware self-similarity and numerical comparison utilities. |
| Route memory | Versioned common/junction/branch/backtrack memory representation. |
| Pipeline | Validated input, sampling, segmentation, scoring, artifacts, and reports. |
| Configuration | Reproducible YAML configuration with validation. |
| CLI | Package commands and `scripts/run_pipeline.py` wrapper. |
| Streamlit UI | Optional local research interface. |
| Research assets | Notebooks, protocols, architecture diagrams, and evaluation documentation. |
| Tests | Unit, integration, regression, and reporting tests. |

---

## Implemented Pages

| Page / Entry Point | Purpose |
|---|---|
| `vxn-ramnet validate-config` | Validate an experiment configuration before execution. |
| `vxn-ramnet run` | Run the configured learning/query pipeline. |
| `scripts/run_pipeline.py` | Small command wrapper for pipeline execution. |
| `apps/streamlit_app.py` | Optional local research/demo UI. |
| `configs/camera_baseline.yaml` | Baseline camera-only experiment configuration. |
| `docs/project-status.md` | Implemented/partial/not-started scope boundary. |

---

## Features

| Area | Current Implementation |
|---|---|
| Video input | Validated local video ingestion and deterministic frame sampling. |
| Embeddings | Frozen EfficientNetB0 descriptors for original/flipped frames. |
| Junction analysis | Constrained junction-revisit and turnaround detection. |
| Route segmentation | Common path, junction, Branch A, backtrack, and Branch B memory. |
| Query classification | Multi-window evidence with known/uncertain/unknown decisions. |
| Artifact safety | Safe NPZ/JSON, run-scoped outputs, manifests, logs, and reports. |
| Configuration | Explicit schema/validation for experiment parameters and paths. |
| Testing | Regression protection for the verified Notebook 4 baseline plus unit/integration coverage. |
| Research safeguards | Explicit uncertainty, limitations, evaluation plan, and technical-debt documentation. |

---

## User Flow

```text
Prepare learning/query videos
  ↓
Copy and edit the baseline configuration
  ↓
Validate configuration
  ↓
Run offline route-learning/query pipeline
  ↓
Inspect evidence, classification, reports, and run artifacts
  ↓
Use uncertainty/unknown outcomes rather than forcing a route decision
```

---

## Structure

```text
VXN-RAMNet/
├── apps/
├── assets/architecture/
├── configs/
├── docs/
├── research/
├── scripts/
├── src/vxn_ramnet/
├── tests/
├── pyproject.toml
├── README.md
└── LICENSE
```

---

## Deployment

VXN-RAMNet is primarily a local Python research package rather than a hosted Vercel application.

Recommended environment:

```bash
python -m venv .venv
pip install -e ".[vision,dev]"
ruff check src tests scripts apps
mypy src/vxn_ramnet
pytest
```

Optional local UI:

```bash
pip install -e ".[vision,ui]"
streamlit run apps/streamlit_app.py
```

`.vercelignore` is included only as repository hygiene for accidental Vercel imports; it does not redefine the supported execution model.

---

## Important Notes

- The topology is constrained to one junction and two branches; this is not a general route graph.
- Branch A/B reflect exploration order, not validated physical left/right direction.
- Research thresholds are not calibrated probabilities or safety confidence.
- Processing is offline/post-hoc rather than real-time guidance.
- The bundled regression fixture verifies implementation fidelity, not independent generalization accuracy.
- The cleanup removes the stray one-byte `.github/github` artifact while preserving all research, test, package-marker, safety, and citation files.

---

## License

Released under the MIT License. Use `CITATION.cff` when citing a specific repository revision.
