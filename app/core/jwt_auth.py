import jwt
import logging

from pathlib import Path
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import (
    JWT_ALGORITHM,
    JWT_ISSUER,
    JWT_AUDIENCE,
    JWT_PRIVATE_KEY_PATH,
    JWT_PUBLIC_KEY_PATH,
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES
)

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)


# Get Private Key
def get_private_key():

    private_key_path = Path(JWT_PRIVATE_KEY_PATH)

    if not private_key_path.exists():
        raise RuntimeError("JWT private key file not found")

    return private_key_path.read_text()


# Get Public Key
def get_public_key():

    public_key_path = Path(JWT_PUBLIC_KEY_PATH)

    if not public_key_path.exists():
        raise RuntimeError("JWT public key file not found")

    return public_key_path.read_text()


# Generate JWT Access Token
def create_access_token(user_id: int):

    private_key = get_private_key()

    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
        "iat": now,
        "exp": now + timedelta(
            minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
    }

    token = jwt.encode(
        payload,
        private_key,
        algorithm=JWT_ALGORITHM
    )

    return token


# Verify JWT Access Token
def verify_jwt_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )

    token = credentials.credentials

    try:

        public_key = get_public_key()

        payload = jwt.decode(
            token,
            public_key,
            algorithms=[JWT_ALGORITHM],
            issuer=JWT_ISSUER,
            audience=JWT_AUDIENCE,
            options={
                "require": ["exp", "iss", "aud", "sub"]
            }
        )

        return payload

    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )

    except jwt.InvalidTokenError:

        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token"
        )