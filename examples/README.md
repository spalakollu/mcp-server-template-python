# Examples

## Portfolio Service workflow

Mock domain example: read, write, and destructive tools.

1. Start the server (from repo root):
   ```bash
   python -m server.main
   ```
2. In another terminal, run the workflow:
   ```bash
   python examples/portfolio_workflow.py
   ```

Optional env vars:
- `MCP_BASE_URL` – server URL (default: http://127.0.0.1:8000)
- `MCP_API_KEY` – API key (optional if server has none configured)
