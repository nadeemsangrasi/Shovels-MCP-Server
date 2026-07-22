"""
FastMCP server instance for the Shovels MCP Server.

Initialises the FastMCP server with Stateless Streamable HTTP transport
for exposing Shovels API tools to AI agents.
"""

from mcp.server.fastmcp import FastMCP
from mcp.server.streamable_http import TransportSecuritySettings

# Initialize FastMCP server with Stateless Streamable HTTP
# DNS rebinding protection is disabled for Render + Cloudflare compatibility.
# Render forwards requests with their own Host header, which would otherwise
# be rejected by the default security middleware.
mcp = FastMCP(
    name="Shovels MCP Server",
    stateless_http=True,
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)
