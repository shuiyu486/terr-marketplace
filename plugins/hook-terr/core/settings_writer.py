import argparse
import json
import os
from copy import deepcopy
from typing import Any, Dict, List, Optional

VALID_CHANNELS = {"sound", "windows_toast", "popup", "custom_command"}
DEFAULT_SOUND_WAV_PATH = r"C:\Windows\Media\tada.wav"
DEFAULT_PRIMARY_MODEL_COMMAND = "/model opus"
DEFAULT_FALLBACK_MODEL_COMMAND = "/model sonnet"
DEFAULT_MATCH = [
    "This content was flagged for possible cybersecurity risk",
    "cybersecurity risk",
]
DEFAULT_MODEL_SWITCH_CONFIRM_MODE = "auto"
DEFAULT_MODEL_SWITCH_CONFIRM_COMMAND = "1"


def settings_path(scope: str, cwd: str) -> str:
    if scope == "global":
        return os.path.join(os.path.expanduser("~"), ".claude", "hook-terr", "settings.json")
    if scope == "project":
        return os.path.join(cwd, ".claude", "hook-terr", "settings.json")
    raise ValueError("scope must be global or project")


def read_settings(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: settings must be a JSON object")
    return data


def write_stop_channels(scope: str, cwd: str, channels: List[str]) -> str:
    unknown = [channel for channel in channels if channel not in VALID_CHANNELS]
    if unknown:
        raise ValueError("unknown channels: " + ", ".join(unknown))

    path = settings_path(scope, cwd)
    settings = deepcopy(read_settings(path))
    events = settings.setdefault("events", {})
    stop = events.setdefault("Stop", {})
    stop["enabled"] = True
    stop["notifications"] = channels

    notifications = settings.setdefault("notifications", {})
    for channel in channels:
        channel_config = notifications.setdefault(channel, {})
        channel_config["enabled"] = True
        if channel == "sound":
            channel_config.setdefault("wavPath", DEFAULT_SOUND_WAV_PATH)

    write_settings(path, settings)
    return path


def write_sound(cwd: str, wav_path: str) -> str:
    path = settings_path("global", cwd)
    settings = deepcopy(read_settings(path))
    notifications = settings.setdefault("notifications", {})
    sound = notifications.setdefault("sound", {})
    sound["enabled"] = True
    sound["wavPath"] = wav_path or DEFAULT_SOUND_WAV_PATH
    replace_stop_channel(settings, "beep", "sound")
    write_settings(path, settings)
    return path


def write_api_error_recovery(
    scope: str,
    cwd: str,
    activation_mode: str,
    primary_model_command: str,
    fallback_model_command: str,
    confirm_model_switch: bool,
    match_texts: Optional[List[str]] = None,
    model_switch_confirm_mode: str = DEFAULT_MODEL_SWITCH_CONFIRM_MODE,
) -> str:
    target_scope = "project" if activation_mode == "project" else "global"
    if activation_mode == "disable-current-dir" and scope in ("global", "project"):
        target_scope = scope
    path = settings_path(target_scope, cwd)
    settings = deepcopy(read_settings(path))
    features = settings.setdefault("features", {})
    recovery = features.setdefault("apiErrorRecovery", {})

    if activation_mode == "disable-current-dir" and target_scope == "project":
        recovery["enabled"] = False
        write_settings(path, settings)
        return path

    if activation_mode != "disable-current-dir":
        recovery["enabled"] = True
        recovery["terminal"] = "wezterm"
        recovery["strategy"] = "escalate_then_restore"
        recovery["primaryModelCommand"] = primary_model_command or DEFAULT_PRIMARY_MODEL_COMMAND
        recovery["fallbackModelCommand"] = fallback_model_command or DEFAULT_FALLBACK_MODEL_COMMAND
        recovery["continueCommand"] = "continue"
        recovery["match"] = clean_match_texts(match_texts) or DEFAULT_MATCH
        recovery["modelSwitchConfirmMode"] = clean_confirm_mode(model_switch_confirm_mode)
        recovery["modelSwitchConfirmCommand"] = DEFAULT_MODEL_SWITCH_CONFIRM_COMMAND
        recovery["primaryConfirmCommand"] = "1" if confirm_model_switch else ""
        recovery["fallbackConfirmCommand"] = "1" if confirm_model_switch else ""
        recovery.setdefault("modelSwitchConfirmDelayMs", 500)
        recovery.setdefault("postModelSwitchDelayMs", 500)
        recovery.setdefault("modelSwitchConfirmScanLines", 20)

    if activation_mode == "project":
        cwd_scope = recovery.setdefault("scopes", {}).setdefault("cwd", {})
        cwd_scope["default"] = True
        cwd_scope["enabled"] = []
        cwd_scope["disabled"] = []
        cwd_scope["enabledPrefixes"] = []
        cwd_scope["disabledPrefixes"] = []
    elif activation_mode == "global-current-dir":
        cwd_scope = recovery.setdefault("scopes", {}).setdefault("cwd", {})
        cwd_scope["default"] = False
        remove_path(cwd_scope, "disabled", cwd)
        remove_covering_prefixes(cwd_scope, "disabledPrefixes", cwd)
        append_unique_path(cwd_scope, "enabledPrefixes", cwd)
    elif activation_mode == "global-default":
        cwd_scope = recovery.setdefault("scopes", {}).setdefault("cwd", {})
        cwd_scope["default"] = True
        remove_path(cwd_scope, "disabled", cwd)
        remove_covering_prefixes(cwd_scope, "disabledPrefixes", cwd)
    elif activation_mode == "disable-current-dir":
        cwd_scope = recovery.setdefault("scopes", {}).setdefault("cwd", {})
        remove_path(cwd_scope, "enabled", cwd)
        remove_path(cwd_scope, "enabledPrefixes", cwd)
        append_unique_path(cwd_scope, "disabledPrefixes", cwd)

    write_settings(path, settings)
    return path


def clean_match_texts(match_texts: Optional[List[str]]) -> List[str]:
    if not match_texts:
        return []
    cleaned: List[str] = []
    for text in match_texts:
        value = str(text or "").strip()
        if value and value not in cleaned:
            cleaned.append(value)
    return cleaned


def clean_confirm_mode(mode: str) -> str:
    normalized = str(mode or DEFAULT_MODEL_SWITCH_CONFIRM_MODE).strip().lower()
    if normalized in ("auto", "always", "never"):
        return normalized
    return DEFAULT_MODEL_SWITCH_CONFIRM_MODE


def append_unique_path(config: Dict[str, Any], key: str, value: str) -> None:
    values = config.setdefault(key, [])
    if not isinstance(values, list):
        values = []
        config[key] = values
    if not any(same_path(existing, value) for existing in values if isinstance(existing, str)):
        values.append(value)


def remove_path(config: Dict[str, Any], key: str, value: str) -> None:
    values = config.get(key)
    if not isinstance(values, list):
        return
    config[key] = [existing for existing in values if not (isinstance(existing, str) and same_path(existing, value))]


def remove_covering_prefixes(config: Dict[str, Any], key: str, value: str) -> None:
    values = config.get(key)
    if not isinstance(values, list):
        return
    normalized = normalize_path(value)
    config[key] = [
        existing
        for existing in values
        if not (isinstance(existing, str) and path_is_or_under(normalized, normalize_path(existing)))
    ]


def path_is_or_under(path: str, prefix: str) -> bool:
    if not path or not prefix:
        return False
    return path == prefix or path.startswith(prefix + os.sep)


def same_path(left: str, right: str) -> bool:
    return normalize_path(left) == normalize_path(right)


def normalize_path(path: str) -> str:
    return os.path.normcase(os.path.normpath(str(path or "")))


def replace_stop_channel(settings: Dict[str, Any], old: str, new: str) -> None:
    stop = settings.get("events", {}).get("Stop", {})
    channels = stop.get("notifications") if isinstance(stop, dict) else None
    if not isinstance(channels, list):
        return
    stop["notifications"] = [new if channel == old else channel for channel in channels]


def write_settings(path: str, settings: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(settings, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def main():
    parser = argparse.ArgumentParser(description="Update hook-terr settings")
    parser.add_argument("--scope", choices=("global", "project"))
    parser.add_argument("--cwd", required=True)
    parser.add_argument("--channels", help="Comma-separated channel list")
    parser.add_argument("--sound-wav-path", help="Global wav file used by the sound notification channel")
    parser.add_argument("--api-error-recovery", action="store_true", help="Update apiErrorRecovery settings")
    parser.add_argument("--activation-mode", choices=("project", "global-current-dir", "global-default", "disable-current-dir"))
    parser.add_argument("--primary-model-command", default=DEFAULT_PRIMARY_MODEL_COMMAND)
    parser.add_argument("--fallback-model-command", default=DEFAULT_FALLBACK_MODEL_COMMAND)
    parser.add_argument("--confirm-model-switch", choices=("true", "false"), default="false")
    parser.add_argument("--model-switch-confirm-mode", choices=("auto", "always", "never"), default=DEFAULT_MODEL_SWITCH_CONFIRM_MODE)
    parser.add_argument("--match-text", action="append", help="StopFailure text to match; may be passed multiple times")
    args = parser.parse_args()

    if args.sound_wav_path:
        path = write_sound(args.cwd, args.sound_wav_path)
    elif args.api_error_recovery:
        if not args.activation_mode:
            raise ValueError("--activation-mode is required when updating apiErrorRecovery")
        path = write_api_error_recovery(
            args.scope or ("project" if args.activation_mode == "project" else "global"),
            args.cwd,
            args.activation_mode,
            args.primary_model_command,
            args.fallback_model_command,
            args.confirm_model_switch == "true",
            args.match_text,
            args.model_switch_confirm_mode,
        )
    else:
        if not args.scope or args.channels is None:
            raise ValueError("--scope and --channels are required when updating Stop channels")
        channels = [channel.strip() for channel in args.channels.split(",") if channel.strip()]
        path = write_stop_channels(args.scope, args.cwd, channels)
    print(path)


if __name__ == "__main__":
    main()
