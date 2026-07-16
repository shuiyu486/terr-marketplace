import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

PLUGIN_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PLUGIN_ROOT not in sys.path:
    sys.path.insert(0, PLUGIN_ROOT)

from core.api_error_recovery import state_root
from core.config_loader import load_configuration, rule_paths, settings_paths
from core.documentation_reminder import state_dir
from core.settings_writer import settings_path, write_stop_channels


class ConfigPathTests(unittest.TestCase):
    def test_custom_claude_config_dir_is_used_consistently(self):
        with tempfile.TemporaryDirectory() as home, tempfile.TemporaryDirectory() as config_dir, patch.dict(
            os.environ,
            {
                "HOME": home,
                "USERPROFILE": home,
                "CLAUDE_CONFIG_DIR": config_dir,
                "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT,
            },
        ):
            cwd = os.path.join(home, "project")
            os.makedirs(cwd)
            global_dir = os.path.join(config_dir, "hook-terr")
            os.makedirs(global_dir)
            with open(os.path.join(global_dir, "settings.json"), "w", encoding="utf-8") as handle:
                json.dump({"enabled": False}, handle)
            rules_dir = os.path.join(global_dir, "rules")
            os.makedirs(rules_dir)
            global_rule = os.path.join(rules_dir, "custom.json")
            with open(global_rule, "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "id": "custom",
                        "event": "Stop",
                        "enabled": False,
                        "decision": "allow",
                        "when": [],
                    },
                    handle,
                )

            settings, _, diagnostics = load_configuration(cwd)
            written_path = write_stop_channels("global", cwd, ["sound"])

            self.assertFalse(settings["enabled"])
            self.assertEqual(diagnostics, [])
            self.assertEqual(settings_path("global", cwd), os.path.join(global_dir, "settings.json"))
            self.assertEqual(written_path, os.path.join(global_dir, "settings.json"))
            self.assertEqual(state_root(), os.path.join(global_dir, "state", "api-error-recovery"))
            self.assertEqual(state_dir(), os.path.join(global_dir, "state", "documentation-reminder"))
            self.assertIn(os.path.join(global_dir, "settings.json"), settings_paths(PLUGIN_ROOT, cwd))
            self.assertIn(global_rule, rule_paths(PLUGIN_ROOT, cwd))


if __name__ == "__main__":
    unittest.main()
