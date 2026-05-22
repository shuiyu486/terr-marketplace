from typing import Any, Dict

from core.action_executor import execute
from core.config_loader import load_configuration, warn
from core.context_builder import build_context
from core.response_builder import build_response, diagnostic_response
from core.rule_matcher import find_match


def run(event_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    context = build_context(event_name, input_data)
    settings, rules, diagnostics = load_configuration(context.cwd)

    for diagnostic in diagnostics:
        warn(f"hook-terr: {diagnostic}")

    if not settings.get("enabled", True):
        return {}

    event_settings = settings.get("events", {}).get(event_name, {})
    if isinstance(event_settings, dict) and not event_settings.get("enabled", True):
        return {}

    rule = find_match(event_name, context, rules)
    if not rule:
        return diagnostic_response(diagnostics)

    message, notification_results = execute(rule, context, settings)
    failures = [f"{result.channel}: {result.error}" for result in notification_results if not result.success]
    if failures:
        for failure in failures:
            warn(f"hook-terr notifier failed: {failure}")

    response = build_response(event_name, rule, message)
    if response:
        return response
    return diagnostic_response(diagnostics + failures)
