import os
from typing import Any, Dict

from core.models import HookContext


def build_context(event_name: str, input_data: Dict[str, Any]) -> HookContext:
    tool_input = input_data.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        tool_input = {}

    return HookContext(
        hook_event_name=event_name,
        tool_name=input_data.get("tool_name", ""),
        tool_input=tool_input,
        reason=input_data.get("reason", ""),
        transcript_path=input_data.get("transcript_path", ""),
        user_prompt=input_data.get("user_prompt", ""),
        cwd=input_data.get("cwd") or os.getcwd(),
        raw_input=input_data,
    )


def get_field(context: HookContext, field: str) -> str:
    if field == "event":
        return context.hook_event_name
    if field == "tool_name":
        return context.tool_name
    if field == "reason":
        return context.reason
    if field == "transcript_path":
        return context.transcript_path
    if field == "user_prompt":
        return context.user_prompt
    if field == "cwd":
        return context.cwd
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
