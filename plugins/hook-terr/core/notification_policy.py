from core.background_tasks import has_pending_background_tasks
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
        return not has_pending_stop_work(context)
    return is_assistance_request(context)


def has_pending_stop_work(context: HookContext) -> bool:
    if context.background_tasks:
        return True
    if context.session_crons:
        return True
    if context.background_tasks is not None:
        return False
    return has_pending_background_tasks(context.transcript_path)


def notification_channel_event(context: HookContext) -> str:
    if is_assistance_request(context):
        return "Stop"
    return context.hook_event_name


def is_pure_stop_notification(rule: Rule, event_name: str) -> bool:
    notify = rule.notify if isinstance(rule.notify, dict) else {}
    return event_name == "Stop" and rule.decision in ("allow", "warn") and notify.get("enabled", False) is True
