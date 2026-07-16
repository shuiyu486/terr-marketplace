import os
import sys
import unittest
from unittest.mock import patch

PLUGIN_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PLUGIN_ROOT not in sys.path:
    sys.path.insert(0, PLUGIN_ROOT)

from core.models import HookContext
from notifiers import windows_toast


class WindowsToastTests(unittest.TestCase):
    def test_silent_toast_includes_audio_suppression_and_skips_balloon(self):
        with patch("notifiers.windows_toast.platform.system", return_value="Windows"), patch(
            "notifiers.windows_toast.popen_hidden"
        ) as popen_hidden:
            windows_toast.send("title", "message", HookContext("Stop"), {"silent": True})

        script = popen_hidden.call_args.args[0]
        self.assertIn('<audio silent="true"/>', script)
        self.assertIn("if ($winrtShown -or $silent)", script)
        self.assertIn("$silent = $true", script)

    def test_non_silent_toast_uses_notify_icon_only_as_fallback(self):
        with patch("notifiers.windows_toast.platform.system", return_value="Windows"), patch(
            "notifiers.windows_toast.popen_hidden"
        ) as popen_hidden:
            windows_toast.send("title", "message", HookContext("Stop"), {"silent": False})

        script = popen_hidden.call_args.args[0]
        self.assertNotIn('<audio silent="true"/>', script)
        self.assertIn("$winrtShown = $true", script)
        self.assertIn("if ($winrtShown -or $silent)", script)
        self.assertIn("$silent = $false", script)
        self.assertLess(script.index("if ($winrtShown -or $silent)"), script.index("$notify.ShowBalloonTip"))

    def test_launcher_uses_absolute_powershell_without_cmd(self):
        process = None
        with patch("notifiers.windows_toast.write_temp_script", return_value=r"C:\Temp&cache\toast.ps1"), patch(
            "notifiers.windows_toast.powershell_executable",
            return_value=r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
        ), patch("notifiers.windows_toast.subprocess.Popen") as popen:
            windows_toast.popen_hidden("script")
            process = popen.call_args

        args, kwargs = process.args[0], process.kwargs
        self.assertEqual(args[0], r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe")
        self.assertNotIn("cmd.exe", args)
        self.assertEqual(args[-1], r"C:\Temp&cache\toast.ps1")
        self.assertTrue(kwargs["close_fds"])


if __name__ == "__main__":
    unittest.main()
