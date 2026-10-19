# Graph Report - Mac-developer-platform-agent  (2026-10-19)

## Corpus Check
- 121 files · ~143,299 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 4, .ini 2, .example 1)

## Summary
- 1309 nodes · 2718 edges · 96 communities (34 shown, 62 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 257 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- IronClawClient
- GmailIntegration
- redact()
- package.json
- database/models.py
- api.ts
- ToolRegistry
- WorkflowEngine
- AgentEvent
- cli()
- get_secrets()
- test_webhooks_api.py
- EventBus
- backend/webhooks/server.py
- load_all_workflows()
- security/secrets.py
- asyncio
- AgentEvent
- Orchestrator
- Base
- test_webhook_security.py
- SlackCommandGateway
- verify_webhook_signature()
- ConversationMemory
- TestWorkflowEngine
- test_webhooks.py
- compilerOptions
- GitHubIntegration
- GmailIntegration
- SlackIntegration
- GitHubIntegration
- SlackIntegration
- fixture
- patch
- pytest
- JiraIntegration
- backend/main.py
- _import_main()
- ToolRegistry
- test_deployment_readiness.py
- JiraIntegration
- main.py
- LLMClient
- test_agent.py
- Orchestrator
- ConfluenceIntegration
- Planner
- get_session()
- IronClawResponse
- ConversationMemory
- TestAPIEndpointEdgeCases
- _strip_html()
- TestSlackCommandGateway
- AppSecrets
- asyncio
- AgentConversation
- TestAppWiring
- TestFastAPIAppImportable
- TestWorkflowLoading
- TestToolCallPattern
- TestDatabaseTablesExist
- next.config.js
- TestEventSource

## God Nodes (most connected - your core abstractions)
1. `get_secrets()` - 67 edges
2. `AgentEvent` - 66 edges
3. `IronClawClient` - 52 edges
4. `AgentEvent` - 35 edges
5. `Orchestrator` - 33 edges
6. `WorkflowEngine` - 33 edges
7. `ConversationMemory` - 31 edges
8. `EventBus` - 29 edges
9. `get_session()` - 28 edges
10. `WorkflowDefinition` - 24 edges

## Surprising Connections (you probably didn't know these)
- `Orchestrator` --uses--> `ConversationMemory`  [INFERRED]
  backend/agent/orchestrator.py → agent/memory.py
- `TestOrchestratorEdgeCases` --uses--> `Orchestrator`  [INFERRED]
  backend/tests/test_edge_cases.py → agent/orchestrator.py
- `TestOrchestrator` --uses--> `Orchestrator`  [INFERRED]
  tests/test_agent.py → agent/orchestrator.py
- `TestPlanner` --uses--> `ActionPlan`  [INFERRED]
  tests/test_agent.py → agent/planner.py
- `TestEventModel` --uses--> `Event`  [INFERRED]
  tests/test_database.py → backend/database/models.py

## Import Cycles
- None detected.

## Communities (96 total, 62 thin omitted)

### Community 0 - "IronClawClient"
Cohesion: 0.05
Nodes (11): IronClawClient, _mock_get_response(), _mock_response(), TestIronClawClient, _mock_get_response(), _mock_response(), TestAgentLogTable, TestIronClawModelConfig (+3 more)

### Community 1 - "GmailIntegration"
Cohesion: 0.06
Nodes (6): ConfluenceIntegration, GmailIntegration, JenkinsIntegration, TestConfluenceIntegration, TestGmailIntegration, TestJenkinsIntegration

### Community 2 - "redact()"
Cohesion: 0.06
Nodes (11): cli(), _setup_logging(), redact(), RedactingFilter, TestSecurityEdgeCases, TestRedact, TestRedactingFilter, redact() (+3 more)

### Community 3 - "package.json"
Cohesion: 0.05
Nodes (35): dependencies, next, react, react-dom, devDependencies, autoprefixer, postcss, tailwindcss (+27 more)

### Community 4 - "database/models.py"
Cohesion: 0.10
Nodes (14): get_engine(), get_session(), TestEventModel, TestToolOutputModel, TestWorkflowRunModel, Base, CachedSummary, Event (+6 more)

### Community 5 - "api.ts"
Cohesion: 0.10
Nodes (23): EventsPage(), sourceBadge(), LEVEL_COLORS, LEVELS, StatusPage(), connectorColor(), ToolsPage(), statusBadge() (+15 more)

### Community 6 - "ToolRegistry"
Cohesion: 0.08
Nodes (5): TestToolRegistry, TestToolSchema, ToolEntry, ToolRegistry, ToolSchema

### Community 7 - "WorkflowEngine"
Cohesion: 0.13
Nodes (6): WorkflowRun, TestWorkflowEngineEdgeCases, TestWorkflowEngine, WorkflowEngine, WorkflowAction, WorkflowDefinition

### Community 8 - "AgentEvent"
Cohesion: 0.08
Nodes (5): EventBus, AgentEvent, TestWorkflowEngineLoad, WorkflowEngine, _is_coroutine()

### Community 9 - "cli()"
Cohesion: 0.09
Nodes (7): _chat_loop(), _print_banner(), start_chat(), cli(), _setup_logging(), TestCLIChat, TestMainCLI

### Community 10 - "get_secrets()"
Cohesion: 0.17
Nodes (15): EventSource, github_webhook(), jenkins_webhook(), jira_webhook(), _persist_log(), set_model_config(), set_openrouter_key(), slack_webhook() (+7 more)

### Community 11 - "test_webhooks_api.py"
Cohesion: 0.07
Nodes (11): client(), TestDashboardAPIEvents, TestDashboardAPIStatus, TestDashboardAPITools, TestDashboardAPIWorkflowRuns, TestDashboardAPIWorkflows, TestGitHubWebhook, TestHealthEndpoint (+3 more)

### Community 12 - "EventBus"
Cohesion: 0.13
Nodes (3): Event, TestEventBus, EventBus

### Community 13 - "backend/webhooks/server.py"
Cohesion: 0.11
Nodes (10): api_agent_conversations(), api_events(), api_logs(), api_model_config(), api_status(), api_tools(), api_workflow_runs(), api_workflows() (+2 more)

### Community 14 - "load_all_workflows()"
Cohesion: 0.13
Nodes (5): TestWorkflowLoader, TestLoadAllWorkflows, TestLoadWorkflow, load_all_workflows(), load_workflow()

### Community 15 - "security/secrets.py"
Cohesion: 0.13
Nodes (3): _strip_html(), AppSecrets, get_secrets()

### Community 16 - "asyncio"
Cohesion: 0.14
Nodes (4): _mock_response(), TestIronClawEdgeCases, TestOrchestratorEdgeCases, _async_tool()

### Community 17 - "AgentEvent"
Cohesion: 0.15
Nodes (4): TestAgentEvent, AgentEvent, TestAgentEvent, TestEventBus

### Community 19 - "Orchestrator"
Cohesion: 0.16
Nodes (4): Orchestrator, ToolOutput, TestOrchestrator, mock_tool()

### Community 20 - "Base"
Cohesion: 0.12
Nodes (6): AgentLog, AgentMemory, Base, TestAgentMemoryModel, TestAgentLogsAPI, db_session()

### Community 21 - "test_webhook_security.py"
Cohesion: 0.10
Nodes (7): _github_signature(), secured_client(), _slack_signature(), TestGitHubWebhookSecurity, TestJenkinsWebhookSecurity, TestJiraWebhookSecurity, TestSlackWebhookSecurity

### Community 23 - "verify_webhook_signature()"
Cohesion: 0.14
Nodes (5): verify_webhook_signature(), TestAppSecrets, TestVerifyWebhookSignature, verify_webhook_signature(), TestVerifyWebhookSignature

### Community 24 - "ConversationMemory"
Cohesion: 0.19
Nodes (3): ConversationMemory, TestConversationMemory, TestConversationMemory

### Community 25 - "TestWorkflowEngine"
Cohesion: 0.15
Nodes (7): load_all_workflows(), load_workflow(), WorkflowAction, WorkflowDefinition, TestWorkflowAction, TestWorkflowDefinition, TestWorkflowEngine

### Community 26 - "test_webhooks.py"
Cohesion: 0.11
Nodes (6): client(), TestGitHubWebhook, TestHealthEndpoint, TestJenkinsWebhook, TestJiraWebhook, TestSlackWebhook

### Community 27 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 34 - "fixture"
Cohesion: 0.13
Nodes (7): async_tool_func(), db_session(), mock_ironclaw_response(), _reset_db_globals(), _reset_secrets_cache(), sample_tool_func(), _tool()

### Community 38 - "backend/main.py"
Cohesion: 0.22
Nodes (6): _agent_summarize(), _build_orchestrator(), run(), _setup_workflow_engine(), webhook_server(), _wire_app()

### Community 39 - "_import_main()"
Cohesion: 0.18
Nodes (3): _import_main(), TestCLIEntryPoint, TestOrchestratorWiring

### Community 43 - "main.py"
Cohesion: 0.24
Nodes (6): _agent_summarize(), _build_orchestrator(), chat(), run(), _setup_workflow_engine(), webhook_server()

### Community 46 - "test_agent.py"
Cohesion: 0.29
Nodes (3): ActionPlan, PlanStep, TestPlanModels

### Community 51 - "get_session()"
Cohesion: 0.22
Nodes (3): TestSessionManagement, get_engine(), get_session()

### Community 52 - "IronClawResponse"
Cohesion: 0.31
Nodes (4): IronClawAction, IronClawResponse, TestIronClawAction, TestIronClawResponse

### Community 61 - "AgentConversation"
Cohesion: 0.47
Nodes (3): AgentConversation, TestAgentConversationModel, TestDashboardAPIConversations

## Knowledge Gaps
- **7 isolated node(s):** `react-dom`, `@types/node`, `@types/react`, `@types/react-dom`, `autoprefixer` (+2 more)
  These have ≤1 connection - possible missing edges. (Counts symbols only; 448 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **62 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_secrets()` connect `get_secrets()` to `IronClawClient`, `GmailIntegration`, `database/models.py`, `backend/webhooks/server.py`, `security/secrets.py`, `test_webhook_security.py`, `verify_webhook_signature()`, `test_webhooks.py`, `tenacity`, `GitHubIntegration`, `GmailIntegration`, `SlackIntegration`, `GitHubIntegration`, `SlackIntegration`, `patch`, `JiraIntegration`, `backend/main.py`, `test_deployment_readiness.py`, `JiraIntegration`, `main.py`, `LLMClient`, `ironclaw.py`, `test_agent.py`, `ConfluenceIntegration`, `get_session()`, `backend/integrations/gmail.py`, `AppSecrets`?**
  _High betweenness centrality (0.115) - this node is a cross-community bridge._
- **Are the 36 inferred relationships involving `IronClawClient` (e.g. with `Orchestrator` and `_agent_summarize()`) actually correct?**
  _`IronClawClient` has 36 INFERRED edges - model-reasoned connections that need verification._
- **What connects `react-dom`, `@types/node`, `@types/react` to the rest of the system?**
  _7 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `IronClawClient` be split into smaller, more focused modules?**
  _Cohesion score 0.0518326545723806 - nodes in this community are weakly interconnected._
- **Why does `Orchestrator` connect `Orchestrator` to `backend/main.py`, `WorkflowEngine`, `main.py`, `LLMClient`, `test_agent.py`, `security/secrets.py`, `asyncio`, `Planner`, `get_session()`, `ConversationMemory`, `Any`, `asyncio`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `AgentEvent` (e.g. with `SlackCommandGateway` and `EventBus`) actually correct?**
  _`AgentEvent` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Should `GmailIntegration` be split into smaller, more focused modules?**
  _Cohesion score 0.05952380952380952 - nodes in this community are weakly interconnected._