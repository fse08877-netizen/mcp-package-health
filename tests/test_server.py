"""Unit tests for mcp-package-health — no mcp dependency needed."""
import pytest
from mcp_package_health.server import (
    get_package_health,
    check_vulnerabilities,
    get_dependency_graph,
)


@pytest.mark.asyncio
async def test_get_package_health_requests():
    result = await get_package_health("requests")
    assert result["name"].lower() == "requests"
    assert "version" in result
    assert "last_release" in result
    assert "license" in result


@pytest.mark.asyncio
async def test_check_vulnerabilities_returns_dict():
    result = await check_vulnerabilities("requests", "2.31.0")
    assert "vulnerability_count" in result
    assert isinstance(result["vulnerabilities"], list)
    assert "package" in result


@pytest.mark.asyncio
async def test_get_dependency_graph():
    result = await get_dependency_graph("requests")
    assert "direct_dependencies" in result
    assert isinstance(result["direct_dependencies"], list)
    assert result["count"] >= 0


@pytest.mark.asyncio
async def test_unsupported_ecosystem_raises():
    with pytest.raises(ValueError, match="Unsupported ecosystem"):
        await get_package_health("lodash", ecosystem="npm")
