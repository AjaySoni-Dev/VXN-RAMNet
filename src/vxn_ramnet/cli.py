from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from .config import BacktrackingPipelineConfig
from .pipeline import BacktrackingPipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run VXN-RAMNet stable backtracking branch-graph pipeline."
    )

    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Optional JSON config path. CLI arguments override config values.",
    )
    parser.add_argument("--root-dir", type=str, default=None)
    parser.add_argument("--videos-dir", type=str, default=None)
    parser.add_argument("--output-dir", type=str, default=None)

    parser.add_argument(
        "--learning-video",
        type=str,
        default=None,
        help="Learning video: root -> junction -> first branch -> backtrack -> junction -> second branch.",
    )
    parser.add_argument(
        "--query-videos",
        nargs="+",
        default=None,
        help="One or more query videos to classify.",
    )

    parser.add_argument("--first-branch-name", type=str, default=None)
    parser.add_argument("--second-branch-name", type=str, default=None)

    parser.add_argument("--learning-frame-count", type=int, default=None)
    parser.add_argument("--query-frame-count", type=int, default=None)
    parser.add_argument("--learning-max-seconds", type=int, default=None)
    parser.add_argument("--query-max-seconds", type=int, default=None)

    return parser


def apply_overrides(config: BacktrackingPipelineConfig, args: argparse.Namespace) -> BacktrackingPipelineConfig:
    if args.root_dir is not None:
        config.root_dir = Path(args.root_dir)
    if args.videos_dir is not None:
        config.videos_dir = Path(args.videos_dir)
    if args.output_dir is not None:
        config.output_dir = Path(args.output_dir)

    if args.learning_video is not None:
        config.learning_video_name = args.learning_video
    if args.query_videos is not None:
        config.query_video_names = list(args.query_videos)

    if args.first_branch_name is not None:
        config.first_branch_name = args.first_branch_name
    if args.second_branch_name is not None:
        config.second_branch_name = args.second_branch_name

    if args.learning_frame_count is not None:
        config.learning_frame_count = args.learning_frame_count
    if args.query_frame_count is not None:
        config.query_frame_count = args.query_frame_count
    if args.learning_max_seconds is not None:
        config.learning_max_seconds = args.learning_max_seconds
    if args.query_max_seconds is not None:
        config.query_max_seconds = args.query_max_seconds

    return config


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.config:
        config = BacktrackingPipelineConfig.from_json(args.config)
    else:
        config = BacktrackingPipelineConfig()

    config = apply_overrides(config, args)

    result = BacktrackingPipeline(config).run()
    print("\nDone.")
    print("Markdown report:", result.final_summary["report_files"]["markdown"])
    print("JSON summary:", result.final_summary["report_files"]["json"])
    print("CSV results:", result.final_summary["report_files"]["csv"])


if __name__ == "__main__":
    main()
