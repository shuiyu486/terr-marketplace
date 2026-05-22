import re
from typing import Any, Dict, List

VALID_EVENTS = {"Stop", "PreToolUse", "PostToolUse", "UserPromptSubmit"}
VALID_DECISIONS = {"allow", "warn", "block"}
VALID_OPERATORS = {"equals", "contains", "regex", "not_regex", "in"}
VALID_CHANNELS = {"windows_toast", "beep", "popup", "custom_command"}


def validate_settings(settings: Any) -> List[str]:
    if not isinstance(settings, dict):
        return ["settings must be a JSON object"]
    return []


def validate_rule(data: Any, source: str) -> List[str]:
    errors = []
    if not isinstance(data, dict):
        return [f"{source}: rule must be a JSON object"]

    for key in ("id", "event", "enabled", "decision"):
        if key not in data:
            errors.append(f"{source}: missing required field '{key}'")

    event = data.get("event")
    if event and event not in VALID_EVENTS:
        errors.append(f"{source}: invalid event '{event}'")

    decision = data.get("decision")
    if decision and decision not in VALID_DECISIONS:
        errors.append(f"{source}: invalid decision '{decision}'")

    notify = data.get("notify", {})
    if isinstance(notify, dict):
        channels = notify.get("channels", [])
        if channels and not isinstance(channels, list):
            errors.append(f"{source}: notify.channels must be an array")
        for channel in channels if isinstance(channels, list) else []:
            if channel not in VALID_CHANNELS:
                errors.append(f"{source}: unknown notification channel '{channel}'")

    when = data.get("when", [])
    if not isinstance(when, list):
        errors.append(f"{source}: when must be an array")
        return errors

    for index, condition in enumerate(when):
        if not isinstance(condition, dict):
            errors.append(f"{source}: condition {index} must be an object")
            continue
        op = condition.get("op")
        if op not in VALID_OPERATORS:
            errors.append(f"{source}: condition {index} has invalid operator '{op}'")
        if op in ("regex", "not_regex"):
            try:
                re.compile(str(condition.get("value", "")))
            except re.error as exc:
                errors.append(f"{source}: condition {index} has invalid regex: {exc}")

    return errors


def is_valid_rule(data: Dict[str, Any], source: str) -> bool:
    return not validate_rule(data, source)
