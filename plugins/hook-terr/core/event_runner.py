from typing import Any, Dict

from core.action_executor import execute, execute_assistance_notification, should_suppress_response
from core.config_loader import load_configuration, warn
from core.context_builder import build_context
from core.documentation_reminder import handle_documentation_reminder
from core.notification_policy import is_assistance_request
from core.response_builder import build_response, diagnostic_response
from core.rule_matcher import find_match


def run(event_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    context = build_context(event_name, input_data)
    settings, rules, diagnostics = load_configuration(context.cwd)

    for diagnostic in diagnostics:
        warn(f"hook-terr: {diagnostic}")

    if not settings.get("enabled", True):
        return {}

    assistance_request = is_assistance_request(context) and not context.is_subagent
    event_settings = settings.get("events", {}).get(event_name, {})
    event_enabled = not (isinstance(event_settings, dict) and not event_settings.get("enabled", True))
    if not event_enabled and not assistance_request:
        return {}

    feature_response, feature_diagnostics = handle_documentation_reminder(event_name, context, settings)
    for diagnostic in feature_diagnostics:
        warn(f"hook-terr documentation reminder: {diagnostic}")
    if feature_response:
        return feature_response

    rule = find_match(event_name, context, rules) if event_enabled else None
    if not rule:
        if assistance_request:
            notify_assistance(context, settings)
        return diagnostic_response(diagnostics)

    message, notification_results, execution_diagnostics = execute(rule, context, settings)
    failures = [f"{result.channel}: {result.error}" for result in notification_results if not result.success]
    for failure in failures:
        warn(f"hook-terr notifier failed: {failure}")
    for diagnostic in execution_diagnostics:
        warn(f"hook-terr notifier diagnostic: {diagnostic}")

    if assistance_request and rule.decision != "block" and not notification_results:
        notify_assistance(context, settings)

    response_diagnostics = diagnostics + execution_diagnostics + failures
    suppress_response = should_suppress_response(rule, context, settings)
    response = build_response(event_name, rule, message, response_diagnostics, suppress_response)
    if response:
        return response
    return diagnostic_response(response_diagnostics)


def notify_assistance(context, settings) -> None:
    notification_results, diagnostics = execute_assistance_notification(context, settings)
    for result in notification_results:
        if not result.success:
            warn(f"hook-terr assistance notifier failed: {result.channel}: {result.error}")
    for diagnostic in diagnostics:
        warn(f"hook-terr assistance notifier diagnostic: {diagnostic}")
