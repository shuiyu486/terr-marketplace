import json
import re
from typing import Dict, Optional


Order = int
_TERMINAL_STATUSES = {"cancelled", "completed", "error", "failed", "killed", "stopped"}
_TASK_NOTIFICATION_PATTERN = re.compile(
    r"<task-notification>.*?<tool-use-id>([^<]+)</tool-use-id>.*?<status>([^<]+)</status>.*?</task-notification>",
    re.DOTALL,
)


def has_pending_background_tasks(transcript_path: str) -> bool:
    if not transcript_path:
        return False

    starts: Dict[str, Order] = {}
    terminals: Dict[str, Order] = {}
    task_to_tool: Dict[str, str] = {}
    stop_requests: Dict[str, str] = {}

    try:
        with open(transcript_path, "r", encoding="utf-8-sig") as handle:
            for line_number, raw_line in enumerate(handle, 1):
                relevant = any(
                    marker in raw_line
                    for marker in (
                        "<task-notification>",
                        "async_launched",
                        '"isAsync"',
                        "backgroundTaskId",
                        "resumedAgentId",
                        '"TaskStop"',
                    )
                )
                if not relevant and stop_requests:
                    relevant = any(tool_use_id in raw_line for tool_use_id in stop_requests)
                if not relevant:
                    continue

                try:
                    item = json.loads(raw_line)
                except (TypeError, ValueError):
                    continue

                collect_task_notification(item, line_number, terminals)
                collect_task_stop_request(item, stop_requests)
                collect_async_result(item, line_number, starts, task_to_tool)
                collect_task_stop_result(item, line_number, terminals, task_to_tool, stop_requests)
    except (OSError, UnicodeError):
        return False

    return any(tool_use_id not in terminals or order > terminals[tool_use_id] for tool_use_id, order in starts.items())


def collect_task_notification(item: dict, order: Order, terminals: Dict[str, Order]) -> None:
    notification = task_notification(item)
    if not notification:
        return
    for tool_use_id, status in _TASK_NOTIFICATION_PATTERN.findall(notification):
        if status.strip().lower() in _TERMINAL_STATUSES:
            record_latest(terminals, tool_use_id.strip(), order)


def collect_async_result(
    item: dict,
    order: Order,
    starts: Dict[str, Order],
    task_to_tool: Dict[str, str],
) -> None:
    if item.get("type") != "user":
        return
    result = item.get("toolUseResult")
    part = tool_result_part(item)
    if not isinstance(result, dict) or not part or part.get("is_error") is True:
        return

    tool_use_id = part.get("tool_use_id")
    if not isinstance(tool_use_id, str) or not tool_use_id:
        return

    resumed_agent_id = result.get("resumedAgentId")
    if isinstance(resumed_agent_id, str) and resumed_agent_id and result.get("success") is True:
        record_latest(starts, tool_use_id, order)
        task_to_tool[resumed_agent_id] = tool_use_id
        return

    background_task_id = result.get("backgroundTaskId")
    async_launched = (
        result.get("status") == "async_launched"
        or result.get("isAsync") is True
        or (isinstance(background_task_id, str) and bool(background_task_id))
    )
    if not async_launched:
        return

    record_latest(starts, tool_use_id, order)
    for key in ("agentId", "taskId", "backgroundTaskId"):
        task_id = result.get(key)
        if isinstance(task_id, str) and task_id:
            task_to_tool[task_id] = tool_use_id


def collect_task_stop_request(item: dict, stop_requests: Dict[str, str]) -> None:
    if item.get("type") != "assistant":
        return
    message = item.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    if not isinstance(content, list):
        return

    for part in content:
        if not isinstance(part, dict) or part.get("type") != "tool_use" or part.get("name") != "TaskStop":
            continue
        tool_input = part.get("input")
        task_id = tool_input.get("task_id") if isinstance(tool_input, dict) else None
        tool_use_id = part.get("id")
        if isinstance(task_id, str) and task_id and isinstance(tool_use_id, str) and tool_use_id:
            stop_requests[tool_use_id] = task_id


def collect_task_stop_result(
    item: dict,
    order: Order,
    terminals: Dict[str, Order],
    task_to_tool: Dict[str, str],
    stop_requests: Dict[str, str],
) -> None:
    if item.get("type") != "user":
        return
    part = tool_result_part(item)
    if not part or part.get("is_error") is True:
        return
    stop_tool_use_id = part.get("tool_use_id")
    if not isinstance(stop_tool_use_id, str):
        return
    task_id = stop_requests.get(stop_tool_use_id)
    if not task_id or not successful_task_stop(item, part, task_id):
        return
    original_tool_use_id = task_to_tool.get(task_id)
    if original_tool_use_id:
        record_latest(terminals, original_tool_use_id, order)


def successful_task_stop(item: dict, part: dict, task_id: str) -> bool:
    result = item.get("toolUseResult")
    if isinstance(result, dict) and result.get("task_id") == task_id:
        return True

    content = part.get("content")
    if not isinstance(content, str):
        return False
    try:
        parsed = json.loads(content)
    except (TypeError, ValueError):
        return False
    return isinstance(parsed, dict) and parsed.get("task_id") == task_id


def tool_result_part(item: dict) -> Optional[dict]:
    message = item.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    if not isinstance(content, list):
        return None
    for part in content:
        if isinstance(part, dict) and part.get("type") == "tool_result":
            return part
    return None


def task_notification(item: dict) -> str:
    if item.get("type") == "queue-operation":
        content = item.get("content")
        return content if isinstance(content, str) and "<task-notification>" in content else ""
    if item.get("type") == "attachment":
        attachment = item.get("attachment")
        if not isinstance(attachment, dict) or attachment.get("type") != "queued_command":
            return ""
        prompt = attachment.get("prompt")
        return prompt if isinstance(prompt, str) and "<task-notification>" in prompt else ""
    return ""


def record_latest(records: Dict[str, Order], key: str, order: Order) -> None:
    if key not in records or order > records[key]:
        records[key] = order
