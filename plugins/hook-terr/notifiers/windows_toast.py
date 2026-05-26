import os
import platform
import subprocess
import tempfile
import uuid
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
$ErrorActionPreference = 'Stop'
$scriptPath = $MyInvocation.MyCommand.Path
$debugLog = $env:HOOK_TERR_WINDOWS_TOAST_LOG
$toastTitle = [System.Security.SecurityElement]::Escape({safe_title})
$toastMessage = [System.Security.SecurityElement]::Escape({safe_message})
try {{
    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
    [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] > $null
    $template = "<toast><visual><binding template=`"ToastGeneric`"><text>$toastTitle</text><text>$toastMessage</text></binding></visual></toast>"
    $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
    $xml.LoadXml($template)
    $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
    $notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Windows PowerShell')
    $notifier.Show($toast)
    if ($debugLog) {{ Add-Content -Path $debugLog -Encoding UTF8 -Value "$(Get-Date -Format o) WinRT shown" }}
}} catch {{
    Write-Error $_
}}
try {{
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
        Remove-Item $scriptPath -Force -ErrorAction SilentlyContinue
        $context.ExitThread()
    }}
    $notify.add_BalloonTipClosed($cleanup)
    $notify.add_BalloonTipClicked($cleanup)
    $timer.Interval = {visible_ms}
    $timer.add_Tick($cleanup)
    $timer.Start()
    $notify.ShowBalloonTip({visible_ms})
    if ($debugLog) {{ Add-Content -Path $debugLog -Encoding UTF8 -Value "$(Get-Date -Format o) NotifyIcon shown" }}
    [System.Windows.Forms.Application]::Run($context)
}} catch {{
    Write-Error $_
    Remove-Item $scriptPath -Force -ErrorAction SilentlyContinue
}}
"""
    popen_hidden(script)


def ps_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def popen_hidden(script: str):
    script_path = write_temp_script(script)
    log_path = os.environ.get("HOOK_TERR_WINDOWS_TOAST_LOG")
    log_handle = open(log_path, "a", encoding="utf-8") if log_path else subprocess.DEVNULL
    subprocess.Popen(
        [
            "cmd.exe",
            "/d",
            "/c",
            "start",
            "",
            "/min",
            "powershell.exe",
            "-NoProfile",
            "-STA",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            script_path,
        ],
        stdin=subprocess.DEVNULL,
        stdout=log_handle,
        stderr=log_handle,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )


def write_temp_script(script: str) -> str:
    directory = os.path.join(tempfile.gettempdir(), "hook-terr")
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, f"windows_toast_{os.getpid()}_{uuid.uuid4().hex}.ps1")
    with open(path, "w", encoding="utf-8-sig") as handle:
        handle.write(script)
    return path
