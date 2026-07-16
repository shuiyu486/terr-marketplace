import hashlib
import json
import os
import shutil
import subprocess
import time
from typing import Any, Dict, List, Optional, Tuple

from core.models import HookContext
from core.paths import hook_terr_dir


DEFAULT_MATCH = [
    "This content was flagged for possible cybersecurity risk",
    "cybersecurity risk",
]
DEFAULT_MODEL_SWITCH_CONFIRM_COMMAND = "1"
DEFAULT_MODEL_SWITCH_CONFIRM_MODE = "auto"
DEFAULT_RECOVERY_MODE = "continue_then_fallback"
MODEL_SWITCH_CONFIRM_MODES = {"auto", "always", "never"}
RECOVERY_MODES = {"continue_only", "continue_then_fallback", "fallback_then_continue"}
MODEL_SWITCH_CONFIRM_MARKERS = ("switch model?", "yes, switch to")


def handle_api_error_recovery(event_name: str, context: HookContext, settings: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    if context.is_subagent:
        return {}, []

    config = recovery_config(settings)
    if not is_recovery_enabled(config, context):
        return {}, []

    pane_id = os.environ.get("WEZTERM_PANE", "").strip()
    session_key = build_session_key(context, pane_id)
    diagnostics: List[str] = []

    if not session_key:
        if event_name == "StopFailure" and matches_error(context, config):
            diagnostics.append("apiErrorRecovery: WEZTERM_PANE、session_id/transcript_path 不完整，跳过自动恢复")
        return {}, diagnostics

    root = state_root()
    state_path = os.path.join(root, session_key + ".json")
    if event_name != "StopFailure" and not os.path.exists(state_path):
        return {}, diagnostics

    os.makedirs(root, exist_ok=True)
    lock_path = os.path.join(root, session_key + ".lock")
    lock_error = acquire_lock(lock_path, int(config.get("lockTimeoutSeconds", 30)))
    if lock_error:
        if event_name == "StopFailure":
            diagnostics.append(lock_error)
        return {}, diagnostics

    try:
        state = read_state(state_path)
        now = now_seconds()
        action, next_state, delete_state = plan_action(event_name, context, config, state, pane_id, session_key, now)
        if not action:
            return {}, diagnostics

        pending_state = None
        if action_model_transition(action["steps"]) == "fallback":
            pending_state = dict(next_state)
            pending_state["modelTransitionPending"] = "fallback"
            write_state(state_path, pending_state)

        error, started_model, completed_model = send_recovery_steps(
            pane_id,
            action["steps"],
            int(config.get("sendDelayMs", 800)),
            config,
        )
        if error:
            if completed_model == "fallback":
                write_state(state_path, next_state)
            elif started_model == "fallback" and pending_state is not None:
                write_state(state_path, pending_state)
            elif pending_state is not None:
                if state:
                    write_state(state_path, state)
                else:
                    delete_file(state_path)
            elif completed_model == "primary":
                delete_file(state_path)
            diagnostics.append(error)
            return {}, diagnostics

        if delete_state:
            delete_file(state_path)
        else:
            write_state(state_path, next_state)
        return {}, diagnostics
    finally:
        release_lock(lock_path)


def recovery_config(settings: Dict[str, Any]) -> Dict[str, Any]:
    features = settings.get("features", {}) if isinstance(settings.get("features", {}), dict) else {}
    config = features.get("apiErrorRecovery", {}) if isinstance(features.get("apiErrorRecovery", {}), dict) else {}
    return config


def is_recovery_enabled(config: Dict[str, Any], context: HookContext) -> bool:
    env_override = coerce_bool(os.environ.get("HOOK_TERR_API_ERROR_RECOVERY"))
    if env_override is False:
        return False
    if env_override is not True and not config.get("enabled", False):
        return False
    if not scope_enabled(config, "sessions", context.session_id, default=True):
        return False
    return scope_enabled(config, "cwd", context.cwd, default=True)


def scope_enabled(config: Dict[str, Any], key: str, value: str, default: bool) -> bool:
    scopes = config.get("scopes")
    if not isinstance(scopes, dict):
        return default
    scope = scopes.get(key)
    if not isinstance(scope, dict):
        return default
    if key == "cwd":
        return cwd_scope_enabled(scope, value, default)
    value = str(value or "")
    if value and value in string_list(scope.get("disabled")):
        return False
    if value and value in string_list(scope.get("enabled")):
        return True
    default_value = scope.get("default")
    return default_value if isinstance(default_value, bool) else default


def cwd_scope_enabled(scope: Dict[str, Any], cwd: str, default: bool) -> bool:
    value = normalize_path(cwd)
    if value and value in [normalize_path(path) for path in string_list(scope.get("disabled"))]:
        return False
    if value and value in [normalize_path(path) for path in string_list(scope.get("enabled"))]:
        return True
    if value and any(path_is_or_under(value, normalize_path(path)) for path in string_list(scope.get("disabledPrefixes"))):
        return False
    if value and any(path_is_or_under(value, normalize_path(path)) for path in string_list(scope.get("enabledPrefixes"))):
        return True
    default_value = scope.get("default")
    return default_value if isinstance(default_value, bool) else default


def path_is_or_under(path: str, prefix: str) -> bool:
    if not path or not prefix:
        return False
    return path == prefix or path.startswith(prefix + os.sep)


def normalize_path(path: str) -> str:
    return os.path.normcase(os.path.normpath(str(path or "")))


def string_list(value: Any) -> List[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, str)]


def coerce_bool(value: Any) -> Optional[bool]:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in ("1", "true", "yes", "y", "on", "enabled", "enable"):
            return True
        if normalized in ("0", "false", "no", "n", "off", "disabled", "disable", ""):
            return False
    return None


def plan_action(event_name: str, context: HookContext, config: Dict[str, Any], state: Dict[str, Any], pane_id: str, session_key: str, now: float):
    if event_name != "StopFailure":
        if should_restore(event_name, config, state, pane_id, now):
            text = restore_text(config)
            if text and not is_duplicate_action(state, text, config, now):
                return {"type": "restore_model", "text": text, "steps": restore_steps(config)}, state, True
        return None, state, False

    error_matches = matches_error(context, config)
    fallback_active = bool(
        state.get("fallbackActive", False)
        or state.get("modelTransitionPending") == "fallback"
    )
    if fallback_active:
        if should_restore(event_name, config, state, pane_id, now):
            if not error_matches:
                text = restore_text(config)
                if text and not is_duplicate_action(state, text, config, now):
                    return {"type": "restore_model", "text": text, "steps": restore_steps(config)}, state, True
                return None, state, False
            error_text = combined_error_text(context)
            text = restore_text(config) + continue_text(config)
            next_state = first_failure_state(context, pane_id, session_key, now, text, error_text, "restore_model_continue")
            if not is_duplicate_action(state, text, config, now):
                return {"type": "restore_model_continue", "text": text, "steps": restore_continue_steps(config)}, next_state, False
        return None, state, False

    if not error_matches:
        return None, state, False

    error_text = combined_error_text(context)

    mode = recovery_mode(config)
    if mode == "continue_only":
        text = continue_text(config)
        next_state = first_failure_state(context, pane_id, session_key, now, text, error_text, "continue")
        if not is_duplicate_action(state, text, config, now):
            return {"type": "continue", "text": text, "steps": continue_steps(config)}, next_state, False
        return None, state, False

    window_seconds = int(config.get("windowSeconds", 600))
    first_failure_at = float(state.get("firstFailureAt", 0) or 0)
    within_window = bool(first_failure_at and now - first_failure_at <= window_seconds)

    if mode == "fallback_then_continue":
        return plan_switch_model_continue(context, config, state, pane_id, session_key, now, error_text, 0)

    if not state or not within_window:
        text = continue_text(config)
        next_state = first_failure_state(context, pane_id, session_key, now, text, error_text, "continue")
        if not is_duplicate_action(state, text, config, now):
            return {"type": "continue", "text": text, "steps": continue_steps(config)}, next_state, False
        return None, state, False

    escalation_count = int(state.get("escalationCount", 0) or 0)
    max_escalations = int(config.get("maxEscalations", 1))
    if escalation_count >= max_escalations:
        return None, state, False

    return plan_switch_model_continue(context, config, state, pane_id, session_key, now, error_text, escalation_count)


def plan_switch_model_continue(
    context: HookContext,
    config: Dict[str, Any],
    state: Dict[str, Any],
    pane_id: str,
    session_key: str,
    now: float,
    error_text: str,
    escalation_count: int,
):
    text = switch_model_continue_text(config)
    next_state = dict(state) if state else base_state(context, pane_id, session_key, now)
    next_state.update(
        {
            "lastFailureAt": now,
            "failureCount": int(state.get("failureCount", 0) or 0) + 1,
            "fallbackActive": True,
            "fallbackStartedAt": now,
            "fallbackRestoredAt": None,
            "escalationCount": escalation_count + 1,
            "lastAction": "switch_model_continue",
            "lastSentText": text,
            "lastSentAt": now,
            "lastError": error_text,
            "paneId": pane_id,
        }
    )
    if not state:
        next_state["firstFailureAt"] = now
    if not is_duplicate_action(state, text, config, now):
        return {"type": "switch_model_continue", "text": text, "steps": switch_model_continue_steps(config)}, next_state, False
    return None, state, False


def recovery_mode(config: Dict[str, Any]) -> str:
    mode = str(config.get("recoveryMode", DEFAULT_RECOVERY_MODE)).strip().lower()
    return mode if mode in RECOVERY_MODES else DEFAULT_RECOVERY_MODE


def should_restore(event_name: str, config: Dict[str, Any], state: Dict[str, Any], pane_id: str, now: float) -> bool:
    if not state or not (
        state.get("fallbackActive")
        or state.get("modelTransitionPending") == "fallback"
    ):
        return False
    if bool(config.get("requireSamePaneForRestore", True)) and str(state.get("paneId", "")) != pane_id:
        return False
    if event_name == "Stop":
        return True
    started_at = float(state.get("fallbackStartedAt", 0) or 0)
    restore_after = int(config.get("restoreAfterSeconds", 600))
    return bool(started_at and now - started_at >= restore_after)


def is_duplicate_action(state: Dict[str, Any], text: str, config: Dict[str, Any], now: float) -> bool:
    if not state:
        return False
    dedupe_seconds = int(config.get("dedupeSeconds", 5))
    last_sent_at = float(state.get("lastSentAt", 0) or 0)
    return bool(last_sent_at and now - last_sent_at <= dedupe_seconds and text == str(state.get("lastSentText", "")))


def first_failure_state(context: HookContext, pane_id: str, session_key: str, now: float, text: str, error_text: str, action: str) -> Dict[str, Any]:
    state = base_state(context, pane_id, session_key, now)
    state.update(
        {
            "firstFailureAt": now,
            "lastFailureAt": now,
            "failureCount": 1,
            "fallbackActive": False,
            "escalationCount": 0,
            "lastAction": action,
            "lastSentText": text,
            "lastSentAt": now,
            "lastError": error_text,
        }
    )
    return state


def base_state(context: HookContext, pane_id: str, session_key: str, now: float) -> Dict[str, Any]:
    return {
        "sessionKey": session_key,
        "sessionId": context.session_id,
        "paneId": pane_id,
        "transcriptPath": context.transcript_path,
        "cwd": context.cwd,
        "createdAt": now,
    }


def matches_error(context: HookContext, config: Dict[str, Any]) -> bool:
    matchers = config.get("match", DEFAULT_MATCH)
    if not isinstance(matchers, list) or not matchers:
        return True
    text = combined_error_text(context).lower()
    return any(str(matcher).lower() in text for matcher in matchers if isinstance(matcher, str) and matcher)


def combined_error_text(context: HookContext) -> str:
    parts = [context.error, context.error_details, context.last_assistant_message, context.reason]
    return "\n".join(str(part) for part in parts if part)


def continue_text(config: Dict[str, Any]) -> str:
    return steps_text(continue_steps(config))


def switch_model_continue_text(config: Dict[str, Any]) -> str:
    return steps_text(switch_model_continue_steps(config))


def restore_text(config: Dict[str, Any]) -> str:
    return steps_text(restore_steps(config))


def continue_steps(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    return text_steps(command_line(str(config.get("continueCommand", "continue"))))


def switch_model_continue_steps(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    return model_steps(config, "fallback") + continue_steps(config)


def restore_steps(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    return model_steps(config, "primary")


def restore_continue_steps(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    return restore_steps(config) + continue_steps(config)


def model_steps(config: Dict[str, Any], kind: str) -> List[Dict[str, Any]]:
    if kind == "fallback":
        command = str(config.get("fallbackModelCommand", "/model sonnet"))
        legacy_confirm = str(config.get("fallbackConfirmCommand", ""))
    else:
        command = str(config.get("primaryModelCommand", "/model opus"))
        legacy_confirm = str(config.get("primaryConfirmCommand", ""))

    steps: List[Dict[str, Any]] = []
    command_text = command_line(command)
    if not command_text:
        return steps

    mode = model_switch_confirm_mode(config)
    confirm_text = command_line(model_switch_confirm_command(config, legacy_confirm)) if mode != "never" else ""
    delay = number_config(config, "modelSwitchConfirmDelayMs", 500) if confirm_text else number_config(config, "postModelSwitchDelayMs", 500)
    step = {"text": command_text, "delayAfterMs": delay, "modelTransition": kind}
    if mode == "auto" and confirm_text:
        step["captureConfirmBaseline"] = True
    steps.append(step)
    if confirm_text:
        steps.append(
            {
                "text": confirm_text,
                "delayAfterMs": number_config(config, "postModelSwitchDelayMs", 500),
                "condition": "model_switch_confirm" if mode == "auto" else "always",
            }
        )
    return steps


def action_model_transition(steps: List[Dict[str, Any]]) -> str:
    for step in steps:
        transition = str(step.get("modelTransition", "")) if isinstance(step, dict) else ""
        if transition in ("fallback", "primary"):
            return transition
    return ""


def text_steps(text: str) -> List[Dict[str, Any]]:
    return [{"text": text, "delayAfterMs": 0}] if text else []


def steps_text(steps: List[Dict[str, Any]]) -> str:
    return "".join(str(step.get("text", "")) for step in steps if isinstance(step, dict))


def command_line(command: str) -> str:
    stripped = command.strip()
    return f"{stripped}\r" if stripped else ""


def model_switch_confirm_mode(config: Dict[str, Any]) -> str:
    mode = str(config.get("modelSwitchConfirmMode", DEFAULT_MODEL_SWITCH_CONFIRM_MODE)).strip().lower()
    return mode if mode in MODEL_SWITCH_CONFIRM_MODES else DEFAULT_MODEL_SWITCH_CONFIRM_MODE


def model_switch_confirm_command(config: Dict[str, Any], legacy_confirm: str) -> str:
    command = str(config.get("modelSwitchConfirmCommand", "")).strip()
    if command:
        return command
    if legacy_confirm.strip():
        return legacy_confirm
    return DEFAULT_MODEL_SWITCH_CONFIRM_COMMAND


def number_config(config: Dict[str, Any], key: str, default: float) -> float:
    value = config.get(key, default)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
        return default
    return float(value)


def send_recovery_steps(
    pane_id: str,
    steps: List[Dict[str, Any]],
    delay_ms: int,
    config: Dict[str, Any],
) -> Tuple[str, str, str]:
    if str(config.get("terminal", "wezterm")) != "wezterm":
        return "apiErrorRecovery: 当前仅支持 terminal=wezterm", "", ""
    if not pane_id:
        return "apiErrorRecovery: WEZTERM_PANE is not set", "", ""
    if not steps:
        return "apiErrorRecovery: recovery steps are empty", "", ""
    if delay_ms > 0:
        time.sleep(delay_ms / 1000)
    confirm_baseline = ""
    confirm_baseline_available = True
    started_model = ""
    completed_model = ""
    for step in steps:
        text = str(step.get("text", "")) if isinstance(step, dict) else ""
        if not text:
            continue
        if bool(step.get("captureConfirmBaseline", False)):
            confirm_baseline, baseline_error = get_wezterm_pane_text(
                pane_id,
                int(config.get("modelSwitchConfirmScanLines", 20)),
            )
            confirm_baseline_available = not bool(baseline_error)
            if not confirm_baseline_available:
                return (
                    "apiErrorRecovery: model switch confirmation baseline unavailable; skip model switch",
                    started_model,
                    completed_model,
                )
        condition = str(step.get("condition", "always")) if isinstance(step, dict) else "always"
        if condition == "model_switch_confirm":
            if not confirm_baseline_available:
                continue
            if not pane_has_model_switch_confirm(pane_id, config, confirm_baseline):
                continue
        transition = str(step.get("modelTransition", "")) if isinstance(step, dict) else ""
        if transition in ("fallback", "primary"):
            started_model = transition
        error = send_text_to_wezterm(pane_id, text)
        if error:
            return error, started_model, completed_model
        if transition in ("fallback", "primary"):
            completed_model = transition
        delay_after_ms = number_config(step, "delayAfterMs", 0)
        if delay_after_ms > 0:
            time.sleep(delay_after_ms / 1000)
    return "", started_model, completed_model


def send_text_to_wezterm(pane_id: str, text: str) -> str:
    kwargs = {
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
        "timeout": 2,
    }
    if os.name == "nt":
        kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    try:
        completed = subprocess.run(["wezterm", "cli", "send-text", "--pane-id", pane_id, "--no-paste", text], **kwargs)
    except Exception as exc:
        return f"apiErrorRecovery: wezterm send-text failed: {exc}"
    if completed.returncode != 0:
        return f"apiErrorRecovery: wezterm send-text failed: exit code {completed.returncode}"
    return ""


def pane_has_model_switch_confirm(pane_id: str, config: Dict[str, Any], baseline: str = "") -> bool:
    text, error = get_wezterm_pane_text(pane_id, int(config.get("modelSwitchConfirmScanLines", 20)))
    if error:
        return False
    scan_text = text_after_baseline(text, baseline)
    return contains_model_switch_confirm(scan_text)


def text_after_baseline(text: str, baseline: str) -> str:
    if not baseline:
        return text
    if text == baseline:
        return ""
    if text.startswith(baseline):
        return text[len(baseline) :]
    overlap = suffix_prefix_overlap(baseline, text)
    if overlap:
        return text[overlap:]
    if contains_model_switch_confirm(baseline):
        return ""
    return text


def suffix_prefix_overlap(previous: str, current: str) -> int:
    max_size = min(len(previous), len(current))
    for size in range(max_size, 0, -1):
        if previous[-size:] == current[:size]:
            return size
    return 0


def contains_model_switch_confirm(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in MODEL_SWITCH_CONFIRM_MARKERS)


def get_wezterm_pane_text(pane_id: str, scan_lines: int) -> Tuple[str, str]:
    end_line = -max(scan_lines, 1)
    kwargs = {
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "text": True,
        "encoding": "utf-8",
        "errors": "replace",
        "timeout": 2,
    }
    if os.name == "nt":
        kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    try:
        completed = subprocess.run(
            ["wezterm", "cli", "get-text", "--pane-id", pane_id, f"--start-line={end_line}"],
            **kwargs,
        )
    except Exception as exc:
        return "", f"apiErrorRecovery: wezterm get-text failed: {exc}"
    if completed.returncode != 0:
        return "", "apiErrorRecovery: wezterm get-text failed"
    return completed.stdout or "", ""


def build_session_key(context: HookContext, pane_id: str) -> str:
    if not pane_id:
        return ""
    if context.session_id:
        source = f"session:{context.session_id}|pane:{pane_id}"
    elif context.transcript_path:
        source = f"transcript:{context.transcript_path}|pane:{pane_id}|cwd:{context.cwd}"
    else:
        return ""
    return hashlib.sha256(source.encode("utf-8", errors="ignore")).hexdigest()


def state_root() -> str:
    return os.path.join(hook_terr_dir(), "state", "api-error-recovery")


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
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as handle:
        json.dump(state, handle, ensure_ascii=False, indent=2)
    os.replace(tmp_path, path)


def delete_file(path: str) -> None:
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def acquire_lock(path: str, timeout_seconds: int) -> str:
    try:
        os.mkdir(path)
        return ""
    except FileExistsError:
        pass
    except OSError as exc:
        return f"apiErrorRecovery: lock failed: {exc}"

    try:
        age = now_seconds() - os.path.getmtime(path)
        if age > timeout_seconds:
            shutil.rmtree(path, ignore_errors=True)
            os.mkdir(path)
            return ""
    except FileExistsError:
        pass
    except OSError as exc:
        return f"apiErrorRecovery: lock cleanup failed: {exc}"
    return "apiErrorRecovery: session lock is active, skip recovery"


def release_lock(path: str) -> None:
    shutil.rmtree(path, ignore_errors=True)


def now_seconds() -> float:
    return time.time()
