"""
Run the stable VXN-RAMNet notebook-4 logic as a modular production pipeline.

Example:
python scripts/run_backtracking_pipeline.py \
  --learning-video videos/backtracking_learning_route.mp4 \
  --query-videos videos/query_route_1.mp4 videos/query_route_2.mp4
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from vxn_ramnet.cli import main  # noqa: E402


if __name__ == "__main__":
    main()
