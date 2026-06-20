import uuid

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.auth.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
)

from app.auth.dependencies import (
    get_current_user,
)

from app.auth.password import (
    hash_password,
    verify_password,
)

from app.auth.jwt import create_access_token

from app.auth.service import get_user_by_email

from app.db.dependencies import get_db

from app.models.user import User


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):

    existing_user = get_user_by_email(
        db,
        request.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists",
        )

    user = User(
        email=request.email,
        hashed_password=hash_password(
            request.password
        ),
        organization_id=uuid.UUID(
            request.organization_id
        ),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User created",
        "user_id": str(user.id),
    }


@router.post("/login",response_model=TokenResponse,)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),):

    user = get_user_by_email(
        db,
        request.email,
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    if not verify_password(
        request.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    token = create_access_token(
        str(user.id)
    )

    return TokenResponse(
        access_token=token,
    )

@router.get("/me")
def me(
    current_user: User = Depends(
        get_current_user
    )
):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "organization_id": str(
            current_user.organization_id
        ),
    }