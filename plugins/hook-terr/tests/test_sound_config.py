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
from core.settings_writer import write_sound
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

    def test_validate_settings_requires_sound_wav_path_string(self):
        errors = validate_settings({"notifications": {"sound": {"wavPath": 123}}})

        self.assertIn("settings.notifications.sound.wavPath must be a string", errors)

    def test_sound_uses_wav_path_when_configured(self):
        calls = []

        def fake_run(args, **kwargs):
            calls.append((args, kwargs))

        with patch("platform.system", return_value="Windows"), patch("subprocess.run", side_effect=fake_run):
            sound.send("title", "message", HookContext("Stop"), {"wavPath": r"C:\Windows\Media\tada.wav", "timeoutMs": 800})

        command = calls[0][0][-1]
        self.assertIn("System.Media.SoundPlayer", command)
        self.assertIn(r"C:\Windows\Media\tada.wav", command)
        self.assertNotIn("Console]::", command)

    def test_sound_uses_default_wav_without_wav_path(self):
        calls = []

        def fake_run(args, **kwargs):
            calls.append((args, kwargs))

        with patch("platform.system", return_value="Windows"), patch("subprocess.run", side_effect=fake_run):
            sound.send("title", "message", HookContext("Stop"), {})

        command = calls[0][0][-1]
        timeout = calls[0][1]["timeout"]
        self.assertIn("System.Media.SoundPlayer", command)
        self.assertIn(r"C:\Windows\Media\tada.wav", command)
        self.assertNotIn("Console]::", command)
        self.assertGreaterEqual(timeout, 2.5)


if __name__ == "__main__":
    unittest.main()
