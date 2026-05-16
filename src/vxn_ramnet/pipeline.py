from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .backtracking_graph import BacktrackingGraphLearner
from .config import BacktrackingPipelineConfig
from .encoder import encode_backtracking_inputs
from .frame_extraction import extract_backtracking_frames
from .query_classifier import BacktrackingQueryClassifier
from .reports import write_final_reports
from .utils import setup_logger


@dataclass
class PipelineResult:
    frame_report_path: str
    embeddings_file: str
    graph_memory_file: str
    graph_metadata_file: str
    final_summary: Dict


class BacktrackingPipeline:
    """
    End-to-end production-grade pipeline for notebook-4 logic.

    User flow:
    1. Put learning/query videos in videos/ or pass paths through config.
    2. Run this pipeline.
    3. Open output_dir/vxn_backtracking_report.md or final JSON/CSV.
    """

    def __init__(self, config: BacktrackingPipelineConfig):
        self.config = config
        self.logger = setup_logger()

    def run(self) -> PipelineResult:
        """Run full backtracking graph pipeline."""
        self.logger.info("Stage 1/5: extracting frames")
        extracted = extract_backtracking_frames(self.config)
        self.logger.info("Frame extraction report: %s", extracted.report_path)

        self.logger.info("Stage 2/5: generating EfficientNetB0 embeddings")
        embedding_result = encode_backtracking_inputs(self.config)
        self.logger.info("Embeddings file: %s", embedding_result.embeddings_file)

        self.logger.info("Stage 3/5: learning backtracking branch graph")
        learner = BacktrackingGraphLearner(self.config)
        graph_result = learner.learn_from_embeddings(embedding_result.embeddings_file)
        self.logger.info("Graph memory: %s", graph_result.graph_memory_file)

        self.logger.info("Stage 4/5: classifying query routes")
        classifier = BacktrackingQueryClassifier(self.config)
        query_result = classifier.classify_all()
        self.logger.info("Query summary: %s", query_result.summary_file)

        self.logger.info("Stage 5/5: writing final JSON/CSV/Markdown reports")
        final_summary = write_final_reports(self.config, query_result.reports)

        self.logger.info("Pipeline complete. Open: %s", final_summary["report_files"]["markdown"])

        return PipelineResult(
            frame_report_path=str(extracted.report_path),
            embeddings_file=str(embedding_result.embeddings_file),
            graph_memory_file=str(graph_result.graph_memory_file),
            graph_metadata_file=str(graph_result.graph_metadata_file),
            final_summary=final_summary,
        )


def run_backtracking_pipeline(config: BacktrackingPipelineConfig | None = None) -> PipelineResult:
    """Convenience function."""
    return BacktrackingPipeline(config or BacktrackingPipelineConfig()).run()
