# Graph Report - Mac-developer-platform-agent  (2026-10-05)

## Corpus Check
- 121 files · ~228,861 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 4, .ini 2, .example 1)

## Summary
- 1309 nodes · 2709 edges · 97 communities (39 shown, 58 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 251 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- logging
- IronClawClient
- redact()
- package.json
- api.ts
- ToolRegistry
- ConversationMemory
- GitHubIntegration
- cli()
- WorkflowEngine
- AgentEvent
- test_edge_cases.py
- EventBus
- test_webhook_security.py
- asyncio
- tests/test_workflows.py
- load_all_workflows()
- AgentEvent
- test_webhooks_api.py
- Orchestrator
- backend/webhooks/server.py
- compilerOptions
- get
- workflows/engine.py
- GmailIntegration
- SlackIntegration
- get_secrets()
- database/models.py
- fixture
- patch
- main.py
- AgentConversation
- _import_main()
- ToolRegistry
- Orchestrator
- test_deployment_readiness.py
- backend/database/models.py
- JiraIntegration
- test_webhooks.py
- LLMClient
- AgentLog
- backend/main.py
- ConfluenceIntegration
- json
- get_session()
- Planner
- GmailIntegration
- SlackIntegration
- TestIronClawEdgeCases
- TestOrchestratorEdgeCases
- test_agent.py
- IronClawResponse
- ConversationMemory
- verify_webhook_signature()
- TestWorkflowEngine
- JiraIntegration
- Event
- backend/tests/test_integrations.py
- asyncio
- fixture
- ConfluenceIntegration
- JenkinsIntegration
- TestJenkinsIntegration
- get_engine()
- TestSlackCommandGateway
- TestAppWiring
- TestGmailIntegration
- TestFastAPIAppImportable
- TestConfluenceIntegration
- TestJiraIntegration
- TestGitHubWebhook
- TestToolCallPattern
- next.config.js

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

## Communities (97 total, 58 thin omitted)

### Community 0 - "logging"
Cohesion: 0.05
Nodes (4): _strip_html(), AppSecrets, get_secrets(), verify_webhook_signature()

### Community 1 - "IronClawClient"
Cohesion: 0.05
Nodes (11): IronClawClient, _mock_get_response(), _mock_response(), TestIronClawClient, _mock_get_response(), _mock_response(), TestAgentLogTable, TestIronClawModelConfig (+3 more)

### Community 2 - "redact()"
Cohesion: 0.06
Nodes (11): cli(), _setup_logging(), redact(), RedactingFilter, TestSecurityEdgeCases, TestRedact, TestRedactingFilter, redact() (+3 more)

### Community 3 - "package.json"
Cohesion: 0.05
Nodes (35): dependencies, next, react, react-dom, devDependencies, autoprefixer, postcss, tailwindcss (+27 more)

### Community 4 - "api.ts"
Cohesion: 0.10
Nodes (23): EventsPage(), sourceBadge(), LEVEL_COLORS, LEVELS, StatusPage(), connectorColor(), ToolsPage(), statusBadge() (+15 more)

### Community 5 - "ToolRegistry"
Cohesion: 0.08
Nodes (5): TestToolRegistry, TestToolSchema, ToolEntry, ToolRegistry, ToolSchema

### Community 6 - "ConversationMemory"
Cohesion: 0.09
Nodes (3): ConversationMemory, TestConversationMemory, TestConversationMemory

### Community 7 - "GitHubIntegration"
Cohesion: 0.11
Nodes (4): GitHubIntegration, TestGitHubIntegration, GitHubIntegration, TestGitHubIntegration

### Community 8 - "cli()"
Cohesion: 0.09
Nodes (7): _chat_loop(), _print_banner(), start_chat(), cli(), _setup_logging(), TestCLIChat, TestMainCLI

### Community 9 - "WorkflowEngine"
Cohesion: 0.16
Nodes (6): WorkflowRun, TestWorkflowEngineEdgeCases, TestWorkflowEngine, WorkflowEngine, WorkflowAction, WorkflowDefinition

### Community 10 - "AgentEvent"
Cohesion: 0.11
Nodes (4): EventBus, AgentEvent, TestWorkflowEngineLoad, WorkflowEngine

### Community 11 - "test_edge_cases.py"
Cohesion: 0.14
Nodes (3): TestEventSource, TestWorkflowAction, EventSource

### Community 12 - "EventBus"
Cohesion: 0.14
Nodes (3): Event, TestEventBus, EventBus

### Community 13 - "test_webhook_security.py"
Cohesion: 0.11
Nodes (7): _github_signature(), secured_client(), _slack_signature(), TestGitHubWebhookSecurity, TestJenkinsWebhookSecurity, TestJiraWebhookSecurity, TestSlackWebhookSecurity

### Community 15 - "tests/test_workflows.py"
Cohesion: 0.15
Nodes (8): load_all_workflows(), load_workflow(), WorkflowAction, WorkflowDefinition, TestLoadWorkflow, TestWorkflowAction, TestWorkflowDefinition, load_workflow()

### Community 16 - "load_all_workflows()"
Cohesion: 0.13
Nodes (4): TestWorkflowLoading, TestWorkflowLoader, TestLoadAllWorkflows, load_all_workflows()

### Community 17 - "AgentEvent"
Cohesion: 0.16
Nodes (4): TestAgentEvent, AgentEvent, TestAgentEvent, TestEventBus

### Community 18 - "test_webhooks_api.py"
Cohesion: 0.10
Nodes (9): client(), TestDashboardAPIStatus, TestDashboardAPITools, TestDashboardAPIWorkflows, TestGitHubWebhook, TestHealthEndpoint, TestJenkinsWebhook, TestJiraWebhook (+1 more)

### Community 19 - "Orchestrator"
Cohesion: 0.18
Nodes (4): Orchestrator, ToolOutput, TestOrchestrator, mock_tool()

### Community 20 - "backend/webhooks/server.py"
Cohesion: 0.23
Nodes (9): EventSource, github_webhook(), jenkins_webhook(), jira_webhook(), _persist_log(), set_model_config(), set_openrouter_key(), slack_webhook() (+1 more)

### Community 21 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 22 - "get"
Cohesion: 0.11
Nodes (9): api_agent_conversations(), api_events(), api_logs(), api_model_config(), api_status(), api_tools(), api_workflow_runs(), api_workflows() (+1 more)

### Community 23 - "workflows/engine.py"
Cohesion: 0.14
Nodes (5): TestWorkflowRunModel, TestDashboardAPIWorkflowRuns, WorkflowRun, TestWorkflowRunModel, _is_coroutine()

### Community 26 - "get_secrets()"
Cohesion: 0.18
Nodes (4): TestAppSecrets, AppSecrets, get_secrets(), TestAppSecrets

### Community 27 - "database/models.py"
Cohesion: 0.21
Nodes (5): Base, CachedSummary, ToolOutput, TestCachedSummaryModel, TestToolOutputModel

### Community 28 - "fixture"
Cohesion: 0.13
Nodes (7): async_tool_func(), db_session(), mock_ironclaw_response(), _reset_db_globals(), _reset_secrets_cache(), sample_tool_func(), _tool()

### Community 30 - "main.py"
Cohesion: 0.22
Nodes (6): _agent_summarize(), _build_orchestrator(), chat(), run(), _setup_workflow_engine(), webhook_server()

### Community 31 - "AgentConversation"
Cohesion: 0.16
Nodes (4): AgentConversation, TestAgentConversationModel, TestAPIEndpointEdgeCases, TestDashboardAPIConversations

### Community 32 - "_import_main()"
Cohesion: 0.18
Nodes (3): _import_main(), TestCLIEntryPoint, TestOrchestratorWiring

### Community 36 - "backend/database/models.py"
Cohesion: 0.19
Nodes (6): AgentMemory, Base, get_engine(), get_session(), TestAgentMemoryModel, db_session()

### Community 38 - "test_webhooks.py"
Cohesion: 0.14
Nodes (5): client(), TestHealthEndpoint, TestJenkinsWebhook, TestJiraWebhook, TestSlackWebhook

### Community 41 - "backend/main.py"
Cohesion: 0.24
Nodes (6): _agent_summarize(), _build_orchestrator(), run(), _setup_workflow_engine(), webhook_server(), _wire_app()

### Community 43 - "json"
Cohesion: 0.32
Nodes (5): github_webhook(), health(), jenkins_webhook(), jira_webhook(), slack_webhook()

### Community 44 - "get_session()"
Cohesion: 0.22
Nodes (3): TestSessionManagement, TestToolOutputModel, get_session()

### Community 51 - "test_agent.py"
Cohesion: 0.33
Nodes (3): ActionPlan, PlanStep, TestPlanModels

### Community 52 - "IronClawResponse"
Cohesion: 0.31
Nodes (4): IronClawAction, IronClawResponse, TestIronClawAction, TestIronClawResponse

### Community 54 - "verify_webhook_signature()"
Cohesion: 0.29
Nodes (3): TestVerifyWebhookSignature, verify_webhook_signature(), TestVerifyWebhookSignature

### Community 57 - "Event"
Cohesion: 0.25
Nodes (4): TestEventModel, TestDashboardAPIEvents, Event, TestEventModel

### Community 66 - "get_engine()"
Cohesion: 0.29
Nodes (3): TestDatabaseTablesExist, _ensure_database_tables(), get_engine()

## Knowledge Gaps
- **50 isolated node(s):** `nextConfig`, `name`, `version`, `private`, `dev` (+45 more)
  These have ≤1 connection - possible missing edges. (Counts symbols only; 449 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **58 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_secrets()` connect `get_secrets()` to `logging`, `IronClawClient`, `GitHubIntegration`, `test_webhook_security.py`, `backend/webhooks/server.py`, `get`, `GmailIntegration`, `SlackIntegration`, `database/models.py`, `patch`, `main.py`, `test_deployment_readiness.py`, `backend/database/models.py`, `JiraIntegration`, `test_webhooks.py`, `LLMClient`, `backend/main.py`, `ConfluenceIntegration`, `json`, `GmailIntegration`, `SlackIntegration`, `test_agent.py`, `JiraIntegration`, `ConfluenceIntegration`, `JenkinsIntegration`, `get_engine()`?**
  _High betweenness centrality (0.115) - this node is a cross-community bridge._
- **Are the 36 inferred relationships involving `IronClawClient` (e.g. with `Orchestrator` and `_agent_summarize()`) actually correct?**
  _`IronClawClient` has 36 INFERRED edges - model-reasoned connections that need verification._
- **What connects `nextConfig`, `name`, `version` to the rest of the system?**
  _50 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `logging` be split into smaller, more focused modules?**
  _Cohesion score 0.05225576111652061 - nodes in this community are weakly interconnected._
- **Why does `Orchestrator` connect `Orchestrator` to `logging`, `Any`, `ConversationMemory`, `LLMClient`, `backend/main.py`, `test_edge_cases.py`, `get_session()`, `Planner`, `TestOrchestratorEdgeCases`, `test_agent.py`, `asyncio`, `main.py`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `AgentEvent` (e.g. with `SlackCommandGateway` and `EventBus`) actually correct?**
  _`AgentEvent` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Should `IronClawClient` be split into smaller, more focused modules?**
  _Cohesion score 0.050721954831543875 - nodes in this community are weakly interconnected._