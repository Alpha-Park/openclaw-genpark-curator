---
name: openclaw-genpark-curator
description: Personalized aesthetic intelligence. Maps human preference vectors directly to verified manufacturer inventories, bypassing social commerce noise.
---
# openclaw-genpark-curator

Personalized aesthetic intelligence. Maps human preference vectors directly to verified manufacturer inventories, bypassing social commerce noise.

## MCP runtime requirements

The standard-library-only policy applies to direct `client.py` use. Running `mcp_server.py` requires Python 3.10+ and the official `mcp` SDK (`mcp>=1.0.0,<2`) from `requirements.txt`. Install it into your chosen environment from the repository checkout:

```bash
python -m pip install -r requirements.txt
```

Configure the MCP client with that environment's absolute Python executable path and the absolute path to `mcp_server.py`. The client launches a local STDIO process; a GitHub URL is not a remote MCP endpoint.
