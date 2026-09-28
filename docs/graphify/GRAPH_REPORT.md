# Graph Report - Mac-developer-platform-agent  (2026-09-28)

## Corpus Check
- 121 files · ~228,589 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 4, .ini 2, .example 1)

## Summary
- 1309 nodes · 2675 edges · 103 communities (68 shown, 35 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 251 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- JiraIntegration
- redact()
- Orchestrator
- package.json
- typing
- api.ts
- ToolRegistry
- tests/test_database.py
- security/secrets.py
- WorkflowEngine
- load_all_workflows()
- cli()
- SlackCommandGateway
- test_webhooks_api.py
- AgentEvent
- backend/webhooks/server.py
- Base
- pytest
- EventBus
- test_webhook_security.py
- ConversationMemory
- EventBus
- compilerOptions
- AgentEvent
- tenacity
- ._completions_post()
- get_secrets()
- GmailIntegration
- SlackIntegration
- GitHubIntegration
- fixture
- JiraIntegration
- patch
- backend/main.py
- _import_main()
- GitHubIntegration
- asyncio
- main.py
- ToolRegistry
- Orchestrator
- ConfluenceIntegration
- test_model_config.py
- _persist_log()
- LLMClient
- IronClawClient
- TestIronClawClient
- asyncio
- ConfluenceIntegration
- Planner
- EventSource
- GmailIntegration
- SlackIntegration
- WorkflowDefinition
- graphify_pipeline.py
- test_agent.py
- ConversationMemory
- verify_webhook_signature()
- TestWorkflowEngine
- test_deployment_readiness.py
- backend/integrations/gmail.py
- TestAPIEndpointEdgeCases
- asyncio
- Any
- backend/integrations/slack.py
- _strip_html()
- AgentConversation
- TestAppWiring
- TestSlackWebhookSecurity
- AppSecrets
- TestFastAPIAppImportable
- TestGitHubWebhookSecurity
- tests/conftest.py
- TestGitHubWebhook
- TestJenkinsWebhookSecurity
- TestToolCallPattern
- .get_context()
- next.config.js
- .add_message()
- .clear()
- .get_summary()
- .__init__()
- .to_llm_messages()
- next-env.d.ts

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
- `TestPlanner` --uses--> `ActionPlan`  [INFERRED]
  tests/test_agent.py → agent/planner.py
- `TestEventModel` --uses--> `Event`  [INFERRED]
  tests/test_database.py → backend/database/models.py
- `TestWorkflowRunModel` --uses--> `WorkflowRun`  [INFERRED]
  tests/test_database.py → backend/database/models.py

## Import Cycles
- None detected.

## Communities (103 total, 35 thin omitted)

### Community 0 - "JiraIntegration"
Cohesion: 0.05
Nodes (13): JenkinsIntegration, Any, retry, Jenkins integration for triggering builds and fetching status/logs., JiraIntegration, Any, retry, Jira integration for tickets, updates, and remote links. (+5 more)

### Community 1 - "redact()"
Cohesion: 0.06
Nodes (21): cli(), group, pass_context, Claw Agent — Developer Automation Platform., _setup_logging(), LogRecord, Logging filter that scrubs sensitive patterns from log records., Replace known secret patterns with <REDACTED>. (+13 more)

### Community 2 - "Orchestrator"
Cohesion: 0.08
Nodes (20): Orchestrator, Main agent orchestrator: manages LLM, planner, memory, and tool execution., Process a user message: add to memory, send to LLM, execute tools as needed.…, Look up tool, invoke it, store result in ToolOutput, return result string.…, IronClawAction, IronClawResponse, BaseModel, A single tool action returned by IronClaw's planner. (+12 more)

### Community 3 - "package.json"
Cohesion: 0.05
Nodes (36): dependencies, next, react, react-dom, devDependencies, autoprefixer, postcss, tailwindcss (+28 more)

### Community 4 - "typing"
Cohesion: 0.11
Nodes (25): Conversation memory module for maintaining chat history and context., Main orchestrator — the brain of the Developer Automation Agent., Workflow planning module for decomposing user requests into tool steps., asyncio, Conversation memory for maintaining chat history and context., Main orchestrator — delegates reasoning to IronClaw, executes tools locally.…, Slack Command Gateway — primary developer interface. Handles @claw mentions and…, SQLAlchemy models and PostgreSQL session management. (+17 more)

### Community 5 - "api.ts"
Cohesion: 0.10
Nodes (23): EventsPage(), sourceBadge(), LEVEL_COLORS, LEVELS, StatusPage(), connectorColor(), ToolsPage(), statusBadge() (+15 more)

### Community 6 - "ToolRegistry"
Cohesion: 0.08
Nodes (17): Unit tests for tools.registry.ToolRegistry., TestToolRegistry, TestToolSchema, Any, BaseModel, Public schema for a registered tool, sent to IronClaw and exposed via API., Internal registry entry binding a schema to its handler., Registry where integration connectors register their tools. Provides tool… (+9 more)

### Community 7 - "tests/test_database.py"
Cohesion: 0.09
Nodes (17): Unit tests for database.models — all tables and session management., TestEventModel, TestSessionManagement, TestToolOutputModel, TestWorkflowRunModel, TestDashboardAPIWorkflowRuns, Base, CachedSummary (+9 more)

### Community 8 - "security/secrets.py"
Cohesion: 0.11
Nodes (23): atlassian, IronClaw Runtime client — HTTP interface to the Rust-based AI reasoning engine.…, Confluence integration using atlassian-python-api., Secure credential loading and redaction utilities., Validate an HMAC webhook signature., verify_webhook_signature(), Unit tests for security.secrets., Tool Schema Registry — integration connectors register tools with schemas. Each… (+15 more)

### Community 9 - "WorkflowEngine"
Cohesion: 0.15
Nodes (11): WorkflowRun, Edge case and error handling tests across all modules. Tests for boundary…, Previous step results should be merged into later step payloads., TestWorkflowEngineEdgeCases, asyncio, TestWorkflowEngine, Loads workflow definitions and executes them when matching events arrive., WorkflowEngine (+3 more)

### Community 10 - "load_all_workflows()"
Cohesion: 0.10
Nodes (11): Validate that real YAML workflow files load correctly., TestWorkflowLoading, TestWorkflowLoader, Tests for workflows/loader.py and workflows/engine.py., TestLoadAllWorkflows, TestLoadWorkflow, TestWorkflowAction, Load workflow definitions and subscribe triggers to the event bus. (+3 more)

### Community 11 - "cli()"
Cohesion: 0.09
Nodes (17): _chat_loop(), _print_banner(), Interactive CLI chat interface for the developer automation agent., click_testing, cli(), group, pass_context, Claw Agent — Developer Automation Agent. (+9 more)

### Community 12 - "SlackCommandGateway"
Cohesion: 0.11
Nodes (13): Any, Routes Slack messages mentioning @claw to the orchestrator and sends results…, Process a Slack event that may contain a @claw command., Extract command text, send to orchestrator, reply in Slack., Strip the @claw mention prefix from the message text., Send a threaded reply back to Slack., SlackCommandGateway, Messages containing 'claw' (not app_mention) should be handled. (+5 more)

### Community 13 - "test_webhooks_api.py"
Cohesion: 0.08
Nodes (12): client(), fixture, Integration tests for webhooks/server.py — webhook and dashboard API endpoints., TestDashboardAPIEvents, TestDashboardAPIStatus, TestDashboardAPITools, TestDashboardAPIWorkflows, TestGitHubWebhook (+4 more)

### Community 14 - "AgentEvent"
Cohesion: 0.15
Nodes (8): Unit tests for events.types and events.bus., TestAgentEvent, AgentEvent, BaseModel, Canonical event that flows through the internal bus., asyncio, TestAgentEvent, TestEventBus

### Community 15 - "backend/webhooks/server.py"
Cohesion: 0.11
Nodes (22): api_agent_conversations(), api_events(), api_logs(), api_model_config(), api_tools(), api_workflow_runs(), api_workflows(), _ensure_database_tables() (+14 more)

### Community 16 - "Base"
Cohesion: 0.12
Nodes (11): AgentLog, AgentMemory, Base, DeclarativeBase, TestAgentMemoryModel, fixture, Webhook handler should persist a log entry., TestAgentLogsAPI (+3 more)

### Community 17 - "pytest"
Cohesion: 0.13
Nodes (15): Shared test fixtures — sets env vars, resets caches, provides mock helpers., Unit tests for agent.ironclaw.IronClawClient., Unit tests for agent.slack_gateway.SlackCommandGateway., Unit tests for workflows.loader and workflows.engine., EventSource, Enum, str, pathlib (+7 more)

### Community 18 - "EventBus"
Cohesion: 0.12
Nodes (10): EventBus, Subscriber, Simple topic-based publish/subscribe event bus. Events are persisted to…, Validate WorkflowEngine.load() with the real YAML directory., TestWorkflowEngineLoad, Any, Loads workflow definitions and executes them when matching events arrive., Load workflow definitions and subscribe triggers to the event bus. (+2 more)

### Community 19 - "test_webhook_security.py"
Cohesion: 0.10
Nodes (13): fixture, Webhook signature verification tests — ensure invalid requests are rejected.…, TestClient with webhook secrets configured., secured_client(), TestJiraWebhookSecurity, fastapi_testclient, client(), fixture (+5 more)

### Community 20 - "ConversationMemory"
Cohesion: 0.19
Nodes (5): ConversationMemory, Stores conversation history for the agent and provides context retrieval., Unit tests for agent.memory.ConversationMemory., TestConversationMemory, TestConversationMemory

### Community 21 - "EventBus"
Cohesion: 0.18
Nodes (9): Event, asyncio, TestEventBus, EventBus, Subscriber, Simple topic-based publish/subscribe event bus., Register a handler for a specific event type., Register a handler that receives every event. (+1 more)

### Community 22 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 23 - "AgentEvent"
Cohesion: 0.14
Nodes (10): Publish an event — persists to DB and dispatches to subscribers., Write event to PostgreSQL., AgentEvent, BaseModel, Canonical event that flows through the internal bus., Publish an event — persists to DB and dispatches to subscribers., Write event to the local SQLite database., _is_coroutine() (+2 more)

### Community 24 - "tenacity"
Cohesion: 0.14
Nodes (12): GitHub integration using PyGithub., Jenkins integration using python-jenkins., Jira integration using the jira Python SDK., github, github_githubexception, GitHub integration using PyGithub., Jenkins integration using python-jenkins., Jira integration using the jira Python SDK. (+4 more)

### Community 25 - "._completions_post()"
Cohesion: 0.16
Nodes (8): Any, Return (url, headers) based on current provider., Send a user message for interpretation and task planning., Delegate content summarization., Check IronClaw runtime health by querying /v1/models., Send a quick test prompt to verify a model is reachable., Send a chat completions request using the active provider., Send a POST request to IronClaw and return the JSON response.

### Community 26 - "get_secrets()"
Cohesion: 0.14
Nodes (12): get_engine(), get_session(), Session, TestAppSecrets, api_status(), System status: IronClaw health, database connectivity, integrations., AppSecrets, get_secrets() (+4 more)

### Community 27 - "GmailIntegration"
Cohesion: 0.25
Nodes (5): TestGmailIntegration, GmailIntegration, Any, retry, Gmail integration for reading, sending, and summarizing emails.

### Community 28 - "SlackIntegration"
Cohesion: 0.17
Nodes (9): TestSlackIntegration, Any, retry, Slack integration for messaging and channel history., Initialize Slack WebClient with token from secrets., Post a message to a Slack channel., Respond to a slash command via response_url., Read recent messages from a Slack channel. (+1 more)

### Community 29 - "GitHubIntegration"
Cohesion: 0.19
Nodes (5): GitHubIntegration, Any, retry, GitHub integration for issues, PRs, branches, and repository activity., TestGitHubIntegration

### Community 30 - "fixture"
Cohesion: 0.13
Nodes (14): async_tool_func(), db_session(), mock_ironclaw_response(), fixture, Factory for IronClaw OpenAI-compatible response dicts., A simple sync tool function for registry tests., A simple async tool function for orchestrator tests., Clear the secrets singleton cache before and after each test. (+6 more)

### Community 31 - "JiraIntegration"
Cohesion: 0.21
Nodes (6): Integration connector tests — mocked external service calls. Tests for GitHub,…, TestJiraIntegration, JiraIntegration, Any, retry, Jira integration for tickets, updates, and remote links.

### Community 32 - "patch"
Cohesion: 0.24
Nodes (6): patch, TestJenkinsIntegration, JenkinsIntegration, Any, retry, Jenkins integration for triggering builds and fetching status/logs.

### Community 33 - "backend/main.py"
Cohesion: 0.20
Nodes (14): _agent_summarize(), _build_orchestrator(), command, option, Developer Automation Agent — main entry point. CLI commands: claw-agent run —…, Attach orchestrator + workflow engine + Slack gateway to the FastAPI app., Start the backend server (API + webhooks + Slack gateway)., Delegate summarization to IronClaw. Used by workflow agent.summarize. (+6 more)

### Community 34 - "_import_main()"
Cohesion: 0.18
Nodes (8): _import_main(), patch, Validate that the CLI group can be invoked., Import main with load_dotenv safely patched., Validate _build_orchestrator registers all expected tools., With no tokens, only gmail + agent.summarize are registered., TestCLIEntryPoint, TestOrchestratorWiring

### Community 35 - "GitHubIntegration"
Cohesion: 0.24
Nodes (5): TestGitHubIntegration, GitHubIntegration, Any, retry, GitHub integration for issues, PRs, branches, and repository activity.

### Community 36 - "asyncio"
Cohesion: 0.20
Nodes (6): _mock_response(), asyncio, When Ollama fails and OpenRouter key is set, should fallback., Without OpenRouter key, Ollama failure should raise., TestModelTest, TestOpenRouterFallback

### Community 37 - "main.py"
Cohesion: 0.23
Nodes (14): start_chat(), _agent_summarize(), _build_orchestrator(), chat(), command, option, Developer Automation Agent — main entry point. CLI commands: claw-agent chat —…, Start an interactive chat session with the agent. (+6 more)

### Community 38 - "ToolRegistry"
Cohesion: 0.20
Nodes (6): Registry of available tools: name -> (callable, description)., Initialize empty registry., Return list of registered tool names., Return formatted string of all tool names and descriptions., ToolRegistry, TestToolRegistry

### Community 39 - "Orchestrator"
Cohesion: 0.19
Nodes (7): Orchestrator, Any, Look up tool, invoke it, persist result, return result string., Store a completed agent conversation in PostgreSQL., Coordinates between IronClaw (reasoning) and tool execution (Python). All…, Register a tool in the schema registry., Process a user message by delegating reasoning to IronClaw and executing the…

### Community 40 - "ConfluenceIntegration"
Cohesion: 0.19
Nodes (6): ConfluenceIntegration, Any, retry, Confluence integration for search, pages, and content., _strip_html(), TestConfluenceIntegration

### Community 41 - "test_model_config.py"
Cohesion: 0.14
Nodes (5): _mock_get_response(), Response, Tests for model configuration, OpenRouter fallback, and agent logs. Covers: -…, TestAgentLogTable, TestModelConfigAPI

### Community 42 - "_persist_log()"
Cohesion: 0.26
Nodes (14): github_webhook(), jenkins_webhook(), jira_webhook(), _persist_log(), post, Request, Switch the active model and provider at runtime., Test if a specific model is reachable without switching. (+6 more)

### Community 43 - "LLMClient"
Cohesion: 0.21
Nodes (6): LLMClient, Create LLMClient, Planner, ConversationMemory, and ToolRegistry., Configurable LLM client supporting OpenRouter, OpenAI, and Ollama., Initialize client from secrets (provider, base_url, api_key)., Send messages to the LLM and return the assistant content. Args: messages: List…, TestLLMClient

### Community 44 - "IronClawClient"
Cohesion: 0.21
Nodes (4): IronClawClient, HTTP client for the IronClaw Rust-based reasoning runtime. Communicates via…, Switch the active model at runtime. Returns the new config., TestIronClawModelConfig

### Community 45 - "TestIronClawClient"
Cohesion: 0.29
Nodes (6): _mock_get_response(), _mock_response(), asyncio, Response, Build an httpx.Response with a request attached so raise_for_status works., TestIronClawClient

### Community 46 - "asyncio"
Cohesion: 0.29
Nodes (6): _mock_response(), asyncio, Response, When IronClaw returns an empty choices array., When IronClaw returns invalid JSON in tool_calls arguments., TestIronClawEdgeCases

### Community 47 - "ConfluenceIntegration"
Cohesion: 0.26
Nodes (5): TestConfluenceIntegration, ConfluenceIntegration, Any, retry, Confluence integration for search, pages, and content.

### Community 48 - "Planner"
Cohesion: 0.24
Nodes (6): Planner, Any, Decomposes user requests into structured action plans using an LLM., Initialize the planner with an LLM client. Args: llm_client: Client with async…, Create an action plan from a user request using available tools. Args:…, TestPlanner

### Community 49 - "EventSource"
Cohesion: 0.29
Nodes (10): EventSource, Enum, str, TestEventSource, github_webhook(), jenkins_webhook(), jira_webhook(), post (+2 more)

### Community 50 - "GmailIntegration"
Cohesion: 0.44
Nodes (4): GmailIntegration, Any, retry, Gmail integration for reading, sending, and summarizing emails.

### Community 51 - "SlackIntegration"
Cohesion: 0.25
Nodes (7): Any, retry, Slack integration for messaging and channel history., Post a message to a Slack channel, optionally in a thread., Respond to a slash command via response_url., Read recent messages from a Slack channel., SlackIntegration

### Community 52 - "WorkflowDefinition"
Cohesion: 0.29
Nodes (9): TestWorkflowAction, load_all_workflows(), load_workflow(), BaseModel, Path, Load and validate YAML workflow definitions., WorkflowAction, WorkflowDefinition (+1 more)

### Community 53 - "graphify_pipeline.py"
Cohesion: 0.18
Nodes (9): graphify_analyze, graphify_build, graphify_cluster, graphify_detect, graphify_export, graphify_extract, graphify_llm, graphify_report (+1 more)

### Community 54 - "test_agent.py"
Cohesion: 0.33
Nodes (7): ActionPlan, PlanStep, BaseModel, A single step in an action plan., Structured plan for executing a user request across multiple tool calls., Tests for agent/memory.py, agent/planner.py, and agent/orchestrator.py., TestPlanModels

### Community 55 - "ConversationMemory"
Cohesion: 0.20
Nodes (4): ConversationMemory, Any, Stores conversation history for the agent and provides context retrieval., Return messages in role/content format for IronClaw context.

### Community 56 - "verify_webhook_signature()"
Cohesion: 0.29
Nodes (4): TestVerifyWebhookSignature, Validate an HMAC webhook signature., verify_webhook_signature(), TestVerifyWebhookSignature

### Community 57 - "TestWorkflowEngine"
Cohesion: 0.27
Nodes (3): asyncio, fixture, TestWorkflowEngine

### Community 58 - "test_deployment_readiness.py"
Cohesion: 0.25
Nodes (6): Root conftest — ensure backend/ is the only import path for project packages., Deployment readiness tests — validate that the app can wire up and boot. These…, Validate that all expected tables are created., TestDatabaseTablesExist, os, sys

### Community 59 - "backend/integrations/gmail.py"
Cohesion: 0.33
Nodes (7): Gmail integration using google-api-python-client., base64, email_mime_text, google_auth_transport_requests, google_oauth2_credentials, googleapiclient_discovery, Gmail integration using google-api-python-client.

### Community 60 - "TestAPIEndpointEdgeCases"
Cohesion: 0.22
Nodes (3): fixture, Status should work even when orchestrator isn't attached., TestAPIEndpointEdgeCases

### Community 61 - "asyncio"
Cohesion: 0.31
Nodes (3): asyncio, fixture, TestOrchestrator

### Community 62 - "Any"
Cohesion: 0.29
Nodes (4): Any, Register a tool. Args: name: Unique tool name. func: Callable to invoke (sync…, Return the callable for the given tool name, or None., Delegate to ToolRegistry.

### Community 63 - "backend/integrations/slack.py"
Cohesion: 0.38
Nodes (5): Slack integration using slack_sdk WebClient., httpx, Slack integration using slack_sdk WebClient., slack_sdk, slack_sdk_errors

### Community 65 - "AgentConversation"
Cohesion: 0.47
Nodes (3): AgentConversation, TestAgentConversationModel, TestDashboardAPIConversations

### Community 67 - "TestSlackWebhookSecurity"
Cohesion: 0.40
Nodes (3): Slack URL verification should work even with signing enabled., _slack_signature(), TestSlackWebhookSecurity

### Community 68 - "AppSecrets"
Cohesion: 0.40
Nodes (5): AppSecrets, get_secrets(), BaseSettings, Central secrets model — all values loaded from env vars / .env., Return the singleton secrets instance.

### Community 71 - "tests/conftest.py"
Cohesion: 0.50
Nodes (4): env_secrets(), fixture, Shared fixtures for the test suite., _reset_secrets_cache()

## Knowledge Gaps
- **50 isolated node(s):** `nextConfig`, `name`, `version`, `private`, `dev` (+45 more)
  These have ≤1 connection - possible missing edges. (Counts symbols only; 449 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **35 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_secrets()` connect `get_secrets()` to `JiraIntegration`, `typing`, `security/secrets.py`, `backend/webhooks/server.py`, `pytest`, `test_webhook_security.py`, `tenacity`, `GmailIntegration`, `SlackIntegration`, `GitHubIntegration`, `JiraIntegration`, `patch`, `backend/main.py`, `GitHubIntegration`, `main.py`, `ConfluenceIntegration`, `_persist_log()`, `LLMClient`, `IronClawClient`, `ConfluenceIntegration`, `EventSource`, `GmailIntegration`, `SlackIntegration`, `test_agent.py`, `test_deployment_readiness.py`, `backend/integrations/gmail.py`, `backend/integrations/slack.py`, `tests/conftest.py`?**
  _High betweenness centrality (0.121) - this node is a cross-community bridge._
- **Why does `Orchestrator` connect `Orchestrator` to `backend/main.py`, `typing`, `main.py`, `WorkflowEngine`, `LLMClient`, `Planner`, `ConversationMemory`, `test_agent.py`, `asyncio`, `Any`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `IronClawClient` connect `IronClawClient` to `backend/main.py`, `asyncio`, `Orchestrator`, `security/secrets.py`, `test_model_config.py`, `TestIronClawClient`, `asyncio`, `._completions_post()`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Are the 36 inferred relationships involving `IronClawClient` (e.g. with `Orchestrator` and `_agent_summarize()`) actually correct?**
  _`IronClawClient` has 36 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `AgentEvent` (e.g. with `SlackCommandGateway` and `EventBus`) actually correct?**
  _`AgentEvent` has 22 INFERRED edges - model-reasoned connections that need verification._
- **What connects `nextConfig`, `name`, `version` to the rest of the system?**
  _50 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `JiraIntegration` be split into smaller, more focused modules?**
  _Cohesion score 0.05454545454545454 - nodes in this community are weakly interconnected._