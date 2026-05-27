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
