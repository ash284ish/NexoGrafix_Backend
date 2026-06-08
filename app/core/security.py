import hmac
import hashlib
import time

from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ── HMAC-signed stateless token ───────────────────────────────────────────────
# Format: "{user_id}.{expires_at_unix}.{hmac_hex}"
# HMAC signs user_id + expires_at so neither field can be tampered with.

def _sign(payload: str) -> str:
    return hmac.new(
        settings.SECRET_KEY.encode(),
        payload.encode(),
        hashlib.sha256,
    ).hexdigest()


def create_token(user_id: int) -> str:
    expire = int(time.time()) + settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    payload = f"{user_id}.{expire}"
    sig = _sign(payload)
    return f"{payload}.{sig}"


def verify_token(token: str) -> int:
    """Return user_id if token is valid and not expired, else raise ValueError."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("malformed")
        user_id_str, expire_str, sig = parts
        payload = f"{user_id_str}.{expire_str}"

        # Constant-time comparison to prevent timing attacks
        expected = _sign(payload)
        if not hmac.compare_digest(sig, expected):
            raise ValueError("invalid signature")

        if int(time.time()) > int(expire_str):
            raise ValueError("token expired")

        return int(user_id_str)
    except ValueError:
        raise
    except Exception:
        raise ValueError("invalid token")
