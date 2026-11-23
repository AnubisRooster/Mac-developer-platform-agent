# Graph Report - Mac-developer-platform-agent  (2026-11-23)

## Corpus Check
- 121 files · ~149,822 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 4, .ini 2, .example 1)

## Summary
- 1415 nodes · 2776 edges · 88 communities (42 shown, 46 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 204 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- logging
- main.py
- test_agent.py
- test_deployment_readiness.py
- Orchestrator
- Orchestrator
- package.json
- backend/tests/conftest.py
- redact()
- api.ts
- tests/test_integrations.py
- ConversationMemory
- AgentEvent
- WorkflowEngine
- integrations
- IronClawClient
- test_edge_cases.py
- backend/webhooks/server.py
- test_webhook_security.py
- tests/test_database.py
- tests/test_workflows.py
- get_session()
- asyncio
- test_model_config.py
- test_webhooks_api.py
- SlackCommandGateway
- backend/main.py
- SlackIntegration
- compilerOptions
- EventBus
- GmailIntegration
- test_ironclaw.py
- JenkinsIntegration
- patch
- args
- AgentConversation
- AgentEvent
- GitHubIntegration
- verify_webhook_signature()
- args
- backend/database/models.py
- JiraIntegration
- get
- args
- test_webhooks.py
- Event
- ConfluenceIntegration
- get_secrets()
- EventBus
- GmailIntegration
- SlackIntegration
- TestModelConfigAPI
- WorkflowEngine
- workflows/build_failed.yaml
- workflows/jira_created.yaml
- workflows/pr_opened.yaml
- ToolOutput
- ConversationMemory
- AgentLog
- GitHubIntegration
- JiraIntegration
- _strip_html()
- TestIronClawModelConfig
- .run_workflow()
- TestGitHubWebhook
- _ensure_database_tables()
- next.config.js

## God Nodes (most connected - your core abstractions)
1. `get_secrets()` - 67 edges
2. `AgentEvent` - 66 edges
3. `AgentEvent` - 35 edges
4. `Orchestrator` - 33 edges
5. `WorkflowEngine` - 33 edges
6. `ConversationMemory` - 31 edges
7. `EventBus` - 29 edges
8. `get_session()` - 28 edges
9. `IronClawClient` - 27 edges
10. `WorkflowDefinition` - 24 edges

## Surprising Connections (you probably didn't know these)
- `Orchestrator` --uses--> `ConversationMemory`  [INFERRED]
  backend/agent/orchestrator.py → agent/memory.py
- `Orchestrator` --uses--> `ToolOutput`  [INFERRED]
  agent/orchestrator.py → backend/database/models.py
- `TestOrchestrator` --uses--> `Orchestrator`  [INFERRED]
  tests/test_agent.py → agent/orchestrator.py
- `db_session()` --uses--> `Base`  [INFERRED]
  tests/test_database.py → backend/database/models.py
- `EventBus` --uses--> `Event`  [INFERRED]
  events/bus.py → backend/database/models.py

## Import Cycles
- None detected.

## Communities (88 total, 46 thin omitted)

### Community 0 - "logging"
Cohesion: 0.06
Nodes (4): _strip_html(), AppSecrets, get_secrets(), verify_webhook_signature()

### Community 1 - "main.py"
Cohesion: 0.05
Nodes (16): LLMClient, ConfluenceIntegration, _chat_loop(), _print_banner(), start_chat(), _agent_summarize(), _build_orchestrator(), chat() (+8 more)

### Community 2 - "test_agent.py"
Cohesion: 0.06
Nodes (9): ToolRegistry, ActionPlan, Planner, PlanStep, TestOrchestrator, TestPlanModels, TestPlanner, TestToolCallPattern (+1 more)

### Community 3 - "test_deployment_readiness.py"
Cohesion: 0.05
Nodes (11): _import_main(), TestAppWiring, TestCLIEntryPoint, TestDatabaseTablesExist, TestFastAPIAppImportable, TestOrchestratorWiring, TestWorkflowEngineLoad, TestWorkflowLoading (+3 more)

### Community 4 - "Orchestrator"
Cohesion: 0.05
Nodes (6): Orchestrator, TestToolRegistry, TestToolSchema, ToolEntry, ToolRegistry, ToolSchema

### Community 5 - "Orchestrator"
Cohesion: 0.08
Nodes (8): Orchestrator, IronClawAction, IronClawResponse, TestOrchestratorEdgeCases, _async_tool(), TestIronClawResponse, TestOrchestrator, mock_tool()

### Community 6 - "package.json"
Cohesion: 0.07
Nodes (35): dependencies, next@^14.2.0, react@^18.3.0, react-dom@^18.3.0, devDependencies, autoprefixer@^10.4.0, postcss@^8.4.0, tailwindcss@^3.4.0 (+27 more)

### Community 7 - "backend/tests/conftest.py"
Cohesion: 0.07
Nodes (9): async_tool_func(), db_session(), mock_ironclaw_response(), _reset_db_globals(), _reset_secrets_cache(), sample_tool_func(), _tool(), env_secrets() (+1 more)

### Community 8 - "redact()"
Cohesion: 0.07
Nodes (9): redact(), RedactingFilter, TestSecurityEdgeCases, TestRedact, TestRedactingFilter, redact(), RedactingFilter, TestRedact (+1 more)

### Community 9 - "api.ts"
Cohesion: 0.10
Nodes (23): EventsPage(), sourceBadge(), LEVEL_COLORS, LEVELS, StatusPage(), connectorColor(), ToolsPage(), statusBadge() (+15 more)

### Community 10 - "tests/test_integrations.py"
Cohesion: 0.07
Nodes (5): TestConfluenceIntegration, TestGitHubIntegration, TestGmailIntegration, TestJiraIntegration, TestSlackIntegration

### Community 11 - "ConversationMemory"
Cohesion: 0.09
Nodes (3): ConversationMemory, TestConversationMemory, TestConversationMemory

### Community 12 - "AgentEvent"
Cohesion: 0.11
Nodes (5): TestAgentEvent, AgentEvent, TestAgentEvent, TestEventBus, TestWorkflowEngine

### Community 13 - "WorkflowEngine"
Cohesion: 0.16
Nodes (5): TestWorkflowEngineEdgeCases, TestWorkflowEngine, WorkflowEngine, WorkflowAction, WorkflowDefinition

### Community 14 - "integrations"
Cohesion: 0.07
Nodes (27): agent, log_file, log_level, name, version, enabled, database, url (+19 more)

### Community 16 - "test_edge_cases.py"
Cohesion: 0.14
Nodes (3): TestEventSource, TestWorkflowAction, EventSource

### Community 17 - "backend/webhooks/server.py"
Cohesion: 0.18
Nodes (11): EventSource, api_events(), api_workflow_runs(), github_webhook(), jenkins_webhook(), jira_webhook(), _persist_log(), set_model_config() (+3 more)

### Community 18 - "test_webhook_security.py"
Cohesion: 0.11
Nodes (7): _github_signature(), secured_client(), _slack_signature(), TestGitHubWebhookSecurity, TestJenkinsWebhookSecurity, TestJiraWebhookSecurity, TestSlackWebhookSecurity

### Community 19 - "tests/test_database.py"
Cohesion: 0.12
Nodes (8): TestWorkflowRunModel, TestDashboardAPIWorkflowRuns, Base, CachedSummary, WorkflowRun, db_session(), TestCachedSummaryModel, TestWorkflowRunModel

### Community 20 - "tests/test_workflows.py"
Cohesion: 0.15
Nodes (8): load_all_workflows(), load_workflow(), WorkflowAction, WorkflowDefinition, TestLoadWorkflow, TestWorkflowAction, TestWorkflowDefinition, load_workflow()

### Community 21 - "get_session()"
Cohesion: 0.17
Nodes (3): TestSessionManagement, get_engine(), get_session()

### Community 22 - "asyncio"
Cohesion: 0.15
Nodes (3): _mock_response(), TestIronClawEdgeCases, TestSlackGatewayEdgeCases

### Community 23 - "test_model_config.py"
Cohesion: 0.14
Nodes (5): _mock_get_response(), _mock_response(), TestAgentLogTable, TestModelTest, TestOpenRouterFallback

### Community 24 - "test_webhooks_api.py"
Cohesion: 0.10
Nodes (9): client(), TestDashboardAPIStatus, TestDashboardAPITools, TestDashboardAPIWorkflows, TestGitHubWebhook, TestHealthEndpoint, TestJenkinsWebhook, TestJiraWebhook (+1 more)

### Community 26 - "backend/main.py"
Cohesion: 0.16
Nodes (8): _agent_summarize(), _build_orchestrator(), cli(), run(), _setup_logging(), _setup_workflow_engine(), webhook_server(), _wire_app()

### Community 28 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 31 - "test_ironclaw.py"
Cohesion: 0.21
Nodes (4): _mock_get_response(), _mock_response(), TestIronClawAction, TestIronClawClient

### Community 34 - "args"
Cohesion: 0.12
Nodes (15): actions, args, description, on_failure, tool, body, channel, labels (+7 more)

### Community 35 - "AgentConversation"
Cohesion: 0.15
Nodes (4): AgentConversation, TestAgentConversationModel, TestAPIEndpointEdgeCases, TestDashboardAPIConversations

### Community 36 - "AgentEvent"
Cohesion: 0.22
Nodes (6): AgentEvent, github_webhook(), health(), jenkins_webhook(), jira_webhook(), slack_webhook()

### Community 38 - "verify_webhook_signature()"
Cohesion: 0.20
Nodes (3): TestVerifyWebhookSignature, verify_webhook_signature(), TestVerifyWebhookSignature

### Community 39 - "args"
Cohesion: 0.13
Nodes (14): actions, args, description, on_failure, tool, channel, github_url, pr_number (+6 more)

### Community 40 - "backend/database/models.py"
Cohesion: 0.20
Nodes (8): AgentMemory, Base, Event, get_engine(), get_session(), ToolOutput, WorkflowRun, TestAgentMemoryModel

### Community 42 - "get"
Cohesion: 0.14
Nodes (7): api_agent_conversations(), api_logs(), api_model_config(), api_status(), api_tools(), api_workflows(), health()

### Community 43 - "args"
Cohesion: 0.14
Nodes (13): actions, args, description, on_failure, tool, build_number, channel, instruction (+5 more)

### Community 44 - "test_webhooks.py"
Cohesion: 0.14
Nodes (5): client(), TestHealthEndpoint, TestJenkinsWebhook, TestJiraWebhook, TestSlackWebhook

### Community 45 - "Event"
Cohesion: 0.17
Nodes (4): TestEventModel, TestDashboardAPIEvents, Event, TestEventModel

### Community 47 - "get_secrets()"
Cohesion: 0.21
Nodes (4): TestAppSecrets, AppSecrets, get_secrets(), TestAppSecrets

### Community 53 - "workflows/build_failed.yaml"
Cohesion: 0.18
Nodes (10): actions, args, description, on_failure, tool, channel, description, enabled (+2 more)

### Community 54 - "workflows/jira_created.yaml"
Cohesion: 0.18
Nodes (10): actions, args, description, on_failure, tool, channel, description, enabled (+2 more)

### Community 55 - "workflows/pr_opened.yaml"
Cohesion: 0.18
Nodes (10): actions, args, description, on_failure, tool, channel, description, enabled (+2 more)

### Community 56 - "ToolOutput"
Cohesion: 0.22
Nodes (3): TestToolOutputModel, ToolOutput, TestToolOutputModel

## Knowledge Gaps
- **46 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_secrets()` connect `get_secrets()` to `logging`, `main.py`, `test_agent.py`, `test_deployment_readiness.py`, `backend/tests/conftest.py`, `IronClawClient`, `backend/webhooks/server.py`, `test_webhook_security.py`, `get_session()`, `backend/main.py`, `SlackIntegration`, `GmailIntegration`, `JenkinsIntegration`, `patch`, `AgentEvent`, `GitHubIntegration`, `verify_webhook_signature()`, `backend/database/models.py`, `JiraIntegration`, `get`, `test_webhooks.py`, `ConfluenceIntegration`, `GmailIntegration`, `SlackIntegration`, `GitHubIntegration`, `JiraIntegration`?**
  _High betweenness centrality (0.105) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `AgentEvent` (e.g. with `SlackCommandGateway` and `EventBus`) actually correct?**
  _`AgentEvent` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Should `logging` be split into smaller, more focused modules?**
  _Cohesion score 0.055135135135135134 - nodes in this community are weakly interconnected._
- **Why does `Orchestrator` connect `Orchestrator` to `logging`, `main.py`, `test_agent.py`, `backend/database/models.py`, `ConversationMemory`, `test_edge_cases.py`, `ToolOutput`, `backend/main.py`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Should `main.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05009920634920635 - nodes in this community are weakly interconnected._
- **Why does `AgentEvent` connect `AgentEvent` to `AgentEvent`, `WorkflowEngine`, `test_edge_cases.py`, `backend/webhooks/server.py`, `tests/test_workflows.py`, `get_session()`, `asyncio`, `SlackCommandGateway`, `EventBus`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Should `test_agent.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05513784461152882 - nodes in this community are weakly interconnected._