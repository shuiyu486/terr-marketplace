import platform
import subprocess
from typing import Any, Dict

from core.models import HookContext


def send(title: str, message: str, context: HookContext, config: Dict[str, Any]):
    if platform.system() != "Windows":
        raise RuntimeError("beep is only supported on Windows")
    timeout = max(float(config.get("timeoutMs", 800)) / 1000, 0.1)
    command = "[Console]::Beep(880, 180)"
    subprocess.run(
        ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=timeout,
        check=False,
    )
