# Graph Report - Mac-developer-platform-agent  (2026-09-07)

## Corpus Check
- Corpus is ~41,302 words - fits in a single context window. You may not need a graph.

## Summary
- 1234 nodes · 2358 edges · 87 communities (60 shown, 7 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 237 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Orchestrator
- tests/test_integrations.py
- package.json
- ToolRegistry
- api.ts
- AgentEvent
- test_deployment_readiness.py
- WorkflowEngine
- load_all_workflows()
- ConversationMemory
- get_secrets()
- cli()
- redact()
- EventBus
- test_webhooks_api.py
- IronClawClient
- ironclaw.py
- test_webhook_security.py
- ToolRegistry
- AgentEvent
- database/models.py
- compilerOptions
- Planner
- backend/main.py
- get
- test_webhooks.py
- ._completions_post()
- backend/database/models.py
- EventSource
- TestIronClawClient
- GmailIntegration
- RedactingFilter
- patch
- backend/webhooks/server.py
- Orchestrator
- AgentConversation
- GitHubIntegration
- SlackIntegration
- test_agent.py
- get_session()
- JiraIntegration
- WorkflowDefinition
- main.py
- LLMClient
- test_edge_cases.py
- AgentLog
- backend/security/secrets.py
- backend/tests/conftest.py
- ConversationMemory
- ConfluenceIntegration
- verify_webhook_signature()
- AppSecrets
- Event
- ConfluenceIntegration
- GmailIntegration
- SlackIntegration
- GitHubIntegration
- JiraIntegration
- backend/tests/test_integrations.py
- TestModelConfigAPI
- TestToolCallPattern
- .get_context()
- _ensure_database_tables()
- next.config.js
- graphify_pipeline.py
- backend/conftest.py
- next-env.d.ts

## God Nodes (most connected - your core abstractions)
1. `get_secrets()` - 67 edges
2. `AgentEvent` - 66 edges
3. `IronClawClient` - 53 edges
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
- `Orchestrator` --uses--> `ToolOutput`  [INFERRED]
  agent/orchestrator.py → backend/database/models.py
- `TestOrchestrator` --uses--> `Orchestrator`  [INFERRED]
  tests/test_agent.py → agent/orchestrator.py
- `TestPlanner` --uses--> `ActionPlan`  [INFERRED]
  tests/test_agent.py → agent/planner.py
- `EventBus` --uses--> `Event`  [INFERRED]
  events/bus.py → backend/database/models.py

## Import Cycles
- None detected.

## Communities (87 total, 7 thin omitted)

### Community 0 - "Orchestrator"
Cohesion: 0.06
Nodes (31): Orchestrator, Main agent orchestrator: manages LLM, planner, memory, and tool execution., Process a user message: add to memory, send to LLM, execute tools as needed.…, IronClawAction, IronClawResponse, BaseModel, A single tool action returned by IronClaw's planner., Structured response from the IronClaw runtime. (+23 more)

### Community 1 - "tests/test_integrations.py"
Cohesion: 0.05
Nodes (12): JenkinsIntegration, Any, retry, Jenkins integration for triggering builds and fetching status/logs., fixture, Tests for all integration connectors., TestConfluenceIntegration, TestGitHubIntegration (+4 more)

### Community 2 - "package.json"
Cohesion: 0.05
Nodes (34): dependencies, next, react, react-dom, devDependencies, autoprefixer, postcss, tailwindcss (+26 more)

### Community 3 - "ToolRegistry"
Cohesion: 0.08
Nodes (18): Unit tests for tools.registry.ToolRegistry., TestToolRegistry, TestToolSchema, Any, BaseModel, Tool Schema Registry — integration connectors register tools with schemas. Each…, Public schema for a registered tool, sent to IronClaw and exposed via API., Internal registry entry binding a schema to its handler. (+10 more)

### Community 4 - "api.ts"
Cohesion: 0.09
Nodes (22): EventsPage(), sourceBadge(), LEVEL_COLORS, LEVELS, connectorColor(), ToolsPage(), statusBadge(), WorkflowRunsPage() (+14 more)

### Community 5 - "AgentEvent"
Cohesion: 0.08
Nodes (18): EventBus, Subscriber, Simple topic-based publish/subscribe event bus. Events are persisted to…, Publish an event — persists to DB and dispatches to subscribers., Write event to PostgreSQL., AgentEvent, BaseModel, Canonical event that flows through the internal bus. (+10 more)

### Community 6 - "test_deployment_readiness.py"
Cohesion: 0.08
Nodes (17): _import_main(), patch, Deployment readiness tests — validate that the app can wire up and boot. These…, Validate that real YAML workflow files load correctly., Validate that all expected tables are created., Validate that the CLI group can be invoked., Validate that the FastAPI app can be imported without error., Import main with load_dotenv safely patched. (+9 more)

### Community 7 - "WorkflowEngine"
Cohesion: 0.15
Nodes (12): Previous step results should be merged into later step payloads., TestWorkflowEngineEdgeCases, asyncio, TestWorkflowEngine, asyncio, fixture, TestWorkflowEngine, Loads workflow definitions and executes them when matching events arrive. (+4 more)

### Community 8 - "load_all_workflows()"
Cohesion: 0.10
Nodes (13): Unit tests for workflows.loader and workflows.engine., TestWorkflowLoader, Workflow execution engine — runs loaded YAML workflows in response to events., In-process async event bus with topic-based pub/sub., Tests for workflows/loader.py and workflows/engine.py., TestLoadAllWorkflows, TestLoadWorkflow, Workflow execution engine — runs loaded YAML workflows in response to events. (+5 more)

### Community 9 - "ConversationMemory"
Cohesion: 0.10
Nodes (11): ConversationMemory, Conversation memory module for maintaining chat history and context., Stores conversation history for the agent and provides context retrieval., Initialize empty conversation history., Add a message to the conversation history. Args: role: Message role (e.g.…, Return a one-line summary of the conversation so far. Returns: Brief summary…, Clear all conversation history., Return messages in OpenAI-style format for API calls. Returns: List of dicts… (+3 more)

### Community 10 - "get_secrets()"
Cohesion: 0.10
Nodes (15): GitHub integration using PyGithub., Gmail integration using google-api-python-client., Jenkins integration using python-jenkins., Jira integration using the jira Python SDK., Slack integration using slack_sdk WebClient., Confluence integration using atlassian-python-api., GitHub integration using PyGithub., Gmail integration using google-api-python-client. (+7 more)

### Community 11 - "cli()"
Cohesion: 0.12
Nodes (13): _chat_loop(), _print_banner(), Interactive CLI chat interface for the developer automation agent., start_chat(), cli(), group, pass_context, Claw Agent — Developer Automation Agent. (+5 more)

### Community 12 - "redact()"
Cohesion: 0.13
Nodes (7): verify_webhook_signature should work with sha1 too., TestSecurityEdgeCases, TestRedact, LogRecord, Replace known secret patterns with <REDACTED>., redact(), TestRedact

### Community 13 - "EventBus"
Cohesion: 0.13
Nodes (11): asyncio, Unit tests for events.types and events.bus., TestEventBus, EventBus, Subscriber, Simple topic-based publish/subscribe event bus., Register a handler for a specific event type., Register a handler that receives every event. (+3 more)

### Community 14 - "test_webhooks_api.py"
Cohesion: 0.08
Nodes (12): client(), fixture, Integration tests for webhooks/server.py — webhook and dashboard API endpoints., TestDashboardAPIStatus, TestDashboardAPITools, TestDashboardAPIWorkflowRuns, TestDashboardAPIWorkflows, TestGitHubWebhook (+4 more)

### Community 15 - "IronClawClient"
Cohesion: 0.14
Nodes (9): IronClawClient, HTTP client for the IronClaw Rust-based reasoning runtime. Communicates via…, Switch the active model at runtime. Returns the new config., _mock_response(), Response, When IronClaw returns an empty choices array., When IronClaw returns invalid JSON in tool_calls arguments., TestIronClawEdgeCases (+1 more)

### Community 16 - "ironclaw.py"
Cohesion: 0.13
Nodes (11): IronClaw Runtime client — HTTP interface to the Rust-based AI reasoning engine.…, _mock_get_response(), _mock_response(), asyncio, Response, Tests for model configuration, OpenRouter fallback, and agent logs. Covers: -…, When Ollama fails and OpenRouter key is set, should fallback., Without OpenRouter key, Ollama failure should raise. (+3 more)

### Community 17 - "test_webhook_security.py"
Cohesion: 0.10
Nodes (12): _github_signature(), fixture, Webhook signature verification tests — ensure invalid requests are rejected.…, Slack URL verification should work even with signing enabled., Jenkins webhook without signature header still passes (only rejects bad sigs)., TestClient with webhook secrets configured., secured_client(), _slack_signature() (+4 more)

### Community 18 - "ToolRegistry"
Cohesion: 0.12
Nodes (10): Any, Registry of available tools: name -> (callable, description)., Initialize empty registry., Register a tool. Args: name: Unique tool name. func: Callable to invoke (sync…, Return the callable for the given tool name, or None., Return list of registered tool names., Return formatted string of all tool names and descriptions., Delegate to ToolRegistry. (+2 more)

### Community 19 - "AgentEvent"
Cohesion: 0.16
Nodes (7): TestAgentEvent, AgentEvent, BaseModel, Canonical event that flows through the internal bus., asyncio, TestAgentEvent, TestEventBus

### Community 20 - "database/models.py"
Cohesion: 0.17
Nodes (11): Main orchestrator — delegates reasoning to IronClaw, executes tools locally.…, Base, CachedSummary, DeclarativeBase, SQLAlchemy models and database session management., ToolOutput, WorkflowRun, Tests for database/models.py. (+3 more)

### Community 21 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 22 - "Planner"
Cohesion: 0.16
Nodes (8): Planner, Any, Decomposes user requests into structured action plans using an LLM., Initialize the planner with an LLM client. Args: llm_client: Client with async…, Create an action plan from a user request using available tools. Args:…, asyncio, TestOrchestrator, TestPlanner

### Community 23 - "backend/main.py"
Cohesion: 0.16
Nodes (17): _agent_summarize(), _build_orchestrator(), cli(), command, group, option, pass_context, Developer Automation Agent — main entry point. CLI commands: claw-agent run —… (+9 more)

### Community 24 - "get"
Cohesion: 0.11
Nodes (18): api_agent_conversations(), api_events(), api_logs(), api_model_config(), api_status(), api_tools(), api_workflow_runs(), api_workflows() (+10 more)

### Community 25 - "test_webhooks.py"
Cohesion: 0.11
Nodes (8): client(), fixture, Tests for webhooks/server.py — FastAPI endpoint validation., TestGitHubWebhook, TestHealthEndpoint, TestJenkinsWebhook, TestJiraWebhook, TestSlackWebhook

### Community 26 - "._completions_post()"
Cohesion: 0.16
Nodes (8): Any, Return (url, headers) based on current provider., Send a user message for interpretation and task planning., Delegate content summarization., Check IronClaw runtime health by querying /v1/models., Send a quick test prompt to verify a model is reachable., Send a chat completions request using the active provider., Send a POST request to IronClaw and return the JSON response.

### Community 27 - "backend/database/models.py"
Cohesion: 0.17
Nodes (14): AgentMemory, Base, Event, get_engine(), get_session(), DeclarativeBase, Session, SQLAlchemy models and PostgreSQL session management. (+6 more)

### Community 28 - "EventSource"
Cohesion: 0.19
Nodes (14): EventSource, Enum, str, Event type definitions for the internal event bus., TestEventSource, github_webhook(), health(), jenkins_webhook() (+6 more)

### Community 29 - "TestIronClawClient"
Cohesion: 0.22
Nodes (9): mock_ironclaw_response(), Factory for IronClaw OpenAI-compatible response dicts., _mock_get_response(), _mock_response(), asyncio, Response, Unit tests for agent.ironclaw.IronClawClient., Build an httpx.Response with a request attached so raise_for_status works. (+1 more)

### Community 30 - "GmailIntegration"
Cohesion: 0.25
Nodes (5): TestGmailIntegration, GmailIntegration, Any, retry, Gmail integration for reading, sending, and summarizing emails.

### Community 31 - "RedactingFilter"
Cohesion: 0.17
Nodes (8): Logging filter that scrubs sensitive patterns from log records., RedactingFilter, Unit tests for security.secrets., TestAppSecrets, TestRedactingFilter, Logging filter that scrubs sensitive patterns from log records., RedactingFilter, TestRedactingFilter

### Community 32 - "patch"
Cohesion: 0.24
Nodes (6): patch, TestJenkinsIntegration, JenkinsIntegration, Any, retry, Jenkins integration for triggering builds and fetching status/logs.

### Community 33 - "backend/webhooks/server.py"
Cohesion: 0.28
Nodes (15): github_webhook(), jenkins_webhook(), jira_webhook(), _persist_log(), post, Request, FastAPI webhook server + dashboard API. Webhook endpoints: POST…, Switch the active model and provider at runtime. (+7 more)

### Community 34 - "Orchestrator"
Cohesion: 0.17
Nodes (8): Orchestrator, Any, Look up tool, invoke it, persist result, return result string., Store a completed agent conversation in PostgreSQL., Coordinates between IronClaw (reasoning) and tool execution (Python). All…, Register a tool in the schema registry., Process a user message by delegating reasoning to IronClaw and executing the…, ToolRegistry

### Community 35 - "AgentConversation"
Cohesion: 0.16
Nodes (6): AgentConversation, TestAgentConversationModel, fixture, Status should work even when orchestrator isn't attached., TestAPIEndpointEdgeCases, TestDashboardAPIConversations

### Community 36 - "GitHubIntegration"
Cohesion: 0.24
Nodes (5): TestGitHubIntegration, GitHubIntegration, Any, retry, GitHub integration for issues, PRs, branches, and repository activity.

### Community 37 - "SlackIntegration"
Cohesion: 0.20
Nodes (8): TestSlackIntegration, Any, retry, Slack integration for messaging and channel history., Post a message to a Slack channel., Respond to a slash command via response_url., Read recent messages from a Slack channel., SlackIntegration

### Community 38 - "test_agent.py"
Cohesion: 0.24
Nodes (9): Main orchestrator — the brain of the Developer Automation Agent., ActionPlan, PlanStep, BaseModel, Workflow planning module for decomposing user requests into tool steps., A single step in an action plan., Structured plan for executing a user request across multiple tool calls., Tests for agent/memory.py, agent/planner.py, and agent/orchestrator.py. (+1 more)

### Community 39 - "get_session()"
Cohesion: 0.16
Nodes (8): Look up tool, invoke it, store result in ToolOutput, return result string.…, Unit tests for database.models — all tables and session management., TestSessionManagement, TestToolOutputModel, TestWorkflowRunModel, get_engine(), get_session(), Session

### Community 40 - "JiraIntegration"
Cohesion: 0.24
Nodes (5): TestJiraIntegration, JiraIntegration, Any, retry, Jira integration for tickets, updates, and remote links.

### Community 41 - "WorkflowDefinition"
Cohesion: 0.22
Nodes (10): TestWorkflowAction, load_all_workflows(), load_workflow(), BaseModel, Path, Load and validate YAML workflow definitions., WorkflowAction, WorkflowDefinition (+2 more)

### Community 42 - "main.py"
Cohesion: 0.24
Nodes (13): _agent_summarize(), _build_orchestrator(), chat(), command, option, Developer Automation Agent — main entry point. CLI commands: claw-agent chat —…, Start an interactive chat session with the agent., Start the webhook server in the foreground. (+5 more)

### Community 43 - "LLMClient"
Cohesion: 0.21
Nodes (6): LLMClient, Create LLMClient, Planner, ConversationMemory, and ToolRegistry., Configurable LLM client supporting OpenRouter, OpenAI, and Ollama., Initialize client from secrets (provider, base_url, api_key)., Send messages to the LLM and return the assistant content. Args: messages: List…, TestLLMClient

### Community 44 - "test_edge_cases.py"
Cohesion: 0.23
Nodes (8): Slack Command Gateway — primary developer interface. Handles @claw mentions and…, Edge case and error handling tests across all modules. Tests for boundary…, Unit tests for agent.slack_gateway.SlackCommandGateway., EventSource, Enum, str, Event type definitions for the internal event bus., Tests for events/types.py and events/bus.py.

### Community 45 - "AgentLog"
Cohesion: 0.22
Nodes (4): AgentLog, fixture, Webhook handler should persist a log entry., TestAgentLogsAPI

### Community 46 - "backend/security/secrets.py"
Cohesion: 0.17
Nodes (11): AppSecrets, get_secrets(), BaseSettings, LogRecord, Secure credential loading and redaction utilities., Validate an HMAC webhook signature., Central secrets model — all values loaded from env vars / .env., Return the singleton secrets instance. (+3 more)

### Community 47 - "backend/tests/conftest.py"
Cohesion: 0.21
Nodes (12): async_tool_func(), db_session(), fixture, Shared test fixtures — sets env vars, resets caches, provides mock helpers., A simple sync tool function for registry tests., A simple async tool function for orchestrator tests., Clear the secrets singleton cache before and after each test., Reset database engine/session globals so each test gets a fresh DB. Uses… (+4 more)

### Community 48 - "ConversationMemory"
Cohesion: 0.17
Nodes (5): ConversationMemory, Any, Conversation memory for maintaining chat history and context., Stores conversation history for the agent and provides context retrieval., Return messages in role/content format for IronClaw context.

### Community 49 - "ConfluenceIntegration"
Cohesion: 0.26
Nodes (5): TestConfluenceIntegration, ConfluenceIntegration, Any, retry, Confluence integration for search, pages, and content.

### Community 50 - "verify_webhook_signature()"
Cohesion: 0.24
Nodes (5): TestVerifyWebhookSignature, Validate an HMAC webhook signature., verify_webhook_signature(), Tests for security/secrets.py., TestVerifyWebhookSignature

### Community 51 - "AppSecrets"
Cohesion: 0.17
Nodes (8): AppSecrets, BaseSettings, Central secrets model — all values loaded from env vars / .env., env_secrets(), fixture, Shared fixtures for the test suite., _reset_secrets_cache(), TestAppSecrets

### Community 52 - "Event"
Cohesion: 0.20
Nodes (5): In-process async event bus with topic-based pub/sub., TestEventModel, TestDashboardAPIEvents, Event, TestEventModel

### Community 53 - "ConfluenceIntegration"
Cohesion: 0.27
Nodes (6): ConfluenceIntegration, Any, retry, Confluence integration using atlassian-python-api., Confluence integration for search, pages, and content., _strip_html()

### Community 54 - "GmailIntegration"
Cohesion: 0.44
Nodes (4): GmailIntegration, Any, retry, Gmail integration for reading, sending, and summarizing emails.

### Community 55 - "SlackIntegration"
Cohesion: 0.25
Nodes (7): Any, retry, Slack integration for messaging and channel history., Post a message to a Slack channel, optionally in a thread., Respond to a slash command via response_url., Read recent messages from a Slack channel., SlackIntegration

### Community 56 - "GitHubIntegration"
Cohesion: 0.38
Nodes (4): GitHubIntegration, Any, retry, GitHub integration for issues, PRs, branches, and repository activity.

### Community 57 - "JiraIntegration"
Cohesion: 0.39
Nodes (4): JiraIntegration, Any, retry, Jira integration for tickets, updates, and remote links.

### Community 58 - "backend/tests/test_integrations.py"
Cohesion: 0.36
Nodes (3): Integration connector tests — mocked external service calls. Tests for GitHub,…, TestStripHtml, _strip_html()

### Community 62 - "_ensure_database_tables()"
Cohesion: 0.67
Nodes (3): _ensure_database_tables(), Guarantee all tables exist before the first request is served., on_event

## Knowledge Gaps
- **50 isolated node(s):** `nextConfig`, `name`, `version`, `private`, `dev` (+45 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 419 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_secrets()` connect `get_secrets()` to `tests/test_integrations.py`, `test_deployment_readiness.py`, `ironclaw.py`, `test_webhook_security.py`, `database/models.py`, `backend/main.py`, `get`, `test_webhooks.py`, `backend/database/models.py`, `EventSource`, `GmailIntegration`, `RedactingFilter`, `patch`, `backend/webhooks/server.py`, `GitHubIntegration`, `test_agent.py`, `get_session()`, `JiraIntegration`, `main.py`, `LLMClient`, `backend/tests/conftest.py`, `ConfluenceIntegration`, `verify_webhook_signature()`, `AppSecrets`, `ConfluenceIntegration`, `GmailIntegration`, `SlackIntegration`, `GitHubIntegration`, `JiraIntegration`?**
  _High betweenness centrality (0.293) - this node is a cross-community bridge._
- **Why does `Orchestrator` connect `Orchestrator` to `test_agent.py`, `get_session()`, `ConversationMemory`, `main.py`, `LLMClient`, `test_edge_cases.py`, `ToolRegistry`, `Planner`, `backend/main.py`, `backend/database/models.py`?**
  _High betweenness centrality (0.104) - this node is a cross-community bridge._
- **Why does `IronClawClient` connect `IronClawClient` to `Orchestrator`, `get_secrets()`, `ironclaw.py`, `backend/main.py`, `._completions_post()`, `TestModelConfigAPI`, `TestIronClawClient`?**
  _High betweenness centrality (0.097) - this node is a cross-community bridge._
- **Are the 36 inferred relationships involving `IronClawClient` (e.g. with `Orchestrator` and `_agent_summarize()`) actually correct?**
  _`IronClawClient` has 36 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `AgentEvent` (e.g. with `SlackCommandGateway` and `EventBus`) actually correct?**
  _`AgentEvent` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `Orchestrator` (e.g. with `ConversationMemory` and `Planner`) actually correct?**
  _`Orchestrator` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `nextConfig`, `name`, `version` to the rest of the system?**
  _50 weakly-connected nodes found - possible documentation gaps or missing edges._