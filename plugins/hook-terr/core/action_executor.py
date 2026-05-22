from typing import Any, Dict, List, Tuple

from core.models import HookContext, NotificationResult, Rule
from notifiers.registry import send_notification


def execute(rule: Rule, context: HookContext, settings: Dict[str, Any]) -> Tuple[str, List[NotificationResult]]:
    title, text = render_message(rule, context)
    results: List[NotificationResult] = []

    notify = rule.notify if isinstance(rule.notify, dict) else {}
    if notify.get("enabled", False):
        event_config = settings.get("events", {}).get(context.hook_event_name, {})
        channels = notify.get("channels") or event_config.get("notifications", [])
        for channel in channels:
            channel_config = settings.get("notifications", {}).get(channel, {})
            if not channel_config.get("enabled", False):
                continue
            results.append(send_notification(channel, title, text, context, channel_config))

    return text, results


def render_message(rule: Rule, context: HookContext) -> Tuple[str, str]:
    message = rule.message if isinstance(rule.message, dict) else {}
    notify = rule.notify if isinstance(rule.notify, dict) else {}
    title = str(notify.get("title") or message.get("title") or "hook-terr")
    text = str(notify.get("text") or message.get("text") or "")
    values = {
        "event": context.hook_event_name,
        "title": title,
        "message": text,
        "cwd": context.cwd,
        "reason": context.reason,
    }
    for key, value in values.items():
        title = title.replace("{{" + key + "}}", str(value))
        text = text.replace("{{" + key + "}}", str(value))
    return title, text
