import base64
import hashlib
import hmac
from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.config import get_settings


def hash_password(password: str) -> str:
    settings = get_settings()
    digest = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        settings.secret_key.encode('utf-8'),
        390000,
    )
    return base64.b64encode(digest).decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    expected = hash_password(password)
    return hmac.compare_digest(expected, hashed_password)


def create_access_token(user_id: str) -> str:
    settings = get_settings()
    issued_at = str(int(datetime.now(timezone.utc).timestamp()))
    payload = f'{user_id}:{issued_at}'
    signature = hmac.new(settings.secret_key.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).hexdigest()
    token = base64.urlsafe_b64encode(f'{payload}:{signature}'.encode('utf-8')).decode('utf-8')
    return token


def decode_access_token(token: str) -> str:
    settings = get_settings()

    try:
        decoded = base64.urlsafe_b64decode(token.encode('utf-8')).decode('utf-8')
        user_id, issued_at, signature = decoded.split(':', 2)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token không hợp lệ.') from exc

    payload = f'{user_id}:{issued_at}'
    expected_signature = hmac.new(
        settings.secret_key.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token không hợp lệ.')

    return user_id
