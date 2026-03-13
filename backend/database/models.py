"""SQLAlchemy models and PostgreSQL session management."""

from __future__ import annotations

import datetime as dt
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Text, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from security.secrets import get_secrets


class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_type: Mapped[str] = mapped_column(String(255), index=True)
    source: Mapped[str] = mapped_column(String(100))
    payload: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    workflow_name: Mapped[str] = mapped_column(String(255), index=True)
    trigger_event: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50), default="pending")
    result: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    started_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    finished_at: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime, nullable=True
    )


class ToolOutput(Base):
    __tablename__ = "tool_outputs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tool_name: Mapped[str] = mapped_column(String(255), index=True)
    input_data: Mapped[str] = mapped_column(Text, default="")
    output_data: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )


class AgentMemory(Base):
    __tablename__ = "agent_memory"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(512), unique=True, index=True)
    value: Mapped[str] = mapped_column(Text, default="")
    context: Mapped[str] = mapped_column(String(100), default="global")
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )


class AgentConversation(Base):
    __tablename__ = "agent_conversations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    conversation_id: Mapped[str] = mapped_column(String(255), index=True)
    user_id: Mapped[str] = mapped_column(String(255), index=True)
    channel: Mapped[str] = mapped_column(String(255), default="")
    user_message: Mapped[str] = mapped_column(Text, default="")
    agent_response: Mapped[str] = mapped_column(Text, default="")
    tools_used: Mapped[str] = mapped_column(Text, default="[]")
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )


class AgentLog(Base):
    __tablename__ = "agent_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    level: Mapped[str] = mapped_column(String(20), index=True, default="INFO")
    source: Mapped[str] = mapped_column(String(255), index=True, default="")
    message: Mapped[str] = mapped_column(Text, default="")
    detail: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )


_engine = None
_SessionLocal = None


def get_engine():
    global _engine
    if _engine is None:
        db_url = get_secrets().database_url
        connect_args: dict = {}
        if db_url.startswith("sqlite"):
            connect_args["check_same_thread"] = False
        _engine = create_engine(db_url, echo=False, connect_args=connect_args)
        Base.metadata.create_all(_engine)
    return _engine


def get_session() -> Session:
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=get_engine())
    return _SessionLocal()
