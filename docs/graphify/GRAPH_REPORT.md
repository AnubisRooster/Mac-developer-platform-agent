# Graph Report - Mac-developer-platform-agent  (2026-11-16)

## Corpus Check
- 121 files · ~149,757 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 4, .ini 2, .example 1)

## Summary
- 1415 nodes · 2829 edges · 103 communities (48 shown, 55 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 257 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- logging
- test_agent.py
- package.json
- Orchestrator
- redact()
- api.ts
- ToolRegistry
- tests/test_integrations.py
- SlackCommandGateway
- load_all_workflows()
- WorkflowEngine
- integrations
- GmailIntegration
- get_secrets()
- verify_webhook_signature()
- EventBus
- test_webhook_security.py
- IronClawClient
- EventBus
- AgentEvent
- test_webhooks_api.py
- ConversationMemory
- backend/main.py
- SlackIntegration
- test_webhooks.py
- compilerOptions
- test_edge_cases.py
- database/models.py
- get_session()
- Event
- GmailIntegration
- AgentEvent
- fixture
- patch
- args
- LLMClient
- WorkflowRun
- _import_main()
- GitHubIntegration
- test_ironclaw.py
- WorkflowDefinition
- args
- test_cli_main.py
- test_deployment_readiness.py
- JiraIntegration
- get
- args
- main.py
- cli()
- AgentLog
- Orchestrator
- asyncio
- ConfluenceIntegration
- SlackIntegration
- workflows/build_failed.yaml
- workflows/jira_created.yaml
- workflows/pr_opened.yaml
- ConversationMemory
- GitHubIntegration
- test_model_config.py
- TestWorkflowEngine
- JiraIntegration
- TestAPIEndpointEdgeCases
- ConfluenceIntegration
- TestModelConfigAPI
- workflows/engine.py
- get_engine()
- _strip_html()
- AgentConversation
- TestAppWiring
- TestFastAPIAppImportable
- AgentMemory
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
- `TestOrchestrator` --uses--> `Orchestrator`  [INFERRED]
  tests/test_agent.py → agent/orchestrator.py
- `TestEventModel` --uses--> `Event`  [INFERRED]
  tests/test_database.py → backend/database/models.py
- `WorkflowEngine` --uses--> `WorkflowRun`  [INFERRED]
  workflows/engine.py → backend/database/models.py
- `TestToolOutputModel` --uses--> `ToolOutput`  [INFERRED]
  tests/test_database.py → backend/database/models.py

## Import Cycles
- None detected.

## Communities (103 total, 55 thin omitted)

### Community 0 - "logging"
Cohesion: 0.06
Nodes (4): _strip_html(), AppSecrets, get_secrets(), verify_webhook_signature()

### Community 1 - "test_agent.py"
Cohesion: 0.05
Nodes (9): ToolRegistry, ActionPlan, Planner, PlanStep, TestOrchestrator, TestPlanModels, TestPlanner, TestToolCallPattern (+1 more)

### Community 2 - "package.json"
Cohesion: 0.07
Nodes (35): dependencies, next@^14.2.0, react@^18.3.0, react-dom@^18.3.0, devDependencies, autoprefixer@^10.4.0, postcss@^8.4.0, tailwindcss@^3.4.0 (+27 more)

### Community 3 - "Orchestrator"
Cohesion: 0.10
Nodes (10): Orchestrator, IronClawAction, IronClawResponse, ToolOutput, TestOrchestratorEdgeCases, _async_tool(), TestIronClawAction, TestIronClawResponse (+2 more)

### Community 4 - "redact()"
Cohesion: 0.07
Nodes (9): redact(), RedactingFilter, TestSecurityEdgeCases, TestRedact, TestRedactingFilter, redact(), RedactingFilter, TestRedact (+1 more)

### Community 5 - "api.ts"
Cohesion: 0.10
Nodes (23): EventsPage(), sourceBadge(), LEVEL_COLORS, LEVELS, StatusPage(), connectorColor(), ToolsPage(), statusBadge() (+15 more)

### Community 6 - "ToolRegistry"
Cohesion: 0.08
Nodes (5): TestToolRegistry, TestToolSchema, ToolEntry, ToolRegistry, ToolSchema

### Community 7 - "tests/test_integrations.py"
Cohesion: 0.07
Nodes (5): TestConfluenceIntegration, TestGitHubIntegration, TestGmailIntegration, TestJiraIntegration, TestSlackIntegration

### Community 8 - "SlackCommandGateway"
Cohesion: 0.11
Nodes (3): SlackCommandGateway, TestSlackGatewayEdgeCases, TestSlackCommandGateway

### Community 9 - "load_all_workflows()"
Cohesion: 0.11
Nodes (6): TestWorkflowLoading, TestWorkflowLoader, TestLoadAllWorkflows, TestLoadWorkflow, load_all_workflows(), load_workflow()

### Community 10 - "WorkflowEngine"
Cohesion: 0.16
Nodes (5): TestWorkflowEngineEdgeCases, TestWorkflowEngine, WorkflowEngine, WorkflowAction, WorkflowDefinition

### Community 11 - "integrations"
Cohesion: 0.07
Nodes (27): agent, log_file, log_level, name, version, enabled, database, url (+19 more)

### Community 12 - "GmailIntegration"
Cohesion: 0.12
Nodes (3): GmailIntegration, JenkinsIntegration, TestJenkinsIntegration

### Community 13 - "get_secrets()"
Cohesion: 0.17
Nodes (12): EventSource, api_model_config(), api_status(), github_webhook(), jenkins_webhook(), jira_webhook(), _persist_log(), set_model_config() (+4 more)

### Community 14 - "verify_webhook_signature()"
Cohesion: 0.11
Nodes (6): TestAppSecrets, TestVerifyWebhookSignature, AppSecrets, verify_webhook_signature(), TestAppSecrets, TestVerifyWebhookSignature

### Community 15 - "EventBus"
Cohesion: 0.14
Nodes (4): Event, TestEventBus, TestEventSource, EventBus

### Community 16 - "test_webhook_security.py"
Cohesion: 0.11
Nodes (7): _github_signature(), secured_client(), _slack_signature(), TestGitHubWebhookSecurity, TestJenkinsWebhookSecurity, TestJiraWebhookSecurity, TestSlackWebhookSecurity

### Community 17 - "IronClawClient"
Cohesion: 0.18
Nodes (4): IronClawClient, TestIronClawModelConfig, TestModelTest, TestOpenRouterFallback

### Community 18 - "EventBus"
Cohesion: 0.12
Nodes (3): EventBus, TestWorkflowEngineLoad, WorkflowEngine

### Community 19 - "AgentEvent"
Cohesion: 0.16
Nodes (4): TestAgentEvent, AgentEvent, TestAgentEvent, TestEventBus

### Community 20 - "test_webhooks_api.py"
Cohesion: 0.10
Nodes (9): client(), TestDashboardAPIStatus, TestDashboardAPITools, TestDashboardAPIWorkflows, TestGitHubWebhook, TestHealthEndpoint, TestJenkinsWebhook, TestJiraWebhook (+1 more)

### Community 22 - "ConversationMemory"
Cohesion: 0.19
Nodes (3): ConversationMemory, TestConversationMemory, TestConversationMemory

### Community 23 - "backend/main.py"
Cohesion: 0.16
Nodes (8): _agent_summarize(), _build_orchestrator(), cli(), run(), _setup_logging(), _setup_workflow_engine(), webhook_server(), _wire_app()

### Community 25 - "test_webhooks.py"
Cohesion: 0.11
Nodes (6): client(), TestGitHubWebhook, TestHealthEndpoint, TestJenkinsWebhook, TestJiraWebhook, TestSlackWebhook

### Community 26 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 28 - "database/models.py"
Cohesion: 0.18
Nodes (5): get_engine(), get_session(), Base, CachedSummary, TestCachedSummaryModel

### Community 29 - "get_session()"
Cohesion: 0.16
Nodes (5): TestSessionManagement, TestToolOutputModel, get_session(), ToolOutput, TestToolOutputModel

### Community 30 - "Event"
Cohesion: 0.12
Nodes (4): TestEventModel, TestDashboardAPIEvents, Event, TestEventModel

### Community 32 - "AgentEvent"
Cohesion: 0.23
Nodes (6): AgentEvent, github_webhook(), health(), jenkins_webhook(), jira_webhook(), slack_webhook()

### Community 33 - "fixture"
Cohesion: 0.13
Nodes (7): async_tool_func(), db_session(), mock_ironclaw_response(), _reset_db_globals(), _reset_secrets_cache(), sample_tool_func(), _tool()

### Community 35 - "args"
Cohesion: 0.12
Nodes (15): actions, args, description, on_failure, tool, body, channel, labels (+7 more)

### Community 36 - "LLMClient"
Cohesion: 0.19
Nodes (3): LLMClient, _agent_summarize(), TestLLMClient

### Community 37 - "WorkflowRun"
Cohesion: 0.16
Nodes (7): Base, WorkflowRun, TestWorkflowRunModel, TestDashboardAPIWorkflowRuns, WorkflowRun, db_session(), TestWorkflowRunModel

### Community 38 - "_import_main()"
Cohesion: 0.18
Nodes (3): _import_main(), TestCLIEntryPoint, TestOrchestratorWiring

### Community 40 - "test_ironclaw.py"
Cohesion: 0.26
Nodes (3): _mock_get_response(), _mock_response(), TestIronClawClient

### Community 41 - "WorkflowDefinition"
Cohesion: 0.20
Nodes (7): TestWorkflowAction, load_all_workflows(), load_workflow(), WorkflowAction, WorkflowDefinition, TestWorkflowAction, TestWorkflowDefinition

### Community 42 - "args"
Cohesion: 0.13
Nodes (14): actions, args, description, on_failure, tool, channel, github_url, pr_number (+6 more)

### Community 43 - "test_cli_main.py"
Cohesion: 0.18
Nodes (4): _chat_loop(), _print_banner(), start_chat(), TestCLIChat

### Community 46 - "get"
Cohesion: 0.14
Nodes (7): api_agent_conversations(), api_events(), api_logs(), api_tools(), api_workflow_runs(), api_workflows(), health()

### Community 47 - "args"
Cohesion: 0.14
Nodes (13): actions, args, description, on_failure, tool, build_number, channel, instruction (+5 more)

### Community 48 - "main.py"
Cohesion: 0.24
Nodes (5): _build_orchestrator(), chat(), run(), _setup_workflow_engine(), webhook_server()

### Community 49 - "cli()"
Cohesion: 0.20
Nodes (3): cli(), _setup_logging(), TestMainCLI

### Community 56 - "workflows/build_failed.yaml"
Cohesion: 0.18
Nodes (10): actions, args, description, on_failure, tool, channel, description, enabled (+2 more)

### Community 57 - "workflows/jira_created.yaml"
Cohesion: 0.18
Nodes (10): actions, args, description, on_failure, tool, channel, description, enabled (+2 more)

### Community 58 - "workflows/pr_opened.yaml"
Cohesion: 0.18
Nodes (10): actions, args, description, on_failure, tool, channel, description, enabled (+2 more)

### Community 61 - "test_model_config.py"
Cohesion: 0.22
Nodes (3): _mock_get_response(), _mock_response(), TestAgentLogTable

### Community 69 - "get_engine()"
Cohesion: 0.29
Nodes (3): TestDatabaseTablesExist, _ensure_database_tables(), get_engine()

### Community 71 - "AgentConversation"
Cohesion: 0.47
Nodes (3): AgentConversation, TestAgentConversationModel, TestDashboardAPIConversations

## Knowledge Gaps
- **55 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_secrets()` connect `get_secrets()` to `logging`, `test_agent.py`, `GmailIntegration`, `verify_webhook_signature()`, `test_webhook_security.py`, `IronClawClient`, `backend/main.py`, `SlackIntegration`, `test_webhooks.py`, `database/models.py`, `GmailIntegration`, `AgentEvent`, `patch`, `LLMClient`, `GitHubIntegration`, `test_deployment_readiness.py`, `JiraIntegration`, `main.py`, `ConfluenceIntegration`, `SlackIntegration`, `GitHubIntegration`, `JiraIntegration`, `ConfluenceIntegration`, `get_engine()`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **Are the 36 inferred relationships involving `IronClawClient` (e.g. with `Orchestrator` and `_agent_summarize()`) actually correct?**
  _`IronClawClient` has 36 INFERRED edges - model-reasoned connections that need verification._
- **Should `logging` be split into smaller, more focused modules?**
  _Cohesion score 0.055135135135135134 - nodes in this community are weakly interconnected._
- **Why does `Orchestrator` connect `Orchestrator` to `logging`, `test_agent.py`, `LLMClient`, `main.py`, `ConversationMemory`, `backend/main.py`, `test_edge_cases.py`, `get_session()`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `AgentEvent` (e.g. with `SlackCommandGateway` and `EventBus`) actually correct?**
  _`AgentEvent` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_agent.py` be split into smaller, more focused modules?**
  _Cohesion score 0.052600818234950324 - nodes in this community are weakly interconnected._
- **Why does `AgentEvent` connect `AgentEvent` to `AgentEvent`, `backend/workflows/engine.py`, `workflows/engine.py`, `SlackCommandGateway`, `load_all_workflows()`, `WorkflowEngine`, `get_secrets()`, `EventBus`, `test_edge_cases.py`, `TestWorkflowEngine`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._