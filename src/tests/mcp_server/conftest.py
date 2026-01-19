from __future__ import annotations

import sys
from pathlib import Path


def pytest_configure():
    repo_root = Path(__file__).resolve().parents[2]
    mcp_root = (
        repo_root
        / "Multi-Agent-Custom-Automation-Engine-Solution-Accelerator"
        / "src"
        / "mcp_server"
    )
    if mcp_root.exists() and str(mcp_root) not in sys.path:
        sys.path.insert(0, str(mcp_root))
