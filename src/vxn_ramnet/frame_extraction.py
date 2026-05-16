from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List
import shutil
import time

import cv2
import numpy as np

from .config import BacktrackingPipelineConfig
from .utils import ensure_dir, to_posix, write_json


@dataclass
class ExtractedFrames:
    learning_dir: Path
    query_dirs: Dict[str, Path]
    report_path: Path
    report: Dict


def find_video(video_name: str, config: BacktrackingPipelineConfig) -> Path:
    """
    Find a video in the standard research locations.

    Search order:
    1. configured videos_dir
    2. root_dir
    3. /mnt/data for notebook/cloud-upload compatibility
    4. direct path supplied by user
    """
    direct = Path(video_name)
    candidates = [
        config.resolved_videos_dir / video_name,
        config.root_dir / video_name,
        Path("/mnt/data") / video_name,
        direct,
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError(
        f"Could not find video '{video_name}'. Place it in {config.resolved_videos_dir}, "
        f"{config.root_dir}, /mnt/data, or pass an absolute path."
    )


def get_video_info(video_path: str | Path) -> Dict:
    """Read FPS, total frame count, and duration from a video."""
    video_path = Path(video_path)
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    fps = float(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if fps <= 0:
        fps = 30.0

    duration = float(total_frames / fps) if fps > 0 else 0.0
    cap.release()

    return {
        "fps": fps,
        "total_frames": total_frames,
        "duration_seconds": duration,
    }


def extract_evenly_spaced_frames(
    video_path: str | Path,
    output_folder: str | Path,
    frame_count: int,
    max_seconds: int | float,
) -> Dict:
    """
    Extract evenly spaced frames from the first max_seconds of a video.

    This function directly mirrors the stable notebook-4 extraction behavior.
    """
    video_path = Path(video_path)
    output_folder = ensure_dir(output_folder)

    info = get_video_info(video_path)

    fps = info["fps"]
    total_frames = info["total_frames"]
    duration = info["duration_seconds"]

    usable_seconds = min(duration, float(max_seconds))
    usable_frame_count = int(usable_seconds * fps)
    usable_frame_count = min(usable_frame_count, total_frames)

    if usable_frame_count <= 0:
        raise ValueError(f"No usable frames found in video: {video_path}")

    frame_indices = np.linspace(
        0,
        usable_frame_count - 1,
        int(frame_count),
        dtype=int,
    )

    cap = cv2.VideoCapture(str(video_path))
    saved_paths: List[str] = []

    for out_idx, frame_idx in enumerate(frame_indices, start=1):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(frame_idx))
        success, frame = cap.read()

        if not success:
            continue

        output_path = output_folder / f"frame_{out_idx:03d}.jpg"
        cv2.imwrite(str(output_path), frame)
        saved_paths.append(to_posix(output_path))

    cap.release()

    return {
        "video_path": to_posix(video_path),
        "fps": fps,
        "original_duration_seconds": duration,
        "used_duration_seconds": usable_seconds,
        "original_total_frames": total_frames,
        "used_frame_count": usable_frame_count,
        "requested_frames": int(frame_count),
        "saved_frames": len(saved_paths),
        "output_folder": to_posix(output_folder),
        "frame_paths": saved_paths,
    }


def extract_backtracking_frames(config: BacktrackingPipelineConfig) -> ExtractedFrames:
    """
    Extract learning and query frames for the backtracking graph pipeline.

    Output layout:
    output_dir/frames/learning
    output_dir/frames/queries/<query_name>
    """
    output_dir = config.resolved_output_dir

    if config.clean_output_dir and output_dir.exists():
        shutil.rmtree(output_dir)

    frames_dir = ensure_dir(output_dir / "frames")
    learning_dir = ensure_dir(frames_dir / "learning")
    query_root = ensure_dir(frames_dir / "queries")

    learning_video_path = find_video(config.learning_video_name, config)
    query_video_paths = [find_video(name, config) for name in config.query_video_names]

    report = {
        "system": "VXN-RAMNet",
        "mode": "backtracking_branch_graph_learning",
        "stage": "frame_extraction",
        "learning_video": config.learning_video_name,
        "query_videos": config.query_video_names,
        "learning_max_seconds": config.learning_max_seconds,
        "query_max_seconds": config.query_max_seconds,
        "learning_frame_count": config.learning_frame_count,
        "query_frame_count": config.query_frame_count,
        "created_at_unix": time.time(),
        "videos": {},
    }

    report["videos"]["learning"] = extract_evenly_spaced_frames(
        learning_video_path,
        learning_dir,
        config.learning_frame_count,
        config.learning_max_seconds,
    )

    query_dirs: Dict[str, Path] = {}

    for query_path in query_video_paths:
        query_name = Path(query_path).stem
        query_folder = ensure_dir(query_root / query_name)
        query_dirs[query_name] = query_folder

        report["videos"][query_name] = extract_evenly_spaced_frames(
            query_path,
            query_folder,
            config.query_frame_count,
            config.query_max_seconds,
        )

    report_path = output_dir / "frame_extraction_report.json"
    write_json(report_path, report)

    return ExtractedFrames(
        learning_dir=learning_dir,
        query_dirs=query_dirs,
        report_path=report_path,
        report=report,
    )


def collect_frames(folder: str | Path, extensions: Iterable[str]) -> List[Path]:
    """Collect image frames from a folder in sorted order."""
    folder = Path(folder)
    ext = {e.lower() for e in extensions}
    return sorted([p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in ext])
