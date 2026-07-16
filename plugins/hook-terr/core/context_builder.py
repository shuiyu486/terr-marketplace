import json
import os
from typing import Any, Dict, Optional, Tuple

from core.models import HookContext


def build_context(event_name: str, input_data: Dict[str, Any]) -> HookContext:
    tool_input = input_data.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        tool_input = {}

    transcript_path = optional_string(input_data.get("transcript_path"))
    is_subagent, agent_type = derive_agent_fields(event_name, input_data, transcript_path)

    return HookContext(
        hook_event_name=event_name,
        tool_name=input_data.get("tool_name", ""),
        tool_input=tool_input,
        reason=input_data.get("reason", ""),
        transcript_path=transcript_path,
        is_subagent=is_subagent,
        agent_type=agent_type,
        user_prompt=input_data.get("user_prompt", ""),
        cwd=input_data.get("cwd") or os.getcwd(),
        session_id=optional_string(input_data.get("session_id")),
        error=str(input_data.get("error", "")),
        error_details=stringify(input_data.get("error_details", "")),
        last_assistant_message=str(input_data.get("last_assistant_message", "")),
        stop_hook_active=coerce_bool(input_data.get("stop_hook_active")) is True,
        raw_input=input_data,
    )


def derive_agent_fields(event_name: str, input_data: Dict[str, Any], transcript_path: str) -> Tuple[bool, str]:
    if event_name == "SubagentStop":
        return True, "subagent"

    explicit_is_subagent = coerce_bool(input_data.get("is_subagent"))
    explicit_agent_type = normalize_agent_type(input_data.get("agent_type"))
    is_sidechain = coerce_bool(input_data.get("isSidechain"))
    agent_id = optional_string(input_data.get("agent_id") or input_data.get("agentId"))

    if explicit_is_subagent is True or explicit_agent_type == "subagent" or is_sidechain is True:
        return True, "subagent"
    if agent_id or path_has_segment(transcript_path, "subagents"):
        return True, "subagent"
    return False, "main"


def coerce_bool(value: Any) -> Optional[bool]:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in ("true", "1", "yes", "y", "on"):
            return True
        if normalized in ("false", "0", "no", "n", "off", ""):
            return False
    return None


def normalize_agent_type(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    normalized = value.strip().lower()
    return normalized if normalized in ("main", "subagent") else ""


def path_has_segment(path: str, segment: str) -> bool:
    if not path:
        return False
    parts = [part for part in path.replace("\\", "/").split("/") if part]
    return segment in parts


def optional_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def stringify(value: Any) -> str:
    if isinstance(value, str):
        return value
    if value is None:
        return ""
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    except (TypeError, ValueError):
        return str(value)


def get_field(context: HookContext, field: str) -> str:
    if field == "event":
        return context.hook_event_name
    if field == "tool_name":
        return context.tool_name
    if field == "reason":
        return context.reason
    if field == "transcript_path":
        return context.transcript_path
    if field == "is_subagent":
        return "true" if context.is_subagent else "false"
    if field == "agent_type":
        return context.agent_type
    if field == "user_prompt":
        return context.user_prompt
    if field == "cwd":
        return context.cwd
    if field == "session_id":
        return context.session_id
    if field == "error":
        return context.error
    if field == "error_details":
        return context.error_details
    if field == "last_assistant_message":
        return context.last_assistant_message
    if field == "stop_hook_active":
        return "true" if context.stop_hook_active else "false"
    if field in context.tool_input:
        value = context.tool_input[field]
        return value if isinstance(value, str) else str(value)
    if context.tool_name == "Bash" and field == "command":
        return str(context.tool_input.get("command", ""))
    if context.tool_name in ("Write", "Edit"):
        if field in ("content", "new_text", "new_string"):
            return str(context.tool_input.get("content") or context.tool_input.get("new_string", ""))
        if field in ("old_text", "old_string"):
            return str(context.tool_input.get("old_string", ""))
        if field == "file_path":
            return str(context.tool_input.get("file_path", ""))
    if context.tool_name == "MultiEdit":
        if field == "file_path":
            return str(context.tool_input.get("file_path", ""))
        if field in ("content", "new_text", "new_string"):
            edits = context.tool_input.get("edits", [])
            if isinstance(edits, list):
                return " ".join(str(edit.get("new_string", "")) for edit in edits if isinstance(edit, dict))
    return ""
