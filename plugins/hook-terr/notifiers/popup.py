import platform
import subprocess
from typing import Any, Dict

from core.models import HookContext
from notifiers.windows_process import powershell_executable


def send(title: str, message: str, context: HookContext, config: Dict[str, Any]):
    if platform.system() != "Windows":
        raise RuntimeError("popup is only supported on Windows")
    popup_title = str(title or config.get("title") or "hook-terr")
    icon = str(config.get("icon", "info")).lower()
    icon_name = {
        "info": "Information",
        "warning": "Warning",
        "error": "Error",
    }.get(icon, "Information")
    script = f"""
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show({ps_quote(message)}, {ps_quote(popup_title)}, 'OK', [System.Windows.Forms.MessageBoxIcon]::{icon_name}) | Out-Null
"""
    subprocess.Popen(
        [powershell_executable(), "-NoProfile", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-Command", script],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0) | getattr(subprocess, "DETACHED_PROCESS", 0),
    )


def ps_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"
