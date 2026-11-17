# -*- coding: utf-8 -*-
import sys, json
from client import OpenClawGenParkCurator

curator = OpenClawGenParkCurator()

def run_tool(name, args):
    if name == "compute_minhash":
        txt = args.get("text", "")
        return {"minhash_signature": curator.compute_minhash(txt)}
    elif name == "estimate_similarity":
        s1 = args.get("signature_a", [])
        s2 = args.get("signature_b", [])
        return {"estimated_jaccard": curator.estimate_jaccard_similarity(s1, s2)}
    elif name == "evaluate_quality":
        txt = args.get("text", "")
        return curator.evaluate_quality(txt)
    else:
        raise ValueError(f"Unknown tool: {name}")

from typing import Any, Dict, List, Optional

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:
    raise SystemExit("MCP requires the mcp package. Run: python -m pip install -r requirements.txt") from exc

mcp = FastMCP('openclaw-genpark-curator')

@mcp.tool()
def compute_minhash(text: str = "") -> str:
    """Compute the MinHash signature of supplied text."""
    return json.dumps(run_tool('compute_minhash', {'text': text}))

@mcp.tool()
def estimate_similarity(signature_a: Optional[List[int]] = None, signature_b: Optional[List[int]] = None) -> str:
    """Estimate the similarity of two MinHash signatures."""
    return json.dumps(run_tool('estimate_similarity', {'signature_a': signature_a if signature_a is not None else [], 'signature_b': signature_b if signature_b is not None else []}))

@mcp.tool()
def evaluate_quality(text: str = "") -> str:
    """Evaluate the quality of supplied text."""
    return json.dumps(run_tool('evaluate_quality', {'text': text}))

def main():
    if "--test" in sys.argv:
        print("[TEST] Running OpenClaw Curator Self-Test...")
        t1 = "OpenClaw GenPark agent framework provides high performance autonomous tools."
        t2 = "OpenClaw GenPark agent framework provides high performance autonomous tools for developers."
        s1 = curator.compute_minhash(t1)
        s2 = curator.compute_minhash(t2)
        sim = curator.estimate_jaccard_similarity(s1, s2)
        assert sim >= 0.2
        q = curator.evaluate_quality(t1)
        assert q["is_usable"] is True or False
        print("[TEST] All tests passed successfully!")
        return

    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
