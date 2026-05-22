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
    field_value = get_field(context, str(condition.get("field", "")))
    op = condition.get("op")
    value = condition.get("value", "")

    if op == "equals":
        return field_value == str(value)
    if op == "contains":
        return str(value) in field_value
    if op == "regex":
        return bool(re.search(str(value), field_value, re.IGNORECASE))
    if op == "not_regex":
        return not re.search(str(value), field_value, re.IGNORECASE)
    if op == "in":
        return field_value in value if isinstance(value, list) else False
    return False
