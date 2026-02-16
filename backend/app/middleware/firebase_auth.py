import json

import firebase_admin
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth, credentials

from app.config import settings

_initialized = False
security = HTTPBearer()


def init_firebase():
    global _initialized
    if not _initialized:
        try:
            # Prefer JSON string env var (for cloud deploys like Render)
            if settings.firebase_credentials_json:
                cred_dict = json.loads(settings.firebase_credentials_json)
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
            else:
                cred = credentials.Certificate(settings.firebase_credentials_path)
                firebase_admin.initialize_app(cred)
        except (FileNotFoundError, ValueError, json.JSONDecodeError):
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
