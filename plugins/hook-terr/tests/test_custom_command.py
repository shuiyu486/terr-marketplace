import os
import sys
import unittest
from unittest.mock import patch

PLUGIN_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PLUGIN_ROOT not in sys.path:
    sys.path.insert(0, PLUGIN_ROOT)

from core.models import HookContext
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
        self.assertNotIn(message, args[-1])

    def test_legacy_template_rendering_is_preserved(self):
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

        args, _ = calls[0]
        self.assertEqual(args[-1], "Write-Host 'message'")


if __name__ == "__main__":
    unittest.main()
