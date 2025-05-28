from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request
from fast.internal.dependencies import get_user_service
from fast.internal.service.user import UserService
from fast.internal.models import user as usermodel

class AgreementMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        open_paths = [
            "/agreement/get-mesid",
            "/agreement/update-mesid",
            "/agreement/update",
            "/docs",
            "/openapi.json",
            "/redoc"
        ]

        if any(path in request.url.path for path in open_paths):
            return await call_next(request)

        try:
            userid = request.headers.get("X-User-ID")
            if not userid:
                return JSONResponse(status_code=400, content={"status": "error", "detail": "User ID required"})

            username = request.headers.get("X-Username")
            full_name = request.headers.get("X-Full-Name")

            userid = int(userid)
            user = usermodel.AddUser(userid=userid, username=username, full_name=full_name)

            user_service: UserService = get_user_service(request)

            result = await user_service.init_or_deny(user)
            if result.get("agreement_status") == "need_agreement":
                return JSONResponse(status_code=403, content={"agreement_status": "need_agreement"})

        except Exception as e:
            return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})

        return await call_next(request)