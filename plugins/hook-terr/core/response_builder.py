from typing import Dict

from core.models import Rule


def build_response(event_name: str, rule: Rule, message: str) -> Dict:
    if rule.decision == "allow":
        return {}

    if rule.decision == "block":
        if event_name == "Stop":
            return {
                "decision": "block",
                "reason": message,
                "systemMessage": message,
            }
        if event_name in ("PreToolUse", "PostToolUse"):
            return {
                "hookSpecificOutput": {
                    "hookEventName": event_name,
                    "permissionDecision": "deny",
                },
                "systemMessage": message,
            }

    return {"systemMessage": message} if message else {}


def diagnostic_response(diagnostics):
    if not diagnostics:
        return {}
    visible = diagnostics[:3]
    suffix = "" if len(diagnostics) <= 3 else f"；另有 {len(diagnostics) - 3} 条诊断"
    return {"systemMessage": "hook-terr 配置诊断：" + "；".join(visible) + suffix}
