import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

PLUGIN_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PLUGIN_ROOT not in sys.path:
    sys.path.insert(0, PLUGIN_ROOT)

from core.models import HookContext
from core.schema import validate_settings
from core.settings_writer import DEFAULT_SOUND_WAV_PATH, write_stop_channels, write_sound
from notifiers import sound


class SoundConfigTests(unittest.TestCase):
    def test_write_sound_sets_sound_config(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home}):
            cwd = os.path.join(home, "project")
            os.makedirs(cwd)
            settings_path = write_sound(cwd, r"C:\Windows\Media\tada.wav")

            with open(settings_path, "r", encoding="utf-8") as handle:
                settings = json.load(handle)

            self.assertEqual(settings["notifications"]["sound"]["wavPath"], r"C:\Windows\Media\tada.wav")
            self.assertTrue(settings["notifications"]["sound"]["enabled"])

    def test_write_sound_replaces_legacy_stop_channel(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home}):
            cwd = os.path.join(home, "project")
            os.makedirs(cwd)
            config_dir = os.path.join(home, ".claude", "hook-terr")
            os.makedirs(config_dir)
            settings_path = os.path.join(config_dir, "settings.json")
            with open(settings_path, "w", encoding="utf-8") as handle:
                json.dump({"events": {"Stop": {"notifications": ["beep", "popup"]}}}, handle)

            write_sound(cwd, r"C:\Windows\Media\tada.wav")

            with open(settings_path, "r", encoding="utf-8") as handle:
                settings = json.load(handle)

            self.assertEqual(settings["events"]["Stop"]["notifications"], ["sound", "popup"])

    def test_write_stop_channels_initializes_default_sound_config(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home}):
            cwd = os.path.join(home, "project")
            os.makedirs(cwd)

            settings_path = write_stop_channels("global", cwd, ["sound"])

            with open(settings_path, "r", encoding="utf-8") as handle:
                settings = json.load(handle)

            self.assertEqual(settings["events"]["Stop"]["notifications"], ["sound"])
            self.assertTrue(settings["notifications"]["sound"]["enabled"])
            self.assertEqual(settings["notifications"]["sound"]["wavPath"], DEFAULT_SOUND_WAV_PATH)

    def test_write_stop_channels_deduplicates_channels(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home}):
            cwd = os.path.join(home, "project")
            os.makedirs(cwd)

            settings_path = write_stop_channels("global", cwd, ["sound", "sound", "popup"])

            with open(settings_path, "r", encoding="utf-8") as handle:
                settings = json.load(handle)

            self.assertEqual(settings["events"]["Stop"]["notifications"], ["sound", "popup"])

    def test_write_stop_channels_preserves_existing_sound_wav_path(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home}):
            cwd = os.path.join(home, "project")
            os.makedirs(cwd)
            custom_path = r"C:\Windows\Media\notify.wav"
            write_sound(cwd, custom_path)

            settings_path = write_stop_channels("global", cwd, ["sound", "popup"])

            with open(settings_path, "r", encoding="utf-8") as handle:
                settings = json.load(handle)

            self.assertEqual(settings["events"]["Stop"]["notifications"], ["sound", "popup"])
            self.assertEqual(settings["notifications"]["sound"]["wavPath"], custom_path)

    def test_validate_settings_requires_sound_wav_path_string(self):
        errors = validate_settings({"notifications": {"sound": {"wavPath": 123}}})

        self.assertIn("settings.notifications.sound.wavPath must be a string", errors)

    def test_validate_settings_checks_sound_and_toast_fields(self):
        errors = validate_settings(
            {
                "notifications": {
                    "sound": {"timeoutMs": "fast"},
                    "windows_toast": {"timeoutMs": 0, "silent": "false"},
                }
            }
        )

        self.assertIn("settings.notifications.sound.timeoutMs must be a positive number", errors)
        self.assertIn("settings.notifications.windows_toast.timeoutMs must be a positive number", errors)
        self.assertIn("settings.notifications.windows_toast.silent must be a boolean", errors)

    def test_sound_uses_wav_path_when_configured(self):
        calls = []

        def fake_run(args, **kwargs):
            calls.append((args, kwargs))

        with patch("platform.system", return_value="Windows"), patch("notifiers.sound.powershell_executable", return_value=r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"), patch("subprocess.run", side_effect=fake_run):
            sound.send("title", "message", HookContext("Stop"), {"wavPath": r"C:\Windows\Media\tada.wav", "timeoutMs": 800})

        args = calls[0][0]
        command = args[-1]
        self.assertEqual(args[0], r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe")
        self.assertIn("System.Media.SoundPlayer", command)
        self.assertIn(r"C:\Windows\Media\tada.wav", command)
        self.assertNotIn("Console]::", command)

    def test_sound_uses_default_wav_without_wav_path(self):
        calls = []

        def fake_run(args, **kwargs):
            calls.append((args, kwargs))

        with patch("platform.system", return_value="Windows"), patch("notifiers.sound.powershell_executable", return_value=r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"), patch("subprocess.run", side_effect=fake_run):
            sound.send("title", "message", HookContext("Stop"), {})

        command = calls[0][0][-1]
        timeout = calls[0][1]["timeout"]
        self.assertIn("System.Media.SoundPlayer", command)
        self.assertIn(r"C:\Windows\Media\tada.wav", command)
        self.assertNotIn("Console]::", command)
        self.assertGreaterEqual(timeout, 2.5)


if __name__ == "__main__":
    unittest.main()
