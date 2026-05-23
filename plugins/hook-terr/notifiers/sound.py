import platform
import subprocess
from typing import Any, Dict

from core.models import HookContext

DEFAULT_WAV_PATH = r"C:\Windows\Media\tada.wav"


def send(title: str, message: str, context: HookContext, config: Dict[str, Any]):
    if platform.system() != "Windows":
        raise RuntimeError("sound is only supported on Windows")
    timeout = max(float(config.get("timeoutMs", 2500)) / 1000, 0.1)
    wav_path = str(config.get("wavPath") or DEFAULT_WAV_PATH).strip()
    command = wav_command(wav_path)
    subprocess.run(
        ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=timeout,
        check=True,
    )


def wav_command(path: str) -> str:
    quoted = ps_quote(path)
    return f"""
$path = {quoted}
if (-not (Test-Path -LiteralPath $path)) {{ throw \"wavPath not found: $path\" }}
$player = New-Object System.Media.SoundPlayer $path
$player.Load()
$player.PlaySync()
"""


def ps_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"
