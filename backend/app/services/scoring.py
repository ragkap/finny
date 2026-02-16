import uuid
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.badge import Badge, UserBadge
from app.models.user import ScoreEvent, User

POINTS = {
    "ticker_identify": 10,
    "jargon_quest": 50,
    "daily_streak": 100,
    "first_message": 10,
}


def award_points(db: Session, user_id: uuid.UUID, event_type: str, metadata: dict | None = None) -> int:
    points = POINTS.get(event_type, 0)
    if points == 0:
        return 0

    event = ScoreEvent(
        user_id=user_id,
        event_type=event_type,
        points=points,
        metadata_=metadata,
    )
    db.add(event)

    user = db.get(User, user_id)
    if user:
        user.finny_score += points
        user.level = user.finny_score // 500 + 1

    db.commit()
    return points


def check_streak(db: Session, user_id: uuid.UUID) -> dict:
    user = db.get(User, user_id)
    if not user:
        return {"streak": 0, "bonus_awarded": False}

    today = date.today()
    bonus_awarded = False

    if user.last_active_date is None:
        user.current_streak = 1
    elif user.last_active_date == today:
        pass  # Already active today
    elif user.last_active_date == today - timedelta(days=1):
        user.current_streak += 1
        bonus_awarded = True
        award_points(db, user_id, "daily_streak")
    else:
        user.current_streak = 1

    if user.current_streak > user.longest_streak:
        user.longest_streak = user.current_streak

    user.last_active_date = today
    db.commit()

    return {"streak": user.current_streak, "bonus_awarded": bonus_awarded}


def check_badge_eligibility(db: Session, user_id: uuid.UUID) -> list[dict]:
    user = db.get(User, user_id)
    if not user:
        return []

    earned_badge_ids = {
        ub.badge_id
        for ub in db.execute(
            select(UserBadge).where(UserBadge.user_id == user_id)
        ).scalars()
    }

    all_badges = db.execute(select(Badge)).scalars().all()
    newly_earned = []

    for badge in all_badges:
        if badge.id in earned_badge_ids:
            continue

        earned = False
        if badge.slug == "market-rookie":
            count = db.execute(
                select(ScoreEvent).where(
                    ScoreEvent.user_id == user_id,
                    ScoreEvent.event_type == "first_message",
                )
            ).scalars().first()
            earned = count is not None

        elif badge.slug == "ticker-spotter":
            count = db.execute(
                select(ScoreEvent).where(
                    ScoreEvent.user_id == user_id,
                    ScoreEvent.event_type == "ticker_identify",
                )
            ).scalars().all()
            earned = len(count) >= 10

        elif badge.slug == "jargon-buster":
            count = db.execute(
                select(ScoreEvent).where(
                    ScoreEvent.user_id == user_id,
                    ScoreEvent.event_type == "jargon_quest",
                )
            ).scalars().all()
            earned = len(count) >= 5

        elif badge.slug == "dividend-detective":
            count = db.execute(
                select(ScoreEvent).where(
                    ScoreEvent.user_id == user_id,
                    ScoreEvent.event_type == "ticker_identify",
                )
            ).scalars().all()
            earned = any(
                e.metadata_ and e.metadata_.get("topic") == "dividend"
                for e in count
            )

        elif badge.slug == "market-whale":
            earned = user.finny_score >= 5000

        elif badge.slug == "streak-master":
            earned = user.longest_streak >= 7

        if earned:
            db.add(UserBadge(user_id=user_id, badge_id=badge.id))
            newly_earned.append({"slug": badge.slug, "name": badge.name, "icon": badge.icon})

    if newly_earned:
        db.commit()

    return newly_earned
