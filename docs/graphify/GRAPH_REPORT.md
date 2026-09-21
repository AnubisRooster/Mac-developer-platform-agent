# Graph Report - Mac-developer-platform-agent  (2026-09-21)

## Corpus Check
- 121 files · ~213,900 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 4, .ini 2, .example 1)

## Summary
- 1309 nodes · 2672 edges · 102 communities (65 shown, 37 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 251 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- test_agent.py
- Orchestrator
- test_deployment_readiness.py
- package.json
- typing
- api.ts
- ToolRegistry
- GmailIntegration
- tests/test_database.py
- security/secrets.py
- WorkflowEngine
- pytest
- graphify_pipeline.py
- AgentEvent
- test_webhooks_api.py
- Base
- redact()
- SlackCommandGateway
- EventBus
- test_webhook_security.py
- ConversationMemory
- compilerOptions
- AgentEvent
- tenacity
- backend/webhooks/server.py
- ._completions_post()
- get_secrets()
- SlackIntegration
- fixture
- patch
- get
- backend/main.py
- GitHubIntegration
- asyncio
- main.py
- cli()
- Orchestrator
- JiraIntegration
- test_model_config.py
- test_cli_main.py
- IronClawClient
- TestIronClawClient
- asyncio
- ConfluenceIntegration
- WorkflowDefinition
- EventSource
- SlackIntegration
- RedactingFilter
- RedactingFilter
- ConversationMemory
- GitHubIntegration
- verify_webhook_signature()
- TestEventBus
- TestWorkflowEngine
- ConfluenceIntegration
- JiraIntegration
- TestAPIEndpointEdgeCases
- backend/tests/test_integrations.py
- fixture
- JenkinsIntegration
- TestJenkinsIntegration
- backend/integrations/slack.py
- TestSlackCommandGateway
- AgentConversation
- TestSlackWebhookSecurity
- TestGitHubIntegration
- AppSecrets
- TestGitHubWebhookSecurity
- .subscribe()
- TestConfluenceIntegration
- TestJiraIntegration
- TestGitHubWebhook
- TestJenkinsWebhookSecurity
- .get_context()
- _ensure_database_tables()
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
- `TestEventModel` --uses--> `Event`  [INFERRED]
  tests/test_database.py → backend/database/models.py
- `TestWorkflowRunModel` --uses--> `WorkflowRun`  [INFERRED]
  tests/test_database.py → backend/database/models.py
- `TestToolOutputModel` --uses--> `ToolOutput`  [INFERRED]
  tests/test_database.py → backend/database/models.py

## Import Cycles
- None detected.

## Communities (102 total, 37 thin omitted)

### Community 0 - "test_agent.py"
Cohesion: 0.05
Nodes (29): LLMClient, Registry of available tools: name -> (callable, description)., Initialize empty registry., Return list of registered tool names., Return formatted string of all tool names and descriptions., Create LLMClient, Planner, ConversationMemory, and ToolRegistry., Configurable LLM client supporting OpenRouter, OpenAI, and Ollama., Initialize client from secrets (provider, base_url, api_key). (+21 more)

### Community 1 - "Orchestrator"
Cohesion: 0.07
Nodes (24): Orchestrator, Any, Register a tool. Args: name: Unique tool name. func: Callable to invoke (sync…, Return the callable for the given tool name, or None., Main agent orchestrator: manages LLM, planner, memory, and tool execution., Delegate to ToolRegistry., Process a user message: add to memory, send to LLM, execute tools as needed.…, Look up tool, invoke it, store result in ToolOutput, return result string.… (+16 more)

### Community 2 - "test_deployment_readiness.py"
Cohesion: 0.05
Nodes (21): _import_main(), patch, Deployment readiness tests — validate that the app can wire up and boot. These…, Validate that real YAML workflow files load correctly., Validate that all expected tables are created., Validate that the CLI group can be invoked., Validate that the FastAPI app can be imported without error., Import main with load_dotenv safely patched. (+13 more)

### Community 3 - "package.json"
Cohesion: 0.05
Nodes (35): dependencies, next, react, react-dom, devDependencies, autoprefixer, postcss, tailwindcss (+27 more)

### Community 4 - "typing"
Cohesion: 0.11
Nodes (25): Conversation memory module for maintaining chat history and context., Main orchestrator — the brain of the Developer Automation Agent., Workflow planning module for decomposing user requests into tool steps., asyncio, Conversation memory for maintaining chat history and context., Main orchestrator — delegates reasoning to IronClaw, executes tools locally.…, Slack Command Gateway — primary developer interface. Handles @claw mentions and…, SQLAlchemy models and PostgreSQL session management. (+17 more)

### Community 5 - "api.ts"
Cohesion: 0.09
Nodes (22): EventsPage(), sourceBadge(), LEVEL_COLORS, LEVELS, connectorColor(), ToolsPage(), statusBadge(), WorkflowRunsPage() (+14 more)

### Community 6 - "ToolRegistry"
Cohesion: 0.08
Nodes (17): Unit tests for tools.registry.ToolRegistry., TestToolRegistry, TestToolSchema, Any, BaseModel, Public schema for a registered tool, sent to IronClaw and exposed via API., Internal registry entry binding a schema to its handler., Registry where integration connectors register their tools. Provides tool… (+9 more)

### Community 7 - "GmailIntegration"
Cohesion: 0.12
Nodes (10): GmailIntegration, Any, retry, Gmail integration for reading, sending, and summarizing emails., TestGmailIntegration, GmailIntegration, Any, retry (+2 more)

### Community 8 - "tests/test_database.py"
Cohesion: 0.09
Nodes (17): Unit tests for database.models — all tables and session management., TestEventModel, TestSessionManagement, TestToolOutputModel, TestWorkflowRunModel, TestDashboardAPIWorkflowRuns, Base, CachedSummary (+9 more)

### Community 9 - "security/secrets.py"
Cohesion: 0.11
Nodes (23): atlassian, IronClaw Runtime client — HTTP interface to the Rust-based AI reasoning engine.…, Confluence integration using atlassian-python-api., Secure credential loading and redaction utilities., Validate an HMAC webhook signature., verify_webhook_signature(), Unit tests for security.secrets., Tool Schema Registry — integration connectors register tools with schemas. Each… (+15 more)

### Community 10 - "WorkflowEngine"
Cohesion: 0.15
Nodes (11): WorkflowRun, Edge case and error handling tests across all modules. Tests for boundary…, Previous step results should be merged into later step payloads., TestWorkflowEngineEdgeCases, asyncio, TestWorkflowEngine, Loads workflow definitions and executes them when matching events arrive., WorkflowEngine (+3 more)

### Community 11 - "pytest"
Cohesion: 0.10
Nodes (20): Shared test fixtures — sets env vars, resets caches, provides mock helpers., Unit tests for agent.ironclaw.IronClawClient., Unit tests for agent.slack_gateway.SlackCommandGateway., Unit tests for workflows.loader and workflows.engine., TestWorkflowAction, EventSource, Enum, str (+12 more)

### Community 12 - "graphify_pipeline.py"
Cohesion: 0.09
Nodes (23): Root conftest — ensure backend/ is the only import path for project packages., Gmail integration using google-api-python-client., base64, email_mime_text, google_auth_transport_requests, google_oauth2_credentials, googleapiclient_discovery, graphify_analyze (+15 more)

### Community 13 - "AgentEvent"
Cohesion: 0.14
Nodes (11): Event, asyncio, Unit tests for events.types and events.bus., TestAgentEvent, TestEventBus, EventBus, Simple topic-based publish/subscribe event bus., AgentEvent (+3 more)

### Community 14 - "test_webhooks_api.py"
Cohesion: 0.08
Nodes (12): client(), fixture, Integration tests for webhooks/server.py — webhook and dashboard API endpoints., TestDashboardAPIEvents, TestDashboardAPIStatus, TestDashboardAPITools, TestDashboardAPIWorkflows, TestGitHubWebhook (+4 more)

### Community 15 - "Base"
Cohesion: 0.12
Nodes (11): AgentLog, AgentMemory, Base, DeclarativeBase, TestAgentMemoryModel, fixture, Webhook handler should persist a log entry., TestAgentLogsAPI (+3 more)

### Community 16 - "redact()"
Cohesion: 0.14
Nodes (6): verify_webhook_signature should work with sha1 too., TestSecurityEdgeCases, TestRedact, Replace known secret patterns with <REDACTED>., redact(), TestRedact

### Community 17 - "SlackCommandGateway"
Cohesion: 0.14
Nodes (11): Any, Routes Slack messages mentioning @claw to the orchestrator and sends results…, Process a Slack event that may contain a @claw command., Extract command text, send to orchestrator, reply in Slack., Strip the @claw mention prefix from the message text., Send a threaded reply back to Slack., SlackCommandGateway, Messages containing 'claw' (not app_mention) should be handled. (+3 more)

### Community 18 - "EventBus"
Cohesion: 0.12
Nodes (10): EventBus, Subscriber, Simple topic-based publish/subscribe event bus. Events are persisted to…, Validate WorkflowEngine.load() with the real YAML directory., TestWorkflowEngineLoad, Any, Loads workflow definitions and executes them when matching events arrive., Load workflow definitions and subscribe triggers to the event bus. (+2 more)

### Community 19 - "test_webhook_security.py"
Cohesion: 0.10
Nodes (13): fixture, Webhook signature verification tests — ensure invalid requests are rejected.…, TestClient with webhook secrets configured., secured_client(), TestJiraWebhookSecurity, fastapi_testclient, client(), fixture (+5 more)

### Community 20 - "ConversationMemory"
Cohesion: 0.19
Nodes (5): ConversationMemory, Stores conversation history for the agent and provides context retrieval., Unit tests for agent.memory.ConversationMemory., TestConversationMemory, TestConversationMemory

### Community 21 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 22 - "AgentEvent"
Cohesion: 0.14
Nodes (10): Publish an event — persists to DB and dispatches to subscribers., Write event to PostgreSQL., AgentEvent, BaseModel, Canonical event that flows through the internal bus., Publish an event — persists to DB and dispatches to subscribers., Write event to the local SQLite database., _is_coroutine() (+2 more)

### Community 23 - "tenacity"
Cohesion: 0.14
Nodes (12): GitHub integration using PyGithub., Jenkins integration using python-jenkins., Jira integration using the jira Python SDK., github, github_githubexception, GitHub integration using PyGithub., Jenkins integration using python-jenkins., Jira integration using the jira Python SDK. (+4 more)

### Community 24 - "backend/webhooks/server.py"
Cohesion: 0.23
Nodes (17): github_webhook(), jenkins_webhook(), jira_webhook(), _persist_log(), post, Request, FastAPI webhook server + dashboard API. Webhook endpoints: POST…, Switch the active model and provider at runtime. (+9 more)

### Community 25 - "._completions_post()"
Cohesion: 0.16
Nodes (8): Any, Return (url, headers) based on current provider., Send a user message for interpretation and task planning., Delegate content summarization., Check IronClaw runtime health by querying /v1/models., Send a quick test prompt to verify a model is reachable., Send a chat completions request using the active provider., Send a POST request to IronClaw and return the JSON response.

### Community 26 - "get_secrets()"
Cohesion: 0.14
Nodes (12): get_engine(), get_session(), Session, TestAppSecrets, api_status(), System status: IronClaw health, database connectivity, integrations., AppSecrets, get_secrets() (+4 more)

### Community 27 - "SlackIntegration"
Cohesion: 0.17
Nodes (9): TestSlackIntegration, Any, retry, Slack integration for messaging and channel history., Initialize Slack WebClient with token from secrets., Post a message to a Slack channel., Respond to a slash command via response_url., Read recent messages from a Slack channel. (+1 more)

### Community 28 - "fixture"
Cohesion: 0.13
Nodes (14): async_tool_func(), db_session(), mock_ironclaw_response(), fixture, Factory for IronClaw OpenAI-compatible response dicts., A simple sync tool function for registry tests., A simple async tool function for orchestrator tests., Clear the secrets singleton cache before and after each test. (+6 more)

### Community 29 - "patch"
Cohesion: 0.24
Nodes (6): patch, TestJenkinsIntegration, JenkinsIntegration, Any, retry, Jenkins integration for triggering builds and fetching status/logs.

### Community 30 - "get"
Cohesion: 0.12
Nodes (16): api_agent_conversations(), api_events(), api_logs(), api_model_config(), api_tools(), api_workflow_runs(), api_workflows(), health() (+8 more)

### Community 31 - "backend/main.py"
Cohesion: 0.20
Nodes (14): _agent_summarize(), _build_orchestrator(), command, option, Developer Automation Agent — main entry point. CLI commands: claw-agent run —…, Attach orchestrator + workflow engine + Slack gateway to the FastAPI app., Start the backend server (API + webhooks + Slack gateway)., Delegate summarization to IronClaw. Used by workflow agent.summarize. (+6 more)

### Community 32 - "GitHubIntegration"
Cohesion: 0.24
Nodes (5): TestGitHubIntegration, GitHubIntegration, Any, retry, GitHub integration for issues, PRs, branches, and repository activity.

### Community 33 - "asyncio"
Cohesion: 0.20
Nodes (6): _mock_response(), asyncio, When Ollama fails and OpenRouter key is set, should fallback., Without OpenRouter key, Ollama failure should raise., TestModelTest, TestOpenRouterFallback

### Community 34 - "main.py"
Cohesion: 0.23
Nodes (14): start_chat(), _agent_summarize(), _build_orchestrator(), chat(), command, option, Developer Automation Agent — main entry point. CLI commands: claw-agent chat —…, Start an interactive chat session with the agent. (+6 more)

### Community 35 - "cli()"
Cohesion: 0.18
Nodes (7): cli(), group, pass_context, Claw Agent — Developer Automation Agent., _setup_logging(), fixture, TestMainCLI

### Community 36 - "Orchestrator"
Cohesion: 0.19
Nodes (7): Orchestrator, Any, Look up tool, invoke it, persist result, return result string., Store a completed agent conversation in PostgreSQL., Coordinates between IronClaw (reasoning) and tool execution (Python). All…, Register a tool in the schema registry., Process a user message by delegating reasoning to IronClaw and executing the…

### Community 37 - "JiraIntegration"
Cohesion: 0.24
Nodes (5): TestJiraIntegration, JiraIntegration, Any, retry, Jira integration for tickets, updates, and remote links.

### Community 38 - "test_model_config.py"
Cohesion: 0.14
Nodes (5): _mock_get_response(), Response, Tests for model configuration, OpenRouter fallback, and agent logs. Covers: -…, TestAgentLogTable, TestModelConfigAPI

### Community 39 - "test_cli_main.py"
Cohesion: 0.16
Nodes (10): _chat_loop(), _print_banner(), Interactive CLI chat interface for the developer automation agent., click_testing, rich_console, rich_markdown, rich_panel, rich_theme (+2 more)

### Community 40 - "IronClawClient"
Cohesion: 0.21
Nodes (4): IronClawClient, HTTP client for the IronClaw Rust-based reasoning runtime. Communicates via…, Switch the active model at runtime. Returns the new config., TestIronClawModelConfig

### Community 41 - "TestIronClawClient"
Cohesion: 0.29
Nodes (6): _mock_get_response(), _mock_response(), asyncio, Response, Build an httpx.Response with a request attached so raise_for_status works., TestIronClawClient

### Community 42 - "asyncio"
Cohesion: 0.29
Nodes (6): _mock_response(), asyncio, Response, When IronClaw returns an empty choices array., When IronClaw returns invalid JSON in tool_calls arguments., TestIronClawEdgeCases

### Community 43 - "ConfluenceIntegration"
Cohesion: 0.26
Nodes (5): TestConfluenceIntegration, ConfluenceIntegration, Any, retry, Confluence integration for search, pages, and content.

### Community 44 - "WorkflowDefinition"
Cohesion: 0.26
Nodes (9): load_all_workflows(), load_workflow(), BaseModel, Path, Load and validate YAML workflow definitions., WorkflowAction, WorkflowDefinition, TestWorkflowAction (+1 more)

### Community 45 - "EventSource"
Cohesion: 0.29
Nodes (10): EventSource, Enum, str, TestEventSource, github_webhook(), jenkins_webhook(), jira_webhook(), post (+2 more)

### Community 46 - "SlackIntegration"
Cohesion: 0.25
Nodes (7): Any, retry, Slack integration for messaging and channel history., Post a message to a Slack channel, optionally in a thread., Respond to a slash command via response_url., Read recent messages from a Slack channel., SlackIntegration

### Community 47 - "RedactingFilter"
Cohesion: 0.18
Nodes (10): cli(), group, pass_context, Claw Agent — Developer Automation Platform., _setup_logging(), LogRecord, Logging filter that scrubs sensitive patterns from log records., Replace known secret patterns with <REDACTED>. (+2 more)

### Community 48 - "RedactingFilter"
Cohesion: 0.24
Nodes (5): TestRedactingFilter, LogRecord, Logging filter that scrubs sensitive patterns from log records., RedactingFilter, TestRedactingFilter

### Community 49 - "ConversationMemory"
Cohesion: 0.20
Nodes (4): ConversationMemory, Any, Stores conversation history for the agent and provides context retrieval., Return messages in role/content format for IronClaw context.

### Community 50 - "GitHubIntegration"
Cohesion: 0.38
Nodes (4): GitHubIntegration, Any, retry, GitHub integration for issues, PRs, branches, and repository activity.

### Community 51 - "verify_webhook_signature()"
Cohesion: 0.29
Nodes (4): TestVerifyWebhookSignature, Validate an HMAC webhook signature., verify_webhook_signature(), TestVerifyWebhookSignature

### Community 52 - "TestEventBus"
Cohesion: 0.31
Nodes (3): asyncio, fixture, TestEventBus

### Community 53 - "TestWorkflowEngine"
Cohesion: 0.27
Nodes (3): asyncio, fixture, TestWorkflowEngine

### Community 54 - "ConfluenceIntegration"
Cohesion: 0.33
Nodes (5): ConfluenceIntegration, Any, retry, Confluence integration for search, pages, and content., _strip_html()

### Community 55 - "JiraIntegration"
Cohesion: 0.39
Nodes (4): JiraIntegration, Any, retry, Jira integration for tickets, updates, and remote links.

### Community 56 - "TestAPIEndpointEdgeCases"
Cohesion: 0.22
Nodes (3): fixture, Status should work even when orchestrator isn't attached., TestAPIEndpointEdgeCases

### Community 57 - "backend/tests/test_integrations.py"
Cohesion: 0.36
Nodes (3): Integration connector tests — mocked external service calls. Tests for GitHub,…, TestStripHtml, _strip_html()

### Community 59 - "JenkinsIntegration"
Cohesion: 0.39
Nodes (4): JenkinsIntegration, Any, retry, Jenkins integration for triggering builds and fetching status/logs.

### Community 61 - "backend/integrations/slack.py"
Cohesion: 0.38
Nodes (5): Slack integration using slack_sdk WebClient., httpx, Slack integration using slack_sdk WebClient., slack_sdk, slack_sdk_errors

### Community 63 - "AgentConversation"
Cohesion: 0.47
Nodes (3): AgentConversation, TestAgentConversationModel, TestDashboardAPIConversations

### Community 64 - "TestSlackWebhookSecurity"
Cohesion: 0.40
Nodes (3): Slack URL verification should work even with signing enabled., _slack_signature(), TestSlackWebhookSecurity

### Community 66 - "AppSecrets"
Cohesion: 0.40
Nodes (5): AppSecrets, get_secrets(), BaseSettings, Central secrets model — all values loaded from env vars / .env., Return the singleton secrets instance.

### Community 68 - ".subscribe()"
Cohesion: 0.40
Nodes (3): Subscriber, Register a handler for a specific event type., Register a handler that receives every event.

### Community 74 - "_ensure_database_tables()"
Cohesion: 0.67
Nodes (3): _ensure_database_tables(), Guarantee all tables exist before the first request is served., on_event

## Knowledge Gaps
- **50 isolated node(s):** `nextConfig`, `name`, `version`, `private`, `dev` (+45 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 451 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_secrets()` connect `get_secrets()` to `test_agent.py`, `test_deployment_readiness.py`, `typing`, `GmailIntegration`, `security/secrets.py`, `pytest`, `graphify_pipeline.py`, `test_webhook_security.py`, `tenacity`, `backend/webhooks/server.py`, `SlackIntegration`, `patch`, `get`, `backend/main.py`, `GitHubIntegration`, `main.py`, `JiraIntegration`, `IronClawClient`, `ConfluenceIntegration`, `EventSource`, `SlackIntegration`, `GitHubIntegration`, `ConfluenceIntegration`, `JiraIntegration`, `JenkinsIntegration`, `backend/integrations/slack.py`?**
  _High betweenness centrality (0.121) - this node is a cross-community bridge._
- **Why does `Orchestrator` connect `Orchestrator` to `test_agent.py`, `main.py`, `typing`, `WorkflowEngine`, `ConversationMemory`, `backend/main.py`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `IronClawClient` connect `IronClawClient` to `asyncio`, `Orchestrator`, `test_model_config.py`, `security/secrets.py`, `asyncio`, `TestIronClawClient`, `._completions_post()`, `backend/main.py`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Are the 36 inferred relationships involving `IronClawClient` (e.g. with `Orchestrator` and `_agent_summarize()`) actually correct?**
  _`IronClawClient` has 36 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `AgentEvent` (e.g. with `SlackCommandGateway` and `EventBus`) actually correct?**
  _`AgentEvent` has 22 INFERRED edges - model-reasoned connections that need verification._
- **What connects `nextConfig`, `name`, `version` to the rest of the system?**
  _50 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_agent.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05027322404371585 - nodes in this community are weakly interconnected._