# Claw Agent — Architecture Diagrams

This document describes the architecture and data flows using Mermaid diagrams. Render in GitHub, VS Code (with Mermaid extension), or [mermaid.live](https://mermaid.live).

---

## 1. System Overview

```mermaid
flowchart TB
    subgraph External["External Services"]
        GH[GitHub]
        J[Jira]
        JK[Jenkins]
        SL[Slack]
        GM[Gmail]
        CF[Confluence]
    end

    subgraph Dashboard["Web Dashboard — localhost:3000"]
        FE[Next.js + Tailwind]
    end

    subgraph ClawAgent["Claw Agent — Python Orchestrator — localhost:8080"]
        subgraph Entry["Entry Points"]
            SGW[Slack Command Gateway]
            WH[Webhook Server]
            API[Dashboard API]
        end

        subgraph Core["Core"]
            ORCH[Orchestrator]
            EB[Event Bus]
            WE[Workflow Engine]
            TR[Tool Schema Registry]
        end

        subgraph Tools["Integration Connectors"]
            SL_I[Slack]
            GH_I[GitHub]
            J_I[Jira]
            CF_I[Confluence]
            JK_I[Jenkins]
            GM_I[Gmail]
        end
    end

    subgraph IronClaw["IronClaw Runtime — Rust — localhost:9090"]
        IC_I[Prompt Interpretation]
        IC_P[Task Planning]
        IC_T[Tool Selection]
        IC_S[Summarization]
    end

    subgraph Persistence["PostgreSQL — localhost:5432"]
        DB[(PostgreSQL)]
    end

    SL -->|@claw commands| SGW
    GH -->|webhook| WH
    J -->|webhook| WH
    JK -->|webhook| WH
    SL -->|webhook| WH

    SGW --> ORCH
    ORCH -->|interpret / plan| IronClaw
    IronClaw -->|action plan| ORCH
    ORCH --> TR
    TR --> Tools
    WH --> EB
    EB --> WE
    WE --> TR
    EB --> DB
    WE --> DB
    ORCH --> DB

    FE -->|fetch| API
    API --> DB
```

---

## 2. Component Diagram

```mermaid
flowchart LR
    subgraph Agent["agent/"]
        ORCH[Orchestrator]
        IC[IronClawClient]
        MEM[ConversationMemory]
        SGW[SlackCommandGateway]
    end

    subgraph ToolsReg["tools/"]
        REG[ToolRegistry]
        SCH[ToolSchema]
    end

    subgraph Events["events/"]
        EB[EventBus]
        ET[AgentEvent]
    end

    subgraph Workflows["workflows/"]
        LOAD[Loader]
        ENG[WorkflowEngine]
    end

    subgraph Integrations["integrations/"]
        SL[slack]
        GH[github]
        JI[jira]
        CF[confluence]
        JK[jenkins]
        GM[gmail]
    end

    subgraph Data["database/"]
        MOD[models]
        SES[get_session]
    end

    subgraph Web["webhooks/"]
        APP[FastAPI app]
        DASH[Dashboard API]
    end

    subgraph Security["security/"]
        SEC[secrets]
    end

    ORCH --> IC
    ORCH --> MEM
    ORCH --> REG
    REG --> SCH
    REG --> Integrations
    SGW --> ORCH
    SGW --> SL
    APP --> EB
    APP --> DASH
    DASH --> MOD
    EB --> ENG
    ENG --> REG
    LOAD --> ENG
    EB --> MOD
    ENG --> MOD
    ORCH --> MOD
    SEC --> ORCH
    SEC --> Integrations
```

---

## 3. IronClaw Communication Flow

```mermaid
sequenceDiagram
    participant User as Slack User
    participant SGW as Slack Gateway
    participant ORCH as Orchestrator
    participant IC as IronClaw Runtime
    participant REG as Tool Registry
    participant Tool as Integration
    participant DB as PostgreSQL

    User->>SGW: @claw summarize today's PRs
    SGW->>ORCH: handle_message(msg, user, channel)
    ORCH->>REG: get_all_schemas()
    REG-->>ORCH: tool schemas (JSON)
    ORCH->>IC: POST /api/v1/interpret {message, tools, context}
    IC->>IC: Prompt interpretation + task planning
    IC-->>ORCH: {type: "action_plan", actions: [...]}

    loop For each action in plan
        ORCH->>REG: get_handler(tool_name)
        REG-->>ORCH: handler function
        ORCH->>Tool: execute(args)
        Tool-->>ORCH: result
        ORCH->>DB: Persist ToolOutput
    end

    ORCH->>IC: POST /api/v1/interpret {message, tools, context + results}
    IC-->>ORCH: {type: "response", response: "Here's a summary..."}
    ORCH->>DB: Persist AgentConversation
    ORCH-->>SGW: response text
    SGW->>User: Slack reply (threaded)
```

---

## 4. Webhook → Workflow Flow

```mermaid
sequenceDiagram
    participant GH as GitHub
    participant WH as Webhook Server
    participant EB as Event Bus
    participant DB as PostgreSQL
    participant WE as Workflow Engine
    participant IC as IronClaw
    participant Slack as Slack Integration

    GH->>WH: POST /webhooks/github (pull_request.opened)
    WH->>WH: Verify signature (HMAC SHA-256)
    WH->>EB: publish(AgentEvent)
    EB->>DB: Persist event
    EB->>WE: _handle_event (subscribed to trigger)
    WE->>WE: run_workflow(pr_opened)
    WE->>DB: Create WorkflowRun
    loop For each action
        WE->>Slack: github.summarize_pr → result
        WE->>IC: agent.summarize → summary
        WE->>Slack: slack.send_message
    end
    WE->>DB: Update WorkflowRun (completed)
    WH-->>GH: 200 OK
```

---

## 5. Event Bus (Pub/Sub)

```mermaid
flowchart TB
    subgraph Publishers["Publishers"]
        WH[Webhook Server]
    end

    subgraph EventBus["EventBus"]
        subgraph Subscribers["Subscribers by trigger"]
            S1["github.pull_request.opened"]
            S2["jira.issue.created"]
            S3["jenkins.build.failed"]
            S4["slack.*"]
        end
    end

    subgraph Handlers["Handlers"]
        WE[WorkflowEngine._handle_event]
        SGW[SlackCommandGateway.handle_event]
    end

    WH -->|publish| EventBus
    EventBus -->|match trigger| S1
    EventBus -->|match trigger| S2
    EventBus -->|match trigger| S3
    S1 --> WE
    S2 --> WE
    S3 --> WE
    S4 --> SGW
    EventBus -->|persist| DB[(PostgreSQL)]
```

---

## 6. Data Model

```mermaid
erDiagram
    Event {
        int id PK
        string event_type
        string source
        text payload
        datetime created_at
    }

    WorkflowRun {
        int id PK
        string workflow_name
        string trigger_event
        string status
        text result
        datetime started_at
        datetime finished_at
    }

    ToolOutput {
        int id PK
        string tool_name
        text input_data
        text output_data
        datetime created_at
    }

    AgentMemory {
        int id PK
        string key UK
        text value
        string context
        datetime created_at
        datetime updated_at
    }

    AgentConversation {
        int id PK
        string conversation_id
        string user_id
        string channel
        text user_message
        text agent_response
        text tools_used
        datetime created_at
    }

    Event ||--o{ WorkflowRun : "triggers"
```

---

## 7. Dashboard Architecture

```mermaid
flowchart LR
    subgraph Frontend["Next.js Dashboard — localhost:3000"]
        P1[Status Page]
        P2[Event Stream]
        P3[Workflows]
        P4[Workflow Runs]
        P5[Tool Registry]
        P6[Conversations]
    end

    subgraph Backend["FastAPI — localhost:8080"]
        A1["GET /api/status"]
        A2["GET /api/events"]
        A3["GET /api/workflows"]
        A4["GET /api/workflow-runs"]
        A5["GET /api/tools"]
        A6["GET /api/agent-conversations"]
    end

    subgraph Data["PostgreSQL"]
        DB[(tables)]
    end

    P1 --> A1
    P2 --> A2
    P3 --> A3
    P4 --> A4
    P5 --> A5
    P6 --> A6
    A1 --> DB
    A2 --> DB
    A4 --> DB
    A6 --> DB
```

---

## 8. Supported Event Types

| Source     | Example triggers                                      |
|------------|-------------------------------------------------------|
| GitHub     | `github.pull_request.opened`, `github.issues.opened`  |
| Jira       | `jira.issue.created`, `jira.issue.updated`             |
| Jenkins    | `jenkins.build.failed`, `jenkins.build.completed`      |
| Slack      | `slack.app_mention.received`, `slack.message.received` |

Workflows subscribe to these triggers via `workflows/*.yaml` `trigger` fields.

---

## 9. Tool Schema Registry

Each tool registers with:

| Field        | Type              | Description                        |
|--------------|-------------------|------------------------------------|
| `name`       | `string`          | Unique identifier                  |
| `description`| `string`          | Human-readable purpose             |
| `parameters` | `JSON Schema`     | Input parameter schema             |
| `handler`    | `Callable`        | Python function that executes tool |

Tool schemas are sent to IronClaw so it can select and parameterize tools during planning.
