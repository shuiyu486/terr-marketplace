import json
import os
import sys
from typing import Any, Dict, List

PLUGIN_ROOT = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PLUGIN_ROOT not in sys.path:
    sys.path.insert(0, PLUGIN_ROOT)

from core.config_loader import load_configuration, plugin_root, rule_paths, settings_paths
from core.context_builder import build_context
from core.models import Rule
from core.rule_matcher import find_match
from core.utf8 import configure_stdio


def build_status(cwd: str) -> Dict[str, Any]:
    settings, rules, diagnostics = load_configuration(cwd)
    context = build_context("Stop", {"cwd": cwd, "reason": "status"})
    stop_rule = find_match("Stop", context, rules)
    stop_channels = resolve_stop_channels(settings, stop_rule)
    root = plugin_root()
    return {
        "cwd": cwd,
        "pluginRoot": root,
        "settingsFiles": existing_paths(settings_paths(root, cwd)),
        "ruleFiles": existing_paths(rule_paths(root, cwd)),
        "enabled": settings.get("enabled", True),
        "features": settings.get("features", {}),
        "events": settings.get("events", {}),
        "notifications": settings.get("notifications", {}),
        "stopRule": rule_to_dict(stop_rule),
        "stopChannels": stop_channels,
        "diagnostics": diagnostics,
    }


def resolve_stop_channels(settings: Dict[str, Any], rule: Rule) -> List[str]:
    notify = rule.notify if rule and isinstance(rule.notify, dict) else {}
    if "channels" in notify:
        channels = notify.get("channels")
        return channels if isinstance(channels, list) else []
    stop_event = settings.get("events", {}).get("Stop", {})
    channels = stop_event.get("notifications", []) if isinstance(stop_event, dict) else []
    return channels if isinstance(channels, list) else []


def existing_paths(paths: List[str]) -> List[str]:
    return [path for path in paths if os.path.exists(path)]


def rule_to_dict(rule: Rule):
    if not rule:
        return None
    return {
        "id": rule.id,
        "event": rule.event,
        "enabled": rule.enabled,
        "decision": rule.decision,
        "priority": rule.priority,
        "match": rule.match,
        "when": rule.when,
        "message": rule.message,
        "notify": rule.notify,
    }


def main():
    configure_stdio()
    cwd = os.environ.get("HOOK_TERR_CWD") or os.getcwd()
    print(json.dumps(build_status(cwd), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
