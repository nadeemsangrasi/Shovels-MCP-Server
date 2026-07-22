"""
FastMCP server instance for the Shovels MCP Server.

Initialises the FastMCP server with Stateless Streamable HTTP transport
for exposing Shovels API tools to AI agents.
"""

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server with Stateless Streamable HTTP
mcp = FastMCP(
    name="Shovels MCP Server",
    stateless_http=True,
)
