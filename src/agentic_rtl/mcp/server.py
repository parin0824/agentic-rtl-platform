from __future__ import annotations

from pathlib import Path

from agentic_rtl.core.security import WorkspacePolicy
from agentic_rtl.tools.eda import EdaTools


def create_server(workspace: Path):
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:
        raise RuntimeError("Install the MCP extra with: pip install -e '.[mcp]'") from exc

    root = workspace.resolve()
    policy = WorkspacePolicy(root)
    tools = EdaTools(root)
    server = FastMCP("agentic-rtl-tools")

    @server.tool()
    def read_text(relative_path: str) -> str:
        return policy.resolve_read(relative_path).read_text(encoding="utf-8")

    @server.tool()
    def run_rtl_lint(relative_path: str, top_module: str) -> dict:
        path = policy.resolve_read(relative_path)
        return tools.lint(path, top_module).model_dump()

    @server.tool()
    def run_synthesis_check(relative_path: str, top_module: str) -> dict:
        path = policy.resolve_read(relative_path)
        return tools.synthesize(path, top_module).model_dump()

    @server.tool()
    def run_cocotb_regression(relative_directory: str, seed: int = 1) -> dict:
        path = policy.resolve_read(relative_directory)
        return tools.regression(path, seed).model_dump()

    @server.tool()
    def write_generated_file(relative_path: str, content: str) -> str:
        path = policy.resolve_write(relative_path, ("workspaces", "reports/generated"))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return str(path.relative_to(root))

    return server


def main() -> None:
    create_server(Path.cwd()).run()


if __name__ == "__main__":
    main()
