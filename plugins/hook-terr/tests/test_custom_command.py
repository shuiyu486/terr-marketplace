import os
import sys
import unittest
from unittest.mock import patch

PLUGIN_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PLUGIN_ROOT not in sys.path:
    sys.path.insert(0, PLUGIN_ROOT)

from core.models import HookContext
from core.schema import validate_settings
from notifiers import custom_command


class CustomCommandTests(unittest.TestCase):
    def test_windows_command_receives_template_values_as_environment(self):
        calls = []

        class FakeProcess:
            def wait(self, timeout=None):
                return 0

        def fake_popen(args, **kwargs):
            calls.append((args, kwargs))
            return FakeProcess()

        message = "hello'); Start-Process calc; #'"
        context = HookContext("Stop", cwd=r"C:\project")
        with patch("platform.system", return_value="Windows"), patch("subprocess.Popen", side_effect=fake_popen):
            custom_command.send("title'", message, context, {"command": "Write-Host $env:HOOK_TERR_MESSAGE", "detached": False})

        args, kwargs = calls[0]
        self.assertEqual(args[-1], "Write-Host $env:HOOK_TERR_MESSAGE")
        self.assertEqual(kwargs["env"]["HOOK_TERR_MESSAGE"], message)
        self.assertEqual(kwargs["env"]["HOOK_TERR_TITLE"], "title'")
        self.assertEqual(kwargs["env"]["HOOK_TERR_CWD"], r"C:\project")
        self.assertEqual(kwargs["env"]["HOOK_TERR_EVENT"], "Stop")
        self.assertIn("HOOK_TERR_TIMESTAMP", kwargs["env"])
        self.assertNotIn(message, args[-1])
        self.assertEqual(kwargs["stdin"], custom_command.subprocess.DEVNULL)
        self.assertEqual(kwargs["stdout"], custom_command.subprocess.DEVNULL)
        self.assertEqual(kwargs["stderr"], custom_command.subprocess.DEVNULL)

    def test_legacy_template_rendering_is_removed(self):
        calls = []

        class FakeProcess:
            def wait(self, timeout=None):
                return 0

        def fake_popen(args, **kwargs):
            calls.append((args, kwargs))
            return FakeProcess()

        context = HookContext("Stop", cwd=r"C:\project")
        with patch("platform.system", return_value="Windows"), patch("subprocess.Popen", side_effect=fake_popen):
            custom_command.send("title", "message", context, {"command": "Write-Host '{{message}}'", "detached": True})

        args, kwargs = calls[0]
        self.assertEqual(args[-1], "Write-Host '{{message}}'")
        self.assertNotIn("message", args[-1].replace("{{message}}", ""))
        self.assertEqual(kwargs["env"]["HOOK_TERR_MESSAGE"], "message")

    def test_non_windows_keeps_shell_true_and_does_not_render_templates(self):
        calls = []

        class FakeProcess:
            def wait(self, timeout=None):
                return 0

        def fake_popen(args, **kwargs):
            calls.append((args, kwargs))
            return FakeProcess()

        context = HookContext("Stop", cwd="/project")
        with patch("platform.system", return_value="Linux"), patch("subprocess.Popen", side_effect=fake_popen):
            custom_command.send("title", "message", context, {"command": "notify-send '{{message}}'", "detached": True})

        command, kwargs = calls[0]
        self.assertEqual(command, "notify-send '{{message}}'")
        self.assertTrue(kwargs["shell"])
        self.assertEqual(kwargs["env"]["HOOK_TERR_MESSAGE"], "message")
        self.assertEqual(kwargs["stdin"], custom_command.subprocess.DEVNULL)
        self.assertEqual(kwargs["stdout"], custom_command.subprocess.DEVNULL)
        self.assertEqual(kwargs["stderr"], custom_command.subprocess.DEVNULL)

    def test_validate_settings_rejects_legacy_custom_command_templates(self):
        for token in ("{{event}}", "{{title}}", "{{message}}", "{{cwd}}", "{{timestamp}}"):
            with self.subTest(token=token):
                errors = validate_settings({"notifications": {"custom_command": {"command": "Write-Host " + token}}})

                self.assertEqual(len(errors), 1)
                self.assertIn("settings.notifications.custom_command.command", errors[0])
                self.assertIn(token, errors[0])
                self.assertIn("HOOK_TERR_MESSAGE", errors[0])

    def test_validate_settings_accepts_hook_terr_environment_variables(self):
        errors = validate_settings({"notifications": {"custom_command": {"command": "Write-Host $env:HOOK_TERR_MESSAGE"}}})

        self.assertEqual(errors, [])

    def test_validate_settings_checks_custom_command_field_types(self):
        errors = validate_settings({"notifications": {"custom_command": {"command": 123, "timeoutMs": "fast", "detached": "yes"}}})

        self.assertIn("settings.notifications.custom_command.command must be a string", errors)
        self.assertIn("settings.notifications.custom_command.timeoutMs must be a number", errors)
        self.assertIn("settings.notifications.custom_command.detached must be a boolean", errors)

    def test_validate_settings_event_notifications_must_contain_strings(self):
        errors = validate_settings({"events": {"Stop": {"notifications": [[]]}}})

        self.assertIn("settings.events.Stop.notifications must contain only strings", errors)


if __name__ == "__main__":
    unittest.main()
