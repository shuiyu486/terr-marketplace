import json
import os
import sys
from typing import Any, Dict, List

PLUGIN_ROOT = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PLUGIN_ROOT not in sys.path:
    sys.path.insert(0, PLUGIN_ROOT)

from core.api_error_recovery import is_recovery_enabled, normalize_path, path_is_or_under, recovery_config, recovery_mode, scope_enabled, string_list
from core.config_loader import load_configuration, plugin_root, rule_paths, settings_paths
from core.context_builder import build_context
from core.models import Rule
from core.rule_matcher import find_match
from core.utf8 import configure_stdio


PLUGIN_METADATA_PATH = os.path.join(PLUGIN_ROOT, ".claude-plugin", "plugin.json")


def build_status(cwd: str) -> Dict[str, Any]:
    settings, rules, diagnostics = load_configuration(cwd)
    context = build_context("Stop", {"cwd": cwd, "reason": "status"})
    stop_rule = find_match("Stop", context, rules)
    stop_channels = resolve_stop_channels(settings, stop_rule)
    root = plugin_root()
    return {
        "cwd": cwd,
        "pluginRoot": root,
        "pluginVersion": plugin_version(root),
        "settingsFiles": existing_paths(settings_paths(root, cwd)),
        "ruleFiles": existing_paths(rule_paths(root, cwd)),
        "enabled": settings.get("enabled", True),
        "features": settings.get("features", {}),
        "apiErrorRecoveryStatus": api_error_recovery_status(settings, cwd),
        "events": settings.get("events", {}),
        "notifications": settings.get("notifications", {}),
        "stopRule": rule_to_dict(stop_rule),
        "stopChannels": stop_channels,
        "diagnostics": diagnostics,
    }


def api_error_recovery_status(settings: Dict[str, Any], cwd: str) -> Dict[str, Any]:
    config = recovery_config(settings)
    context = build_context("StopFailure", {"cwd": cwd, "session_id": "status"})
    cwd_scope = config.get("scopes", {}).get("cwd", {}) if isinstance(config.get("scopes"), dict) else {}
    return {
        "enabled": bool(config.get("enabled", False)),
        "effectiveForCwd": is_recovery_enabled(config, context),
        "recoveryMode": recovery_mode(config),
        "recoveryModeLabel": recovery_mode_label(recovery_mode(config)),
        "cwdScope": cwd_scope_status(cwd_scope, cwd),
    }


def recovery_mode_label(mode: str) -> str:
    labels = {
        "continue_only": "只 continue",
        "continue_then_fallback": "二次失败再切",
        "fallback_then_continue": "立即切模型",
    }
    return labels.get(mode, mode)


def cwd_scope_status(scope: Any, cwd: str) -> Dict[str, Any]:
    if not isinstance(scope, dict):
        return {"effective": True, "matchedBy": "default", "matchedValue": None, "default": True}
    default = scope.get("default") if isinstance(scope.get("default"), bool) else True
    matched_by = "default"
    matched_value = None
    value = normalize_path(cwd)
    if value and value in [normalize_path(path) for path in string_list(scope.get("disabled"))]:
        matched_by = "disabled"
        matched_value = cwd
    elif value and value in [normalize_path(path) for path in string_list(scope.get("enabled"))]:
        matched_by = "enabled"
        matched_value = cwd
    else:
        for path in string_list(scope.get("disabledPrefixes")):
            if value and path_is_or_under(value, normalize_path(path)):
                matched_by = "disabledPrefixes"
                matched_value = path
                break
        if matched_by == "default":
            for path in string_list(scope.get("enabledPrefixes")):
                if value and path_is_or_under(value, normalize_path(path)):
                    matched_by = "enabledPrefixes"
                    matched_value = path
                    break
    return {
        "effective": scope_enabled({"scopes": {"cwd": scope}}, "cwd", cwd, default=True),
        "matchedBy": matched_by,
        "matchedValue": matched_value,
        "default": default,
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


def plugin_version(root: str) -> str:
    path = os.path.join(root, ".claude-plugin", "plugin.json") if root else PLUGIN_METADATA_PATH
    try:
        with open(path, "r", encoding="utf-8-sig") as handle:
            metadata = json.load(handle)
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return ""
    version = metadata.get("version") if isinstance(metadata, dict) else ""
    return str(version).strip() if version is not None else ""


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
