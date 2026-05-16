# VXN-RAMNet Configs

This folder contains configuration and dependency files for the modular stable Notebook 4 pipeline.

## Files

```text
backtracking_default.json.example
requirements-src.txt
requirements-ui.txt
```

## Why .json.example?

The existing repository `.gitignore` ignores generic `.json` files. Using `.json.example` keeps the config visible on GitHub while still being valid JSON content for the pipeline.

You can run it directly:

```bash
python scripts/run_backtracking_pipeline.py --config configs/backtracking_default.json.example
```

Or copy it locally:

```bash
copy configs/backtracking_default.json.example configs/backtracking_default.local.json
```

Then edit the local copy for your videos and output folder.
