# Claw Agent — Developer Automation Platform

A local developer AI automation platform that connects engineering tools and exposes an AI assistant through Slack and a web dashboard. All reasoning is delegated to **IronClaw**, the Rust-based OpenClaw runtime.

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  Slack / Webhooks                                            │
│  (GitHub, Jira, Jenkins)                                     │
└────────────┬─────────────────────────────────────────────────┘
             │
┌────────────▼─────────────────────────────────────────────────┐
│  Python Orchestrator (FastAPI)               localhost:8080   │
│  ┌──────────────┐  ┌─────────────┐  ┌──────────────────┐    │
│  │ Slack Gateway │  │ Event Bus   │  │ Workflow Engine   │    │
│  └──────┬───────┘  └──────┬──────┘  └────────┬─────────┘    │
│         │                 │                   │              │
│  ┌──────▼─────────────────▼───────────────────▼──────────┐   │
│  │              Tool Schema Registry                     │   │
│  │  slack · github · jira · confluence · jenkins · gmail │   │
│  └──────────────────────────┬────────────────────────────┘   │
└─────────────────────────────┼────────────────────────────────┘
                              │  HTTP
┌─────────────────────────────▼────────────────────────────────┐
│  IronClaw Runtime (Rust)                     localhost:9090   │
│  Prompt interpretation · Task planning · Tool selection       │
│  Summarization                                                │
└──────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼────────────────────────────────┐
│  PostgreSQL                                  localhost:5432   │
│  events · workflow_runs · tool_outputs · agent_memory         │
│  agent_conversations                                          │
└──────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼────────────────────────────────┐
│  Web Dashboard (Next.js + Tailwind)          localhost:3000   │
│  Status · Events · Workflows · Runs · Tools · Conversations  │
└──────────────────────────────────────────────────────────────┘
```

## Components

| Component | Description |
|-----------|-------------|
| **Python Orchestrator** | FastAPI backend that coordinates tool execution and exposes the dashboard API |
| **IronClaw Runtime** | Rust-based reasoning engine — all prompt interpretation, planning, and summarization |
| **Tool Schema Registry** | Registry where integrations register tools with JSON parameter schemas |
| **Event Bus** | In-process pub/sub with wildcard matching and PostgreSQL persistence |
| **Workflow Engine** | Executes YAML-defined automation workflows triggered by events |
| **Slack Command Gateway** | Routes `@claw` mentions to the orchestrator and replies in-thread |
| **Web Dashboard** | Next.js + Tailwind CSS frontend showing system status, events, workflows, and conversations |

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- IronClaw runtime (see [IronClaw docs])

## Quick Start

### 1. Database

```bash
createdb clawagent
# Or with custom credentials:
psql -c "CREATE USER claw WITH PASSWORD 'claw';"
psql -c "CREATE DATABASE clawagent OWNER claw;"
```

### 2. Backend

```bash
cp .env.example .env
# Edit .env with your credentials

pip install -r requirements.txt
cd backend
python main.py run
# Backend starts on http://localhost:8080
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
# Dashboard starts on http://localhost:3000
```

### 4. IronClaw Runtime

Start the IronClaw runtime on port 9090 (see IronClaw documentation).

## Slack Commands

| Command | Description |
|---------|-------------|
| `@claw summarize today's PRs` | Summarize recent pull requests |
| `@claw investigate Jenkins build 1234` | Fetch logs and analyze a build failure |
| `@claw create Jira ticket from this email` | Create a Jira ticket from email content |

## Webhook Endpoints

| Endpoint | Source |
|----------|--------|
| `POST /webhooks/github` | GitHub events (validated via `X-Hub-Signature-256`) |
| `POST /webhooks/jira` | Jira events |
| `POST /webhooks/jenkins` | Jenkins build notifications |
| `POST /webhooks/slack` | Slack events and commands |

## Dashboard API

| Endpoint | Description |
|----------|-------------|
| `GET /api/status` | System health (IronClaw, database, integrations) |
| `GET /api/events` | Event stream from PostgreSQL |
| `GET /api/workflows` | Loaded workflow definitions |
| `GET /api/workflow-runs` | Workflow execution history |
| `GET /api/tools` | Registered tools with JSON schemas |
| `GET /api/agent-conversations` | Agent conversation history |

## Workflow Example

```yaml
name: pr_opened
trigger: github.pull_request.opened
description: Summarize new PRs and post to Slack

actions:
  - tool: github.summarize_pr
    args:
      repo: "{{ repo }}"
      pr_number: "{{ pr_number }}"
    description: Summarize the pull request

  - tool: slack.send_message
    args:
      channel: "#dev-notifications"
      text: "New PR opened: {{ title }}"
    description: Notify Slack channel
```

## Project Structure

```
developer-agent/
├── backend/
│   ├── main.py                 # Entry point
│   ├── agent/
│   │   ├── ironclaw.py         # IronClaw HTTP client
│   │   ├── orchestrator.py     # Tool execution coordinator
│   │   ├── memory.py           # Conversation memory
│   │   └── slack_gateway.py    # Slack command gateway
│   ├── tools/
│   │   └── registry.py         # Tool schema registry
│   ├── database/
│   │   └── models.py           # SQLAlchemy models (PostgreSQL)
│   ├── events/
│   │   ├── bus.py              # Event bus (pub/sub)
│   │   └── types.py            # Event type definitions
│   ├── workflows/
│   │   ├── engine.py           # Workflow execution engine
│   │   ├── loader.py           # YAML workflow loader
│   │   ├── pr_opened.yaml
│   │   ├── build_failed.yaml
│   │   └── jira_created.yaml
│   ├── webhooks/
│   │   └── server.py           # FastAPI (webhooks + dashboard API)
│   ├── integrations/
│   │   ├── slack.py
│   │   ├── github_integration.py
│   │   ├── jira_integration.py
│   │   ├── confluence.py
│   │   ├── jenkins.py
│   │   └── gmail.py
│   └── security/
│       └── secrets.py          # Credential loading + redaction
├── frontend/
│   ├── src/
│   │   ├── app/                # Next.js App Router pages
│   │   ├── components/         # Sidebar, StatusCard
│   │   └── lib/api.ts          # Backend API client
│   ├── package.json
│   └── tailwind.config.ts
├── config/
│   └── config.yaml
├── logs/
├── .env.example
├── requirements.txt
└── README.md
```

## Security

- Secrets loaded from `.env` via `pydantic-settings` — never hardcoded
- Webhook signatures validated (HMAC SHA-256)
- Secrets redacted from all log output via `RedactingFilter`
- PostgreSQL credentials managed via `DATABASE_URL`
