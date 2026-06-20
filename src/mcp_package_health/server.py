"""MCP server: package health, vulnerability scan, and dependency graph."""
import httpx

try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("mcp-package-health")
    _MCP_AVAILABLE = True
except ImportError:
    mcp = None
    _MCP_AVAILABLE = False


async def get_package_health(package_name: str, ecosystem: str = "pypi") -> dict:
    """Return health metrics for a package: latest version, release age, license."""
    ecosystem = ecosystem.lower()
    if ecosystem == "pypi":
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"https://pypi.org/pypi/{package_name}/json")
            r.raise_for_status()
            data = r.json()
        info = data["info"]
        releases = data["releases"]
        latest = info["version"]
        release_dates = [
            f["upload_time"]
            for f in releases.get(latest, [])
            if f.get("upload_time")
        ]
        last_release = max(release_dates) if release_dates else "unknown"
        return {
            "name": info["name"],
            "version": latest,
            "summary": info["summary"],
            "last_release": last_release,
            "license": info.get("license", "unknown"),
            "project_url": info.get("project_url") or info.get("home_page", ""),
        }
    raise ValueError(f"Unsupported ecosystem: {ecosystem}. Supported: pypi")


async def check_vulnerabilities(package_name: str, version: str) -> dict:
    """Query OSV.dev for known CVEs / vulnerabilities for a given package+version."""
    payload = {"version": version, "package": {"name": package_name, "ecosystem": "PyPI"}}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post("https://api.osv.dev/v1/query", json=payload)
        r.raise_for_status()
        data = r.json()
    vulns = data.get("vulns", [])
    return {
        "package": package_name,
        "version": version,
        "vulnerability_count": len(vulns),
        "vulnerabilities": [
            {
                "id": v["id"],
                "summary": v.get("summary", ""),
                "severity": v.get("database_specific", {}).get("severity", "UNKNOWN"),
            }
            for v in vulns[:10]
        ],
    }


async def get_dependency_graph(package_name: str) -> dict:
    """Return direct dependencies for a PyPI package."""
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"https://pypi.org/pypi/{package_name}/json")
        r.raise_for_status()
        data = r.json()
    requires = data["info"].get("requires_dist") or []
    direct = []
    for req in requires:
        name = req.split(";")[0].split()[0].split(">=")[0].split("<=")[0].split("==")[0].strip()
        if name:
            direct.append(name)
    return {
        "package": package_name,
        "direct_dependencies": direct,
        "count": len(direct),
    }


# register tools only if mcp is available
if _MCP_AVAILABLE:
    mcp.tool()(get_package_health)
    mcp.tool()(check_vulnerabilities)
    mcp.tool()(get_dependency_graph)


if __name__ == "__main__":
    if _MCP_AVAILABLE:
        mcp.run()
    else:
        print("Install mcp: pip install mcp-package-health[mcp]")
