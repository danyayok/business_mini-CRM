import hashlib
import secrets
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.core.config import settings

def verify_password(plain_password, hashed_password):
    return secrets.compare_digest(
        hashed_password,
        hashlib.sha256(plain_password.encode()).hexdigest()
    )

def get_password_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=7)
    data.update({"exp": expire})
    return jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)

def decode_token(token: str):
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        return None