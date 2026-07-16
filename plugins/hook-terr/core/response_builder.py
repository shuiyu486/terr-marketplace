from typing import Dict, List, Optional

from core.models import Rule


def build_response(event_name: str, rule: Rule, message: str, diagnostics: Optional[List[str]] = None, suppress_message: bool = False) -> Dict:
    if suppress_message:
        return {}

    final_message = append_diagnostic_text(message, diagnostics or [])

    if rule.decision == "allow":
        return {"systemMessage": final_message} if final_message else {}

    if rule.decision == "block":
        if event_name in ("Stop", "SubagentStop"):
            return {
                "decision": "block",
                "reason": final_message,
                "systemMessage": final_message,
            }
        if event_name == "PreToolUse":
            return {
                "hookSpecificOutput": {
                    "hookEventName": event_name,
                    "permissionDecision": "deny",
                    "permissionDecisionReason": final_message,
                },
                "systemMessage": final_message,
            }
        if event_name in ("PostToolUse", "UserPromptSubmit"):
            return {
                "decision": "block",
                "reason": final_message,
                "systemMessage": final_message,
            }

    return {"systemMessage": final_message} if final_message else {}


def append_diagnostic_text(message: str, diagnostics: List[str]) -> str:
    if not diagnostics:
        return message
    visible = diagnostics[:3]
    suffix = "" if len(diagnostics) <= 3 else f"；另有 {len(diagnostics) - 3} 条诊断"
    diagnostic_text = "hook-terr 诊断：" + "；".join(visible) + suffix
    return f"{message}\n\n{diagnostic_text}" if message else diagnostic_text


def diagnostic_response(diagnostics):
    if not diagnostics:
        return {}
    return {"systemMessage": append_diagnostic_text("", diagnostics)}
