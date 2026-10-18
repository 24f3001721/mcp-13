import hashlib

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_request

mcp = FastMCP("Exam Challenge Server")

NORMALIZED_EMAIL = "24f3001721@ds.study.iitm.ac.in"


@mcp.tool(name="solve_challenge")
def solve_challenge() -> str:
    """Return the challenge hash from the current HTTP request headers."""

    request = get_http_request()
    challenge = request.headers.get("X-Exam-Challenge", "")

    if len(challenge) != 32:
        raise ValueError("Invalid X-Exam-Challenge header")

    if any(c not in "0123456789abcdef" for c in challenge):
        raise ValueError("Challenge must be lowercase hexadecimal")

    message = f"{challenge}:{NORMALIZED_EMAIL}"
    digest = hashlib.sha256(message.encode("utf-8")).hexdigest()

    return digest[:16]


app = mcp.http_app(path="/mcp")
