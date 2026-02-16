"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-02-16
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("firebase_uid", sa.String(128), unique=True, nullable=False, index=True),
        sa.Column("display_name", sa.String(100), nullable=False),
        sa.Column("avatar_url", sa.Text, nullable=True),
        sa.Column("finny_score", sa.Integer, server_default="0"),
        sa.Column("level", sa.Integer, server_default="1"),
        sa.Column("current_streak", sa.Integer, server_default="0"),
        sa.Column("longest_streak", sa.Integer, server_default="0"),
        sa.Column("last_active_date", sa.Date, nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "badges",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("slug", sa.String(50), unique=True, nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("icon", sa.String(50), nullable=False),
        sa.Column("xp_required", sa.Integer, nullable=True),
    )

    op.create_table(
        "user_badges",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("badge_id", sa.Integer, sa.ForeignKey("badges.id"), nullable=False),
        sa.Column("earned_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "score_events",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("user_id", UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("event_type", sa.String(50), nullable=False),
        sa.Column("points", sa.Integer, nullable=False),
        sa.Column("metadata", JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # Seed badges
    op.bulk_insert(
        sa.table(
            "badges",
            sa.column("slug", sa.String),
            sa.column("name", sa.String),
            sa.column("description", sa.Text),
            sa.column("icon", sa.String),
            sa.column("xp_required", sa.Integer),
        ),
        [
            {"slug": "market-rookie", "name": "Market Rookie", "description": "Send your first chat message", "icon": "🐣", "xp_required": 0},
            {"slug": "ticker-spotter", "name": "Ticker Spotter", "description": "Identify 10 stock tickers", "icon": "🔍", "xp_required": 100},
            {"slug": "jargon-buster", "name": "Jargon Buster", "description": "Complete 5 Jargon Quests", "icon": "📖", "xp_required": 250},
            {"slug": "dividend-detective", "name": "Dividend Detective", "description": "Ask about dividends", "icon": "🕵️", "xp_required": None},
            {"slug": "market-whale", "name": "Market Whale", "description": "Reach 5000 XP", "icon": "🐋", "xp_required": 5000},
            {"slug": "streak-master", "name": "Streak Master", "description": "Maintain a 7-day streak", "icon": "🔥", "xp_required": None},
        ],
    )


def downgrade() -> None:
    op.drop_table("score_events")
    op.drop_table("user_badges")
    op.drop_table("badges")
    op.drop_table("users")
