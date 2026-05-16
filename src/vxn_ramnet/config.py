from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Tuple
import json


@dataclass
class BacktrackingPipelineConfig:
    """
    Configuration for the stable backtracking branch-graph pipeline.

    This config mirrors the working notebook-4 defaults, but keeps them
    centralized so research experiments can be repeated and tuned safely.
    """

    root_dir: Path = Path(".")
    videos_dir: Path = Path("videos")
    output_dir: Path = Path("vxn_backtracking_graph_outputs")

    learning_video_name: str = "backtracking_learning_route.mp4"
    query_video_names: List[str] = field(
        default_factory=lambda: ["query_route_1.mp4", "query_route_2.mp4"]
    )

    learning_max_seconds: int = 45
    query_max_seconds: int = 20
    learning_frame_count: int = 270
    query_frame_count: int = 120

    first_branch_name: str = "LEFT_BRANCH"
    second_branch_name: str = "RIGHT_BRANCH"

    model_input_size: Tuple[int, int] = (224, 224)
    batch_size: int = 16

    video_extensions: Tuple[str, ...] = (".mp4", ".mov", ".avi", ".mkv", ".webm")
    image_extensions: Tuple[str, ...] = (".jpg", ".jpeg", ".png", ".webp", ".bmp")

    # Graph detection settings copied from the stable notebook logic.
    first_junction_search: Tuple[float, float] = (0.12, 0.48)
    return_junction_search: Tuple[float, float] = (0.48, 0.86)
    junction_window: int = 5
    junction_memory_radius: int = 6
    min_junction_gap_ratio: float = 0.18

    good_junction_score: float = 0.70
    acceptable_junction_score: float = 0.56
    good_backtrack_score: float = 0.56
    acceptable_backtrack_score: float = 0.42

    # Query classifier thresholds copied from the stable notebook logic.
    min_branch_score: float = 0.58
    min_branch_gap: float = 0.040
    strong_branch_score: float = 0.72
    strong_branch_gap: float = 0.070
    unknown_score: float = 0.54

    save_self_similarity_matrix: bool = True
    clean_output_dir: bool = True

    @classmethod
    def from_json(cls, path: str | Path) -> "BacktrackingPipelineConfig":
        """Load config from JSON."""
        path = Path(path)
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BacktrackingPipelineConfig":
        """Create config from a dictionary while converting path/tuple fields."""
        converted = dict(data)

        for key in ["root_dir", "videos_dir", "output_dir"]:
            if key in converted:
                converted[key] = Path(converted[key])

        tuple_fields = [
            "model_input_size",
            "video_extensions",
            "image_extensions",
            "first_junction_search",
            "return_junction_search",
        ]

        for key in tuple_fields:
            if key in converted and isinstance(converted[key], list):
                converted[key] = tuple(converted[key])

        return cls(**converted)

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to a JSON-serializable dictionary."""
        data = asdict(self)
        for key in ["root_dir", "videos_dir", "output_dir"]:
            data[key] = str(data[key])
        return data

    def save_json(self, path: str | Path) -> None:
        """Save config to JSON."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")

    @property
    def resolved_videos_dir(self) -> Path:
        return self.root_dir / self.videos_dir

    @property
    def resolved_output_dir(self) -> Path:
        return self.root_dir / self.output_dir
