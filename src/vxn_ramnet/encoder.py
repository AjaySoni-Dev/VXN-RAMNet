from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple
import time

import numpy as np
from PIL import Image, ImageOps

from .config import BacktrackingPipelineConfig
from .frame_extraction import collect_frames
from .utils import to_posix


def l2_normalize_matrix(x: np.ndarray) -> np.ndarray:
    """L2-normalize rows of a matrix."""
    x = np.asarray(x, dtype=np.float32)
    norms = np.linalg.norm(x, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return x / norms


@dataclass
class EmbeddingResult:
    embeddings_file: Path
    learning_embeddings_shape: Tuple[int, int]
    query_names: List[str]
    timing: Dict


class EfficientNetB0Encoder:
    """
    Frozen EfficientNetB0 visual encoder.

    TensorFlow imports are intentionally delayed until initialization so that
    other package modules can be imported without requiring TensorFlow to load.
    """

    def __init__(self, config: BacktrackingPipelineConfig):
        self.config = config
        self.model_input_size = tuple(config.model_input_size)
        self.batch_size = int(config.batch_size)

        try:
            import tensorflow as tf  # noqa: F401
            from tensorflow.keras.applications import EfficientNetB0
            from tensorflow.keras.applications.efficientnet import preprocess_input
            from tensorflow.keras.preprocessing import image as keras_image
        except ImportError as exc:
            raise ImportError(
                "TensorFlow is required for EfficientNetB0 embedding generation. "
                "Install dependencies with: pip install -r requirements.txt"
            ) from exc

        self._preprocess_input = preprocess_input
        self._keras_image = keras_image

        self.model = EfficientNetB0(
            input_shape=(224, 224, 3),
            include_top=False,
            weights="imagenet",
            pooling="avg",
        )
        self.model.trainable = False

        dummy = np.zeros((1, 224, 224, 3), dtype=np.float32)
        _ = self.model.predict(dummy, verbose=0)

    def load_image_array(self, img_path: str | Path, flip: bool = False) -> np.ndarray:
        """Load and preprocess one image into a raw array before model preprocessing."""
        img = Image.open(img_path).convert("RGB")
        img = ImageOps.exif_transpose(img)

        if flip:
            img = ImageOps.mirror(img)

        img = img.resize(self.model_input_size)
        return self._keras_image.img_to_array(img)

    def encode_frames(
        self,
        frame_paths: List[Path],
        label: str,
        flip: bool = False,
    ) -> Tuple[np.ndarray, np.ndarray, Dict]:
        """Encode frame paths into L2-normalized embeddings."""
        embeddings = []
        paths = []
        start_time = time.time()

        for start in range(0, len(frame_paths), self.batch_size):
            batch_paths = frame_paths[start:start + self.batch_size]
            batch = [self.load_image_array(p, flip=flip) for p in batch_paths]
            batch = np.asarray(batch, dtype=np.float32)
            batch = self._preprocess_input(batch)

            emb = self.model.predict(batch, verbose=0).astype(np.float32)
            emb = l2_normalize_matrix(emb)

            embeddings.append(emb)
            paths.extend([to_posix(p) for p in batch_paths])

        if not embeddings:
            raise ValueError(f"No frames were provided for encoding: {label}")

        matrix = np.vstack(embeddings).astype(np.float32)
        elapsed = time.time() - start_time

        timing = {
            "label": label,
            "frame_count": len(frame_paths),
            "elapsed_seconds": elapsed,
            "avg_ms_per_frame": (elapsed / max(1, len(frame_paths))) * 1000,
        }

        return matrix, np.asarray(paths), timing


def encode_backtracking_inputs(config: BacktrackingPipelineConfig) -> EmbeddingResult:
    """
    Encode learning frames and query frames exactly like notebook 4.

    Saves:
    output_dir/vxn_backtracking_embeddings.npz
    """
    output_dir = config.resolved_output_dir
    frames_dir = output_dir / "frames"
    learning_frames_dir = frames_dir / "learning"
    query_frames_root = frames_dir / "queries"

    if not learning_frames_dir.exists():
        raise FileNotFoundError("Learning frames missing. Run frame extraction first.")

    learning_frames = collect_frames(learning_frames_dir, config.image_extensions)
    query_folders = sorted([p for p in query_frames_root.iterdir() if p.is_dir()])
    query_frames_map = {
        folder.name: collect_frames(folder, config.image_extensions)
        for folder in query_folders
    }

    encoder = EfficientNetB0Encoder(config)
    timing: Dict[str, Dict] = {}

    learning_embeddings, learning_paths, t = encoder.encode_frames(
        learning_frames,
        "LEARNING_ORIGINAL",
        flip=False,
    )
    timing["learning_original"] = t

    learning_embeddings_flip, _, t = encoder.encode_frames(
        learning_frames,
        "LEARNING_FLIPPED",
        flip=True,
    )
    timing["learning_flipped"] = t

    query_embedding_dict = {}
    query_embedding_flip_dict = {}
    query_path_dict = {}

    for query_name, frames in query_frames_map.items():
        q_emb, q_paths, t = encoder.encode_frames(
            frames,
            f"{query_name}_ORIGINAL",
            flip=False,
        )
        timing[f"{query_name}_original"] = t

        q_flip, _, t = encoder.encode_frames(
            frames,
            f"{query_name}_FLIPPED",
            flip=True,
        )
        timing[f"{query_name}_flipped"] = t

        query_embedding_dict[query_name] = q_emb
        query_embedding_flip_dict[query_name] = q_flip
        query_path_dict[query_name] = q_paths

    save_dict = {
        "learning_embeddings": learning_embeddings,
        "learning_embeddings_flip": learning_embeddings_flip,
        "learning_frame_paths": learning_paths,
        "query_names": np.array(list(query_embedding_dict.keys())),
    }

    for query_name in query_embedding_dict:
        save_dict[f"query_embeddings__{query_name}"] = query_embedding_dict[query_name]
        save_dict[f"query_embeddings_flip__{query_name}"] = query_embedding_flip_dict[query_name]
        save_dict[f"query_frame_paths__{query_name}"] = query_path_dict[query_name]

    embeddings_file = output_dir / "vxn_backtracking_embeddings.npz"
    np.savez_compressed(embeddings_file, **save_dict)

    return EmbeddingResult(
        embeddings_file=embeddings_file,
        learning_embeddings_shape=learning_embeddings.shape,
        query_names=list(query_embedding_dict.keys()),
        timing=timing,
    )
