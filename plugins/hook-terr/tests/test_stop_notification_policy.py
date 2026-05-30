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
from core.models import NotificationResult


class StopNotificationPolicyTests(unittest.TestCase):
    def test_default_stop_rule_warns_without_external_notification(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            os.makedirs(cwd)

            with patch("core.action_executor.send_notification") as send_notification:
                response = run("Stop", {"cwd": cwd, "transcript_path": os.path.join(home, "transcript.jsonl")})

            self.assertIn("systemMessage", response)
            self.assertIn("准备结束本轮回复前", response["systemMessage"])
            send_notification.assert_not_called()

    def test_default_stop_rule_ignores_subagent_transcript_path(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            os.makedirs(cwd)
            transcript_path = os.path.join(home, "session", "subagents", "agent.jsonl")

            with patch("core.action_executor.send_notification") as send_notification:
                response = run("Stop", {"cwd": cwd, "transcript_path": transcript_path})

            self.assertEqual(response, {})
            send_notification.assert_not_called()

    def test_user_rule_can_match_subagent_stop_by_is_subagent(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            rules_dir = os.path.join(home, ".claude", "hook-terr", "rules")
            os.makedirs(rules_dir)
            os.makedirs(cwd)
            with open(os.path.join(rules_dir, "subagent.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "version": 1,
                        "id": "subagent",
                        "enabled": True,
                        "event": "Stop",
                        "priority": 200,
                        "decision": "warn",
                        "when": [{"field": "is_subagent", "op": "equals", "value": True}],
                        "message": {"text": "subagent stop"},
                        "notify": {"enabled": False},
                    },
                    handle,
                )
            transcript_path = os.path.join(home, "session", "subagents", "agent.jsonl")

            response = run("Stop", {"cwd": cwd, "transcript_path": transcript_path})

            self.assertEqual(response, {"systemMessage": "subagent stop"})

    def test_user_rule_can_match_subagent_stop_by_agent_type(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            rules_dir = os.path.join(home, ".claude", "hook-terr", "rules")
            os.makedirs(rules_dir)
            os.makedirs(cwd)
            with open(os.path.join(rules_dir, "agent-type.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "version": 1,
                        "id": "agent-type",
                        "enabled": True,
                        "event": "Stop",
                        "priority": 200,
                        "decision": "warn",
                        "when": [{"field": "agent_type", "op": "equals", "value": "subagent"}],
                        "message": {"text": "subagent type"},
                        "notify": {"enabled": False},
                    },
                    handle,
                )
            transcript_path = os.path.join(home, "session", "subagents", "agent.jsonl")

            response = run("Stop", {"cwd": cwd, "transcript_path": transcript_path})

            self.assertEqual(response, {"systemMessage": "subagent type"})

    def test_legacy_custom_command_template_settings_are_rejected(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            config_dir = os.path.join(home, ".claude", "hook-terr")
            os.makedirs(config_dir)
            os.makedirs(cwd)
            with open(os.path.join(config_dir, "settings.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "notifications": {
                            "custom_command": {
                                "enabled": True,
                                "command": "Write-Host '{{message}}'",
                            }
                        },
                        "events": {"Stop": {"notifications": ["custom_command"]}},
                    },
                    handle,
                )

            with patch("core.action_executor.send_notification") as send_notification:
                response = run("Stop", {"cwd": cwd})

            self.assertIn("systemMessage", response)
            self.assertIn("custom_command.command", response["systemMessage"])
            self.assertIn("removed legacy template", response["systemMessage"])
            send_notification.assert_not_called()

    def test_explicit_empty_notify_channels_does_not_add_diagnostic(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            rules_dir = os.path.join(home, ".claude", "hook-terr", "rules")
            os.makedirs(rules_dir)
            os.makedirs(cwd)
            with open(os.path.join(rules_dir, "empty-channels.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "version": 1,
                        "id": "empty-channels",
                        "enabled": True,
                        "event": "Stop",
                        "priority": 200,
                        "decision": "warn",
                        "when": [],
                        "message": {"text": "empty channels"},
                        "notify": {"enabled": True, "channels": []},
                    },
                    handle,
                )

            with patch("core.action_executor.send_notification") as send_notification:
                response = run("Stop", {"cwd": cwd})

            self.assertEqual(response, {"systemMessage": "empty channels"})
            send_notification.assert_not_called()

    def test_notify_without_rule_channels_uses_event_channels(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            config_dir = os.path.join(home, ".claude", "hook-terr")
            rules_dir = os.path.join(home, ".claude", "hook-terr", "rules")
            os.makedirs(config_dir)
            os.makedirs(rules_dir)
            os.makedirs(cwd)
            with open(os.path.join(config_dir, "settings.json"), "w", encoding="utf-8") as handle:
                json.dump({"events": {"Stop": {"notifications": ["sound"]}}}, handle)
            with open(os.path.join(rules_dir, "event-channels.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "version": 1,
                        "id": "event-channels",
                        "enabled": True,
                        "event": "Stop",
                        "priority": 200,
                        "decision": "warn",
                        "when": [],
                        "message": {"text": "event channels"},
                        "notify": {"enabled": True, "title": "title", "text": "text"},
                    },
                    handle,
                )

            with patch("core.action_executor.send_notification", return_value=NotificationResult("sound", True)) as send_notification:
                response = run("Stop", {"cwd": cwd})

            self.assertEqual(response, {"systemMessage": "event channels"})
            send_notification.assert_called_once()
            self.assertEqual(send_notification.call_args.args[0], "sound")

    def test_explicit_stop_notify_rule_still_sends_notification(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            rules_dir = os.path.join(home, ".claude", "hook-terr", "rules")
            os.makedirs(rules_dir)
            os.makedirs(cwd)
            with open(os.path.join(rules_dir, "always-notify.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "version": 1,
                        "id": "always-notify",
                        "enabled": True,
                        "event": "Stop",
                        "priority": 200,
                        "decision": "warn",
                        "when": [],
                        "message": {"text": "explicit notify"},
                        "notify": {"enabled": True, "channels": ["sound"], "title": "title", "text": "text"},
                    },
                    handle,
                )

            with patch("core.action_executor.send_notification", return_value=NotificationResult("sound", True)) as send_notification:
                response = run("Stop", {"cwd": cwd})

            self.assertEqual(response, {"systemMessage": "explicit notify"})
            send_notification.assert_called_once()


if __name__ == "__main__":
    unittest.main()
