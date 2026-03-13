"""Load and validate YAML workflow definitions."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel, Field

logger = logging.getLogger("claw-agent.workflows")


class WorkflowAction(BaseModel):
    tool: str
    args: Dict[str, Any] = Field(default_factory=dict)
    description: str = ""
    on_failure: str = "stop"


class WorkflowDefinition(BaseModel):
    name: str
    trigger: str
    description: str = ""
    actions: List[WorkflowAction]
    enabled: bool = True


def load_workflow(path: Path) -> WorkflowDefinition:
    with open(path) as f:
        raw = yaml.safe_load(f)
    actions = []
    for step in raw.get("actions", []):
        actions.append(
            WorkflowAction(
                tool=step["tool"],
                args=step.get("args", {}),
                description=step.get("description", ""),
                on_failure=step.get("on_failure", "stop"),
            )
        )
    return WorkflowDefinition(
        name=raw.get("name", path.stem),
        trigger=raw["trigger"],
        description=raw.get("description", ""),
        actions=actions,
        enabled=raw.get("enabled", True),
    )


def load_all_workflows(directory: str = "workflows") -> Dict[str, WorkflowDefinition]:
    workflows: Dict[str, WorkflowDefinition] = {}
    workflow_dir = Path(directory)
    if not workflow_dir.exists():
        logger.warning("Workflow directory %s does not exist", directory)
        return workflows
    for yaml_file in sorted(workflow_dir.glob("*.yaml")):
        try:
            wf = load_workflow(yaml_file)
            if wf.enabled:
                workflows[wf.trigger] = wf
                logger.info("Loaded workflow: %s (trigger: %s)", wf.name, wf.trigger)
        except Exception:
            logger.exception("Failed to load workflow from %s", yaml_file)
    logger.info("Loaded %d workflow(s) from %s", len(workflows), directory)
    return workflows
