# Graph Report - Mac-developer-platform-agent  (2026-09-14)

## Corpus Check
- 121 files · ~211,849 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 4, .ini 2, .example 1)

## Summary
- 1252 nodes · 2377 edges · 100 communities (69 shown, 11 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 251 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- ToolRegistry
- Orchestrator
- main.py
- package.json
- api.ts
- tests/test_integrations.py
- SlackCommandGateway
- ConversationMemory
- EventBus
- load_all_workflows()
- test_webhook_security.py
- _import_main()
- EventBus
- AgentEvent
- test_webhooks_api.py
- database/models.py
- redact()
- test_model_config.py
- WorkflowDefinition
- get_session()
- AgentEvent
- WorkflowEngine
- GmailIntegration
- compilerOptions
- JenkinsIntegration
- backend/tests/conftest.py
- test_webhooks.py
- test_edge_cases.py
- ._completions_post()
- GitHubIntegration
- SlackIntegration
- Planner
- patch
- backend/webhooks/server.py
- backend/main.py
- _build_orchestrator()
- RedactingFilter
- TestIronClawClient
- ToolRegistry
- test_agent.py
- IronClawClient
- test_deployment_readiness.py
- JiraIntegration
- get
- LLMClient
- AgentLog
- GmailIntegration
- SlackIntegration
- RedactingFilter
- ConversationMemory
- GitHubIntegration
- verify_webhook_signature()
- ConfluenceIntegration
- JiraIntegration
- TestIronClawEdgeCases
- backend/tests/test_integrations.py
- backend/database/models.py
- WorkflowDefinition
- TestWorkflowEngine
- TestAPIEndpointEdgeCases
- get_secrets()
- tests/test_security.py
- TestModelConfigAPI
- security/secrets.py
- agent/orchestrator.py
- AgentConversation
- .run_workflow()
- .subscribe()
- tests/conftest.py
- AgentMemory
- backend/workflows/engine.py
- TestToolCallPattern
- .get_context()
- TestDashboardAPIWorkflowRuns
- TestSlackWebhook
- next.config.js
- graphify_pipeline.py
- db_session()
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
- `db_session()` --uses--> `Base`  [INFERRED]
  tests/test_database.py → backend/database/models.py

## Import Cycles
- None detected.

## Communities (100 total, 11 thin omitted)

### Community 0 - "ToolRegistry"
Cohesion: 0.06
Nodes (26): Orchestrator, Any, Look up tool, invoke it, persist result, return result string., Store a completed agent conversation in PostgreSQL., Coordinates between IronClaw (reasoning) and tool execution (Python). All…, Register a tool in the schema registry., Process a user message by delegating reasoning to IronClaw and executing the…, Unit tests for tools.registry.ToolRegistry. (+18 more)

### Community 1 - "Orchestrator"
Cohesion: 0.07
Nodes (24): Orchestrator, Any, Register a tool. Args: name: Unique tool name. func: Callable to invoke (sync…, Return the callable for the given tool name, or None., Main agent orchestrator: manages LLM, planner, memory, and tool execution., Delegate to ToolRegistry., Process a user message: add to memory, send to LLM, execute tools as needed.…, Look up tool, invoke it, store result in ToolOutput, return result string.… (+16 more)

### Community 2 - "main.py"
Cohesion: 0.09
Nodes (26): _chat_loop(), _print_banner(), Interactive CLI chat interface for the developer automation agent., start_chat(), _agent_summarize(), _build_orchestrator(), chat(), cli() (+18 more)

### Community 3 - "package.json"
Cohesion: 0.05
Nodes (34): dependencies, next, react, react-dom, devDependencies, autoprefixer, postcss, tailwindcss (+26 more)

### Community 4 - "api.ts"
Cohesion: 0.09
Nodes (22): EventsPage(), sourceBadge(), LEVEL_COLORS, LEVELS, connectorColor(), ToolsPage(), statusBadge(), WorkflowRunsPage() (+14 more)

### Community 5 - "tests/test_integrations.py"
Cohesion: 0.07
Nodes (7): fixture, Tests for all integration connectors., TestConfluenceIntegration, TestGitHubIntegration, TestGmailIntegration, TestJiraIntegration, TestSlackIntegration

### Community 6 - "SlackCommandGateway"
Cohesion: 0.11
Nodes (13): Any, Routes Slack messages mentioning @claw to the orchestrator and sends results…, Process a Slack event that may contain a @claw command., Extract command text, send to orchestrator, reply in Slack., Strip the @claw mention prefix from the message text., Send a threaded reply back to Slack., SlackCommandGateway, Messages containing 'claw' (not app_mention) should be handled. (+5 more)

### Community 7 - "ConversationMemory"
Cohesion: 0.11
Nodes (9): ConversationMemory, Stores conversation history for the agent and provides context retrieval., Initialize empty conversation history., Add a message to the conversation history. Args: role: Message role (e.g.…, Return a one-line summary of the conversation so far. Returns: Brief summary…, Clear all conversation history., Return messages in OpenAI-style format for API calls. Returns: List of dicts…, TestConversationMemory (+1 more)

### Community 8 - "EventBus"
Cohesion: 0.10
Nodes (12): EventBus, Subscriber, Simple topic-based publish/subscribe event bus. Events are persisted to…, Publish an event — persists to DB and dispatches to subscribers., Write event to PostgreSQL., Validate WorkflowEngine.load() with the real YAML directory., TestWorkflowEngineLoad, Any (+4 more)

### Community 9 - "load_all_workflows()"
Cohesion: 0.12
Nodes (9): Validate that real YAML workflow files load correctly., TestWorkflowLoading, TestWorkflowLoader, TestLoadAllWorkflows, TestLoadWorkflow, Load workflow definitions and subscribe triggers to the event bus., load_all_workflows(), load_workflow() (+1 more)

### Community 10 - "test_webhook_security.py"
Cohesion: 0.10
Nodes (12): _github_signature(), fixture, Webhook signature verification tests — ensure invalid requests are rejected.…, Slack URL verification should work even with signing enabled., Jenkins webhook without signature header still passes (only rejects bad sigs)., TestClient with webhook secrets configured., secured_client(), _slack_signature() (+4 more)

### Community 11 - "_import_main()"
Cohesion: 0.13
Nodes (10): _import_main(), patch, Validate that the CLI group can be invoked., Import main with load_dotenv safely patched., Validate _build_orchestrator registers all expected tools., With no tokens, only gmail + agent.summarize are registered., Validate _wire_app attaches state to the FastAPI app., TestAppWiring (+2 more)

### Community 12 - "EventBus"
Cohesion: 0.16
Nodes (9): asyncio, Unit tests for events.types and events.bus., TestEventBus, TestEventSource, EventBus, Simple topic-based publish/subscribe event bus., Publish an event — persists to DB and dispatches to subscribers., Write event to the local SQLite database. (+1 more)

### Community 13 - "AgentEvent"
Cohesion: 0.16
Nodes (7): TestAgentEvent, AgentEvent, BaseModel, Canonical event that flows through the internal bus., asyncio, TestAgentEvent, TestEventBus

### Community 14 - "test_webhooks_api.py"
Cohesion: 0.10
Nodes (11): client(), fixture, Integration tests for webhooks/server.py — webhook and dashboard API endpoints., TestDashboardAPIEvents, TestDashboardAPIStatus, TestDashboardAPITools, TestDashboardAPIWorkflows, TestGitHubWebhook (+3 more)

### Community 15 - "database/models.py"
Cohesion: 0.17
Nodes (11): Main orchestrator — delegates reasoning to IronClaw, executes tools locally.…, Base, CachedSummary, DeclarativeBase, SQLAlchemy models and database session management., ToolOutput, WorkflowRun, Tests for database/models.py. (+3 more)

### Community 16 - "redact()"
Cohesion: 0.16
Nodes (5): TestSecurityEdgeCases, TestRedact, Replace known secret patterns with <REDACTED>., redact(), TestRedact

### Community 17 - "test_model_config.py"
Cohesion: 0.15
Nodes (10): _mock_get_response(), _mock_response(), asyncio, Response, Tests for model configuration, OpenRouter fallback, and agent logs. Covers: -…, When Ollama fails and OpenRouter key is set, should fallback., Without OpenRouter key, Ollama failure should raise., TestAgentLogTable (+2 more)

### Community 18 - "WorkflowDefinition"
Cohesion: 0.20
Nodes (10): asyncio, Unit tests for workflows.loader and workflows.engine., TestWorkflowAction, TestWorkflowEngine, Tests for workflows/loader.py and workflows/engine.py., TestWorkflowAction, BaseModel, Load and validate YAML workflow definitions. (+2 more)

### Community 19 - "get_session()"
Cohesion: 0.13
Nodes (10): In-process async event bus with topic-based pub/sub., Unit tests for database.models — all tables and session management., TestEventModel, TestSessionManagement, TestToolOutputModel, TestWorkflowRunModel, Event, get_session() (+2 more)

### Community 20 - "AgentEvent"
Cohesion: 0.19
Nodes (16): AgentEvent, EventSource, BaseModel, Enum, str, Event type definitions for the internal event bus., Canonical event that flows through the internal bus., github_webhook() (+8 more)

### Community 21 - "WorkflowEngine"
Cohesion: 0.18
Nodes (5): asyncio, Previous step results should be merged into later step payloads., TestWorkflowEngineEdgeCases, Loads workflow definitions and executes them when matching events arrive., WorkflowEngine

### Community 22 - "GmailIntegration"
Cohesion: 0.21
Nodes (6): TestGmailIntegration, GmailIntegration, Any, retry, Gmail integration using google-api-python-client., Gmail integration for reading, sending, and summarizing emails.

### Community 23 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 24 - "JenkinsIntegration"
Cohesion: 0.14
Nodes (6): JenkinsIntegration, Any, retry, Jenkins integration using python-jenkins., Jenkins integration for triggering builds and fetching status/logs., TestJenkinsIntegration

### Community 25 - "backend/tests/conftest.py"
Cohesion: 0.15
Nodes (15): async_tool_func(), db_session(), mock_ironclaw_response(), fixture, Shared test fixtures — sets env vars, resets caches, provides mock helpers., Factory for IronClaw OpenAI-compatible response dicts., A simple sync tool function for registry tests., A simple async tool function for orchestrator tests. (+7 more)

### Community 26 - "test_webhooks.py"
Cohesion: 0.11
Nodes (8): client(), fixture, Tests for webhooks/server.py — FastAPI endpoint validation., TestGitHubWebhook, TestHealthEndpoint, TestJenkinsWebhook, TestJiraWebhook, TestSlackWebhook

### Community 27 - "test_edge_cases.py"
Cohesion: 0.17
Nodes (10): IronClaw Runtime client — HTTP interface to the Rust-based AI reasoning engine.…, Slack Command Gateway — primary developer interface. Handles @claw mentions and…, Edge case and error handling tests across all modules. Tests for boundary…, Unit tests for agent.slack_gateway.SlackCommandGateway., EventSource, Enum, str, Event type definitions for the internal event bus. (+2 more)

### Community 28 - "._completions_post()"
Cohesion: 0.16
Nodes (8): Any, Return (url, headers) based on current provider., Send a user message for interpretation and task planning., Delegate content summarization., Check IronClaw runtime health by querying /v1/models., Send a quick test prompt to verify a model is reachable., Send a chat completions request using the active provider., Send a POST request to IronClaw and return the JSON response.

### Community 29 - "GitHubIntegration"
Cohesion: 0.20
Nodes (6): TestGitHubIntegration, GitHubIntegration, Any, retry, GitHub integration using PyGithub., GitHub integration for issues, PRs, branches, and repository activity.

### Community 30 - "SlackIntegration"
Cohesion: 0.17
Nodes (9): TestSlackIntegration, Any, retry, Slack integration for messaging and channel history., Initialize Slack WebClient with token from secrets., Post a message to a Slack channel., Respond to a slash command via response_url., Read recent messages from a Slack channel. (+1 more)

### Community 31 - "Planner"
Cohesion: 0.19
Nodes (7): Planner, Any, Decomposes user requests into structured action plans using an LLM., Initialize the planner with an LLM client. Args: llm_client: Client with async…, asyncio, TestOrchestrator, TestPlanner

### Community 32 - "patch"
Cohesion: 0.24
Nodes (6): patch, TestJenkinsIntegration, JenkinsIntegration, Any, retry, Jenkins integration for triggering builds and fetching status/logs.

### Community 33 - "backend/webhooks/server.py"
Cohesion: 0.28
Nodes (15): github_webhook(), jenkins_webhook(), jira_webhook(), _persist_log(), post, Request, FastAPI webhook server + dashboard API. Webhook endpoints: POST…, Switch the active model and provider at runtime. (+7 more)

### Community 34 - "backend/main.py"
Cohesion: 0.19
Nodes (14): cli(), command, group, option, pass_context, Developer Automation Agent — main entry point. CLI commands: claw-agent run —…, Attach orchestrator + workflow engine + Slack gateway to the FastAPI app., Claw Agent — Developer Automation Platform. (+6 more)

### Community 35 - "_build_orchestrator()"
Cohesion: 0.19
Nodes (8): _agent_summarize(), _build_orchestrator(), Delegate summarization to IronClaw. Used by workflow agent.summarize., TestConfluenceIntegration, ConfluenceIntegration, Any, retry, Confluence integration for search, pages, and content.

### Community 36 - "RedactingFilter"
Cohesion: 0.15
Nodes (13): AppSecrets, get_secrets(), BaseSettings, LogRecord, Secure credential loading and redaction utilities., Validate an HMAC webhook signature., Logging filter that scrubs sensitive patterns from log records., Central secrets model — all values loaded from env vars / .env. (+5 more)

### Community 37 - "TestIronClawClient"
Cohesion: 0.26
Nodes (7): _mock_get_response(), _mock_response(), asyncio, Response, Unit tests for agent.ironclaw.IronClawClient., Build an httpx.Response with a request attached so raise_for_status works., TestIronClawClient

### Community 38 - "ToolRegistry"
Cohesion: 0.20
Nodes (6): Registry of available tools: name -> (callable, description)., Initialize empty registry., Return list of registered tool names., Return formatted string of all tool names and descriptions., ToolRegistry, TestToolRegistry

### Community 39 - "test_agent.py"
Cohesion: 0.23
Nodes (9): ActionPlan, PlanStep, BaseModel, Workflow planning module for decomposing user requests into tool steps., A single step in an action plan., Structured plan for executing a user request across multiple tool calls., Create an action plan from a user request using available tools. Args:…, Tests for agent/memory.py, agent/planner.py, and agent/orchestrator.py. (+1 more)

### Community 40 - "IronClawClient"
Cohesion: 0.20
Nodes (4): IronClawClient, HTTP client for the IronClaw Rust-based reasoning runtime. Communicates via…, Switch the active model at runtime. Returns the new config., TestIronClawModelConfig

### Community 41 - "test_deployment_readiness.py"
Cohesion: 0.15
Nodes (9): Deployment readiness tests — validate that the app can wire up and boot. These…, Validate that all expected tables are created., Validate that the FastAPI app can be imported without error., TestDatabaseTablesExist, TestFastAPIAppImportable, _ensure_database_tables(), Guarantee all tables exist before the first request is served., get_engine() (+1 more)

### Community 42 - "JiraIntegration"
Cohesion: 0.24
Nodes (5): TestJiraIntegration, JiraIntegration, Any, retry, Jira integration for tickets, updates, and remote links.

### Community 43 - "get"
Cohesion: 0.14
Nodes (14): api_agent_conversations(), api_events(), api_logs(), api_tools(), api_workflow_runs(), api_workflows(), health(), get (+6 more)

### Community 44 - "LLMClient"
Cohesion: 0.21
Nodes (6): LLMClient, Create LLMClient, Planner, ConversationMemory, and ToolRegistry., Configurable LLM client supporting OpenRouter, OpenAI, and Ollama., Initialize client from secrets (provider, base_url, api_key)., Send messages to the LLM and return the assistant content. Args: messages: List…, TestLLMClient

### Community 45 - "AgentLog"
Cohesion: 0.22
Nodes (4): AgentLog, fixture, Webhook handler should persist a log entry., TestAgentLogsAPI

### Community 46 - "GmailIntegration"
Cohesion: 0.33
Nodes (5): GmailIntegration, Any, retry, Gmail integration using google-api-python-client., Gmail integration for reading, sending, and summarizing emails.

### Community 47 - "SlackIntegration"
Cohesion: 0.21
Nodes (8): Any, retry, Slack integration using slack_sdk WebClient., Slack integration for messaging and channel history., Post a message to a Slack channel, optionally in a thread., Respond to a slash command via response_url., Read recent messages from a Slack channel., SlackIntegration

### Community 48 - "RedactingFilter"
Cohesion: 0.21
Nodes (6): Unit tests for security.secrets., TestRedactingFilter, LogRecord, Logging filter that scrubs sensitive patterns from log records., RedactingFilter, TestRedactingFilter

### Community 49 - "ConversationMemory"
Cohesion: 0.17
Nodes (5): ConversationMemory, Any, Conversation memory for maintaining chat history and context., Stores conversation history for the agent and provides context retrieval., Return messages in role/content format for IronClaw context.

### Community 50 - "GitHubIntegration"
Cohesion: 0.29
Nodes (5): GitHubIntegration, Any, retry, GitHub integration using PyGithub., GitHub integration for issues, PRs, branches, and repository activity.

### Community 51 - "verify_webhook_signature()"
Cohesion: 0.23
Nodes (5): verify_webhook_signature should work with sha1 too., TestVerifyWebhookSignature, Validate an HMAC webhook signature., verify_webhook_signature(), TestVerifyWebhookSignature

### Community 52 - "ConfluenceIntegration"
Cohesion: 0.27
Nodes (6): ConfluenceIntegration, Any, retry, Confluence integration using atlassian-python-api., Confluence integration for search, pages, and content., _strip_html()

### Community 53 - "JiraIntegration"
Cohesion: 0.29
Nodes (5): JiraIntegration, Any, retry, Jira integration using the jira Python SDK., Jira integration for tickets, updates, and remote links.

### Community 54 - "TestIronClawEdgeCases"
Cohesion: 0.24
Nodes (5): _mock_response(), Response, When IronClaw returns an empty choices array., When IronClaw returns invalid JSON in tool_calls arguments., TestIronClawEdgeCases

### Community 55 - "backend/tests/test_integrations.py"
Cohesion: 0.27
Nodes (4): Integration connector tests — mocked external service calls. Tests for GitHub,…, TestStripHtml, Confluence integration using atlassian-python-api., _strip_html()

### Community 56 - "backend/database/models.py"
Cohesion: 0.29
Nodes (9): Base, Event, get_engine(), get_session(), DeclarativeBase, Session, SQLAlchemy models and PostgreSQL session management., ToolOutput (+1 more)

### Community 57 - "WorkflowDefinition"
Cohesion: 0.36
Nodes (8): load_all_workflows(), load_workflow(), BaseModel, Path, Load and validate YAML workflow definitions., WorkflowAction, WorkflowDefinition, TestWorkflowDefinition

### Community 58 - "TestWorkflowEngine"
Cohesion: 0.27
Nodes (3): asyncio, fixture, TestWorkflowEngine

### Community 59 - "TestAPIEndpointEdgeCases"
Cohesion: 0.22
Nodes (3): fixture, Status should work even when orchestrator isn't attached., TestAPIEndpointEdgeCases

### Community 60 - "get_secrets()"
Cohesion: 0.25
Nodes (7): TestAppSecrets, api_model_config(), api_status(), System status: IronClaw health, database connectivity, integrations., Return the current model configuration and available models., get_secrets(), Return the singleton secrets instance.

### Community 61 - "tests/test_security.py"
Cohesion: 0.25
Nodes (5): AppSecrets, BaseSettings, Central secrets model — all values loaded from env vars / .env., Tests for security/secrets.py., TestAppSecrets

### Community 63 - "security/secrets.py"
Cohesion: 0.25
Nodes (4): Jenkins integration using python-jenkins., Jira integration using the jira Python SDK., Slack integration using slack_sdk WebClient., Secure credential loading and redaction utilities.

### Community 64 - "agent/orchestrator.py"
Cohesion: 0.33
Nodes (3): Conversation memory module for maintaining chat history and context., Main orchestrator — the brain of the Developer Automation Agent., Unit tests for agent.memory.ConversationMemory.

### Community 65 - "AgentConversation"
Cohesion: 0.47
Nodes (3): AgentConversation, TestAgentConversationModel, TestDashboardAPIConversations

### Community 66 - ".run_workflow()"
Cohesion: 0.40
Nodes (3): _is_coroutine(), Any, Register an executable tool that workflows can invoke.

### Community 67 - ".subscribe()"
Cohesion: 0.40
Nodes (3): Subscriber, Register a handler for a specific event type., Register a handler that receives every event.

### Community 68 - "tests/conftest.py"
Cohesion: 0.50
Nodes (4): env_secrets(), fixture, Shared fixtures for the test suite., _reset_secrets_cache()

### Community 77 - "db_session()"
Cohesion: 0.67
Nodes (3): db_session(), fixture, Create an in-memory SQLite session for testing.

## Knowledge Gaps
- **50 isolated node(s):** `nextConfig`, `name`, `version`, `private`, `dev` (+45 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 434 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_secrets()` connect `get_secrets()` to `main.py`, `test_webhook_security.py`, `database/models.py`, `AgentEvent`, `GmailIntegration`, `JenkinsIntegration`, `backend/tests/conftest.py`, `test_webhooks.py`, `test_edge_cases.py`, `GitHubIntegration`, `SlackIntegration`, `patch`, `backend/webhooks/server.py`, `backend/main.py`, `_build_orchestrator()`, `test_agent.py`, `IronClawClient`, `test_deployment_readiness.py`, `JiraIntegration`, `LLMClient`, `GmailIntegration`, `SlackIntegration`, `RedactingFilter`, `GitHubIntegration`, `ConfluenceIntegration`, `JiraIntegration`, `backend/tests/test_integrations.py`, `backend/database/models.py`, `tests/test_security.py`, `security/secrets.py`, `agent/orchestrator.py`, `tests/conftest.py`?**
  _High betweenness centrality (0.265) - this node is a cross-community bridge._
- **Why does `Orchestrator` connect `Orchestrator` to `agent/orchestrator.py`, `backend/main.py`, `_build_orchestrator()`, `main.py`, `ConversationMemory`, `test_agent.py`, `LLMClient`, `backend/database/models.py`, `test_edge_cases.py`, `Planner`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Why does `WorkflowEngine` connect `WorkflowEngine` to `backend/main.py`, `main.py`, `.run_workflow()`, `EventBus`, `test_deployment_readiness.py`, `load_all_workflows()`, `WorkflowDefinition`, `AgentEvent`, `backend/database/models.py`, `WorkflowDefinition`, `TestWorkflowEngine`, `test_edge_cases.py`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Are the 36 inferred relationships involving `IronClawClient` (e.g. with `Orchestrator` and `_agent_summarize()`) actually correct?**
  _`IronClawClient` has 36 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `AgentEvent` (e.g. with `SlackCommandGateway` and `EventBus`) actually correct?**
  _`AgentEvent` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `Orchestrator` (e.g. with `ConversationMemory` and `Planner`) actually correct?**
  _`Orchestrator` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `nextConfig`, `name`, `version` to the rest of the system?**
  _50 weakly-connected nodes found - possible documentation gaps or missing edges._