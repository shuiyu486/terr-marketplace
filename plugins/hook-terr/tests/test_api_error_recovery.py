import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

PLUGIN_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PLUGIN_ROOT not in sys.path:
    sys.path.insert(0, PLUGIN_ROOT)

from core.event_runner import run


class ApiErrorRecoveryTests(unittest.TestCase):
    def test_first_stop_failure_sends_continue(self):
        with self.project_env() as (home, cwd):
            with self.recovery_patches("101", [1000]) as send_text:
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))

            send_text.assert_called_once_with("101", "continue\r")

    def test_second_stop_failure_within_window_switches_model_then_continues(self):
        with self.project_env() as (home, cwd):
            with self.recovery_patches("101", [1000, 1100]) as send_text:
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))

            self.assertEqual(send_text.call_args_list[0].args, ("101", "continue\r"))
            self.assertEqual(send_text.call_args_list[1].args, ("101", "/model sonnet\r"))
            self.assertEqual(send_text.call_args_list[2].args, ("101", "continue\r"))

    def test_second_stop_failure_after_window_starts_new_continue_window(self):
        with self.project_env() as (home, cwd):
            with self.recovery_patches("101", [1000, 1701]) as send_text:
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))

            self.assertEqual(send_text.call_count, 2)
            self.assertEqual(send_text.call_args_list[0].args, ("101", "continue\r"))
            self.assertEqual(send_text.call_args_list[1].args, ("101", "continue\r"))

    def test_stop_restores_primary_model_after_fallback(self):
        with self.project_env() as (home, cwd):
            with self.recovery_patches("101", [1000, 1100, 1200]) as send_text:
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))
                run("Stop", {"cwd": cwd, "session_id": "s1"})

            self.assertEqual(send_text.call_args_list[3].args, ("101", "/model opus\r"))

    def test_model_switch_auto_sends_confirmation_when_prompt_visible(self):
        with self.project_env(
            {
                "features": {
                    "apiErrorRecovery": {
                        "enabled": True,
                        "sendDelayMs": 0,
                        "modelSwitchConfirmMode": "auto",
                        "modelSwitchConfirmCommand": "1",
                        "modelSwitchConfirmDelayMs": 0,
                        "postModelSwitchDelayMs": 0,
                    }
                }
            }
        ) as (home, cwd):
            pane_texts = [
                ("", ""),
                ("Switch model?\n1. Yes, switch to glm-5.2[1m]", ""),
                ("", ""),
                ("Switch model?\n1. Yes, switch to gpt-5.5[1m]", ""),
            ]
            with self.recovery_patches("101", [1000, 1100, 1200], pane_texts) as send_text:
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))
                run("Stop", {"cwd": cwd, "session_id": "s1"})

            self.assertEqual(send_text.call_args_list[1].args, ("101", "/model sonnet\r"))
            self.assertEqual(send_text.call_args_list[2].args, ("101", "1\r"))
            self.assertEqual(send_text.call_args_list[3].args, ("101", "continue\r"))
            self.assertEqual(send_text.call_args_list[4].args, ("101", "/model opus\r"))
            self.assertEqual(send_text.call_args_list[5].args, ("101", "1\r"))

    def test_model_switch_auto_skips_confirmation_without_prompt(self):
        with self.project_env(
            {
                "features": {
                    "apiErrorRecovery": {
                        "enabled": True,
                        "sendDelayMs": 0,
                        "modelSwitchConfirmMode": "auto",
                        "modelSwitchConfirmCommand": "1",
                        "modelSwitchConfirmDelayMs": 0,
                        "postModelSwitchDelayMs": 0,
                    }
                }
            }
        ) as (home, cwd):
            with self.recovery_patches("101", [1000, 1100]) as send_text:
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))

            self.assertEqual(send_text.call_args_list[1].args, ("101", "/model sonnet\r"))
            self.assertEqual(send_text.call_args_list[2].args, ("101", "continue\r"))
            self.assertEqual(send_text.call_count, 3)

    def test_model_switch_always_sends_confirmation(self):
        with self.project_env(
            {
                "features": {
                    "apiErrorRecovery": {
                        "enabled": True,
                        "sendDelayMs": 0,
                        "modelSwitchConfirmMode": "always",
                        "modelSwitchConfirmCommand": "1",
                        "modelSwitchConfirmDelayMs": 0,
                        "postModelSwitchDelayMs": 0,
                    }
                }
            }
        ) as (home, cwd):
            with self.recovery_patches("101", [1000, 1100]) as send_text:
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))

            self.assertEqual(send_text.call_args_list[1].args, ("101", "/model sonnet\r"))
            self.assertEqual(send_text.call_args_list[2].args, ("101", "1\r"))
            self.assertEqual(send_text.call_args_list[3].args, ("101", "continue\r"))

    def test_quick_second_stop_failure_switches_model(self):
        with self.project_env() as (home, cwd):
            with self.recovery_patches("101", [1000, 1002]) as send_text:
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))

            self.assertEqual(send_text.call_args_list[0].args, ("101", "continue\r"))
            self.assertEqual(send_text.call_args_list[1].args, ("101", "/model sonnet\r"))
            self.assertEqual(send_text.call_args_list[2].args, ("101", "continue\r"))

    def test_duplicate_same_action_is_deduped(self):
        with self.project_env({"features": {"apiErrorRecovery": {"enabled": True, "sendDelayMs": 0, "windowSeconds": 1, "dedupeSeconds": 5}}}) as (home, cwd):
            with self.recovery_patches("101", [1000, 1002]) as send_text:
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))

            send_text.assert_called_once_with("101", "continue\r")

    def test_fallback_active_stop_failure_after_window_keeps_restore_state(self):
        with self.project_env({"features": {"apiErrorRecovery": {"enabled": True, "sendDelayMs": 0, "windowSeconds": 100, "restoreAfterSeconds": 600}}}) as (home, cwd):
            with self.recovery_patches("101", [1000, 1010, 1120, 1130]) as send_text:
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))
                run("Stop", {"cwd": cwd, "session_id": "s1"})

            self.assertEqual(send_text.call_args_list[0].args, ("101", "continue\r"))
            self.assertEqual(send_text.call_args_list[1].args, ("101", "/model sonnet\r"))
            self.assertEqual(send_text.call_args_list[2].args, ("101", "continue\r"))
            self.assertEqual(send_text.call_args_list[3].args, ("101", "/model opus\r"))

    def test_expired_fallback_stop_failure_restores_and_continues(self):
        with self.project_env({"features": {"apiErrorRecovery": {"enabled": True, "sendDelayMs": 0, "windowSeconds": 100, "restoreAfterSeconds": 100}}}) as (home, cwd):
            with self.recovery_patches("101", [1000, 1010, 1120]) as send_text:
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))

            self.assertEqual(send_text.call_args_list[3].args, ("101", "/model opus\r"))
            self.assertEqual(send_text.call_args_list[4].args, ("101", "continue\r"))

    def test_stop_failure_event_disabled_skips_recovery(self):
        with self.project_env({"features": {"apiErrorRecovery": {"enabled": True, "sendDelayMs": 0}}, "events": {"StopFailure": {"enabled": False}}}) as (home, cwd):
            with self.recovery_patches("101", [1000]) as send_text:
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))

            send_text.assert_not_called()

    def test_multiple_sessions_and_panes_are_isolated(self):
        with self.project_env() as (home, cwd):
            with patch("core.api_error_recovery.send_text_to_wezterm", return_value="") as send_text, patch(
                "core.api_error_recovery.now_seconds", side_effect=[1000, 1000, 1100]
            ):
                with patch.dict(os.environ, {"WEZTERM_PANE": "101"}, clear=False):
                    run("StopFailure", self.stop_failure_payload(cwd, "session-a"))
                with patch.dict(os.environ, {"WEZTERM_PANE": "202"}, clear=False):
                    run("StopFailure", self.stop_failure_payload(cwd, "session-b"))
                with patch.dict(os.environ, {"WEZTERM_PANE": "101"}, clear=False):
                    run("StopFailure", self.stop_failure_payload(cwd, "session-a"))

            self.assertEqual(send_text.call_args_list[0].args, ("101", "continue\r"))
            self.assertEqual(send_text.call_args_list[1].args, ("202", "continue\r"))
            self.assertEqual(send_text.call_args_list[2].args, ("101", "/model sonnet\r"))
            self.assertEqual(send_text.call_args_list[3].args, ("101", "continue\r"))

    def test_missing_wezterm_pane_skips_recovery(self):
        with self.project_env() as (home, cwd):
            with patch.dict(os.environ, {"WEZTERM_PANE": ""}, clear=False), patch(
                "core.api_error_recovery.send_text_to_wezterm", return_value=""
            ) as send_text, patch("core.api_error_recovery.now_seconds", return_value=1000):
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))

            send_text.assert_not_called()

    def test_non_matching_error_skips_recovery(self):
        with self.project_env() as (home, cwd):
            with self.recovery_patches("101", [1000]) as send_text:
                run(
                    "StopFailure",
                    {
                        "cwd": cwd,
                        "session_id": "s1",
                        "error": "server_error",
                        "error_details": "temporary upstream failure",
                    },
                )

            send_text.assert_not_called()

    def test_session_scope_can_disable_recovery(self):
        with self.project_env(
            {
                "features": {
                    "apiErrorRecovery": {
                        "enabled": True,
                        "sendDelayMs": 0,
                        "scopes": {"sessions": {"disabled": ["s1"]}},
                    }
                }
            }
        ) as (home, cwd):
            with self.recovery_patches("101", [1000]) as send_text:
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))

            send_text.assert_not_called()

    def test_custom_match_text_can_trigger_recovery(self):
        with self.project_env(
            {
                "features": {
                    "apiErrorRecovery": {
                        "enabled": True,
                        "sendDelayMs": 0,
                        "match": ["upstream quota exceeded"],
                    }
                }
            }
        ) as (home, cwd):
            with self.recovery_patches("101", [1000]) as send_text:
                run(
                    "StopFailure",
                    {
                        "cwd": cwd,
                        "session_id": "s1",
                        "error": "invalid_request",
                        "error_details": "API Error: 400 upstream quota exceeded.",
                    },
                )

            send_text.assert_called_once_with("101", "continue\r")

    def test_confirm_prompt_from_baseline_is_ignored(self):
        baseline = "Switch model?\n1. Yes, switch to old-model"
        with self.project_env(
            {
                "features": {
                    "apiErrorRecovery": {
                        "enabled": True,
                        "sendDelayMs": 0,
                        "modelSwitchConfirmMode": "auto",
                        "modelSwitchConfirmCommand": "1",
                        "modelSwitchConfirmDelayMs": 0,
                        "postModelSwitchDelayMs": 0,
                    }
                }
            }
        ) as (home, cwd):
            with self.recovery_patches("101", [1000, 1100], [(baseline, ""), (baseline, "")]) as send_text:
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))

            self.assertEqual(send_text.call_args_list[1].args, ("101", "/model sonnet\r"))
            self.assertEqual(send_text.call_args_list[2].args, ("101", "continue\r"))
            self.assertEqual(send_text.call_count, 3)

    def test_shifted_stale_confirm_prompt_is_ignored(self):
        baseline = "line a\nSwitch model?\n1. Yes, switch to old-model\nline d"
        shifted = "Switch model?\n1. Yes, switch to old-model\nline d\n/model sonnet"
        with self.project_env(
            {
                "features": {
                    "apiErrorRecovery": {
                        "enabled": True,
                        "sendDelayMs": 0,
                        "modelSwitchConfirmMode": "auto",
                        "modelSwitchConfirmCommand": "1",
                        "modelSwitchConfirmDelayMs": 0,
                        "postModelSwitchDelayMs": 0,
                    }
                }
            }
        ) as (home, cwd):
            with self.recovery_patches("101", [1000, 1100], [(baseline, ""), (shifted, "")]) as send_text:
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))

            self.assertEqual(send_text.call_args_list[1].args, ("101", "/model sonnet\r"))
            self.assertEqual(send_text.call_args_list[2].args, ("101", "continue\r"))
            self.assertEqual(send_text.call_count, 3)

    def test_legacy_fallback_confirm_command_is_used_when_new_command_absent(self):
        with self.project_env(
            {
                "features": {
                    "apiErrorRecovery": {
                        "enabled": True,
                        "sendDelayMs": 0,
                        "modelSwitchConfirmMode": "auto",
                        "fallbackConfirmCommand": "y",
                        "modelSwitchConfirmDelayMs": 0,
                        "postModelSwitchDelayMs": 0,
                    }
                }
            }
        ) as (home, cwd):
            with self.recovery_patches("101", [1000, 1100], [("", ""), ("Switch model?\n1. Yes, switch to glm", "")]) as send_text:
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))

            self.assertEqual(send_text.call_args_list[1].args, ("101", "/model sonnet\r"))
            self.assertEqual(send_text.call_args_list[2].args, ("101", "y\r"))
            self.assertEqual(send_text.call_args_list[3].args, ("101", "continue\r"))

    def test_cwd_scope_can_enable_only_selected_directory(self):
        with self.project_env(
            {
                "features": {
                    "apiErrorRecovery": {
                        "enabled": True,
                        "sendDelayMs": 0,
                        "scopes": {"cwd": {"default": False, "enabled": []}},
                    }
                }
            }
        ) as (home, cwd):
            settings_path = os.path.join(home, ".claude", "hook-terr", "settings.json")
            with open(settings_path, "r", encoding="utf-8") as handle:
                settings = json.load(handle)
            settings["features"]["apiErrorRecovery"]["scopes"]["cwd"]["enabled"] = [cwd]
            with open(settings_path, "w", encoding="utf-8") as handle:
                json.dump(settings, handle)

            with self.recovery_patches("101", [1000]) as send_text:
                run("StopFailure", self.stop_failure_payload(cwd, "s1"))

            send_text.assert_called_once_with("101", "continue\r")

    def project_env(self, settings=None):
        return ProjectEnv(settings)

    def recovery_patches(self, pane_id, times, pane_texts=None):
        return RecoveryPatches(pane_id, times, pane_texts)

    def stop_failure_payload(self, cwd, session_id):
        return {
            "cwd": cwd,
            "session_id": session_id,
            "error": "invalid_request",
            "error_details": "API Error: 400 This content was flagged for possible cybersecurity risk.",
        }


class ProjectEnv:
    def __init__(self, settings=None):
        self.settings = settings

    def __enter__(self):
        self.temp = tempfile.TemporaryDirectory()
        self.home = self.temp.__enter__()
        self.patch = patch.dict(os.environ, {"USERPROFILE": self.home, "HOME": self.home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT})
        self.patch.__enter__()
        self.cwd = os.path.join(self.home, "project")
        os.makedirs(self.cwd)
        config_dir = os.path.join(self.home, ".claude", "hook-terr")
        os.makedirs(config_dir)
        settings = self.settings or {
            "features": {
                "apiErrorRecovery": {
                    "enabled": True,
                    "sendDelayMs": 0,
                    "windowSeconds": 600,
                    "restoreAfterSeconds": 600,
                    "dedupeSeconds": 5,
                    "primaryModelCommand": "/model opus",
                    "fallbackModelCommand": "/model sonnet",
                    "continueCommand": "continue",
                    "modelSwitchConfirmDelayMs": 0,
                    "postModelSwitchDelayMs": 0,
                }
            }
        }
        with open(os.path.join(config_dir, "settings.json"), "w", encoding="utf-8") as handle:
            json.dump(settings, handle)
        return self.home, self.cwd

    def __exit__(self, exc_type, exc, tb):
        self.patch.__exit__(exc_type, exc, tb)
        self.temp.__exit__(exc_type, exc, tb)


class RecoveryPatches:
    def __init__(self, pane_id, times, pane_texts=None):
        self.pane_id = pane_id
        self.times = times
        self.pane_texts = pane_texts or []

    def __enter__(self):
        self.env_patch = patch.dict(os.environ, {"WEZTERM_PANE": self.pane_id}, clear=False)
        self.send_patch = patch("core.api_error_recovery.send_text_to_wezterm", return_value="")
        self.get_text_patch = patch("core.api_error_recovery.get_wezterm_pane_text", side_effect=self.pane_text)
        self.time_patch = patch("core.api_error_recovery.now_seconds", side_effect=self.times)
        self.env_patch.__enter__()
        self.send_text = self.send_patch.__enter__()
        self.get_text_patch.__enter__()
        self.time_patch.__enter__()
        return self.send_text

    def pane_text(self, pane_id, scan_lines):
        if self.pane_texts:
            return self.pane_texts.pop(0)
        return "", ""

    def __exit__(self, exc_type, exc, tb):
        self.time_patch.__exit__(exc_type, exc, tb)
        self.get_text_patch.__exit__(exc_type, exc, tb)
        self.send_patch.__exit__(exc_type, exc, tb)
        self.env_patch.__exit__(exc_type, exc, tb)


if __name__ == "__main__":
    unittest.main()
