from mcp.server import FastMCP

mcp = FastMCP(name="MCP Server",
              stateless_http=False)

# SERVER TOOLS
@mcp.tool()
def test_tool(sub: str, whole: str) -> bool:
    """
    test function that checks if sub is in whole
    """
    return sub in whole

mcp.run(transport="streamable-http")