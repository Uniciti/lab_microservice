# app/models/user.py
from pydantic import BaseModel
from typing import Optional
import sqlalchemy

class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str
    active: Optional[bool] = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    active: Optional[bool] = None

def get_user_table(metadata):
    return sqlalchemy.Table(
        "users",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("username", sqlalchemy.String, unique=True),
        sqlalchemy.Column("email", sqlalchemy.String, unique=True),
        sqlalchemy.Column("full_name", sqlalchemy.String),
        sqlalchemy.Column("active", sqlalchemy.Boolean, default=True),
    )