# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Curator
Standard Library only: hashlib, typing.
High-throughput MinHash Locality-Sensitive Hashing (LSH) near-duplicate detector
and dataset content quality evaluator.
"""

import hashlib
from typing import Dict, List, Set, Any

class OpenClawGenParkCurator:
    def __init__(self, num_perm: int = 16):
        self.num_perm = num_perm

    def _get_shingles(self, text: str, k: int = 3) -> Set[str]:
        words = text.lower().split()
        if len(words) < k:
            return set(words)
        return set(" ".join(words[i:i+k]) for i in range(len(words) - k + 1))

    def compute_minhash(self, text: str) -> List[int]:
        """
        Computes deterministic MinHash signature vector of length num_perm.
        """
        shingles = self._get_shingles(text)
        if not shingles:
            return [0] * self.num_perm

        signature = []
        for seed in range(self.num_perm):
            min_val = float('inf')
            for s in shingles:
                h = int(hashlib.md5(f"{seed}:{s}".encode("utf-8")).hexdigest()[:8], 16)
                if h < min_val:
                    min_val = h
            signature.append(int(min_val))

        return signature

    def estimate_jaccard_similarity(self, sig1: List[int], sig2: List[int]) -> float:
        """
        Estimates Jaccard similarity as fraction of matching MinHash values.
        """
        if len(sig1) != len(sig2) or not sig1:
            return 0.0
        matches = sum(1 for a, b in zip(sig1, sig2) if a == b)
        return round(matches / len(sig1), 4)

    def evaluate_quality(self, text: str) -> Dict[str, Any]:
        """
        Evaluates lexical diversity, length, and format quality.
        """
        words = text.split()
        n = len(words)
        if n == 0:
            return {"quality_score": 0.0, "is_usable": False}

        unique_ratio = len(set(words)) / n
        avg_word_len = sum(len(w) for w in words) / n

        # High quality criteria: adequate length, good lexical diversity
        score = 0.0
        if 20 <= n <= 2000: score += 0.4
        elif n > 10: score += 0.2

        if unique_ratio >= 0.5: score += 0.4
        elif unique_ratio >= 0.3: score += 0.2

        if 3.5 <= avg_word_len <= 8.5: score += 0.2

        score = min(1.0, round(score, 3))

        return {
            "quality_score": score,
            "is_usable": score >= 0.6,
            "word_count": n,
            "lexical_diversity": round(unique_ratio, 3),
            "avg_word_length": round(avg_word_len, 2)
        }
