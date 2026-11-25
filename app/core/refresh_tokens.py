import secrets
import hashlib


# Generate Secure Refresh Token
def generate_refresh_token() -> str:

    return secrets.token_urlsafe(48)


# Hash Refresh Token
def hash_refresh_token(token: str) -> str:

    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()