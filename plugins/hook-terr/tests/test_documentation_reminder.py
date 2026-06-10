import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

PLUGIN_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PLUGIN_ROOT not in sys.path:
    sys.path.insert(0, PLUGIN_ROOT)

from core.event_runner import run


class DocumentationReminderTests(unittest.TestCase):
    def test_write_in_project_blocks_stop_once(self):
        with self.project_env() as (home, cwd):
            run("PostToolUse", self.tool_payload(cwd, "s1", "Write", os.path.join(cwd, "app.py")))

            first = run("Stop", {"cwd": cwd, "session_id": "s1"})
            second = run("Stop", {"cwd": cwd, "session_id": "s1"})

            self.assertEqual(first.get("decision"), "block")
            self.assertIn("更新相关", first.get("reason", ""))
            self.assertIn("测试/验证", first.get("reason", ""))
            self.assertNotIn("commit/push", first.get("reason", ""))
            self.assertNotEqual(second.get("decision"), "block")

    def test_supported_modify_tools_trigger(self):
        for tool_name in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
            with self.subTest(tool_name=tool_name), self.project_env() as (home, cwd):
                path_key = "notebook_path" if tool_name == "NotebookEdit" else "file_path"
                payload = {
                    "cwd": cwd,
                    "session_id": tool_name,
                    "tool_name": tool_name,
                    "tool_input": {path_key: os.path.join(cwd, "doc.ipynb" if tool_name == "NotebookEdit" else "app.py")},
                }
                run("PostToolUse", payload)

                response = run("Stop", {"cwd": cwd, "session_id": tool_name})

                self.assertEqual(response.get("decision"), "block")

    def test_non_modify_tools_do_not_trigger(self):
        for tool_name in ("Read", "Bash", "Grep"):
            with self.subTest(tool_name=tool_name), self.project_env() as (home, cwd):
                run("PostToolUse", self.tool_payload(cwd, tool_name, tool_name, os.path.join(cwd, "app.py")))

                response = run("Stop", {"cwd": cwd, "session_id": tool_name})

                self.assertNotEqual(response.get("decision"), "block")

    def test_non_project_directory_does_not_trigger(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "scratch")
            os.makedirs(cwd)

            run("PostToolUse", self.tool_payload(cwd, "scratch", "Write", os.path.join(cwd, "note.txt")))
            response = run("Stop", {"cwd": cwd, "session_id": "scratch"})

            self.assertNotEqual(response.get("decision"), "block")

    def test_home_claude_directory_does_not_make_scratch_a_project(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            os.makedirs(os.path.join(home, ".claude"))
            cwd = os.path.join(home, "scratch")
            os.makedirs(cwd)

            run("PostToolUse", self.tool_payload(cwd, "scratch", "Write", os.path.join(cwd, "note.txt")))
            response = run("Stop", {"cwd": cwd, "session_id": "scratch"})

            self.assertNotEqual(response.get("decision"), "block")

    def test_outside_cwd_file_does_not_trigger(self):
        with self.project_env() as (home, cwd):
            outside = os.path.join(home, "outside.py")

            run("PostToolUse", self.tool_payload(cwd, "outside", "Write", outside))
            response = run("Stop", {"cwd": cwd, "session_id": "outside"})

            self.assertNotEqual(response.get("decision"), "block")

    def test_sessions_do_not_share_state(self):
        with self.project_env() as (home, cwd):
            run("PostToolUse", self.tool_payload(cwd, "s1", "Edit", os.path.join(cwd, "app.py")))

            other = run("Stop", {"cwd": cwd, "session_id": "s2"})
            edited = run("Stop", {"cwd": cwd, "session_id": "s1"})

            self.assertNotEqual(other.get("decision"), "block")
            self.assertEqual(edited.get("decision"), "block")

    def test_transcript_path_fallback_isolated(self):
        with self.project_env() as (home, cwd):
            transcript_one = os.path.join(home, "one.jsonl")
            transcript_two = os.path.join(home, "two.jsonl")
            payload = self.tool_payload(cwd, "", "Write", os.path.join(cwd, "app.py"))
            payload.pop("session_id")
            payload["transcript_path"] = transcript_one
            run("PostToolUse", payload)

            other = run("Stop", {"cwd": cwd, "transcript_path": transcript_two})
            edited = run("Stop", {"cwd": cwd, "transcript_path": transcript_one})

            self.assertNotEqual(other.get("decision"), "block")
            self.assertEqual(edited.get("decision"), "block")

    def test_user_prompt_submit_resets_turn(self):
        with self.project_env() as (home, cwd):
            run("PostToolUse", self.tool_payload(cwd, "s1", "Write", os.path.join(cwd, "app.py")))
            self.assertEqual(run("Stop", {"cwd": cwd, "session_id": "s1"}).get("decision"), "block")
            self.assertNotEqual(run("Stop", {"cwd": cwd, "session_id": "s1"}).get("decision"), "block")

            run("UserPromptSubmit", {"cwd": cwd, "session_id": "s1", "user_prompt": "next"})
            run("PostToolUse", self.tool_payload(cwd, "s1", "Edit", os.path.join(cwd, "app.py")))
            response = run("Stop", {"cwd": cwd, "session_id": "s1"})

            self.assertEqual(response.get("decision"), "block")

    def test_feature_can_be_disabled(self):
        with self.project_env() as (home, cwd):
            config_dir = os.path.join(home, ".claude", "hook-terr")
            os.makedirs(config_dir)
            with open(os.path.join(config_dir, "settings.json"), "w", encoding="utf-8") as handle:
                json.dump({"features": {"documentationReminder": {"enabled": False}}}, handle)

            run("PostToolUse", self.tool_payload(cwd, "s1", "Write", os.path.join(cwd, "app.py")))
            response = run("Stop", {"cwd": cwd, "session_id": "s1"})

            self.assertNotEqual(response.get("decision"), "block")

    def test_missing_session_key_fails_open(self):
        with self.project_env() as (home, cwd):
            payload = self.tool_payload(cwd, "", "Write", os.path.join(cwd, "app.py"))
            payload.pop("session_id")
            run("PostToolUse", payload)

            response = run("Stop", {"cwd": cwd})

            self.assertNotEqual(response.get("decision"), "block")

    def project_env(self):
        return ProjectEnv()

    def tool_payload(self, cwd, session_id, tool_name, file_path):
        return {
            "cwd": cwd,
            "session_id": session_id,
            "tool_name": tool_name,
            "tool_input": {"file_path": file_path},
        }


class ProjectEnv:
    def __enter__(self):
        self.temp = tempfile.TemporaryDirectory()
        self.home = self.temp.__enter__()
        self.patch = patch.dict(os.environ, {"USERPROFILE": self.home, "HOME": self.home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT})
        self.patch.__enter__()
        self.cwd = os.path.join(self.home, "project")
        os.makedirs(self.cwd)
        with open(os.path.join(self.cwd, "README.md"), "w", encoding="utf-8") as handle:
            handle.write("# project\n")
        return self.home, self.cwd

    def __exit__(self, exc_type, exc, tb):
        self.patch.__exit__(exc_type, exc, tb)
        self.temp.__exit__(exc_type, exc, tb)


if __name__ == "__main__":
    unittest.main()
