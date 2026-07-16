import os
import sys
import unittest
from unittest.mock import patch

PLUGIN_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PLUGIN_ROOT not in sys.path:
    sys.path.insert(0, PLUGIN_ROOT)

from core.models import HookContext
from notifiers import popup


class PopupNotifierTests(unittest.TestCase):
    def test_rule_title_takes_precedence_over_popup_config_title(self):
        with patch("notifiers.popup.platform.system", return_value="Windows"), patch("notifiers.popup.powershell_executable", return_value=r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"), patch("notifiers.popup.subprocess.Popen") as popen:
            popup.send("Rule Title", "message", HookContext("Stop"), {"title": "Config Title", "icon": "info"})

        args = popen.call_args.args[0]
        command = args[-1]
        self.assertEqual(args[0], r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe")
        self.assertIn("'Rule Title'", command)
        self.assertNotIn("'Config Title'", command)

    def test_popup_config_title_is_fallback(self):
        with patch("notifiers.popup.platform.system", return_value="Windows"), patch("notifiers.popup.powershell_executable", return_value=r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"), patch("notifiers.popup.subprocess.Popen") as popen:
            popup.send("", "message", HookContext("Stop"), {"title": "Config Title", "icon": "info"})

        command = popen.call_args.args[0][-1]
        self.assertIn("'Config Title'", command)


if __name__ == "__main__":
    unittest.main()
