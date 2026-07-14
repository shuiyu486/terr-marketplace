from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class HookContext:
    hook_event_name: str
    tool_name: str = ""
    tool_input: Dict[str, Any] = field(default_factory=dict)
    reason: str = ""
    transcript_path: str = ""
    is_subagent: bool = False
    agent_type: str = "main"
    user_prompt: str = ""
    cwd: str = ""
    session_id: str = ""
    error: str = ""
    error_details: str = ""
    last_assistant_message: str = ""
    raw_input: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Rule:
    id: str
    event: str
    enabled: bool
    decision: str
    priority: int = 0
    match: str = "all"
    when: List[Dict[str, Any]] = field(default_factory=list)
    message: Dict[str, Any] = field(default_factory=dict)
    notify: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MatchResult:
    rule: Optional[Rule]
    diagnostics: List[str] = field(default_factory=list)


@dataclass
class NotificationResult:
    channel: str
    success: bool
    error: str = ""
