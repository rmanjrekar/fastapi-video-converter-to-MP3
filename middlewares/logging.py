from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"[LOG] {request.method} {request.url}")
        response = await call_next(request)
        print(f"[LOG] Response status: {response.status_code}")
        return response
