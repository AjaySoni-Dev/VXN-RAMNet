from __future__ import annotations

from typing import List, Tuple
import numpy as np


def max_similarity_matrix(A: np.ndarray, AF: np.ndarray, B: np.ndarray, BF: np.ndarray) -> np.ndarray:
    """
    Flip-aware maximum cosine similarity matrix.

    A  = original embeddings of sequence A
    AF = flipped embeddings of sequence A
    B  = original embeddings of sequence B
    BF = flipped embeddings of sequence B
    """
    sims = [
        A @ B.T,
        AF @ B.T,
        A @ BF.T,
        AF @ BF.T,
    ]
    return np.maximum.reduce(sims)


def moving_average(x: np.ndarray, window: int = 7) -> np.ndarray:
    """Centered moving average with edge padding."""
    x = np.asarray(x, dtype=np.float32)

    if len(x) < window:
        return x

    pad = window // 2
    padded = np.pad(x, (pad, pad), mode="edge")
    return np.convolve(padded, np.ones(window) / window, mode="valid")


def safe_range(start: int, end: int, total: int) -> List[int]:
    """Inclusive integer range clipped to [0, total - 1]."""
    start = max(0, int(start))
    end = min(total - 1, int(end))

    if end < start:
        end = start

    return list(range(start, end + 1))


def segment_centroid(emb: np.ndarray, embedding_dim: int | None = None) -> np.ndarray:
    """Return normalized centroid for a segment embedding matrix."""
    if len(emb) == 0:
        if embedding_dim is None:
            raise ValueError("embedding_dim is required when segment is empty.")
        return np.zeros((embedding_dim,), dtype=np.float32)

    c = np.mean(emb, axis=0, keepdims=True)
    norm = np.linalg.norm(c, axis=1, keepdims=True)
    norm[norm == 0] = 1.0
    return (c / norm)[0].astype(np.float32)


def window_similarity_score(S: np.ndarray, i: int, j: int, radius: int = 5) -> Tuple[float, float, float]:
    """
    Score whether a local window around i matches a local window around j.

    Returns:
    max(same_order_score, reverse_order_score), same_order_score, reverse_order_score
    """
    offsets = list(range(-radius, radius + 1))
    same_order_scores = []
    reverse_order_scores = []

    for d in offsets:
        i1 = i + d
        j_same = j + d
        j_rev = j - d

        if 0 <= i1 < S.shape[0] and 0 <= j_same < S.shape[1]:
            same_order_scores.append(S[i1, j_same])

        if 0 <= i1 < S.shape[0] and 0 <= j_rev < S.shape[1]:
            reverse_order_scores.append(S[i1, j_rev])

    same_score = float(np.mean(same_order_scores)) if same_order_scores else -1.0
    reverse_score = float(np.mean(reverse_order_scores)) if reverse_order_scores else -1.0

    return max(same_score, reverse_score), same_score, reverse_score


def component_score(
    q_emb: np.ndarray,
    q_flip: np.ndarray,
    mem_emb: np.ndarray,
    mem_flip: np.ndarray,
    centroid: np.ndarray,
) -> Tuple[float, np.ndarray]:
    """
    Score query evidence against one memory component.

    Mirrors notebook-4 scoring:
    0.50 best frame match + 0.30 top-3 mean + 0.20 centroid similarity.
    """
    if len(q_emb) == 0 or len(mem_emb) == 0:
        return 0.0, np.array([], dtype=np.float32)

    sim = max_similarity_matrix(q_emb, q_flip, mem_emb, mem_flip)

    best = np.max(sim, axis=1)

    top3 = []
    for row in sim:
        r = np.sort(row)[::-1]
        top3.append(np.mean(r[:min(3, len(r))]))

    top3 = np.array(top3, dtype=np.float32)

    c = centroid.reshape(1, -1)
    centroid_score = np.maximum(
        (q_emb @ c.T).reshape(-1),
        (q_flip @ c.T).reshape(-1),
    )

    per_frame = (
        0.50 * best
        + 0.30 * top3
        + 0.20 * centroid_score
    )

    return float(np.mean(per_frame)), per_frame.astype(np.float32)
