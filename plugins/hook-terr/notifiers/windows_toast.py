import platform
import subprocess
from typing import Any, Dict

from core.models import HookContext


def send(title: str, message: str, context: HookContext, config: Dict[str, Any]):
    if platform.system() != "Windows":
        raise RuntimeError("windows_toast is only supported on Windows")
    safe_title = ps_quote(title)
    safe_message = ps_quote(message)
    timeout_ms = int(config.get("timeoutMs", 5000))
    visible_ms = min(max(timeout_ms, 5000), 30000)
    script = f"""
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
[System.Windows.Forms.Application]::EnableVisualStyles()
$context = New-Object System.Windows.Forms.ApplicationContext
$notify = New-Object System.Windows.Forms.NotifyIcon
$timer = New-Object System.Windows.Forms.Timer
$notify.Icon = [System.Drawing.SystemIcons]::Information
$notify.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::Info
$notify.BalloonTipTitle = {safe_title}
$notify.BalloonTipText = {safe_message}
$notify.Visible = $true
$cleanup = {{
    $timer.Stop()
    $notify.Visible = $false
    $notify.Dispose()
    $timer.Dispose()
    $context.ExitThread()
}}
$notify.add_BalloonTipClosed($cleanup)
$notify.add_BalloonTipClicked($cleanup)
$timer.Interval = {visible_ms}
$timer.add_Tick($cleanup)
$timer.Start()
$notify.ShowBalloonTip({visible_ms})
[System.Windows.Forms.Application]::Run($context)
"""
    popen_hidden(script)


def ps_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def popen_hidden(script: str):
    subprocess.Popen(
        ["powershell.exe", "-NoProfile", "-STA", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-Command", script],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0) | getattr(subprocess, "DETACHED_PROCESS", 0),
    )
