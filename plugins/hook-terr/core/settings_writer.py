import argparse
import json
import os
from copy import deepcopy
from typing import Any, Dict, List

VALID_CHANNELS = {"sound", "windows_toast", "popup", "custom_command"}
DEFAULT_SOUND_WAV_PATH = r"C:\Windows\Media\tada.wav"


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
    args = parser.parse_args()

    if args.sound_wav_path:
        path = write_sound(args.cwd, args.sound_wav_path)
    else:
        if not args.scope or args.channels is None:
            raise ValueError("--scope and --channels are required when updating Stop channels")
        channels = [channel.strip() for channel in args.channels.split(",") if channel.strip()]
        path = write_stop_channels(args.scope, args.cwd, channels)
    print(path)


if __name__ == "__main__":
    main()
