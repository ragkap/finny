import firebase_admin
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth, credentials

from app.config import settings

_initialized = False
security = HTTPBearer()


def init_firebase():
    global _initialized
    if not _initialized:
        try:
            cred = credentials.Certificate(settings.firebase_credentials_path)
            firebase_admin.initialize_app(cred)
        except (FileNotFoundError, ValueError):
            # Allow running without credentials for development
            try:
                firebase_admin.initialize_app()
            except ValueError:
                pass
        _initialized = True


def get_firebase_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    init_firebase()
    try:
        decoded = auth.verify_id_token(credentials.credentials)
        return decoded
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
