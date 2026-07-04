from fastmcp import FastMCP
import sys, traceback, io

mcp = FastMCP("SandboxMCP")

@mcp.tool()
def run_python_code(code: str) -> str:
    """安全执行Python代码沙箱"""
    try:
        buf = io.StringIO()
        sys.stdout = buf
        exec(code, {"__builtins__": __builtins__})
        sys.stdout = sys.__stdout__
        return buf.getvalue()
    except Exception as e:
        return traceback.format_exc()

@mcp.tool()
def fetch_url(url: str) -> str:
    """读取网页内容"""
    import httpx
    r = httpx.get(url, timeout=8)
    return r.text[:5000]

if __name__ == "__main__":
    # Wasmer只认sse，不认streamable-http
    mcp.run(transport="sse", host="0.0.0.0", port=8080)
