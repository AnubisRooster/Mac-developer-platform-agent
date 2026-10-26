# Graph Report - Mac-developer-platform-agent  (2026-10-26)

## Corpus Check
- 121 files · ~144,034 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 4, .ini 2, .example 1)

## Summary
- 1415 nodes · 2827 edges · 106 communities (46 shown, 60 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 257 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- test_agent.py
- backend/main.py
- package.json
- Orchestrator
- redact()
- api.ts
- ToolRegistry
- database/models.py
- tests/test_integrations.py
- load_all_workflows()
- AgentEvent
- SlackCommandGateway
- WorkflowEngine
- integrations
- test_webhook_security.py
- backend/webhooks/server.py
- test_webhooks_api.py
- test_edge_cases.py
- security/secrets.py
- IronClawClient
- EventBus
- ConversationMemory
- EventBus
- SlackIntegration
- compilerOptions
- backend/database/models.py
- GmailIntegration
- get_secrets()
- patch
- args
- LLMClient
- _import_main()
- GitHubIntegration
- test_ironclaw.py
- args
- test_cli_main.py
- test_deployment_readiness.py
- JiraIntegration
- github_webhook()
- args
- test_webhooks.py
- main.py
- cli()
- AgentLog
- json
- fixture
- Orchestrator
- AgentEvent
- asyncio
- ConfluenceIntegration
- WorkflowDefinition
- GmailIntegration
- workflows/build_failed.yaml
- workflows/jira_created.yaml
- workflows/pr_opened.yaml
- get_session()
- ConversationMemory
- GitHubIntegration
- test_model_config.py
- verify_webhook_signature()
- JiraIntegration
- TestAPIEndpointEdgeCases
- TestModelConfigAPI
- TestJenkinsIntegration
- _strip_html()
- AgentConversation
- TestAppWiring
- .run_workflow()
- TestFastAPIAppImportable
- TestGitHubWebhook
- mock_ironclaw_response()
- TestDatabaseTablesExist
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
- `TestWorkflowRunModel` --uses--> `WorkflowRun`  [INFERRED]
  tests/test_database.py → backend/database/models.py
- `WorkflowEngine` --uses--> `WorkflowRun`  [INFERRED]
  workflows/engine.py → backend/database/models.py

## Import Cycles
- None detected.

## Communities (106 total, 60 thin omitted)

### Community 0 - "test_agent.py"
Cohesion: 0.05
Nodes (9): ToolRegistry, ActionPlan, Planner, PlanStep, TestOrchestrator, TestPlanModels, TestPlanner, TestToolCallPattern (+1 more)

### Community 1 - "backend/main.py"
Cohesion: 0.07
Nodes (11): ConfluenceIntegration, JenkinsIntegration, SlackIntegration, _agent_summarize(), _build_orchestrator(), cli(), run(), _setup_logging() (+3 more)

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

### Community 7 - "database/models.py"
Cohesion: 0.11
Nodes (12): TestEventModel, TestToolOutputModel, TestWorkflowRunModel, Base, CachedSummary, Event, ToolOutput, WorkflowRun (+4 more)

### Community 8 - "tests/test_integrations.py"
Cohesion: 0.07
Nodes (5): TestConfluenceIntegration, TestGitHubIntegration, TestGmailIntegration, TestJiraIntegration, TestSlackIntegration

### Community 9 - "load_all_workflows()"
Cohesion: 0.10
Nodes (7): TestWorkflowLoading, TestWorkflowLoader, TestLoadAllWorkflows, TestLoadWorkflow, TestWorkflowAction, load_all_workflows(), load_workflow()

### Community 10 - "AgentEvent"
Cohesion: 0.11
Nodes (5): TestAgentEvent, AgentEvent, TestAgentEvent, TestEventBus, TestWorkflowEngine

### Community 11 - "SlackCommandGateway"
Cohesion: 0.11
Nodes (3): SlackCommandGateway, TestSlackGatewayEdgeCases, TestSlackCommandGateway

### Community 12 - "WorkflowEngine"
Cohesion: 0.16
Nodes (5): TestWorkflowEngineEdgeCases, TestWorkflowEngine, WorkflowEngine, WorkflowAction, WorkflowDefinition

### Community 13 - "integrations"
Cohesion: 0.07
Nodes (27): agent, log_file, log_level, name, version, enabled, database, url (+19 more)

### Community 14 - "test_webhook_security.py"
Cohesion: 0.10
Nodes (8): verify_webhook_signature(), _github_signature(), secured_client(), _slack_signature(), TestGitHubWebhookSecurity, TestJenkinsWebhookSecurity, TestJiraWebhookSecurity, TestSlackWebhookSecurity

### Community 15 - "backend/webhooks/server.py"
Cohesion: 0.11
Nodes (10): api_agent_conversations(), api_events(), api_logs(), api_model_config(), api_status(), api_tools(), api_workflow_runs(), api_workflows() (+2 more)

### Community 16 - "test_webhooks_api.py"
Cohesion: 0.08
Nodes (10): client(), TestDashboardAPIEvents, TestDashboardAPIStatus, TestDashboardAPITools, TestDashboardAPIWorkflows, TestGitHubWebhook, TestHealthEndpoint, TestJenkinsWebhook (+2 more)

### Community 18 - "security/secrets.py"
Cohesion: 0.14
Nodes (3): _strip_html(), AppSecrets, get_secrets()

### Community 19 - "IronClawClient"
Cohesion: 0.18
Nodes (4): IronClawClient, TestIronClawModelConfig, TestModelTest, TestOpenRouterFallback

### Community 20 - "EventBus"
Cohesion: 0.12
Nodes (3): EventBus, TestWorkflowEngineLoad, WorkflowEngine

### Community 23 - "ConversationMemory"
Cohesion: 0.19
Nodes (3): ConversationMemory, TestConversationMemory, TestConversationMemory

### Community 24 - "EventBus"
Cohesion: 0.18
Nodes (3): Event, TestEventBus, EventBus

### Community 26 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 27 - "backend/database/models.py"
Cohesion: 0.14
Nodes (8): AgentMemory, Base, get_engine(), get_session(), WorkflowRun, TestAgentMemoryModel, TestDashboardAPIWorkflowRuns, db_session()

### Community 30 - "get_secrets()"
Cohesion: 0.18
Nodes (4): TestAppSecrets, AppSecrets, get_secrets(), TestAppSecrets

### Community 32 - "args"
Cohesion: 0.12
Nodes (15): actions, args, description, on_failure, tool, body, channel, labels (+7 more)

### Community 33 - "LLMClient"
Cohesion: 0.19
Nodes (3): LLMClient, _agent_summarize(), TestLLMClient

### Community 34 - "_import_main()"
Cohesion: 0.18
Nodes (3): _import_main(), TestCLIEntryPoint, TestOrchestratorWiring

### Community 36 - "test_ironclaw.py"
Cohesion: 0.26
Nodes (3): _mock_get_response(), _mock_response(), TestIronClawClient

### Community 37 - "args"
Cohesion: 0.13
Nodes (14): actions, args, description, on_failure, tool, channel, github_url, pr_number (+6 more)

### Community 38 - "test_cli_main.py"
Cohesion: 0.18
Nodes (4): _chat_loop(), _print_banner(), start_chat(), TestCLIChat

### Community 41 - "github_webhook()"
Cohesion: 0.26
Nodes (8): github_webhook(), jenkins_webhook(), jira_webhook(), _persist_log(), set_model_config(), set_openrouter_key(), slack_webhook(), test_model()

### Community 42 - "args"
Cohesion: 0.14
Nodes (13): actions, args, description, on_failure, tool, build_number, channel, instruction (+5 more)

### Community 43 - "test_webhooks.py"
Cohesion: 0.14
Nodes (5): client(), TestHealthEndpoint, TestJenkinsWebhook, TestJiraWebhook, TestSlackWebhook

### Community 44 - "main.py"
Cohesion: 0.24
Nodes (5): _build_orchestrator(), chat(), run(), _setup_workflow_engine(), webhook_server()

### Community 45 - "cli()"
Cohesion: 0.20
Nodes (3): cli(), _setup_logging(), TestMainCLI

### Community 48 - "json"
Cohesion: 0.32
Nodes (6): EventSource, github_webhook(), health(), jenkins_webhook(), jira_webhook(), slack_webhook()

### Community 49 - "fixture"
Cohesion: 0.17
Nodes (6): async_tool_func(), db_session(), _reset_db_globals(), _reset_secrets_cache(), sample_tool_func(), _tool()

### Community 54 - "WorkflowDefinition"
Cohesion: 0.27
Nodes (6): TestWorkflowAction, load_all_workflows(), load_workflow(), WorkflowAction, WorkflowDefinition, TestWorkflowDefinition

### Community 57 - "workflows/build_failed.yaml"
Cohesion: 0.18
Nodes (10): actions, args, description, on_failure, tool, channel, description, enabled (+2 more)

### Community 58 - "workflows/jira_created.yaml"
Cohesion: 0.18
Nodes (10): actions, args, description, on_failure, tool, channel, description, enabled (+2 more)

### Community 59 - "workflows/pr_opened.yaml"
Cohesion: 0.18
Nodes (10): actions, args, description, on_failure, tool, channel, description, enabled (+2 more)

### Community 60 - "get_session()"
Cohesion: 0.22
Nodes (3): TestSessionManagement, get_engine(), get_session()

### Community 63 - "test_model_config.py"
Cohesion: 0.22
Nodes (3): _mock_get_response(), _mock_response(), TestAgentLogTable

### Community 64 - "verify_webhook_signature()"
Cohesion: 0.29
Nodes (3): TestVerifyWebhookSignature, verify_webhook_signature(), TestVerifyWebhookSignature

### Community 71 - "AgentConversation"
Cohesion: 0.47
Nodes (3): AgentConversation, TestAgentConversationModel, TestDashboardAPIConversations

## Knowledge Gaps
- **60 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_secrets()` connect `get_secrets()` to `test_agent.py`, `backend/main.py`, `database/models.py`, `test_webhook_security.py`, `backend/webhooks/server.py`, `security/secrets.py`, `IronClawClient`, `logging`, `SlackIntegration`, `backend/database/models.py`, `tenacity`, `GmailIntegration`, `patch`, `LLMClient`, `GitHubIntegration`, `test_deployment_readiness.py`, `JiraIntegration`, `github_webhook()`, `test_webhooks.py`, `main.py`, `ironclaw.py`, `json`, `ConfluenceIntegration`, `GmailIntegration`, `get_session()`, `GitHubIntegration`, `backend/integrations/gmail.py`, `JiraIntegration`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **Are the 36 inferred relationships involving `IronClawClient` (e.g. with `Orchestrator` and `_agent_summarize()`) actually correct?**
  _`IronClawClient` has 36 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_agent.py` be split into smaller, more focused modules?**
  _Cohesion score 0.052600818234950324 - nodes in this community are weakly interconnected._
- **Why does `Orchestrator` connect `Orchestrator` to `test_agent.py`, `LLMClient`, `backend/main.py`, `main.py`, `test_edge_cases.py`, `logging`, `ConversationMemory`, `get_session()`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `AgentEvent` (e.g. with `SlackCommandGateway` and `EventBus`) actually correct?**
  _`AgentEvent` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Should `backend/main.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06570048309178744 - nodes in this community are weakly interconnected._
- **Why does `AgentEvent` connect `AgentEvent` to `database/models.py`, `github_webhook()`, `load_all_workflows()`, `SlackCommandGateway`, `WorkflowEngine`, `backend/webhooks/server.py`, `json`, `test_edge_cases.py`, `logging`, `EventBus`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._