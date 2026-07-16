import os
import sys
import tempfile
import unittest
from unittest.mock import patch

PLUGIN_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PLUGIN_ROOT not in sys.path:
    sys.path.insert(0, PLUGIN_ROOT)

from core.config_status import api_error_recovery_status, build_status


class ConfigStatusTests(unittest.TestCase):
    def test_build_status_reports_loaded_plugin_version_and_root(self):
        with self.env() as cwd:
            status = build_status(cwd)

            self.assertEqual(status["pluginVersion"], "1.4.5")
            self.assertEqual(os.path.normcase(status["pluginRoot"]), os.path.normcase(PLUGIN_ROOT))

    def test_api_error_recovery_status_reports_recovery_mode_label(self):
        with self.env() as cwd:
            settings = {
                "features": {
                    "apiErrorRecovery": {
                        "enabled": True,
                        "recoveryMode": "continue_only",
                    }
                }
            }

            status = api_error_recovery_status(settings, cwd)

            self.assertTrue(status["enabled"])
            self.assertTrue(status["effectiveForCwd"])
            self.assertEqual(status["recoveryMode"], "continue_only")
            self.assertEqual(status["recoveryModeLabel"], "只 continue")

    def test_api_error_recovery_status_reports_cwd_disabled_prefix(self):
        with self.env() as cwd:
            parent = os.path.dirname(cwd)
            settings = {
                "features": {
                    "apiErrorRecovery": {
                        "enabled": True,
                        "scopes": {
                            "cwd": {
                                "default": True,
                                "disabledPrefixes": [parent],
                            }
                        },
                    }
                }
            }

            status = api_error_recovery_status(settings, cwd)

            self.assertTrue(status["enabled"])
            self.assertFalse(status["effectiveForCwd"])
            self.assertFalse(status["cwdScope"]["effective"])
            self.assertEqual(status["cwdScope"]["matchedBy"], "disabledPrefixes")
            self.assertEqual(status["cwdScope"]["matchedValue"], parent)

    def env(self):
        return TempEnv()


class TempEnv:
    def __enter__(self):
        self.temp = tempfile.TemporaryDirectory()
        self.home = self.temp.__enter__()
        self.patch = patch.dict(os.environ, {"USERPROFILE": self.home, "HOME": self.home})
        self.patch.__enter__()
        self.cwd = os.path.join(self.home, "project")
        os.makedirs(self.cwd)
        return self.cwd

    def __exit__(self, exc_type, exc, tb):
        self.patch.__exit__(exc_type, exc, tb)
        self.temp.__exit__(exc_type, exc, tb)


if __name__ == "__main__":
    unittest.main()
