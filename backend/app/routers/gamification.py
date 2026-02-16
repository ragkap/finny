import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.firebase_auth import get_firebase_user
from app.models.badge import Badge, UserBadge
from app.models.user import User

router = APIRouter(prefix="/api", tags=["gamification"])


class ScoreResponse(BaseModel):
    finny_score: int
    level: int
    current_streak: int
    longest_streak: int
    next_level_xp: int
    progress_percent: float


class BadgeResponse(BaseModel):
    slug: str
    name: str
    description: str
    icon: str
    earned: bool
    earned_at: str | None = None


@router.get("/score", response_model=ScoreResponse)
def get_score(
    firebase_user: dict = Depends(get_firebase_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.firebase_uid == firebase_user["uid"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    next_level_xp = user.level * 500
    progress = (user.finny_score % 500) / 500 * 100

    return ScoreResponse(
        finny_score=user.finny_score,
        level=user.level,
        current_streak=user.current_streak,
        longest_streak=user.longest_streak,
        next_level_xp=next_level_xp,
        progress_percent=round(progress, 1),
    )


@router.get("/badges", response_model=list[BadgeResponse])
def get_badges(
    firebase_user: dict = Depends(get_firebase_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.firebase_uid == firebase_user["uid"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    all_badges = db.execute(select(Badge)).scalars().all()
    earned = db.execute(
        select(UserBadge).where(UserBadge.user_id == user.id)
    ).scalars().all()
    earned_map = {ub.badge_id: ub for ub in earned}

    result = []
    for badge in all_badges:
        ub = earned_map.get(badge.id)
        result.append(
            BadgeResponse(
                slug=badge.slug,
                name=badge.name,
                description=badge.description,
                icon=badge.icon,
                earned=ub is not None,
                earned_at=ub.earned_at.isoformat() if ub else None,
            )
        )
    return result
