import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

PLUGIN_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PLUGIN_ROOT not in sys.path:
    sys.path.insert(0, PLUGIN_ROOT)

from core.settings_writer import write_api_error_recovery


class SettingsWriterTests(unittest.TestCase):
    def test_project_api_error_recovery_enable(self):
        with self.env() as (home, cwd):
            path = write_api_error_recovery("project", cwd, "project", "/model opus", "/model sonnet", True)

            self.assertEqual(path, os.path.join(cwd, ".claude", "hook-terr", "settings.json"))
            settings = self.read_json(path)
            recovery = settings["features"]["apiErrorRecovery"]
            self.assertTrue(recovery["enabled"])
            self.assertEqual(recovery["primaryModelCommand"], "/model opus")
            self.assertEqual(recovery["fallbackModelCommand"], "/model sonnet")
            self.assertEqual(recovery["modelSwitchConfirmMode"], "auto")
            self.assertEqual(recovery["modelSwitchConfirmCommand"], "1")
            self.assertEqual(recovery["primaryConfirmCommand"], "1")
            self.assertEqual(recovery["fallbackConfirmCommand"], "1")
            self.assertEqual(
                recovery["match"],
                ["This content was flagged for possible cybersecurity risk", "cybersecurity risk"],
            )

    def test_global_current_dir_appends_enabled_prefix_once(self):
        with self.env() as (home, cwd):
            path = write_api_error_recovery("global", cwd, "global-current-dir", "/model opus", "/model sonnet", False)
            write_api_error_recovery("global", cwd, "global-current-dir", "/model opus", "/model sonnet", False)

            settings = self.read_json(path)
            cwd_scope = settings["features"]["apiErrorRecovery"]["scopes"]["cwd"]
            self.assertFalse(cwd_scope["default"])
            self.assertEqual(cwd_scope["enabledPrefixes"], [cwd])
            self.assertEqual(settings["features"]["apiErrorRecovery"]["fallbackConfirmCommand"], "")
            self.assertEqual(settings["features"]["apiErrorRecovery"]["modelSwitchConfirmMode"], "auto")

    def test_api_error_recovery_writes_custom_match_texts(self):
        with self.env() as (home, cwd):
            path = write_api_error_recovery(
                "project",
                cwd,
                "project",
                "/model opus",
                "/model sonnet",
                False,
                ["cybersecurity risk", "API Error: 400", "cybersecurity risk"],
            )

            recovery = self.read_json(path)["features"]["apiErrorRecovery"]
            self.assertEqual(recovery["match"], ["cybersecurity risk", "API Error: 400"])
            self.assertEqual(recovery["modelSwitchConfirmMode"], "auto")
            self.assertEqual(recovery["modelSwitchConfirmCommand"], "1")

    def test_api_error_recovery_writes_confirm_mode_override(self):
        with self.env() as (home, cwd):
            path = write_api_error_recovery(
                "project",
                cwd,
                "project",
                "/model opus",
                "/model sonnet",
                False,
                None,
                "never",
            )

            recovery = self.read_json(path)["features"]["apiErrorRecovery"]
            self.assertEqual(recovery["modelSwitchConfirmMode"], "never")

    def test_global_current_dir_removes_conflicting_disabled_prefix(self):
        with self.env() as (home, cwd):
            path = write_api_error_recovery("global", cwd, "disable-current-dir", "/model opus", "/model sonnet", True)
            write_api_error_recovery("global", cwd, "global-current-dir", "/model opus", "/model sonnet", True)

            cwd_scope = self.read_json(path)["features"]["apiErrorRecovery"]["scopes"]["cwd"]
            self.assertEqual(cwd_scope.get("disabledPrefixes"), [])
            self.assertEqual(cwd_scope.get("enabledPrefixes"), [cwd])

    def test_global_current_dir_removes_disabled_parent_prefix(self):
        with self.env() as (home, cwd):
            path = write_api_error_recovery("global", home, "disable-current-dir", "/model opus", "/model sonnet", True)
            write_api_error_recovery("global", cwd, "global-current-dir", "/model opus", "/model sonnet", True)

            cwd_scope = self.read_json(path)["features"]["apiErrorRecovery"]["scopes"]["cwd"]
            self.assertEqual(cwd_scope.get("disabledPrefixes"), [])
            self.assertEqual(cwd_scope.get("enabledPrefixes"), [cwd])

    def test_global_default_sets_cwd_default_true(self):
        with self.env() as (home, cwd):
            path = write_api_error_recovery("global", cwd, "global-default", "/model opus", "/model sonnet", True)

            settings = self.read_json(path)
            self.assertTrue(settings["features"]["apiErrorRecovery"]["scopes"]["cwd"]["default"])

    def test_disable_current_dir_global_appends_disabled_prefix(self):
        with self.env() as (home, cwd):
            path = write_api_error_recovery("global", cwd, "disable-current-dir", "/model opus", "/model sonnet", True)

            settings = self.read_json(path)
            self.assertEqual(settings["features"]["apiErrorRecovery"]["scopes"]["cwd"]["disabledPrefixes"], [cwd])

    def test_disable_current_dir_project_sets_enabled_false(self):
        with self.env() as (home, cwd):
            path = write_api_error_recovery("project", cwd, "disable-current-dir", "/model opus", "/model sonnet", True)

            settings = self.read_json(path)
            self.assertFalse(settings["features"]["apiErrorRecovery"]["enabled"])

    def test_project_enable_overrides_inherited_cwd_default_false(self):
        with self.env() as (home, cwd):
            path = write_api_error_recovery("project", cwd, "project", "/model opus", "/model sonnet", True)

            cwd_scope = self.read_json(path)["features"]["apiErrorRecovery"]["scopes"]["cwd"]
            self.assertTrue(cwd_scope["default"])
            self.assertEqual(cwd_scope["disabled"], [])
            self.assertEqual(cwd_scope["disabledPrefixes"], [])

    def test_disable_current_dir_removes_enabled_prefix(self):
        with self.env() as (home, cwd):
            path = write_api_error_recovery("global", cwd, "global-current-dir", "/model opus", "/model sonnet", True)
            write_api_error_recovery("global", cwd, "disable-current-dir", "/model opus", "/model sonnet", True)

            cwd_scope = self.read_json(path)["features"]["apiErrorRecovery"]["scopes"]["cwd"]
            self.assertEqual(cwd_scope.get("enabledPrefixes"), [])
            self.assertEqual(cwd_scope.get("disabledPrefixes"), [cwd])

    def env(self):
        return TempEnv()

    def read_json(self, path):
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)


class TempEnv:
    def __enter__(self):
        self.temp = tempfile.TemporaryDirectory()
        self.home = self.temp.__enter__()
        self.patch = patch.dict(os.environ, {"USERPROFILE": self.home, "HOME": self.home})
        self.patch.__enter__()
        self.cwd = os.path.join(self.home, "project")
        os.makedirs(self.cwd)
        return self.home, self.cwd

    def __exit__(self, exc_type, exc, tb):
        self.patch.__exit__(exc_type, exc, tb)
        self.temp.__exit__(exc_type, exc, tb)


if __name__ == "__main__":
    unittest.main()
