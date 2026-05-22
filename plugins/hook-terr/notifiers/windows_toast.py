import platform
import subprocess
from typing import Any, Dict

from core.models import HookContext


def send(title: str, message: str, context: HookContext, config: Dict[str, Any]):
    if platform.system() != "Windows":
        raise RuntimeError("windows_toast is only supported on Windows")
    safe_title = ps_quote(title)
    safe_message = ps_quote(message)
    timeout_ms = int(config.get("timeoutMs", 1500))
    script = f"""
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$notify = New-Object System.Windows.Forms.NotifyIcon
$notify.Icon = [System.Drawing.SystemIcons]::Information
$notify.BalloonTipTitle = {safe_title}
$notify.BalloonTipText = {safe_message}
$notify.Visible = $true
$notify.ShowBalloonTip({timeout_ms})
Start-Sleep -Milliseconds {min(max(timeout_ms, 300), 3000)}
$notify.Dispose()
"""
    popen_hidden(script)


def ps_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def popen_hidden(script: str):
    subprocess.Popen(
        ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-Command", script],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0) | getattr(subprocess, "DETACHED_PROCESS", 0),
    )
