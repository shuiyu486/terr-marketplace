import os
import platform
import signal
import subprocess
from datetime import datetime
from typing import Any, Dict

from core.models import HookContext
from notifiers.windows_process import powershell_executable, system_executable


def send(title: str, message: str, context: HookContext, config: Dict[str, Any]):
    command = str(config.get("command", "")).strip()
    if not command:
        raise RuntimeError("custom_command.command is empty")

    values = template_values(title, message, context)
    env = command_environment(values)
    timeout = max(float(config.get("timeoutMs", 1000)) / 1000, 0.1)
    detached = bool(config.get("detached", True))

    if platform.system() == "Windows":
        args = [powershell_executable(), "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command]
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        if detached:
            flags |= getattr(subprocess, "DETACHED_PROCESS", 0)
        process = subprocess.Popen(
            args,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=flags,
            env=env,
        )
    else:
        process = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env,
            start_new_session=True,
        )

    if detached:
        return
    wait_for_process(process, timeout, platform.system())


def wait_for_process(process, timeout: float, system_name: str) -> None:
    try:
        return_code = process.wait(timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        if system_name == "Windows":
            kill_windows_process_tree(process)
        else:
            kill_process_group(process.pid)
        process.wait()
        raise RuntimeError("custom_command timed out") from exc
    if return_code != 0:
        raise RuntimeError(f"custom_command exited with code {return_code}")


def kill_windows_process_tree(process) -> None:
    try:
        subprocess.run(
            [system_executable("taskkill.exe"), "/PID", str(process.pid), "/T", "/F"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5,
            check=True,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    except Exception:
        process.kill()


def kill_process_group(pid: int) -> None:
    os.killpg(pid, signal.SIGKILL)


def template_values(title: str, message: str, context: HookContext) -> Dict[str, str]:
    return {
        "event": context.hook_event_name,
        "title": title,
        "message": message,
        "cwd": context.cwd,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }


def command_environment(values: Dict[str, str]) -> Dict[str, str]:
    env = os.environ.copy()
    for key, value in values.items():
        env["HOOK_TERR_" + key.upper()] = str(value)
    return env
