import re
from typing import Any, List, Optional

from core.context_builder import get_field
from core.models import HookContext, Rule


def find_match(event_name: str, context: HookContext, rules: List[Rule]) -> Optional[Rule]:
    candidates = [rule for rule in rules if rule.enabled and rule.event == event_name]
    candidates.sort(key=lambda rule: rule.priority, reverse=True)
    for rule in candidates:
        if matches_rule(rule, context):
            return rule
    return None


def matches_rule(rule: Rule, context: HookContext) -> bool:
    if not rule.when:
        return True
    checks = [matches_condition(condition, context) for condition in rule.when]
    return any(checks) if rule.match == "any" else all(checks)


def matches_condition(condition: dict, context: HookContext) -> bool:
    field = condition.get("field")
    if not isinstance(field, str) or not field.strip():
        return False
    field_value = get_field(context, field)
    op = condition.get("op")
    value = condition.get("value", "")

    expected = condition_value(value)

    if op == "equals":
        return field_value == expected
    if op == "contains":
        return expected in field_value
    if op == "regex":
        return bool(re.search(expected, field_value, re.IGNORECASE))
    if op == "not_regex":
        return not re.search(expected, field_value, re.IGNORECASE)
    if op == "in":
        return field_value in [condition_value(item) for item in value] if isinstance(value, list) else False
    return False


def condition_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)
