import jwt
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

private_key = (BASE_DIR / "private.pem").read_text()

payload = {
    "sub": "test-user-123",
    "iss": "django-auth",
    "aud": "college-admission-rag",
    "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    "iat": datetime.now(timezone.utc),
}

token = jwt.encode(
    payload,
    private_key,
    algorithm="RS256"
)

print("\nGenerated Access Token:\n")
print(token)