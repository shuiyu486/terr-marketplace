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


if __name__ == "__main__":
    unittest.main()
