[![Tests](https://github.com/spalakollu/mcp-server-template-python/actions/workflows/tests.yml/badge.svg)](https://github.com/spalakollu/mcp-server-template-python/actions/workflows/tests.yml)

License: MIT

# MCP Server Template - Python

## Overview
Production-ready MCP server template for safely exposing tools to AI agents.  
Includes tool registration, permissions, logging, error handling, and example workflows.

## What This Repo Is NOT
- Not a framework for creating domain logic
- Not a ready-to-run trading or financial system

## Features
- Tool categories: Read / Write / Destructive
- Scoped permissions & authentication stub
- Standardized error handling
- Logging and observability hooks
- Dockerized for easy deployment
- Example workflows using a mock domain

## Getting Started
1. Clone the repo
2. Install dependencies
   ```bash
   pip install -r requirements.txt  # Python
   # npm install                    # TypeScript
   ```
3. Run the server
   ```bash
   python -m server.main
   ```
4. (Optional) Run example workflows from `examples/`
5. (Optional) Run with Docker
   ```bash
   docker build -t mcp-server-template .
   docker run mcp-server-template
   ```

## Structure
- **server/** – Server code and entrypoint
  - **tools/** – MCP tools (read, write, destructive)
  - **permissions/** – Permission definitions
  - **errors/** – Error types and handlers
- **examples/** – Usage examples and mock-domain workflows
- **tests/** – Test suite
