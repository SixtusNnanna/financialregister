from typing import Annotated
from collections.abc import Callable
from uuid import UUID

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database.models import User, Role
from app.database.session import get_db


def get_current_user(
        request: Request,
        db: Annotated[Session, Depends(get_db)]
):
    user_id = request.session.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=303,
            headers={"Location": "/login"}
        )
    user_uuid = UUID(user_id)
    user = db.get(User, user_uuid)
    if user is None:
        raise HTTPException(
            status_code=303,
            headers={"Location": "/login"}
        )
    return user


def require_roles(*allowed_roles: Role) -> Callable:
    def role_checker(
        user: Annotated[User, Depends(get_current_user)],
    ) -> User:

        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this page.",
            )

        return user
    return role_checker
