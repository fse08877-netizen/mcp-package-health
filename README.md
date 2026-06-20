# mcp-package-health

[![CI](https://github.com/fse08877-netizen/mcp-package-health/actions/workflows/ci.yml/badge.svg)](https://github.com/fse08877-netizen/mcp-package-health/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/mcp-package-health)](https://pypi.org/project/mcp-package-health/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)

**An [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server that gives AI agents real-time package health data, vulnerability reports, and dependency graphs — directly inside Claude, Cursor, and any MCP-compatible client.**

---

## Why this exists

Every developer has asked Claude something like *"is this package still maintained?"* or *"does this version have any CVEs?"* — and Claude has to say *"I don't have real-time data."*

`mcp-package-health` fixes that. It exposes three tools that any MCP-compatible AI agent can call live:

| Tool | What it does |
|------|-------------|
| `get_package_health` | Latest version, release date, license, summary from PyPI |
| `check_vulnerabilities` | CVE/vulnerability scan via [OSV.dev](https://osv.dev) |
| `get_dependency_graph` | Direct + transitive dependency list |

---

## Install

```bash
pip install mcp-package-health
```

Or from source:

```bash
git clone https://github.com/fse08877-netizen/mcp-package-health.git
cd mcp-package-health
pip install -e ".[dev]"
```

---

## Usage with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "package-health": {
      "command": "mcp-package-health"
    }
  }
}
```

Then ask Claude:
- *"Is numpy safe to use at version 1.24.0?"*
- *"What are the dependencies of fastapi?"*
- *"When was the last release of httpx?"*

---

## Tool Reference

### `get_package_health(package_name, ecosystem="pypi")`

```json
{
  "name": "requests",
  "version": "2.32.3",
  "summary": "Python HTTP for Humans.",
  "last_release": "2024-05-29T17:05:40",
  "license": "Apache-2.0",
  "project_url": "https://requests.readthedocs.io"
}
```

### `check_vulnerabilities(package_name, version)`

```json
{
  "package": "Pillow",
  "version": "9.0.0",
  "vulnerability_count": 3,
  "vulnerabilities": [
    {
      "id": "GHSA-56pw-mpj4-fxww",
      "summary": "Pillow uninitialized memory",
      "severity": "HIGH"
    }
  ]
}
```

### `get_dependency_graph(package_name)`

```json
{
  "package": "fastapi",
  "direct_dependencies": ["starlette", "pydantic", "typing-extensions"],
  "count": 3
}
```

---

## Development

```bash
pytest tests/ -v
```

---

## License

MIT © [fse08877-netizen](https://github.com/fse08877-netizen/mcp-package-health)
