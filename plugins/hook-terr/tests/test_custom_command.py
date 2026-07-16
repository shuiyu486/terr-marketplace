import os
import sys
import unittest
from subprocess import TimeoutExpired
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
        with patch("platform.system", return_value="Windows"), patch("notifiers.custom_command.powershell_executable", return_value=r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"), patch("subprocess.Popen", side_effect=fake_popen):
            custom_command.send("title'", message, context, {"command": "Write-Host $env:HOOK_TERR_MESSAGE", "detached": False})

        args, kwargs = calls[0]
        self.assertEqual(args[0], r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe")
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
        with patch("platform.system", return_value="Windows"), patch("notifiers.custom_command.powershell_executable", return_value=r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"), patch("subprocess.Popen", side_effect=fake_popen):
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

    def test_non_windows_detached_starts_new_session(self):
        calls = []

        def fake_popen(args, **kwargs):
            calls.append((args, kwargs))
            return object()

        with patch("platform.system", return_value="Linux"), patch("subprocess.Popen", side_effect=fake_popen):
            custom_command.send("title", "message", HookContext("Stop"), {"command": "notify-send hello", "detached": True})

        self.assertTrue(calls[0][1]["start_new_session"])

    def test_attached_nonzero_exit_raises(self):
        class FakeProcess:
            def wait(self, timeout=None):
                return 7

        with patch("platform.system", return_value="Linux"), patch("subprocess.Popen", return_value=FakeProcess()):
            with self.assertRaisesRegex(RuntimeError, "exited with code 7"):
                custom_command.send("title", "message", HookContext("Stop"), {"command": "false", "detached": False})

    def test_attached_timeout_kills_and_reaps_process_group(self):
        class FakeProcess:
            pid = 123

            def __init__(self):
                self.wait_calls = 0

            def wait(self, timeout=None):
                self.wait_calls += 1
                if self.wait_calls == 1:
                    raise TimeoutExpired("command", timeout)
                return -9

        process = FakeProcess()
        with patch("platform.system", return_value="Linux"), patch("subprocess.Popen", return_value=process), patch(
            "notifiers.custom_command.kill_process_group"
        ) as kill_process_group:
            with self.assertRaisesRegex(RuntimeError, "timed out"):
                custom_command.send("title", "message", HookContext("Stop"), {"command": "sleep 10", "detached": False, "timeoutMs": 1})

        kill_process_group.assert_called_once_with(123)
        self.assertEqual(process.wait_calls, 2)

    def test_windows_attached_timeout_kills_process_tree(self):
        class FakeProcess:
            pid = 456

            def __init__(self):
                self.wait_calls = 0

            def wait(self, timeout=None):
                self.wait_calls += 1
                if self.wait_calls == 1:
                    raise TimeoutExpired("command", timeout)
                return 1

        process = FakeProcess()
        with patch("platform.system", return_value="Windows"), patch(
            "notifiers.custom_command.powershell_executable",
            return_value=r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
        ), patch("subprocess.Popen", return_value=process), patch(
            "notifiers.custom_command.kill_windows_process_tree"
        ) as kill_tree:
            with self.assertRaisesRegex(RuntimeError, "timed out"):
                custom_command.send("title", "message", HookContext("Stop"), {"command": "Start-Process child", "detached": False, "timeoutMs": 1})

        kill_tree.assert_called_once_with(process)
        self.assertEqual(process.wait_calls, 2)

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
        non_positive_errors = validate_settings({"notifications": {"custom_command": {"timeoutMs": 0}}})

        self.assertIn("settings.notifications.custom_command.command must be a string", errors)
        self.assertIn("settings.notifications.custom_command.timeoutMs must be a number", errors)
        self.assertIn("settings.notifications.custom_command.detached must be a boolean", errors)
        self.assertIn("settings.notifications.custom_command.timeoutMs must be positive", non_positive_errors)

    def test_validate_settings_event_notifications_must_contain_strings(self):
        errors = validate_settings({"events": {"Stop": {"notifications": [[]]}}})

        self.assertIn("settings.events.Stop.notifications must contain only strings", errors)


if __name__ == "__main__":
    unittest.main()
