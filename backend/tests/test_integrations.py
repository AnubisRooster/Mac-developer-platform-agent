"""Integration connector tests — mocked external service calls.

Tests for GitHub, Jira, Slack, Jenkins, Confluence, Gmail integrations
using mocked SDK clients to validate call patterns and return formats.
"""

from unittest.mock import MagicMock, patch, PropertyMock

import pytest


# ─── Confluence helpers ──────────────────────────────────────────────────────

class TestStripHtml:
    def test_strips_tags(self):
        from integrations.confluence import _strip_html
        assert _strip_html("<p>Hello <b>world</b></p>") == "Hello world"

    def test_empty_string(self):
        from integrations.confluence import _strip_html
        assert _strip_html("") == ""

    def test_none_returns_empty(self):
        from integrations.confluence import _strip_html
        assert _strip_html(None) == ""

    def test_unescapes_entities(self):
        from integrations.confluence import _strip_html
        assert "R&D" in _strip_html("<p>R&amp;D</p>")

    def test_collapses_whitespace(self):
        from integrations.confluence import _strip_html
        result = _strip_html("<div>  too   many   spaces  </div>")
        assert "  " not in result


# ─── Slack Integration ───────────────────────────────────────────────────────

class TestSlackIntegration:
    @patch("integrations.slack.WebClient")
    def test_send_message(self, mock_webclient_cls):
        mock_client = MagicMock()
        mock_client.chat_postMessage.return_value = {"ts": "123.456", "channel": "C01", "ok": True}
        mock_webclient_cls.return_value = mock_client

        from integrations.slack import SlackIntegration
        slack = SlackIntegration()
        slack._client = mock_client
        result = slack.send_message(channel="#test", text="hello")
        assert result["ok"] is True
        assert result["ts"] == "123.456"
        mock_client.chat_postMessage.assert_called_once()

    @patch("integrations.slack.WebClient")
    def test_send_message_with_thread(self, mock_webclient_cls):
        mock_client = MagicMock()
        mock_client.chat_postMessage.return_value = {"ts": "123.456", "channel": "C01", "ok": True}
        mock_webclient_cls.return_value = mock_client

        from integrations.slack import SlackIntegration
        slack = SlackIntegration()
        slack._client = mock_client
        slack.send_message(channel="#test", text="reply", thread_ts="100.200")
        call_kwargs = mock_client.chat_postMessage.call_args[1]
        assert call_kwargs["thread_ts"] == "100.200"

    @patch("integrations.slack.WebClient")
    def test_read_channel_history(self, mock_webclient_cls):
        mock_client = MagicMock()
        mock_client.conversations_history.return_value = {
            "messages": [
                {"ts": "1", "user": "U01", "text": "hi", "type": "message"},
                {"ts": "2", "user": "U02", "text": "hello", "type": "message"},
            ]
        }
        mock_webclient_cls.return_value = mock_client

        from integrations.slack import SlackIntegration
        slack = SlackIntegration()
        slack._client = mock_client
        result = slack.read_channel_history(channel="C01", limit=10)
        assert len(result) == 2
        assert result[0]["text"] == "hi"

    @patch("integrations.slack.WebClient")
    @patch("integrations.slack.httpx.Client")
    def test_respond_to_command(self, mock_httpx_cls, mock_webclient_cls):
        mock_http = MagicMock()
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.status_code = 200
        mock_http.__enter__ = MagicMock(return_value=mock_http)
        mock_http.__exit__ = MagicMock(return_value=False)
        mock_http.post.return_value = mock_response
        mock_httpx_cls.return_value = mock_http

        mock_webclient_cls.return_value = MagicMock()

        from integrations.slack import SlackIntegration
        slack = SlackIntegration()
        result = slack.respond_to_command("https://hooks.slack.com/response", "Done!")
        assert result["ok"] is True


# ─── GitHub Integration ──────────────────────────────────────────────────────

class TestGitHubIntegration:
    @patch("integrations.github_integration.Github")
    def test_create_issue(self, mock_github_cls):
        mock_client = MagicMock()
        mock_repo = MagicMock()
        mock_issue = MagicMock()
        mock_issue.number = 42
        mock_issue.html_url = "https://github.com/org/repo/issues/42"
        mock_issue.title = "Test Issue"
        mock_repo.create_issue.return_value = mock_issue
        mock_client.get_repo.return_value = mock_repo
        mock_github_cls.return_value = mock_client

        from integrations.github_integration import GitHubIntegration
        gh = GitHubIntegration()
        result = gh.create_issue("org/repo", "Test Issue", "Body text")
        assert result["number"] == 42
        assert result["title"] == "Test Issue"

    @patch("integrations.github_integration.Github")
    def test_summarize_pr(self, mock_github_cls):
        mock_client = MagicMock()
        mock_repo = MagicMock()
        mock_pr = MagicMock()
        mock_pr.title = "Add feature"
        mock_pr.body = "Description here"
        mock_pr.changed_files = 3
        mock_pr.additions = 100
        mock_pr.deletions = 20
        mock_pr.html_url = "https://github.com/org/repo/pull/1"
        mock_pr.state = "open"
        mock_repo.get_pull.return_value = mock_pr
        mock_client.get_repo.return_value = mock_repo
        mock_github_cls.return_value = mock_client

        from integrations.github_integration import GitHubIntegration
        gh = GitHubIntegration()
        result = gh.summarize_pull_request("org/repo", 1)
        assert result["title"] == "Add feature"
        assert result["changed_files_count"] == 3
        assert result["state"] == "open"

    @patch("integrations.github_integration.Github")
    def test_comment_on_pr(self, mock_github_cls):
        mock_client = MagicMock()
        mock_repo = MagicMock()
        mock_pr = MagicMock()
        mock_comment = MagicMock()
        mock_comment.html_url = "https://github.com/org/repo/pull/1#comment-1"
        mock_comment.id = 999
        mock_pr.create_issue_comment.return_value = mock_comment
        mock_repo.get_pull.return_value = mock_pr
        mock_client.get_repo.return_value = mock_repo
        mock_github_cls.return_value = mock_client

        from integrations.github_integration import GitHubIntegration
        gh = GitHubIntegration()
        result = gh.comment_on_pr("org/repo", 1, "LGTM")
        assert result["id"] == 999

    @patch("integrations.github_integration.Github")
    def test_create_branch(self, mock_github_cls):
        mock_client = MagicMock()
        mock_repo = MagicMock()
        mock_repo.html_url = "https://github.com/org/repo"
        mock_branch = MagicMock()
        mock_branch.commit.sha = "abc123"
        mock_repo.get_branch.return_value = mock_branch
        mock_ref = MagicMock()
        mock_ref.ref = "refs/heads/feature-x"
        mock_repo.create_git_ref.return_value = mock_ref
        mock_client.get_repo.return_value = mock_repo
        mock_github_cls.return_value = mock_client

        from integrations.github_integration import GitHubIntegration
        gh = GitHubIntegration()
        result = gh.create_branch("org/repo", "feature-x")
        assert result["ref"] == "refs/heads/feature-x"


# ─── Jira Integration ────────────────────────────────────────────────────────

class TestJiraIntegration:
    @patch("integrations.jira_integration.JIRA")
    def test_create_ticket(self, mock_jira_cls):
        mock_client = MagicMock()
        mock_issue = MagicMock()
        mock_issue.key = "PROJ-123"
        mock_issue.fields.summary = "New ticket"
        mock_client.create_issue.return_value = mock_issue
        mock_client.server_url = "https://jira.fake"
        mock_jira_cls.return_value = mock_client

        from integrations.jira_integration import JiraIntegration
        jira = JiraIntegration()
        result = jira.create_ticket("PROJ", "New ticket", "Description")
        assert result["key"] == "PROJ-123"

    @patch("integrations.jira_integration.JIRA")
    def test_update_ticket(self, mock_jira_cls):
        mock_client = MagicMock()
        mock_issue = MagicMock()
        mock_client.issue.return_value = mock_issue
        mock_jira_cls.return_value = mock_client

        from integrations.jira_integration import JiraIntegration
        jira = JiraIntegration()
        result = jira.update_ticket("PROJ-1", summary="Updated")
        assert result["updated"] is True
        mock_issue.update.assert_called_once()

    @patch("integrations.jira_integration.JIRA")
    def test_get_ticket_details(self, mock_jira_cls):
        mock_client = MagicMock()
        mock_issue = MagicMock()
        mock_issue.key = "PROJ-1"
        mock_issue.fields.summary = "Bug fix"
        mock_issue.fields.status = "In Progress"
        mock_issue.fields.assignee = None
        mock_issue.fields.description = "Fix the bug"
        mock_client.issue.return_value = mock_issue
        mock_jira_cls.return_value = mock_client

        from integrations.jira_integration import JiraIntegration
        jira = JiraIntegration()
        result = jira.get_ticket_details("PROJ-1")
        assert result["key"] == "PROJ-1"
        assert result["assignee"] is None

    @patch("integrations.jira_integration.JIRA")
    def test_link_github_issue(self, mock_jira_cls):
        mock_client = MagicMock()
        mock_jira_cls.return_value = mock_client

        from integrations.jira_integration import JiraIntegration
        jira = JiraIntegration()
        result = jira.link_github_issue("PROJ-1", "https://github.com/org/repo/issues/1")
        assert result["linked"] is True


# ─── Jenkins Integration ─────────────────────────────────────────────────────

class TestJenkinsIntegration:
    @patch("integrations.jenkins.jenkins.Jenkins")
    def test_trigger_build(self, mock_jenkins_cls):
        mock_client = MagicMock()
        mock_client.build_job.return_value = 42
        mock_jenkins_cls.return_value = mock_client

        from integrations.jenkins import JenkinsIntegration
        jk = JenkinsIntegration()
        result = jk.trigger_build("my-job")
        assert result["queue_id"] == 42

    @patch("integrations.jenkins.jenkins.Jenkins")
    def test_get_build_status_specific(self, mock_jenkins_cls):
        mock_client = MagicMock()
        mock_client.get_build_info.return_value = {
            "number": 10, "result": "SUCCESS", "url": "http://j/10", "duration": 5000
        }
        mock_jenkins_cls.return_value = mock_client

        from integrations.jenkins import JenkinsIntegration
        jk = JenkinsIntegration()
        result = jk.get_build_status("my-job", build_number=10)
        assert result["status"] == "SUCCESS"
        assert result["number"] == 10

    @patch("integrations.jenkins.jenkins.Jenkins")
    def test_get_build_status_latest(self, mock_jenkins_cls):
        mock_client = MagicMock()
        mock_client.get_job_info.return_value = {"lastBuild": {"number": 5}}
        mock_client.get_build_info.return_value = {
            "number": 5, "result": "FAILURE", "url": "http://j/5", "duration": 3000
        }
        mock_jenkins_cls.return_value = mock_client

        from integrations.jenkins import JenkinsIntegration
        jk = JenkinsIntegration()
        result = jk.get_build_status("my-job")
        assert result["number"] == 5

    @patch("integrations.jenkins.jenkins.Jenkins")
    def test_get_build_status_no_builds(self, mock_jenkins_cls):
        mock_client = MagicMock()
        mock_client.get_job_info.return_value = {"lastBuild": None}
        mock_jenkins_cls.return_value = mock_client

        from integrations.jenkins import JenkinsIntegration
        jk = JenkinsIntegration()
        result = jk.get_build_status("my-job")
        assert result["status"] == "unknown"

    @patch("integrations.jenkins.jenkins.Jenkins")
    def test_fetch_build_logs(self, mock_jenkins_cls):
        mock_client = MagicMock()
        mock_client.get_build_console_output.return_value = "BUILD SUCCESS\nDone."
        mock_jenkins_cls.return_value = mock_client

        from integrations.jenkins import JenkinsIntegration
        jk = JenkinsIntegration()
        result = jk.fetch_build_logs("my-job", build_number=1)
        assert "BUILD SUCCESS" in result["log_tail"]

    @patch("integrations.jenkins.jenkins.Jenkins")
    def test_fetch_build_logs_truncates(self, mock_jenkins_cls):
        mock_client = MagicMock()
        mock_client.get_build_console_output.return_value = "x" * 10000
        mock_jenkins_cls.return_value = mock_client

        from integrations.jenkins import JenkinsIntegration
        jk = JenkinsIntegration()
        result = jk.fetch_build_logs("my-job", build_number=1)
        assert len(result["log_tail"]) == 5000


# ─── Confluence Integration ──────────────────────────────────────────────────

class TestConfluenceIntegration:
    @patch("integrations.confluence.Confluence")
    def test_search_docs(self, mock_conf_cls):
        mock_client = MagicMock()
        mock_client.url = "https://wiki.fake"
        mock_client.cql.return_value = {
            "results": [{"content": {"title": "Setup Guide", "id": "123"}}]
        }
        mock_conf_cls.return_value = mock_client

        from integrations.confluence import ConfluenceIntegration
        conf = ConfluenceIntegration()
        results = conf.search_docs("setup")
        assert len(results) == 1
        assert results[0]["title"] == "Setup Guide"

    @patch("integrations.confluence.Confluence")
    def test_summarize_page(self, mock_conf_cls):
        mock_client = MagicMock()
        mock_client.url = "https://wiki.fake"
        mock_client.get_page_by_id.return_value = {
            "title": "Architecture",
            "body": {"storage": {"value": "<p>System design doc</p>"}},
        }
        mock_conf_cls.return_value = mock_client

        from integrations.confluence import ConfluenceIntegration
        conf = ConfluenceIntegration()
        result = conf.summarize_page("456")
        assert result["title"] == "Architecture"
        assert "System design doc" in result["content_preview"]

    @patch("integrations.confluence.Confluence")
    def test_create_page(self, mock_conf_cls):
        mock_client = MagicMock()
        mock_client.url = "https://wiki.fake"
        mock_client.create_page.return_value = {"id": "789", "title": "New Page"}
        mock_conf_cls.return_value = mock_client

        from integrations.confluence import ConfluenceIntegration
        conf = ConfluenceIntegration()
        result = conf.create_page("SPACE", "New Page", "<p>Content</p>")
        assert result["id"] == "789"


# ─── Gmail Integration ───────────────────────────────────────────────────────

class TestGmailIntegration:
    @patch("integrations.gmail.os.path.exists", return_value=False)
    def test_init_without_credentials(self, _):
        from integrations.gmail import GmailIntegration
        gmail = GmailIntegration()
        assert gmail._service is None

    @patch("integrations.gmail.os.path.exists", return_value=False)
    def test_ensure_service_returns_error(self, _):
        from integrations.gmail import GmailIntegration
        gmail = GmailIntegration()
        err = gmail._ensure_service()
        assert err is not None
        assert err["ok"] is False

    @patch("integrations.gmail.os.path.exists", return_value=False)
    def test_read_emails_without_service(self, _):
        from integrations.gmail import GmailIntegration
        gmail = GmailIntegration()
        result = gmail.read_emails()
        assert len(result) == 1
        assert result[0]["ok"] is False

    @patch("integrations.gmail.os.path.exists", return_value=False)
    def test_send_email_without_service(self, _):
        from integrations.gmail import GmailIntegration
        gmail = GmailIntegration()
        result = gmail.send_email("to@test.com", "Subject", "Body")
        assert result["ok"] is False

    @patch("integrations.gmail.os.path.exists", return_value=False)
    def test_summarize_thread_without_service(self, _):
        from integrations.gmail import GmailIntegration
        gmail = GmailIntegration()
        result = gmail.summarize_thread("thread-1")
        assert result["ok"] is False
