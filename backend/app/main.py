from fastapi import FastAPI
from sqlalchemy import text

from app.db.session import engine
from app.db.base import Base

from app.models.organization import Organization
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.user_role import UserRole
from app.models.role_permission import RolePermission
from app.models.audit_log import AuditLog
from app.auth.api import router as auth_router

from app.auth.dependencies import (get_current_user)

from fastapi import Depends
app = FastAPI(title="Enterprise AI Decision Intelligence Copilot")
app.include_router(auth_router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db-health")
def db_health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    return {"database": "connected"}

@app.on_event("startup")
def startup():
    print("Application Started")

@app.get("/test-org")
def test_org():
    return {
        "message": "organization endpoint working"
    }



@app.get("/protected")
def protected(
    current_user = Depends(
        get_current_user
    )
):
    return {
        "message": "success",
        "user": current_user.email
    }