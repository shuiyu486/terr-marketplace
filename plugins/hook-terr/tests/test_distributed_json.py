import glob
import json
import os
import sys
import unittest

PLUGIN_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PLUGIN_ROOT not in sys.path:
    sys.path.insert(0, PLUGIN_ROOT)

from core.schema import validate_rule, validate_settings


class DistributedJsonTests(unittest.TestCase):
    def test_default_settings_json_is_valid(self):
        path = os.path.join(PLUGIN_ROOT, "defaults", "settings.json")

        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)

        self.assertEqual(validate_settings(data), [])

    def test_default_rules_json_is_valid(self):
        for path in glob.glob(os.path.join(PLUGIN_ROOT, "defaults", "rules", "*.json")):
            with self.subTest(path=path):
                with open(path, "r", encoding="utf-8") as handle:
                    data = json.load(handle)

                self.assertEqual(validate_rule(data, path), [])

    def test_python_hooks_use_exec_form(self):
        path = os.path.join(PLUGIN_ROOT, "hooks", "hooks.json")

        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)

        for event_name, matchers in data.get("hooks", {}).items():
            for matcher in matchers:
                for hook in matcher.get("hooks", []):
                    if hook.get("type") != "command":
                        continue
                    with self.subTest(event=event_name, hook=hook.get("args")):
                        self.assertEqual(hook.get("command"), "python3")
                        self.assertIn("args", hook)
                        self.assertEqual(len(hook["args"]), 1)
                        self.assertTrue(hook["args"][0].startswith("${CLAUDE_PLUGIN_ROOT}/hooks/"))
                        self.assertTrue(hook["args"][0].endswith(".py"))

    def test_presets_json_is_valid(self):
        for path in glob.glob(os.path.join(PLUGIN_ROOT, "presets", "*.json")):
            with self.subTest(path=path):
                with open(path, "r", encoding="utf-8") as handle:
                    data = json.load(handle)

                settings = data.get("settings") if isinstance(data, dict) else None
                if settings is not None:
                    self.assertEqual(validate_settings(settings), [])

    def test_custom_command_sample_uses_environment_variables(self):
        path = os.path.join(PLUGIN_ROOT, "presets", "custom-command.sample.json")
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)

        command = data["settings"]["notifications"]["custom_command"]["command"]
        self.assertIn("$env:HOOK_TERR_MESSAGE", command)
        self.assertIn("$env:HOOK_TERR_TITLE", command)
        self.assertNotIn("{{", command)


if __name__ == "__main__":
    unittest.main()
