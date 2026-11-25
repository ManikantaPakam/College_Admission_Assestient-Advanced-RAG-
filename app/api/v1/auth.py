import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.api.schemas.auth import UserLogin, TokenResponse
from app.core.security import verify_password
from app.core.jwt_auth import create_access_token
from app.core.database import get_db
from app.core.jwt_auth import verify_jwt_token
from app.core.security import hash_password
from app.models.user import User
from app.api.schemas.auth import (
    UserRegister,
    UserResponse
)
from datetime import datetime, timedelta, timezone
from app.core.config import JWT_REFRESH_TOKEN_EXPIRE_DAYS
from app.core.refresh_tokens import (
    generate_refresh_token,
    hash_refresh_token
)
from app.models.refresh_token import RefreshToken
from sqlalchemy.exc import SQLAlchemyError
from app.api.schemas.auth import RefreshTokenRequest



logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=TokenResponse
)
def login_user(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):

    # Step 1: Find User
    user = db.scalar(
        select(User).where(
            User.email == str(login_data.email)
        )
    )

    # Step 2: Verify Password
    if user is None or not verify_password(
        login_data.password,
        user.hashed_password
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Step 3: Check User Status
    if not user.is_active:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Step 4: Generate Access Token
    access_token = create_access_token(
        user_id=user.id
    )

    # Step 5: Generate Refresh Token
    refresh_token = generate_refresh_token()

    # Step 6: Hash Refresh Token
    refresh_token_hash = hash_refresh_token(
        refresh_token
    )

    # Step 7: Calculate Expiration
    refresh_token_expiry = (
        datetime.now(timezone.utc)
        + timedelta(days=JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    )

    # Step 8: Create Database Record
    refresh_token_record = RefreshToken(
        user_id=user.id,
        token_hash=refresh_token_hash,
        expires_at=refresh_token_expiry
    )

    try:

        db.add(refresh_token_record)

        db.commit()

    except Exception:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Unable to create refresh token"
        )

    # Step 9: Return Both Tokens
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post(
    "/refresh",
    response_model=TokenResponse
)
def refresh_access_token(
    token_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):

    # Step 1: Hash the received refresh token
    incoming_token_hash = hash_refresh_token(
        token_data.refresh_token
    )

    try:

        # Step 2: Find token and lock its database row
        stored_token = db.scalar(
            select(RefreshToken)
            .where(
                RefreshToken.token_hash == incoming_token_hash
            )
            .with_for_update()
        )

        # Step 3: Validate token existence and revocation
        if stored_token is None or stored_token.revoked_at is not None:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

        # Step 4: Check expiration
        now = datetime.now(timezone.utc)

        if stored_token.expires_at <= now:
            raise HTTPException(
                status_code=401,
                detail="Refresh token has expired"
            )

        # Step 5: Find associated user
        user = db.get(User, stored_token.user_id)

        if user is None or not user.is_active:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

        # Step 6: Revoke old refresh token
        stored_token.revoked_at = now

        # Step 7: Generate new access token
        new_access_token = create_access_token(
            user_id=user.id
        )

        # Step 8: Generate new refresh token
        new_refresh_token = generate_refresh_token()

        new_refresh_token_hash = hash_refresh_token(
            new_refresh_token
        )

        # Step 9: Calculate new expiration
        new_expiry = (
            now + timedelta(
                days=JWT_REFRESH_TOKEN_EXPIRE_DAYS
            )
        )

        # Step 10: Store new refresh token hash
        new_token_record = RefreshToken(
            user_id=user.id,
            token_hash=new_refresh_token_hash,
            expires_at=new_expiry
        )

        db.add(new_token_record)

        # Old token revocation and new token creation
        # are committed in the same transaction.
        db.commit()

        # Step 11: Return new token pair
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )

    except HTTPException:
        db.rollback()
        raise

    except SQLAlchemyError:
        db.rollback()

        logger.exception("Refresh token database operation failed")

        raise HTTPException(
            status_code=500,
            detail="Unable to refresh authentication token"
        )


# --------------------------------
# User Registration API
# --------------------------------

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):

    # Step 1: Check existing email
    existing_email = db.scalar(
        select(User).where(
            User.email == user_data.email
        )
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Step 2: Check existing username
    existing_username = db.scalar(
        select(User).where(
            User.username == user_data.username
        )
    )

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken"
        )

    # Step 3: Hash password
    hashed_password = hash_password(
        user_data.password
    )

    # Step 4: Create User object
    new_user = User(
        username=user_data.username,
        email=str(user_data.email),
        hashed_password=hashed_password,
        role="user",
        is_active=True
    )

    # Step 5: Save user in PostgreSQL
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or username already exists"
        )

    # Step 6: Return user response
    return new_user


# --------------------------------
# Existing JWT Authentication API
# --------------------------------

@router.get("/me")
def get_current_user(
    payload: dict = Depends(verify_jwt_token)
):
    return {
        "message": "Authentication successful",
        "user": payload
    }


@router.post("/logout")
def logout(
    token_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    # Step 1: Hash the incoming refresh token
    incoming_token_hash = hash_refresh_token(
        token_data.refresh_token
    )

    try:
        # Step 2: Find the refresh token in database
        stored_token = db.scalar(
            select(RefreshToken)
            .where(
                RefreshToken.token_hash == incoming_token_hash
            )
            .with_for_update()
        )

        # Step 3: Validate refresh token
        if stored_token is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

        # Step 4: Check whether token is already revoked
        if stored_token.revoked_at is not None:
            raise HTTPException(
                status_code=401,
                detail="Refresh token already revoked"
            )

        # Step 5: Revoke refresh token
        stored_token.revoked_at = datetime.now(timezone.utc)

        # Step 6: Save changes
        db.commit()

        return {
            "message": "Logout successful"
        }

    except HTTPException:
        db.rollback()
        raise

    except SQLAlchemyError:
        db.rollback()

        logger.exception(
            "Logout database operation failed"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to logout"
        )