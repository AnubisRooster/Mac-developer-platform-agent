"""Gmail integration using google-api-python-client."""

from __future__ import annotations

import base64
import logging
import os
from email.mime.text import MIMEText
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from security.secrets import get_secrets

logger = logging.getLogger("claw-agent.integrations.gmail")

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/gmail.send", "https://www.googleapis.com/auth/gmail.modify"]


class GmailIntegration:
    """Gmail integration for reading, sending, and summarizing emails."""

    def __init__(self) -> None:
        self._logger = logger
        secrets = get_secrets()
        self._credentials_path = secrets.gmail_credentials_file
        self._token_path = secrets.gmail_token_file
        self._service = self._build_service()

    def _build_service(self) -> Any:
        creds = None
        if os.path.exists(self._token_path):
            try:
                creds = Credentials.from_authorized_user_file(self._token_path, SCOPES)
            except Exception as e:
                self._logger.warning("Failed to load token file %s: %s", self._token_path, e)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception:
                    pass
            if not creds or not creds.valid:
                if not os.path.exists(self._credentials_path):
                    self._logger.warning("Gmail OAuth not configured: credentials file %s not found.", self._credentials_path)
                    return None
                self._logger.warning("Gmail OAuth flow needed: token file %s missing or invalid.", self._token_path)
                return None
        try:
            return build("gmail", "v1", credentials=creds)
        except Exception as e:
            self._logger.warning("Failed to build Gmail service: %s", e)
            return None

    def _ensure_service(self) -> dict[str, Any] | None:
        if self._service is None:
            return {"ok": False, "error": "Gmail credentials not configured. Run OAuth flow to create token file."}
        return None

    @retry(
        retry=retry_if_exception_type(Exception),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    def read_emails(self, query: str = "is:unread", max_results: int = 10) -> list[dict[str, Any]]:
        err = self._ensure_service()
        if err:
            return [err]
        self._logger.info("Reading emails: query=%s, max=%s", query, max_results)
        results = self._service.users().messages().list(userId="me", q=query, maxResults=max_results).execute()
        messages = results.get("messages", [])
        out = []
        for msg_ref in messages:
            msg = self._service.users().messages().get(userId="me", id=msg_ref["id"], format="metadata", metadataHeaders=["Subject", "From", "Date"]).execute()
            headers = {h["name"].lower(): h["value"] for h in msg.get("payload", {}).get("headers", [])}
            out.append({"id": msg["id"], "subject": headers.get("subject", ""), "from": headers.get("from", ""), "snippet": msg.get("snippet", ""), "date": headers.get("date", "")})
        return out

    @retry(
        retry=retry_if_exception_type(Exception),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    def summarize_thread(self, thread_id: str) -> dict[str, Any]:
        err = self._ensure_service()
        if err:
            return err
        self._logger.info("Summarizing thread %s", thread_id)
        thread = self._service.users().threads().get(userId="me", id=thread_id, format="metadata", metadataHeaders=["Subject", "From", "Date"]).execute()
        messages_data = []
        for msg in thread.get("messages", []):
            headers = {h["name"].lower(): h["value"] for h in msg.get("payload", {}).get("headers", [])}
            messages_data.append({"from": headers.get("from", ""), "date": headers.get("date", ""), "snippet": msg.get("snippet", "")})
        subject = ""
        if messages_data:
            first_headers = {h["name"].lower(): h["value"] for h in thread["messages"][0].get("payload", {}).get("headers", [])}
            subject = first_headers.get("subject", "")
        return {"thread_id": thread_id, "subject": subject, "message_count": len(messages_data), "messages": messages_data}

    @retry(
        retry=retry_if_exception_type(Exception),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    def send_email(self, to: str, subject: str, body: str) -> dict[str, Any]:
        err = self._ensure_service()
        if err:
            return err
        self._logger.info("Sending email to %s: %s", to, subject)
        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        sent = self._service.users().messages().send(userId="me", body={"raw": raw}).execute()
        return {"id": sent.get("id"), "thread_id": sent.get("threadId")}

    @retry(
        retry=retry_if_exception_type(Exception),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    def extract_action_items(self, thread_id: str) -> dict[str, Any]:
        err = self._ensure_service()
        if err:
            return err
        self._logger.info("Extracting action items from thread %s", thread_id)
        summary = self.summarize_thread(thread_id)
        if "error" in summary:
            return summary
        parts = [f"From: {m.get('from', '')}\nDate: {m.get('date', '')}\n\n{m.get('snippet', '')}" for m in summary.get("messages", [])]
        return {"thread_id": thread_id, "raw_text": "\n\n---\n\n".join(parts)}
