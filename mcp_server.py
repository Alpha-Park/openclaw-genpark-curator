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

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            res = run_tool(req.get("name"), req.get("arguments", {}))
            print(json.dumps({"jsonrpc": "2.0", "id": req.get("id"), "result": res}))
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}))
        sys.stdout.flush()

if __name__ == "__main__":
    main()
