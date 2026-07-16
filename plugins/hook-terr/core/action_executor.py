from typing import Any, Dict, List, Tuple

from core.models import HookContext, NotificationResult, Rule
from core.notification_policy import can_send_external_notification, is_pure_stop_notification, notification_channel_event
from notifiers.registry import send_notification


def execute(rule: Rule, context: HookContext, settings: Dict[str, Any]) -> Tuple[str, List[NotificationResult], List[str]]:
    title, notification_text, response_text = render_message(rule, context)
    results: List[NotificationResult] = []
    diagnostics: List[str] = []

    notify = rule.notify if isinstance(rule.notify, dict) else {}
    if notify.get("enabled", False) and can_send_external_notification(rule, context):
        channels = resolve_channels(rule, context, settings)
        explicit_channels = "channels" in notify
        if not channels and not explicit_channels:
            diagnostics.append(f"{context.hook_event_name}: notify.enabled=true 但没有可执行通知通道")
        for channel in channels:
            channel_config = settings.get("notifications", {}).get(channel, {})
            if not channel_config.get("enabled", False):
                diagnostics.append(f"{channel}: 通道已配置但 notifications.{channel}.enabled=false")
                continue
            results.append(
                send_notification(
                    channel,
                    configured_channel_title(rule, title, channel_config),
                    notification_text,
                    context,
                    channel_config,
                )
            )

    return response_text, results, diagnostics


def execute_assistance_notification(context: HookContext, settings: Dict[str, Any]) -> Tuple[List[NotificationResult], List[str]]:
    results: List[NotificationResult] = []
    diagnostics: List[str] = []
    channels = stop_channels(settings)
    if not channels:
        return results, diagnostics
    for channel in channels:
        channel_config = settings.get("notifications", {}).get(channel, {})
        if not channel_config.get("enabled", False):
            diagnostics.append(f"{channel}: 通道已配置但 notifications.{channel}.enabled=false")
            continue
        results.append(send_notification(channel, "Claude Code 需要你协助", "Claude Code 正在等待你的输入或选择。", context, channel_config))
    return results, diagnostics


def should_suppress_response(rule: Rule, context: HookContext, settings: Dict[str, Any]) -> bool:
    notify = rule.notify if isinstance(rule.notify, dict) else {}
    if notify.get("channels") == []:
        return False
    return is_pure_stop_notification(rule, context.hook_event_name) and can_send_external_notification(rule, context) and bool(resolve_channels(rule, context, settings))


def resolve_channels(rule: Rule, context: HookContext, settings: Dict[str, Any]) -> List[str]:
    notify = rule.notify if isinstance(rule.notify, dict) else {}
    if "channels" in notify:
        channels = notify.get("channels")
        return unique_channels(channels) if isinstance(channels, list) else []
    event_config = settings.get("events", {}).get(notification_channel_event(context), {})
    channels = event_config.get("notifications", []) if isinstance(event_config, dict) else []
    return unique_channels(channels) if isinstance(channels, list) else []


def stop_channels(settings: Dict[str, Any]) -> List[str]:
    event_config = settings.get("events", {}).get("Stop", {})
    channels = event_config.get("notifications", []) if isinstance(event_config, dict) else []
    return unique_channels(channels) if isinstance(channels, list) else []


def unique_channels(channels: List[str]) -> List[str]:
    return list(dict.fromkeys(channels))


def configured_channel_title(rule: Rule, title: str, channel_config: Dict[str, Any]) -> str:
    message = rule.message if isinstance(rule.message, dict) else {}
    notify = rule.notify if isinstance(rule.notify, dict) else {}
    if notify.get("title") or message.get("title"):
        return title
    return str(channel_config.get("title") or title)


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
