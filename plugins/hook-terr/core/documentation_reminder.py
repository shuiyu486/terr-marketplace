import hashlib
import json
import os
import time
from typing import Any, Dict, List, Optional, Tuple

from core.models import HookContext


FEATURE_KEY = "documentationReminder"
STATE_VERSION = 1
DEFAULT_TOOLS = ["Write", "Edit", "MultiEdit", "NotebookEdit"]
DEFAULT_TTL_HOURS = 168
DEFAULT_MESSAGE = (
    "本轮会话已经修改过项目文件。结束前请完成文档收尾：更新相关 README、CLAUDE.md、"
    "reference、配置说明或示例文档；然后执行必要的测试/验证，并在确认无误后 commit/push。"
    "若无需更新文档，请在最终回复中明确说明原因。完成后再次结束即可继续。"
)
PROJECT_MARKERS = {
    ".git",
    ".hg",
    ".svn",
    ".claude",
    "CLAUDE.md",
    "CLAUDE.local.md",
    "README.md",
    "README.rst",
    "README.txt",
    "package.json",
    "pyproject.toml",
    "Cargo.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "settings.gradle",
    "composer.json",
    "Gemfile",
    "requirements.txt",
    "Makefile",
}
EXCLUDED_PARTS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "dist",
    "build",
}
LOCK_WAIT_SECONDS = 0.5
LOCK_SLEEP_SECONDS = 0.025
STALE_LOCK_SECONDS = 600


def handle_documentation_reminder(event_name: str, context: HookContext, settings: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    config = _feature_config(settings)
    if not config.get("enabled", True):
        return {}, []

    diagnostics: List[str] = []
    try:
        cleanup_expired_states(int(config.get("stateTtlHours", DEFAULT_TTL_HOURS)))
        if event_name == "UserPromptSubmit":
            reset_turn(context)
        elif event_name == "PostToolUse":
            mark_modified_if_project_file(context, config)
        elif event_name == "Stop":
            return maybe_block_stop(context, config), diagnostics
    except Exception as exc:
        diagnostics.append(str(exc))
    return {}, diagnostics


def _feature_config(settings: Dict[str, Any]) -> Dict[str, Any]:
    features = settings.get("features", {}) if isinstance(settings, dict) else {}
    config = features.get(FEATURE_KEY, {}) if isinstance(features, dict) else {}
    result = {
        "enabled": True,
        "tools": DEFAULT_TOOLS,
        "stateTtlHours": DEFAULT_TTL_HOURS,
        "message": DEFAULT_MESSAGE,
    }
    if isinstance(config, dict):
        result.update(config)
    if not isinstance(result.get("tools"), list):
        result["tools"] = DEFAULT_TOOLS
    if not isinstance(result.get("message"), str):
        result["message"] = DEFAULT_MESSAGE
    return result


def reset_turn(context: HookContext) -> None:
    key, source = session_key(context)
    if not key:
        return

    def mutate(state: Dict[str, Any]) -> Dict[str, Any]:
        now = time.time()
        return {
            "version": STATE_VERSION,
            "sessionKey": key,
            "source": source,
            "cwd": context.cwd,
            "transcriptPath": context.transcript_path,
            "dirty": False,
            "reminded": False,
            "tools": [],
            "updatedAt": now,
        }

    update_state(key, mutate)


def mark_modified_if_project_file(context: HookContext, config: Dict[str, Any]) -> None:
    tools = [str(tool) for tool in config.get("tools", DEFAULT_TOOLS) if isinstance(tool, str)]
    if context.tool_name not in tools:
        return
    if not is_project_file_change(context):
        return

    key, source = session_key(context)
    if not key:
        return

    def mutate(state: Dict[str, Any]) -> Dict[str, Any]:
        now = time.time()
        state = dict(state) if isinstance(state, dict) else {}
        current_tools = state.get("tools", [])
        if not isinstance(current_tools, list):
            current_tools = []
        if context.tool_name not in current_tools:
            current_tools.append(context.tool_name)
        state.update(
            {
                "version": STATE_VERSION,
                "sessionKey": key,
                "source": source,
                "cwd": context.cwd,
                "transcriptPath": context.transcript_path,
                "dirty": True,
                "tools": current_tools,
                "updatedAt": now,
            }
        )
        state.setdefault("reminded", False)
        return state

    update_state(key, mutate)


def maybe_block_stop(context: HookContext, config: Dict[str, Any]) -> Dict[str, Any]:
    key, _ = session_key(context)
    if not key:
        return {}

    should_block = False

    def mutate(state: Dict[str, Any]) -> Dict[str, Any]:
        nonlocal should_block
        state = dict(state) if isinstance(state, dict) else {}
        if state.get("dirty") is True and state.get("reminded") is not True:
            should_block = True
            state["reminded"] = True
            state["updatedAt"] = time.time()
        return state

    update_state(key, mutate)
    if not should_block:
        return {}

    message = str(config.get("message") or DEFAULT_MESSAGE)
    return {"decision": "block", "reason": message, "systemMessage": message}


def is_project_file_change(context: HookContext) -> bool:
    cwd = _normalize_path(context.cwd)
    if not cwd or not os.path.isdir(cwd):
        return False
    if not looks_like_project(cwd):
        return False

    target = modified_path(context)
    if not target:
        return False
    if not os.path.isabs(target):
        target = os.path.join(cwd, target)
    target = _normalize_path(target)
    if not is_within(target, cwd):
        return False
    return not has_excluded_part(target, cwd)


def modified_path(context: HookContext) -> str:
    tool_input = context.tool_input if isinstance(context.tool_input, dict) else {}
    for key in ("file_path", "notebook_path", "path"):
        value = tool_input.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return ""


def looks_like_project(cwd: str) -> bool:
    current = _normalize_path(cwd)
    home = _normalize_path(os.path.expanduser("~"))
    while current and os.path.isdir(current):
        if current == home:
            break
        for marker in PROJECT_MARKERS:
            if os.path.exists(os.path.join(current, marker)):
                return True
        parent = _normalize_path(os.path.dirname(current))
        if parent == current:
            break
        current = parent
    return False


def has_excluded_part(path: str, cwd: str) -> bool:
    try:
        relative = os.path.relpath(path, cwd)
    except ValueError:
        return True
    parts = set(relative.split(os.sep))
    if ".claude" in parts and "hook-terr" in parts and "state" in parts:
        return True
    return bool(parts & EXCLUDED_PARTS)


def session_key(context: HookContext) -> Tuple[str, str]:
    session_id = context.raw_input.get("session_id", "") if isinstance(context.raw_input, dict) else ""
    if isinstance(session_id, str) and session_id.strip():
        return _hash_key("session_id:" + session_id.strip()), "session_id"
    if isinstance(context.transcript_path, str) and context.transcript_path.strip():
        source = _normalize_path(context.transcript_path.strip())
        return _hash_key("transcript_path:" + source), "transcript_path"
    return "", ""


def update_state(key: str, mutate) -> None:
    path = state_path(key)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with state_lock(key):
        state = read_state(path)
        new_state = mutate(state)
        write_state(path, new_state)


def read_state(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return {}


def write_state(path: str, state: Dict[str, Any]) -> None:
    tmp_path = f"{path}.{os.getpid()}.{int(time.time() * 1000000)}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as handle:
        json.dump(state, handle, ensure_ascii=False, indent=2)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp_path, path)


class state_lock:
    def __init__(self, key: str):
        self.path = os.path.join(state_dir(), key + ".lock")
        self.acquired = False

    def __enter__(self):
        deadline = time.time() + LOCK_WAIT_SECONDS
        while True:
            try:
                os.mkdir(self.path)
                self.acquired = True
                return self
            except FileExistsError:
                self._remove_stale_lock()
                if time.time() >= deadline:
                    raise TimeoutError("documentation reminder state lock timeout")
                time.sleep(LOCK_SLEEP_SECONDS)

    def __exit__(self, exc_type, exc, tb):
        if self.acquired:
            try:
                os.rmdir(self.path)
            except OSError:
                pass

    def _remove_stale_lock(self) -> None:
        try:
            if time.time() - os.path.getmtime(self.path) > STALE_LOCK_SECONDS:
                os.rmdir(self.path)
        except OSError:
            pass


def cleanup_expired_states(ttl_hours: int) -> None:
    if ttl_hours <= 0:
        return
    directory = state_dir()
    if not os.path.isdir(directory):
        return
    cutoff = time.time() - ttl_hours * 3600
    removed = 0
    for name in os.listdir(directory):
        if removed >= 20:
            break
        path = os.path.join(directory, name)
        try:
            if name.endswith(".lock"):
                if time.time() - os.path.getmtime(path) > STALE_LOCK_SECONDS:
                    os.rmdir(path)
                    removed += 1
                continue
            if not name.endswith(".json"):
                continue
            updated_at = _state_updated_at(path)
            if updated_at < cutoff:
                os.remove(path)
                removed += 1
        except OSError:
            continue


def _state_updated_at(path: str) -> float:
    state = read_state(path)
    updated_at = state.get("updatedAt") if isinstance(state, dict) else None
    if isinstance(updated_at, (int, float)):
        return float(updated_at)
    return os.path.getmtime(path)


def state_path(key: str) -> str:
    return os.path.join(state_dir(), key + ".json")


def state_dir() -> str:
    return os.path.join(os.path.expanduser("~"), ".claude", "hook-terr", "state", "documentation-reminder")


def is_within(path: str, root: str) -> bool:
    try:
        return os.path.commonpath([path, root]) == root
    except ValueError:
        return False


def _normalize_path(path: str) -> str:
    return os.path.normcase(os.path.abspath(os.path.normpath(path))) if path else ""


def _hash_key(source: str) -> str:
    return hashlib.sha256(source.encode("utf-8")).hexdigest()
