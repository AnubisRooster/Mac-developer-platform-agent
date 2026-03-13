"""FastAPI webhook server + dashboard API.

Webhook endpoints:
    POST /webhooks/github
    POST /webhooks/jira
    POST /webhooks/jenkins
    POST /webhooks/slack

Dashboard API endpoints:
    GET /api/status
    GET /api/events
    GET /api/workflows
    GET /api/workflow-runs
    GET /api/tools
    GET /api/agent-conversations
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
from typing import Any, Dict, Optional

from fastapi import FastAPI, Header, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware

from database.models import (
    AgentConversation,
    Event as EventRow,
    WorkflowRun,
    get_session,
)
from events.bus import event_bus
from events.types import AgentEvent, EventSource
from security.secrets import get_secrets, verify_webhook_signature

logger = logging.getLogger("claw-agent.webhooks")

app = FastAPI(title="Claw Agent API", version="0.2.0", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def _ensure_database_tables():
    """Guarantee all tables exist before the first request is served."""
    from database.models import get_engine

    get_engine()
    logger.info("Database tables verified")


# ─── Health ──────────────────────────────────────────────────────────────────


@app.get("/health")
async def health():
    return {"status": "ok"}


# ─── Webhook Endpoints ──────────────────────────────────────────────────────


@app.post("/webhooks/github")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str | None = Header(None),
    x_github_event: str | None = Header(None),
):
    body = await request.body()
    secrets = get_secrets()
    if secrets.github_webhook_secret:
        if not x_hub_signature_256:
            raise HTTPException(status_code=401, detail="Missing signature")
        if not verify_webhook_signature(
            body, x_hub_signature_256, secrets.github_webhook_secret, "sha256"
        ):
            raise HTTPException(status_code=403, detail="Invalid signature")
    payload: Dict[str, Any] = json.loads(body)
    action = payload.get("action", "")
    event_type = f"github.{x_github_event or 'unknown'}"
    if action:
        event_type = f"{event_type}.{action}"
    event = AgentEvent(
        event_type=event_type, source=EventSource.GITHUB, payload=payload
    )
    logger.info("Received GitHub webhook: %s", event_type)
    await event_bus.publish(event)
    return {"accepted": True, "event_type": event_type}


@app.post("/webhooks/jira")
async def jira_webhook(request: Request):
    body = await request.body()
    secrets = get_secrets()
    if secrets.jira_webhook_secret:
        sig = request.headers.get("x-hub-signature", "")
        if not verify_webhook_signature(
            body, sig, secrets.jira_webhook_secret, "sha256"
        ):
            raise HTTPException(status_code=403, detail="Invalid signature")
    payload: Dict[str, Any] = json.loads(body)
    webhook_event = payload.get("webhookEvent", "unknown")
    event_type = f"jira.{webhook_event}".replace(":", ".").replace("_", ".")
    event = AgentEvent(
        event_type=event_type, source=EventSource.JIRA, payload=payload
    )
    logger.info("Received Jira webhook: %s", event_type)
    await event_bus.publish(event)
    return {"accepted": True, "event_type": event_type}


@app.post("/webhooks/jenkins")
async def jenkins_webhook(request: Request):
    body = await request.body()
    secrets = get_secrets()
    if secrets.jenkins_webhook_secret:
        sig = request.headers.get("x-jenkins-signature", "")
        if sig and not verify_webhook_signature(
            body, sig, secrets.jenkins_webhook_secret, "sha256"
        ):
            raise HTTPException(status_code=403, detail="Invalid signature")
    payload: Dict[str, Any] = json.loads(body)
    build_phase = payload.get("build", {}).get("phase", "unknown").lower()
    build_status = payload.get("build", {}).get("status", "").lower()
    job_name = payload.get("name", "unknown")
    event_type = f"jenkins.build.{build_phase}"
    if build_status:
        event_type = f"jenkins.build.{build_status}"
    event = AgentEvent(
        event_type=event_type,
        source=EventSource.JENKINS,
        payload={**payload, "job_name": job_name},
    )
    logger.info("Received Jenkins webhook: %s", event_type)
    await event_bus.publish(event)
    return {"accepted": True, "event_type": event_type}


@app.post("/webhooks/slack")
async def slack_webhook(request: Request):
    body = await request.body()
    secrets = get_secrets()
    if secrets.slack_signing_secret:
        timestamp = request.headers.get("x-slack-request-timestamp", "")
        slack_sig = request.headers.get("x-slack-signature", "")
        sig_basestring = f"v0:{timestamp}:{body.decode()}"
        computed = "v0=" + hmac.new(
            secrets.slack_signing_secret.encode(),
            sig_basestring.encode(),
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(computed, slack_sig):
            raise HTTPException(status_code=403, detail="Invalid Slack signature")
    payload: Dict[str, Any] = json.loads(body)

    if payload.get("type") == "url_verification":
        return {"challenge": payload.get("challenge")}

    event_type_raw = payload.get("event", {}).get("type", "command")
    event_type = f"slack.{event_type_raw}.received"
    event = AgentEvent(
        event_type=event_type, source=EventSource.SLACK, payload=payload
    )
    logger.info("Received Slack webhook: %s", event_type)
    await event_bus.publish(event)

    # Route @claw commands through the Slack command gateway
    if hasattr(app.state, "slack_gateway"):
        import asyncio

        asyncio.create_task(app.state.slack_gateway.handle_event(event))

    return {"accepted": True, "event_type": event_type}


# ─── Dashboard API Endpoints ────────────────────────────────────────────────


@app.get("/api/status")
async def api_status():
    """System status: IronClaw health, database connectivity, integrations."""
    secrets = get_secrets()

    # IronClaw health
    ironclaw_status: Dict[str, Any] = {"status": "not_configured"}
    if hasattr(app.state, "orchestrator"):
        try:
            ironclaw_status = await app.state.orchestrator.ironclaw.health()
        except Exception as e:
            ironclaw_status = {
                "status": "unreachable",
                "error": f"IronClaw runtime not running on {get_secrets().ironclaw_url} — start it to enable AI features",
            }

    # Database health
    db_status: Dict[str, Any] = {"status": "unknown"}
    try:
        session = get_session()
        session.execute(EventRow.__table__.select().limit(1))
        session.close()
        db_status = {"status": "connected"}
    except Exception as e:
        db_status = {"status": "error", "error": str(e)}

    # Integration connectivity
    integrations = {
        "slack": {"connected": bool(secrets.slack_bot_token)},
        "github": {"connected": bool(secrets.github_token)},
        "jira": {"connected": bool(secrets.jira_api_token)},
        "confluence": {"connected": bool(secrets.confluence_api_token)},
        "jenkins": {"connected": bool(secrets.jenkins_api_token)},
        "gmail": {"connected": bool(secrets.gmail_credentials_file)},
    }

    return {
        "ironclaw": ironclaw_status,
        "database": db_status,
        "integrations": integrations,
    }


@app.get("/api/events")
async def api_events(
    limit: int = Query(default=50, le=200),
    offset: int = Query(default=0, ge=0),
):
    """Return system events from PostgreSQL."""
    session = get_session()
    try:
        total = session.query(EventRow).count()
        rows = (
            session.query(EventRow)
            .order_by(EventRow.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        events = [
            {
                "id": r.id,
                "event_type": r.event_type,
                "source": r.source,
                "payload": json.loads(r.payload) if r.payload else {},
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]
        return {"events": events, "total": total}
    finally:
        session.close()


@app.get("/api/workflows")
async def api_workflows():
    """Return all loaded workflow definitions."""
    if hasattr(app.state, "workflow_engine"):
        return {"workflows": app.state.workflow_engine.get_workflows()}
    return {"workflows": []}


@app.get("/api/workflow-runs")
async def api_workflow_runs(
    limit: int = Query(default=50, le=200),
    offset: int = Query(default=0, ge=0),
):
    """Return workflow run history from PostgreSQL."""
    session = get_session()
    try:
        total = session.query(WorkflowRun).count()
        rows = (
            session.query(WorkflowRun)
            .order_by(WorkflowRun.started_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        runs = [
            {
                "id": r.id,
                "workflow_name": r.workflow_name,
                "trigger_event": r.trigger_event,
                "status": r.status,
                "result": json.loads(r.result) if r.result else None,
                "started_at": r.started_at.isoformat() if r.started_at else None,
                "finished_at": r.finished_at.isoformat() if r.finished_at else None,
            }
            for r in rows
        ]
        return {"runs": runs, "total": total}
    finally:
        session.close()


@app.get("/api/tools")
async def api_tools():
    """Return all tools registered in the tool schema registry."""
    if hasattr(app.state, "orchestrator"):
        return {"tools": app.state.orchestrator.registry.get_all_schemas()}
    return {"tools": []}


@app.get("/api/agent-conversations")
async def api_agent_conversations(
    limit: int = Query(default=50, le=200),
    offset: int = Query(default=0, ge=0),
):
    """Return agent conversation history from PostgreSQL."""
    session = get_session()
    try:
        total = session.query(AgentConversation).count()
        rows = (
            session.query(AgentConversation)
            .order_by(AgentConversation.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        conversations = [
            {
                "id": r.id,
                "conversation_id": r.conversation_id,
                "user_id": r.user_id,
                "channel": r.channel,
                "user_message": r.user_message,
                "agent_response": r.agent_response,
                "tools_used": json.loads(r.tools_used) if r.tools_used else [],
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]
        return {"conversations": conversations, "total": total}
    finally:
        session.close()
