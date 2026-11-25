from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Registration Request
class UserRegister(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128
    )


# Registration Response
class UserResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

# Login Request
class UserLogin(BaseModel):

    email: EmailStr

    password: str = Field(
        min_length=1,
        max_length=128
    )


# JWT Token Response
class TokenResponse(BaseModel):

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):

    refresh_token: str = Field(
        min_length=1,
        max_length=500
    )