from core.models import HookContext, Rule


ASSISTANCE_TOOL_NAMES = {"AskUserQuestion"}


def is_assistance_request(context: HookContext) -> bool:
    return context.hook_event_name == "PreToolUse" and context.tool_name in ASSISTANCE_TOOL_NAMES


def can_send_external_notification(rule: Rule, context: HookContext) -> bool:
    if rule.decision == "block":
        return False
    if context.is_subagent:
        return False
    if context.hook_event_name == "Stop":
        return True
    return is_assistance_request(context)


def notification_channel_event(context: HookContext) -> str:
    if is_assistance_request(context):
        return "Stop"
    return context.hook_event_name


def is_pure_stop_notification(rule: Rule, event_name: str) -> bool:
    notify = rule.notify if isinstance(rule.notify, dict) else {}
    return event_name == "Stop" and rule.decision in ("allow", "warn") and notify.get("enabled", False) is True
