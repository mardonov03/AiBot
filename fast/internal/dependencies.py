from fast.internal.service.user import UserService
from fast.internal.service.agreement import AgreementService
from fast.internal.service.ai import AiService
from fastapi.security import OAuth2PasswordBearer
from fastapi import Request

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

def get_user_service(request: Request) -> UserService:
    return UserService(request.app.state.pool, request.app.state.redis_pool)

def get_agreement_service(request: Request) -> AgreementService:
    return AgreementService(request.app.state.pool)

def get_ai_service(request: Request) -> AiService:
    return AiService(request.app.state.pool)