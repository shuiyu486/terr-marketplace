import argparse
import json
import os
from copy import deepcopy
from typing import Any, Dict, List

VALID_CHANNELS = {"beep", "windows_toast", "popup", "custom_command"}


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

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(settings, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return path


def main():
    parser = argparse.ArgumentParser(description="Update hook-terr Stop notification channels")
    parser.add_argument("--scope", choices=("global", "project"), required=True)
    parser.add_argument("--cwd", required=True)
    parser.add_argument("--channels", required=True, help="Comma-separated channel list")
    args = parser.parse_args()
    channels = [channel.strip() for channel in args.channels.split(",") if channel.strip()]
    path = write_stop_channels(args.scope, args.cwd, channels)
    print(path)


if __name__ == "__main__":
    main()
