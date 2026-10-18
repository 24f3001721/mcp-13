import hashlib
import os
from fastmcp import FastMCP
from starlette.requests import Request

mcp = FastMCP("Exam Challenge Server")

NORMALIZED_EMAIL = "24f3001721@ds.study.iitm.ac.in"


@mcp.tool()
def solve_challenge() -> str:
    """Solve the current exam challenge using its HTTP request headers."""
    request = mcp.get_context().get_http_request()

    challenge = request.headers.get("X-Exam-Challenge", "")

    if len(challenge) != 32:
        raise ValueError("Missing or invalid challenge header")

    if any(c not in "0123456789abcdef" for c in challenge):
        raise ValueError("Challenge must be lowercase hexadecimal")

    value = f"{challenge}:{NORMALIZED_EMAIL}"
    result = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]

    return result


app = mcp.http_app(path="/mcp")
