import glob
import json
import os
import sys
from copy import deepcopy
from typing import Any, Dict, List, Tuple

from core.models import Rule
from core.schema import validate_rule, validate_settings


def plugin_root() -> str:
    return os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def load_configuration(cwd: str) -> Tuple[Dict[str, Any], List[Rule], List[str]]:
    diagnostics: List[str] = []
    root = plugin_root()

    settings: Dict[str, Any] = {}
    for path in settings_paths(root, cwd):
        internal = is_plugin_file(root, path)
        data, errors = read_json_object(path, required=False)
        record_diagnostics(errors, diagnostics, internal)
        if data is None:
            continue
        validation_errors = [f"{path}: {error}" for error in validate_settings(data)]
        if validation_errors:
            record_diagnostics(validation_errors, diagnostics, internal)
            continue
        settings = deep_merge(settings, data)

    rules_by_id: Dict[str, Rule] = {}
    for path in rule_paths(root, cwd):
        internal = is_plugin_file(root, path)
        data, errors = read_json_object(path, required=False)
        record_diagnostics(errors, diagnostics, internal)
        if data is None:
            continue
        validation_errors = validate_rule(data, path)
        if validation_errors:
            record_diagnostics(validation_errors, diagnostics, internal)
            continue
        rule = Rule(
            id=str(data["id"]),
            event=str(data["event"]),
            enabled=bool(data["enabled"]),
            decision=str(data["decision"]),
            priority=int(data.get("priority", 0)),
            match=str(data.get("match", "all")),
            when=data.get("when", []),
            message=data.get("message", {}),
            notify=data.get("notify", {}),
        )
        rules_by_id[rule.id] = rule

    return settings, list(rules_by_id.values()), diagnostics


def settings_paths(root: str, cwd: str) -> List[str]:
    return [
        os.path.join(root, "defaults", "settings.json"),
        os.path.join(os.path.expanduser("~"), ".claude", "hook-terr", "settings.json"),
        os.path.join(cwd, ".claude", "hook-terr", "settings.json"),
    ]


def rule_paths(root: str, cwd: str) -> List[str]:
    patterns = [
        os.path.join(root, "defaults", "rules", "*.json"),
        os.path.join(os.path.expanduser("~"), ".claude", "hook-terr", "rules", "*.json"),
        os.path.join(cwd, ".claude", "hook-terr", "rules", "*.json"),
    ]
    files: List[str] = []
    for pattern in patterns:
        files.extend(sorted(glob.glob(pattern)))
    return files


def read_json_object(path: str, required: bool) -> Tuple[Any, List[str]]:
    if not os.path.exists(path):
        return None, [f"missing required file: {path}"] if required else []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle), []
    except (OSError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        return None, [f"{path}: {exc}"]


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    result = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result


def is_plugin_file(root: str, path: str) -> bool:
    return os.path.abspath(path).startswith(os.path.abspath(root) + os.sep)


def record_diagnostics(errors: List[str], diagnostics: List[str], internal: bool):
    for error in errors:
        if internal:
            warn(f"hook-terr internal: {error}")
        else:
            diagnostics.append(error)


def warn(message: str):
    print(message, file=sys.stderr)
