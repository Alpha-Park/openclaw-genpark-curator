# -*- coding: utf-8 -*-
from client import OpenClawGenParkCurator

def main():
    curator = OpenClawGenParkCurator(num_perm=32)
    print("=== OpenClaw GenPark Curator & Deduplicator ===")

    doc1 = "Autonomous AI agents require robust cryptographic signatures and low latency tool calling."
    doc2 = "Autonomous AI agents require robust cryptographic signatures and very low latency tool calling."
    doc3 = "Completely unrelated text discussing culinary recipes and baking sourdough bread."

    sig1 = curator.compute_minhash(doc1)
    sig2 = curator.compute_minhash(doc2)
    sig3 = curator.compute_minhash(doc3)

    sim12 = curator.estimate_jaccard_similarity(sig1, sig2)
    sim13 = curator.estimate_jaccard_similarity(sig1, sig3)

    print(f"Similarity (Doc1 vs Near-Duplicate Doc2): {sim12 * 100:.1f}%")
    print(f"Similarity (Doc1 vs Unrelated Doc3):      {sim13 * 100:.1f}%")

    qual = curator.evaluate_quality(doc1)
    print(f"Content Quality Score: {qual['quality_score']} (Usable={qual['is_usable']})")

if __name__ == "__main__":
    main()
