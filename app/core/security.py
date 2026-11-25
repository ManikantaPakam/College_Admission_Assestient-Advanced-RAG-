from pwdlib import PasswordHash


# Initialize Argon2 password hasher
password_hash = PasswordHash.recommended()


# Hash the original password
def hash_password(password: str) -> str:

    return password_hash.hash(password)


# Verify the entered password
def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return password_hash.verify(
        plain_password,
        hashed_password
    )