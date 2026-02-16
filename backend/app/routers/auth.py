from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.firebase_auth import get_firebase_user
from app.models.user import User

router = APIRouter(prefix="/api/auth", tags=["auth"])


class UserResponse(BaseModel):
    id: str
    firebase_uid: str
    display_name: str
    avatar_url: str | None
    finny_score: int
    level: int
    current_streak: int
    longest_streak: int

    model_config = {"from_attributes": True}


@router.post("/register", response_model=UserResponse)
def register(
    firebase_user: dict = Depends(get_firebase_user),
    db: Session = Depends(get_db),
):
    existing = db.query(User).filter(User.firebase_uid == firebase_user["uid"]).first()
    if existing:
        return existing

    user = User(
        firebase_uid=firebase_user["uid"],
        display_name=firebase_user.get("name", "Finny Learner"),
        avatar_url=firebase_user.get("picture"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/me", response_model=UserResponse)
def get_me(
    firebase_user: dict = Depends(get_firebase_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.firebase_uid == firebase_user["uid"]).first()
    if not user:
        return register(firebase_user=firebase_user, db=db)
    return user
