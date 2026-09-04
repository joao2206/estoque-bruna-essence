from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)

DatabaseSession = Annotated[Session, Depends(get_db)]
BearerCredentials = Annotated[
    HTTPAuthorizationCredentials | None,
    Depends(bearer_scheme),
]


def get_current_user(
    credentials: BearerCredentials,
    database: DatabaseSession,
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise credentials_error

    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        user_id = int(payload.get("sub"))

    except (InvalidTokenError, TypeError, ValueError):
        raise credentials_error

    user = database.get(User, user_id)

    if user is None or not user.active:
        raise credentials_error

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]