import os
import platform
import subprocess
from datetime import datetime
from typing import Any, Dict

from core.models import HookContext


def send(title: str, message: str, context: HookContext, config: Dict[str, Any]):
    command = str(config.get("command", "")).strip()
    if not command:
        raise RuntimeError("custom_command.command is empty")

    rendered = render(command, title, message, context)
    timeout = max(float(config.get("timeoutMs", 1000)) / 1000, 0.1)
    detached = bool(config.get("detached", True))

    if platform.system() == "Windows":
        args = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", rendered]
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        if detached:
            flags |= getattr(subprocess, "DETACHED_PROCESS", 0)
        process = subprocess.Popen(args, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=flags)
    else:
        process = subprocess.Popen(rendered, shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not detached:
        process.wait(timeout=timeout)


def render(template: str, title: str, message: str, context: HookContext) -> str:
    values = {
        "event": context.hook_event_name,
        "title": title,
        "message": message,
        "cwd": context.cwd,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", str(value))
    return rendered
