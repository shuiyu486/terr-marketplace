import re
from typing import Any, Dict, List

VALID_EVENTS = {"Stop", "SubagentStop", "PreToolUse", "PostToolUse", "UserPromptSubmit"}
VALID_DECISIONS = {"allow", "warn", "block"}
VALID_OPERATORS = {"equals", "contains", "regex", "not_regex", "in"}
VALID_CHANNELS = {"windows_toast", "sound", "popup", "custom_command"}
LEGACY_CUSTOM_COMMAND_TOKENS = ("{{event}}", "{{title}}", "{{message}}", "{{cwd}}", "{{timestamp}}")


def validate_settings(settings: Any) -> List[str]:
    errors = []
    if not isinstance(settings, dict):
        return ["settings must be a JSON object"]

    enabled = settings.get("enabled")
    if enabled is not None and not isinstance(enabled, bool):
        errors.append("settings.enabled must be a boolean")

    notifications = settings.get("notifications", {})
    if notifications is not None and not isinstance(notifications, dict):
        errors.append("settings.notifications must be an object")
    elif isinstance(notifications, dict):
        for channel, config in notifications.items():
            if channel not in VALID_CHANNELS:
                errors.append(f"settings.notifications has unknown channel '{channel}'")
                continue
            if not isinstance(config, dict):
                errors.append(f"settings.notifications.{channel} must be an object")
                continue
            channel_enabled = config.get("enabled")
            if channel_enabled is not None and not isinstance(channel_enabled, bool):
                errors.append(f"settings.notifications.{channel}.enabled must be a boolean")
            if channel == "sound":
                wav_path = config.get("wavPath")
                if wav_path is not None and not isinstance(wav_path, str):
                    errors.append("settings.notifications.sound.wavPath must be a string")
            if channel == "popup":
                icon = config.get("icon")
                if icon is not None and icon not in ("info", "warning", "error"):
                    errors.append("settings.notifications.popup.icon must be one of info, warning, error")
            if channel == "custom_command":
                command = config.get("command")
                if command is not None and not isinstance(command, str):
                    errors.append("settings.notifications.custom_command.command must be a string")
                legacy_tokens = legacy_custom_command_tokens(command)
                if legacy_tokens:
                    errors.append(
                        "settings.notifications.custom_command.command uses removed legacy template token(s): "
                        + ", ".join(legacy_tokens)
                        + "; use HOOK_TERR_MESSAGE, HOOK_TERR_TITLE, HOOK_TERR_EVENT, HOOK_TERR_CWD, and HOOK_TERR_TIMESTAMP environment variables instead"
                    )
                timeout_ms = config.get("timeoutMs")
                if timeout_ms is not None and (isinstance(timeout_ms, bool) or not isinstance(timeout_ms, (int, float))):
                    errors.append("settings.notifications.custom_command.timeoutMs must be a number")
                detached = config.get("detached")
                if detached is not None and not isinstance(detached, bool):
                    errors.append("settings.notifications.custom_command.detached must be a boolean")

    events = settings.get("events", {})
    if events is not None and not isinstance(events, dict):
        errors.append("settings.events must be an object")
    elif isinstance(events, dict):
        for event_name, config in events.items():
            if event_name not in VALID_EVENTS:
                errors.append(f"settings.events has unknown event '{event_name}'")
                continue
            if not isinstance(config, dict):
                errors.append(f"settings.events.{event_name} must be an object")
                continue
            event_enabled = config.get("enabled")
            if event_enabled is not None and not isinstance(event_enabled, bool):
                errors.append(f"settings.events.{event_name}.enabled must be a boolean")
            channels = config.get("notifications")
            if channels is not None:
                if not isinstance(channels, list):
                    errors.append(f"settings.events.{event_name}.notifications must be an array")
                else:
                    for channel in channels:
                        if not isinstance(channel, str):
                            errors.append(f"settings.events.{event_name}.notifications must contain only strings")
                        elif channel not in VALID_CHANNELS:
                            errors.append(f"settings.events.{event_name}.notifications has unknown channel '{channel}'")

    features = settings.get("features", {})
    if features is not None and not isinstance(features, dict):
        errors.append("settings.features must be an object")
    elif isinstance(features, dict):
        reminder = features.get("documentationReminder")
        if reminder is not None:
            if not isinstance(reminder, dict):
                errors.append("settings.features.documentationReminder must be an object")
            else:
                reminder_enabled = reminder.get("enabled")
                if reminder_enabled is not None and not isinstance(reminder_enabled, bool):
                    errors.append("settings.features.documentationReminder.enabled must be a boolean")
                tools = reminder.get("tools")
                if tools is not None:
                    if not isinstance(tools, list):
                        errors.append("settings.features.documentationReminder.tools must be an array")
                    else:
                        for tool in tools:
                            if not isinstance(tool, str):
                                errors.append("settings.features.documentationReminder.tools must contain only strings")
                                break
                ttl = reminder.get("stateTtlHours")
                if ttl is not None:
                    if not isinstance(ttl, int) or ttl <= 0:
                        errors.append("settings.features.documentationReminder.stateTtlHours must be a positive integer")
                message = reminder.get("message")
                if message is not None and not isinstance(message, str):
                    errors.append("settings.features.documentationReminder.message must be a string")

    return errors


def legacy_custom_command_tokens(command: Any) -> List[str]:
    if not isinstance(command, str):
        return []
    return [token for token in LEGACY_CUSTOM_COMMAND_TOKENS if token in command]


def validate_rule(data: Any, source: str) -> List[str]:
    errors = []
    if not isinstance(data, dict):
        return [f"{source}: rule must be a JSON object"]

    for key in ("id", "event", "enabled", "decision"):
        if key not in data:
            errors.append(f"{source}: missing required field '{key}'")

    for key in ("id", "event", "decision"):
        if key in data and not isinstance(data.get(key), str):
            errors.append(f"{source}: {key} must be a string")

    enabled = data.get("enabled")
    if "enabled" in data and not isinstance(enabled, bool):
        errors.append(f"{source}: enabled must be a boolean")

    event = data.get("event")
    if isinstance(event, str) and event not in VALID_EVENTS:
        errors.append(f"{source}: invalid event '{event}'")

    decision = data.get("decision")
    if isinstance(decision, str) and decision not in VALID_DECISIONS:
        errors.append(f"{source}: invalid decision '{decision}'")

    priority = data.get("priority")
    if priority is not None and (isinstance(priority, bool) or not isinstance(priority, int)):
        errors.append(f"{source}: priority must be an integer")

    match = data.get("match")
    if match is not None:
        if not isinstance(match, str):
            errors.append(f"{source}: match must be a string")
        elif match not in ("all", "any"):
            errors.append(f"{source}: match must be one of all, any")

    message = data.get("message", {})
    if message is not None and not isinstance(message, dict):
        errors.append(f"{source}: message must be an object")

    notify = data.get("notify", {})
    if notify is not None and not isinstance(notify, dict):
        errors.append(f"{source}: notify must be an object")
    if isinstance(notify, dict):
        notify_enabled = notify.get("enabled")
        if notify_enabled is not None and not isinstance(notify_enabled, bool):
            errors.append(f"{source}: notify.enabled must be a boolean")
        channels = notify.get("channels", [])
        if channels is not None and not isinstance(channels, list):
            errors.append(f"{source}: notify.channels must be an array")
        for channel in channels if isinstance(channels, list) else []:
            if not isinstance(channel, str):
                errors.append(f"{source}: notify.channels must contain only strings")
            elif channel not in VALID_CHANNELS:
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
        if not isinstance(op, str):
            errors.append(f"{source}: condition {index} operator must be a string")
        elif op not in VALID_OPERATORS:
            errors.append(f"{source}: condition {index} has invalid operator '{op}'")
        if op in ("regex", "not_regex"):
            try:
                re.compile(str(condition.get("value", "")))
            except re.error as exc:
                errors.append(f"{source}: condition {index} has invalid regex: {exc}")

    return errors


def is_valid_rule(data: Dict[str, Any], source: str) -> bool:
    return not validate_rule(data, source)
