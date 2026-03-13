"""Developer Automation Agent — main entry point.

CLI commands:
    claw-agent run             — start the backend server (API + webhooks)
    claw-agent webhook-server  — alias for run
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

import click
import uvicorn
from dotenv import load_dotenv

load_dotenv()

_PROJECT_ROOT = Path(__file__).resolve().parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from security.secrets import RedactingFilter, get_secrets


def _setup_logging() -> None:
    log_dir = _PROJECT_ROOT.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stdout)]
    log_file = log_dir / "agent.log"
    handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
    logging.basicConfig(level=logging.INFO, format=fmt, handlers=handlers)
    for handler in logging.root.handlers:
        handler.addFilter(RedactingFilter())


async def _agent_summarize(
    content: str = "", instruction: str = "", log_tail: str = "", **kwargs
) -> str:
    """Delegate summarization to IronClaw. Used by workflow agent.summarize."""
    from agent.ironclaw import IronClawClient

    client = IronClawClient()
    text = content or log_tail or "(no content provided)"
    return await client.summarize(text, instruction)


def _build_orchestrator():
    from agent.orchestrator import Orchestrator
    from integrations.slack import SlackIntegration
    from integrations.github_integration import GitHubIntegration
    from integrations.jira_integration import JiraIntegration
    from integrations.confluence import ConfluenceIntegration
    from integrations.jenkins import JenkinsIntegration
    from integrations.gmail import GmailIntegration

    orch = Orchestrator()
    secrets = get_secrets()

    if secrets.slack_bot_token:
        slack = SlackIntegration()
        orch.register_tool(
            "slack.send_message",
            slack.send_message,
            "Send a message to a Slack channel",
            {
                "type": "object",
                "properties": {
                    "channel": {"type": "string", "description": "Slack channel ID or name"},
                    "text": {"type": "string", "description": "Message text"},
                    "thread_ts": {"type": "string", "description": "Thread timestamp for replies"},
                },
                "required": ["channel", "text"],
            },
        )
        orch.register_tool(
            "slack.read_channel_history",
            slack.read_channel_history,
            "Read recent messages from a Slack channel",
            {
                "type": "object",
                "properties": {
                    "channel": {"type": "string", "description": "Slack channel ID"},
                    "limit": {"type": "integer", "description": "Max messages to return", "default": 50},
                },
                "required": ["channel"],
            },
        )

    if secrets.github_token:
        gh = GitHubIntegration()
        orch.register_tool(
            "github.create_issue",
            gh.create_issue,
            "Create a GitHub issue",
            {
                "type": "object",
                "properties": {
                    "repo": {"type": "string", "description": "Repository (owner/repo)"},
                    "title": {"type": "string", "description": "Issue title"},
                    "body": {"type": "string", "description": "Issue body"},
                },
                "required": ["repo", "title"],
            },
        )
        orch.register_tool(
            "github.summarize_pr",
            gh.summarize_pull_request,
            "Summarize a GitHub pull request",
            {
                "type": "object",
                "properties": {
                    "repo": {"type": "string", "description": "Repository (owner/repo)"},
                    "pr_number": {"type": "integer", "description": "PR number"},
                },
                "required": ["repo", "pr_number"],
            },
        )
        orch.register_tool(
            "github.comment_on_pr",
            gh.comment_on_pr,
            "Comment on a GitHub pull request",
            {
                "type": "object",
                "properties": {
                    "repo": {"type": "string", "description": "Repository (owner/repo)"},
                    "pr_number": {"type": "integer", "description": "PR number"},
                    "comment": {"type": "string", "description": "Comment text"},
                },
                "required": ["repo", "pr_number", "comment"],
            },
        )
        orch.register_tool(
            "github.create_branch",
            gh.create_branch,
            "Create a new Git branch",
            {
                "type": "object",
                "properties": {
                    "repo": {"type": "string", "description": "Repository (owner/repo)"},
                    "branch_name": {"type": "string", "description": "New branch name"},
                    "from_branch": {"type": "string", "description": "Source branch", "default": "main"},
                },
                "required": ["repo", "branch_name"],
            },
        )
        orch.register_tool(
            "github.get_repo_activity",
            gh.get_repo_activity,
            "Get recent repository activity",
            {
                "type": "object",
                "properties": {
                    "repo": {"type": "string", "description": "Repository (owner/repo)"},
                    "days": {"type": "integer", "description": "Number of days to look back", "default": 1},
                },
                "required": ["repo"],
            },
        )

    if secrets.jira_api_token:
        jira = JiraIntegration()
        orch.register_tool(
            "jira.create_ticket",
            jira.create_ticket,
            "Create a Jira ticket",
            {
                "type": "object",
                "properties": {
                    "project": {"type": "string", "description": "Jira project key"},
                    "summary": {"type": "string", "description": "Ticket summary"},
                    "description": {"type": "string", "description": "Ticket description"},
                    "issue_type": {"type": "string", "description": "Issue type", "default": "Task"},
                },
                "required": ["project", "summary"],
            },
        )
        orch.register_tool(
            "jira.update_ticket",
            jira.update_ticket,
            "Update a Jira ticket",
            {
                "type": "object",
                "properties": {
                    "ticket_key": {"type": "string", "description": "Jira ticket key (e.g. PROJ-123)"},
                },
                "required": ["ticket_key"],
            },
        )
        orch.register_tool(
            "jira.link_github_issue",
            jira.link_github_issue,
            "Link a GitHub issue to a Jira ticket",
            {
                "type": "object",
                "properties": {
                    "ticket_key": {"type": "string", "description": "Jira ticket key"},
                    "github_url": {"type": "string", "description": "GitHub issue URL"},
                },
                "required": ["ticket_key", "github_url"],
            },
        )
        orch.register_tool(
            "jira.get_ticket_details",
            jira.get_ticket_details,
            "Get details of a Jira ticket",
            {
                "type": "object",
                "properties": {
                    "ticket_key": {"type": "string", "description": "Jira ticket key"},
                },
                "required": ["ticket_key"],
            },
        )

    if secrets.confluence_api_token:
        conf = ConfluenceIntegration()
        orch.register_tool(
            "confluence.search_docs",
            conf.search_docs,
            "Search Confluence documentation",
            {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "CQL search query"},
                    "limit": {"type": "integer", "description": "Max results", "default": 10},
                },
                "required": ["query"],
            },
        )
        orch.register_tool(
            "confluence.summarize_page",
            conf.summarize_page,
            "Summarize a Confluence page",
            {
                "type": "object",
                "properties": {
                    "page_id": {"type": "string", "description": "Confluence page ID"},
                },
                "required": ["page_id"],
            },
        )
        orch.register_tool(
            "confluence.create_page",
            conf.create_page,
            "Create a Confluence page",
            {
                "type": "object",
                "properties": {
                    "space": {"type": "string", "description": "Confluence space key"},
                    "title": {"type": "string", "description": "Page title"},
                    "body": {"type": "string", "description": "Page body (HTML)"},
                    "parent_id": {"type": "string", "description": "Parent page ID"},
                },
                "required": ["space", "title", "body"],
            },
        )

    if secrets.jenkins_api_token:
        jk = JenkinsIntegration()
        orch.register_tool(
            "jenkins.trigger_build",
            jk.trigger_build,
            "Trigger a Jenkins build",
            {
                "type": "object",
                "properties": {
                    "job_name": {"type": "string", "description": "Jenkins job name"},
                    "parameters": {"type": "object", "description": "Build parameters"},
                },
                "required": ["job_name"],
            },
        )
        orch.register_tool(
            "jenkins.get_build_status",
            jk.get_build_status,
            "Get Jenkins build status",
            {
                "type": "object",
                "properties": {
                    "job_name": {"type": "string", "description": "Jenkins job name"},
                    "build_number": {"type": "integer", "description": "Build number (latest if omitted)"},
                },
                "required": ["job_name"],
            },
        )
        orch.register_tool(
            "jenkins.fetch_logs",
            jk.fetch_build_logs,
            "Fetch Jenkins build logs",
            {
                "type": "object",
                "properties": {
                    "job_name": {"type": "string", "description": "Jenkins job name"},
                    "build_number": {"type": "integer", "description": "Build number (latest if omitted)"},
                },
                "required": ["job_name"],
            },
        )

    gmail = GmailIntegration()
    orch.register_tool(
        "gmail.read_emails",
        gmail.read_emails,
        "Read emails from Gmail",
        {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Gmail search query", "default": "is:unread"},
                "max_results": {"type": "integer", "description": "Max emails to return", "default": 10},
            },
        },
    )
    orch.register_tool(
        "gmail.summarize_thread",
        gmail.summarize_thread,
        "Summarize a Gmail thread",
        {
            "type": "object",
            "properties": {
                "thread_id": {"type": "string", "description": "Gmail thread ID"},
            },
            "required": ["thread_id"],
        },
    )
    orch.register_tool(
        "gmail.send_email",
        gmail.send_email,
        "Send an email via Gmail",
        {
            "type": "object",
            "properties": {
                "to": {"type": "string", "description": "Recipient email address"},
                "subject": {"type": "string", "description": "Email subject"},
                "body": {"type": "string", "description": "Email body text"},
            },
            "required": ["to", "subject", "body"],
        },
    )
    orch.register_tool(
        "gmail.read_thread",
        gmail.extract_action_items,
        "Extract action items from a Gmail thread",
        {
            "type": "object",
            "properties": {
                "thread_id": {"type": "string", "description": "Gmail thread ID"},
            },
            "required": ["thread_id"],
        },
    )

    orch.register_tool(
        "agent.summarize",
        _agent_summarize,
        "Summarize content using IronClaw",
        {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "Content to summarize"},
                "instruction": {"type": "string", "description": "Summarization instruction"},
            },
        },
    )

    return orch


def _setup_workflow_engine(orchestrator):
    from workflows.engine import WorkflowEngine

    workflow_dir = str(_PROJECT_ROOT.parent / "workflows")
    engine = WorkflowEngine(workflow_dir=workflow_dir)
    for name in orchestrator.registry.list_tools():
        handler = orchestrator.registry.get_handler(name)
        if handler:
            engine.register_tool(name, handler)
    engine.load()
    return engine


def _wire_app(orchestrator, workflow_engine):
    """Attach orchestrator + workflow engine + Slack gateway to the FastAPI app."""
    from webhooks.server import app

    app.state.orchestrator = orchestrator
    app.state.workflow_engine = workflow_engine

    secrets = get_secrets()
    if secrets.slack_bot_token:
        from agent.slack_gateway import SlackCommandGateway
        from integrations.slack import SlackIntegration

        slack = SlackIntegration()
        gateway = SlackCommandGateway(orchestrator, slack)
        app.state.slack_gateway = gateway


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Claw Agent — Developer Automation Platform."""
    _setup_logging()
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.option("--host", default=None, help="Bind host (default from .env or 0.0.0.0)")
@click.option("--port", default=None, type=int, help="Bind port (default from .env or 8080)")
def run(host: str | None, port: int | None):
    """Start the backend server (API + webhooks + Slack gateway)."""
    secrets = get_secrets()
    bind_host = host or secrets.webhook_host
    bind_port = port or secrets.webhook_port

    orchestrator = _build_orchestrator()
    workflow_engine = _setup_workflow_engine(orchestrator)
    _wire_app(orchestrator, workflow_engine)

    logging.getLogger("claw-agent").info(
        "Starting Claw Agent on %s:%s", bind_host, bind_port
    )
    uvicorn.run(
        "webhooks.server:app",
        host=bind_host,
        port=bind_port,
        log_level="info",
    )


@cli.command(name="webhook-server")
@click.option("--host", default=None)
@click.option("--port", default=None, type=int)
def webhook_server(host: str | None, port: int | None):
    """Alias for run."""
    ctx = click.get_current_context()
    ctx.invoke(run, host=host, port=port)


if __name__ == "__main__":
    cli()
