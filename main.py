from fastmcp import fastmcp
import sys, traceback, io

server = fastmcp("sandbox")

@server.tool()
def run_python_code(code: str) -> str:
    try:
        buf = io.StringIO()
        sys.stdout = buf
        exec(code, {"__builtins__": __builtins__})
        sys.stdout = sys.__stdout__
        return buf.getvalue()
    except Exception as e:
        return traceback.format_exc()

@server.tool()
def fetch_url(url: str) -> str:
    import httpx
    r = httpx.get(url, timeout=8)
    return r.text[:5000]

if __name__ == "__main__":
    server.run(transport="sse", host="0.0.0.0", port=8080)
