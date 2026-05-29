from typing import Any, Dict, List, Tuple

from core.models import HookContext, NotificationResult, Rule
from notifiers.registry import send_notification


def execute(rule: Rule, context: HookContext, settings: Dict[str, Any]) -> Tuple[str, List[NotificationResult], List[str]]:
    title, notification_text, response_text = render_message(rule, context)
    results: List[NotificationResult] = []
    diagnostics: List[str] = []

    notify = rule.notify if isinstance(rule.notify, dict) else {}
    if notify.get("enabled", False):
        channels = resolve_channels(rule, context, settings)
        explicit_channels = "channels" in notify
        if not channels and not explicit_channels:
            diagnostics.append(f"{context.hook_event_name}: notify.enabled=true 但没有可执行通知通道")
        for channel in channels:
            channel_config = settings.get("notifications", {}).get(channel, {})
            if not channel_config.get("enabled", False):
                diagnostics.append(f"{channel}: 通道已配置但 notifications.{channel}.enabled=false")
                continue
            results.append(send_notification(channel, title, notification_text, context, channel_config))

    return response_text, results, diagnostics


def resolve_channels(rule: Rule, context: HookContext, settings: Dict[str, Any]) -> List[str]:
    notify = rule.notify if isinstance(rule.notify, dict) else {}
    if "channels" in notify:
        channels = notify.get("channels")
        return channels if isinstance(channels, list) else []
    event_config = settings.get("events", {}).get(context.hook_event_name, {})
    channels = event_config.get("notifications", []) if isinstance(event_config, dict) else []
    return channels if isinstance(channels, list) else []


def render_message(rule: Rule, context: HookContext) -> Tuple[str, str, str]:
    message = rule.message if isinstance(rule.message, dict) else {}
    notify = rule.notify if isinstance(rule.notify, dict) else {}
    title = str(notify.get("title") or message.get("title") or "hook-terr")
    response_text = str(message.get("text") or "")
    notification_text = str(notify.get("text") or response_text)
    values = {
        "event": context.hook_event_name,
        "title": title,
        "message": notification_text,
        "cwd": context.cwd,
        "reason": context.reason,
    }
    for key, value in values.items():
        title = title.replace("{{" + key + "}}", str(value))
        response_text = response_text.replace("{{" + key + "}}", str(value))
        notification_text = notification_text.replace("{{" + key + "}}", str(value))
    return title, notification_text, response_text
