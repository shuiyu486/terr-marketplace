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
from core.models import NotificationResult


class StopNotificationPolicyTests(unittest.TestCase):
    def test_default_stop_rule_is_silent_without_external_notification(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            os.makedirs(cwd)

            with patch("core.action_executor.send_notification") as send_notification:
                response = run("Stop", {"cwd": cwd, "transcript_path": os.path.join(home, "transcript.jsonl")})

            self.assertEqual(response, {})
            send_notification.assert_not_called()

    def test_default_stop_rule_ignores_subagent_transcript_path(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            os.makedirs(cwd)
            transcript_path = os.path.join(home, "session", "subagents", "agent.jsonl")

            with patch("core.action_executor.send_notification") as send_notification:
                response = run("Stop", {"cwd": cwd, "transcript_path": transcript_path})

            self.assertEqual(response, {})
            send_notification.assert_not_called()

    def test_user_rule_can_match_subagent_stop_by_is_subagent(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            rules_dir = os.path.join(home, ".claude", "hook-terr", "rules")
            os.makedirs(rules_dir)
            os.makedirs(cwd)
            with open(os.path.join(rules_dir, "subagent.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "version": 1,
                        "id": "subagent",
                        "enabled": True,
                        "event": "Stop",
                        "priority": 200,
                        "decision": "warn",
                        "when": [{"field": "is_subagent", "op": "equals", "value": True}],
                        "message": {"text": "subagent stop"},
                        "notify": {"enabled": False},
                    },
                    handle,
                )
            transcript_path = os.path.join(home, "session", "subagents", "agent.jsonl")

            response = run("Stop", {"cwd": cwd, "transcript_path": transcript_path})

            self.assertEqual(response, {"systemMessage": "subagent stop"})

    def test_user_rule_can_match_subagent_stop_by_agent_type(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            rules_dir = os.path.join(home, ".claude", "hook-terr", "rules")
            os.makedirs(rules_dir)
            os.makedirs(cwd)
            with open(os.path.join(rules_dir, "agent-type.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "version": 1,
                        "id": "agent-type",
                        "enabled": True,
                        "event": "Stop",
                        "priority": 200,
                        "decision": "warn",
                        "when": [{"field": "agent_type", "op": "equals", "value": "subagent"}],
                        "message": {"text": "subagent type"},
                        "notify": {"enabled": False},
                    },
                    handle,
                )
            transcript_path = os.path.join(home, "session", "subagents", "agent.jsonl")

            response = run("Stop", {"cwd": cwd, "transcript_path": transcript_path})

            self.assertEqual(response, {"systemMessage": "subagent type"})

    def test_legacy_custom_command_template_settings_are_rejected(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            config_dir = os.path.join(home, ".claude", "hook-terr")
            os.makedirs(config_dir)
            os.makedirs(cwd)
            with open(os.path.join(config_dir, "settings.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "notifications": {
                            "custom_command": {
                                "enabled": True,
                                "command": "Write-Host '{{message}}'",
                            }
                        },
                        "events": {"Stop": {"notifications": ["custom_command"]}},
                    },
                    handle,
                )

            with patch("core.action_executor.send_notification") as send_notification:
                response = run("Stop", {"cwd": cwd})

            self.assertIn("systemMessage", response)
            self.assertIn("custom_command.command", response["systemMessage"])
            self.assertIn("removed legacy template", response["systemMessage"])
            send_notification.assert_not_called()

    def test_explicit_empty_notify_channels_does_not_add_diagnostic(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            rules_dir = os.path.join(home, ".claude", "hook-terr", "rules")
            os.makedirs(rules_dir)
            os.makedirs(cwd)
            with open(os.path.join(rules_dir, "empty-channels.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "version": 1,
                        "id": "empty-channels",
                        "enabled": True,
                        "event": "Stop",
                        "priority": 200,
                        "decision": "warn",
                        "when": [],
                        "message": {"text": "empty channels"},
                        "notify": {"enabled": True, "channels": []},
                    },
                    handle,
                )

            with patch("core.action_executor.send_notification") as send_notification:
                response = run("Stop", {"cwd": cwd})

            self.assertEqual(response, {"systemMessage": "empty channels"})
            send_notification.assert_not_called()

    def test_notify_without_rule_channels_uses_event_channels(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            config_dir = os.path.join(home, ".claude", "hook-terr")
            rules_dir = os.path.join(home, ".claude", "hook-terr", "rules")
            os.makedirs(config_dir)
            os.makedirs(rules_dir)
            os.makedirs(cwd)
            with open(os.path.join(config_dir, "settings.json"), "w", encoding="utf-8") as handle:
                json.dump({"events": {"Stop": {"notifications": ["sound"]}}}, handle)
            with open(os.path.join(rules_dir, "event-channels.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "version": 1,
                        "id": "event-channels",
                        "enabled": True,
                        "event": "Stop",
                        "priority": 200,
                        "decision": "warn",
                        "when": [],
                        "message": {"text": "event channels"},
                        "notify": {"enabled": True, "title": "title", "text": "text"},
                    },
                    handle,
                )

            with patch("core.action_executor.send_notification", return_value=NotificationResult("sound", True)) as send_notification:
                response = run("Stop", {"cwd": cwd})

            self.assertEqual(response, {})
            send_notification.assert_called_once()
            self.assertEqual(send_notification.call_args.args[0], "sound")

    def test_stop_notification_is_suppressed_by_runtime_background_tasks(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            rules_dir = os.path.join(home, ".claude", "hook-terr", "rules")
            os.makedirs(rules_dir)
            os.makedirs(cwd)
            with open(os.path.join(rules_dir, "always-notify.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "version": 1,
                        "id": "always-notify",
                        "enabled": True,
                        "event": "Stop",
                        "priority": 200,
                        "decision": "warn",
                        "when": [],
                        "message": {"text": "explicit notify"},
                        "notify": {"enabled": True, "channels": ["sound"]},
                    },
                    handle,
                )

            with patch("core.action_executor.send_notification", return_value=NotificationResult("sound", True)) as send_notification:
                response = run(
                    "Stop",
                    {
                        "cwd": cwd,
                        "background_tasks": [
                            {
                                "id": "agent-one",
                                "type": "subagent",
                                "status": "running",
                                "description": "review",
                            }
                        ],
                        "session_crons": [],
                    },
                )

            self.assertEqual(response, {})
            send_notification.assert_not_called()

    def test_stop_notification_is_suppressed_by_runtime_session_crons(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            rules_dir = os.path.join(home, ".claude", "hook-terr", "rules")
            os.makedirs(rules_dir)
            os.makedirs(cwd)
            with open(os.path.join(rules_dir, "always-notify.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "version": 1,
                        "id": "always-notify",
                        "enabled": True,
                        "event": "Stop",
                        "priority": 200,
                        "decision": "warn",
                        "when": [],
                        "message": {"text": "explicit notify"},
                        "notify": {"enabled": True, "channels": ["sound"]},
                    },
                    handle,
                )

            with patch("core.action_executor.send_notification", return_value=NotificationResult("sound", True)) as send_notification:
                response = run(
                    "Stop",
                    {
                        "cwd": cwd,
                        "background_tasks": [],
                        "session_crons": [
                            {
                                "id": "wakeup-one",
                                "schedule": "0 9 * * *",
                                "recurring": False,
                                "prompt": "continue",
                            }
                        ],
                    },
                )

            self.assertEqual(response, {})
            send_notification.assert_not_called()

    def test_empty_runtime_background_tasks_override_stale_transcript(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            rules_dir = os.path.join(home, ".claude", "hook-terr", "rules")
            os.makedirs(rules_dir)
            os.makedirs(cwd)
            with open(os.path.join(rules_dir, "always-notify.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "version": 1,
                        "id": "always-notify",
                        "enabled": True,
                        "event": "Stop",
                        "priority": 200,
                        "decision": "warn",
                        "when": [],
                        "message": {"text": "explicit notify"},
                        "notify": {"enabled": True, "channels": ["sound"]},
                    },
                    handle,
                )
            transcript_path = os.path.join(home, "transcript.jsonl")
            with open(transcript_path, "w", encoding="utf-8") as handle:
                handle.write(
                    json.dumps(
                        {
                            "type": "user",
                            "message": {"content": [{"type": "tool_result", "tool_use_id": "call-agent"}]},
                            "toolUseResult": {"status": "async_launched", "agentId": "agent-one"},
                        }
                    )
                    + "\n"
                )

            with patch("core.action_executor.send_notification", return_value=NotificationResult("sound", True)) as send_notification:
                response = run(
                    "Stop",
                    {
                        "cwd": cwd,
                        "transcript_path": transcript_path,
                        "background_tasks": [],
                        "session_crons": [],
                    },
                )

            self.assertEqual(response, {})
            send_notification.assert_called_once()

    def test_task_reminder_does_not_suppress_stop_notification(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            rules_dir = os.path.join(home, ".claude", "hook-terr", "rules")
            os.makedirs(rules_dir)
            os.makedirs(cwd)
            with open(os.path.join(rules_dir, "always-notify.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "version": 1,
                        "id": "always-notify",
                        "enabled": True,
                        "event": "Stop",
                        "priority": 200,
                        "decision": "warn",
                        "when": [],
                        "message": {"text": "explicit notify"},
                        "notify": {"enabled": True, "channels": ["sound"]},
                    },
                    handle,
                )
            transcript_path = os.path.join(home, "transcript.jsonl")
            with open(transcript_path, "w", encoding="utf-8") as handle:
                handle.write(
                    json.dumps(
                        {
                            "type": "attachment",
                            "attachment": {
                                "type": "task_reminder",
                                "content": [{"id": "1", "status": "pending", "subject": "future work"}],
                            },
                        }
                    )
                    + "\n"
                )

            with patch("core.action_executor.send_notification", return_value=NotificationResult("sound", True)) as send_notification:
                response = run("Stop", {"cwd": cwd, "transcript_path": transcript_path})

            self.assertEqual(response, {})
            send_notification.assert_called_once()

    def test_stop_notification_is_suppressed_while_background_agent_is_running(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            rules_dir = os.path.join(home, ".claude", "hook-terr", "rules")
            os.makedirs(rules_dir)
            os.makedirs(cwd)
            with open(os.path.join(rules_dir, "always-notify.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "version": 1,
                        "id": "always-notify",
                        "enabled": True,
                        "event": "Stop",
                        "priority": 200,
                        "decision": "warn",
                        "when": [],
                        "message": {"text": "explicit notify"},
                        "notify": {"enabled": True, "channels": ["sound"], "title": "title", "text": "text"},
                    },
                    handle,
                )
            transcript_path = os.path.join(home, "transcript.jsonl")
            records = [
                {
                    "type": "assistant",
                    "timestamp": "2026-08-07T10:00:00Z",
                    "message": {
                        "content": [
                            {
                                "type": "tool_use",
                                "id": "call-agent",
                                "name": "Agent",
                                "input": {"run_in_background": True},
                            }
                        ]
                    },
                },
                {
                    "type": "user",
                    "timestamp": "2026-08-07T10:00:01Z",
                    "message": {"content": [{"type": "tool_result", "tool_use_id": "call-agent"}]},
                    "toolUseResult": {"status": "async_launched", "agentId": "agent-one"},
                },
            ]
            with open(transcript_path, "w", encoding="utf-8") as handle:
                for record in records:
                    handle.write(json.dumps(record) + "\n")

            with patch("core.action_executor.send_notification", return_value=NotificationResult("sound", True)) as send_notification:
                response = run("Stop", {"cwd": cwd, "transcript_path": transcript_path})

            self.assertEqual(response, {})
            send_notification.assert_not_called()

    def test_stop_notification_is_suppressed_after_one_agent_finishes_when_another_is_running(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            rules_dir = os.path.join(home, ".claude", "hook-terr", "rules")
            os.makedirs(rules_dir)
            os.makedirs(cwd)
            with open(os.path.join(rules_dir, "always-notify.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "version": 1,
                        "id": "always-notify",
                        "enabled": True,
                        "event": "Stop",
                        "priority": 200,
                        "decision": "warn",
                        "when": [],
                        "message": {"text": "explicit notify"},
                        "notify": {"enabled": True, "channels": ["sound"]},
                    },
                    handle,
                )
            transcript_path = os.path.join(home, "transcript.jsonl")
            records = [
                {
                    "type": "assistant",
                    "timestamp": "2026-08-07T10:00:00Z",
                    "message": {
                        "content": [
                            {"type": "tool_use", "id": "call-one", "name": "Agent", "input": {"run_in_background": True}},
                            {"type": "tool_use", "id": "call-two", "name": "Agent", "input": {"run_in_background": True}},
                        ]
                    },
                },
                {
                    "type": "user",
                    "timestamp": "2026-08-07T10:00:01Z",
                    "message": {"content": [{"type": "tool_result", "tool_use_id": "call-one"}]},
                    "toolUseResult": {"status": "async_launched", "agentId": "agent-one"},
                },
                {
                    "type": "user",
                    "timestamp": "2026-08-07T10:00:02Z",
                    "message": {"content": [{"type": "tool_result", "tool_use_id": "call-two"}]},
                    "toolUseResult": {"status": "async_launched", "agentId": "agent-two"},
                },
                {
                    "type": "queue-operation",
                    "operation": "enqueue",
                    "timestamp": "2026-08-07T10:01:00Z",
                    "content": "<task-notification><tool-use-id>call-one</tool-use-id><status>completed</status></task-notification>",
                },
            ]
            with open(transcript_path, "w", encoding="utf-8") as handle:
                for record in records:
                    handle.write(json.dumps(record) + "\n")

            with patch("core.action_executor.send_notification", return_value=NotificationResult("sound", True)) as send_notification:
                response = run("Stop", {"cwd": cwd, "transcript_path": transcript_path})

            self.assertEqual(response, {})
            send_notification.assert_not_called()

    def test_quoted_task_notification_does_not_mark_background_task_finished(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            rules_dir = os.path.join(home, ".claude", "hook-terr", "rules")
            os.makedirs(rules_dir)
            os.makedirs(cwd)
            with open(os.path.join(rules_dir, "always-notify.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "version": 1,
                        "id": "always-notify",
                        "enabled": True,
                        "event": "Stop",
                        "priority": 200,
                        "decision": "warn",
                        "when": [],
                        "message": {"text": "explicit notify"},
                        "notify": {"enabled": True, "channels": ["sound"]},
                    },
                    handle,
                )
            transcript_path = os.path.join(home, "transcript.jsonl")
            records = [
                {
                    "type": "assistant",
                    "timestamp": "2026-08-07T10:00:00Z",
                    "message": {"content": [{"type": "tool_use", "id": "call-agent", "name": "Agent", "input": {"run_in_background": True}}]},
                },
                {
                    "type": "user",
                    "timestamp": "2026-08-07T10:00:01Z",
                    "message": {"content": [{"type": "tool_result", "tool_use_id": "call-agent"}]},
                    "toolUseResult": {"status": "async_launched", "agentId": "agent-one"},
                },
                {
                    "type": "user",
                    "timestamp": "2026-08-07T10:01:00Z",
                    "message": {"content": "quoted <task-notification><tool-use-id>call-agent</tool-use-id><status>completed</status></task-notification>"},
                },
            ]
            with open(transcript_path, "w", encoding="utf-8") as handle:
                for record in records:
                    handle.write(json.dumps(record) + "\n")

            with patch("core.action_executor.send_notification", return_value=NotificationResult("sound", True)) as send_notification:
                response = run("Stop", {"cwd": cwd, "transcript_path": transcript_path})

            self.assertEqual(response, {})
            send_notification.assert_not_called()

    def test_stop_notification_sends_after_all_background_tasks_finish(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            rules_dir = os.path.join(home, ".claude", "hook-terr", "rules")
            os.makedirs(rules_dir)
            os.makedirs(cwd)
            with open(os.path.join(rules_dir, "always-notify.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "version": 1,
                        "id": "always-notify",
                        "enabled": True,
                        "event": "Stop",
                        "priority": 200,
                        "decision": "warn",
                        "when": [],
                        "message": {"text": "explicit notify"},
                        "notify": {"enabled": True, "channels": ["sound"]},
                    },
                    handle,
                )
            transcript_path = os.path.join(home, "transcript.jsonl")
            records = [
                {
                    "type": "assistant",
                    "timestamp": "2026-08-07T10:00:00Z",
                    "message": {
                        "content": [
                            {"type": "tool_use", "id": "call-agent", "name": "Agent", "input": {"run_in_background": True}},
                            {"type": "tool_use", "id": "call-command", "name": "Bash", "input": {"run_in_background": True}},
                        ]
                    },
                },
                {
                    "type": "user",
                    "timestamp": "2026-08-07T10:00:01Z",
                    "message": {"content": [{"type": "tool_result", "tool_use_id": "call-agent"}]},
                    "toolUseResult": {"status": "async_launched", "agentId": "agent-one"},
                },
                {
                    "type": "user",
                    "timestamp": "2026-08-07T10:00:02Z",
                    "message": {"content": [{"type": "tool_result", "tool_use_id": "call-command"}]},
                    "toolUseResult": {"backgroundTaskId": "command-one"},
                },
                {
                    "type": "queue-operation",
                    "timestamp": "2026-08-07T10:01:00Z",
                    "content": "<task-notification><tool-use-id>call-agent</tool-use-id><status>completed</status></task-notification>",
                },
                {
                    "type": "queue-operation",
                    "timestamp": "2026-08-07T10:02:00Z",
                    "content": "<task-notification><tool-use-id>call-command</tool-use-id><status>completed</status></task-notification>",
                },
            ]
            with open(transcript_path, "w", encoding="utf-8") as handle:
                for record in records:
                    handle.write(json.dumps(record) + "\n")

            with patch("core.action_executor.send_notification", return_value=NotificationResult("sound", True)) as send_notification:
                response = run("Stop", {"cwd": cwd, "transcript_path": transcript_path})

            self.assertEqual(response, {})
            send_notification.assert_called_once()

    def test_stop_notification_stays_suppressed_after_completed_agent_is_resumed(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            rules_dir = os.path.join(home, ".claude", "hook-terr", "rules")
            os.makedirs(rules_dir)
            os.makedirs(cwd)
            with open(os.path.join(rules_dir, "always-notify.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "version": 1,
                        "id": "always-notify",
                        "enabled": True,
                        "event": "Stop",
                        "priority": 200,
                        "decision": "warn",
                        "when": [],
                        "message": {"text": "explicit notify"},
                        "notify": {"enabled": True, "channels": ["sound"]},
                    },
                    handle,
                )
            transcript_path = os.path.join(home, "transcript.jsonl")
            records = [
                {
                    "type": "assistant",
                    "timestamp": "2026-08-07T10:00:00Z",
                    "message": {"content": [{"type": "tool_use", "id": "call-agent", "name": "Agent", "input": {"run_in_background": True}}]},
                },
                {
                    "type": "user",
                    "timestamp": "2026-08-07T10:00:01Z",
                    "message": {"content": [{"type": "tool_result", "tool_use_id": "call-agent"}]},
                    "toolUseResult": {"status": "async_launched", "agentId": "agent-one"},
                },
                {
                    "type": "queue-operation",
                    "timestamp": "2026-08-07T10:01:00Z",
                    "content": "<task-notification><tool-use-id>call-agent</tool-use-id><status>completed</status></task-notification>",
                },
                {
                    "type": "assistant",
                    "timestamp": "2026-08-07T10:02:00Z",
                    "message": {"content": [{"type": "tool_use", "id": "call-message", "name": "SendMessage", "input": {"to": "agent-one"}}]},
                },
                {
                    "type": "user",
                    "timestamp": "2026-08-07T10:02:01Z",
                    "message": {"content": [{"type": "tool_result", "tool_use_id": "call-message"}]},
                    "toolUseResult": {"success": True, "resumedAgentId": "agent-one"},
                },
            ]
            with open(transcript_path, "w", encoding="utf-8") as handle:
                for record in records:
                    handle.write(json.dumps(record) + "\n")

            with patch("core.action_executor.send_notification", return_value=NotificationResult("sound", True)) as send_notification:
                response = run("Stop", {"cwd": cwd, "transcript_path": transcript_path})

            self.assertEqual(response, {})
            send_notification.assert_not_called()

    def test_explicit_stop_notify_rule_still_sends_notification(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            rules_dir = os.path.join(home, ".claude", "hook-terr", "rules")
            os.makedirs(rules_dir)
            os.makedirs(cwd)
            with open(os.path.join(rules_dir, "always-notify.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "version": 1,
                        "id": "always-notify",
                        "enabled": True,
                        "event": "Stop",
                        "priority": 200,
                        "decision": "warn",
                        "when": [],
                        "message": {"text": "explicit notify"},
                        "notify": {"enabled": True, "channels": ["sound"], "title": "title", "text": "text"},
                    },
                    handle,
                )

            with patch("core.action_executor.send_notification", return_value=NotificationResult("sound", True)) as send_notification:
                response = run("Stop", {"cwd": cwd})

            self.assertEqual(response, {})
            send_notification.assert_called_once()

    def test_overbroad_stop_notify_rule_does_not_notify_subagent(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            rules_dir = os.path.join(home, ".claude", "hook-terr", "rules")
            os.makedirs(rules_dir)
            os.makedirs(cwd)
            with open(os.path.join(rules_dir, "always-notify.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "version": 1,
                        "id": "always-notify",
                        "enabled": True,
                        "event": "Stop",
                        "priority": 200,
                        "decision": "warn",
                        "when": [],
                        "message": {"text": "explicit notify"},
                        "notify": {"enabled": True, "channels": ["sound"], "title": "title", "text": "text"},
                    },
                    handle,
                )
            transcript_path = os.path.join(home, "session", "subagents", "agent.jsonl")

            with patch("core.action_executor.send_notification", return_value=NotificationResult("sound", True)) as send_notification:
                response = run("Stop", {"cwd": cwd, "transcript_path": transcript_path})

            self.assertEqual(response, {"systemMessage": "explicit notify"})
            send_notification.assert_not_called()

    def test_official_agent_id_stop_does_not_notify_subagent(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            rules_dir = os.path.join(home, ".claude", "hook-terr", "rules")
            os.makedirs(rules_dir)
            os.makedirs(cwd)
            with open(os.path.join(rules_dir, "always-notify.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "version": 1,
                        "id": "always-notify",
                        "enabled": True,
                        "event": "Stop",
                        "priority": 200,
                        "decision": "warn",
                        "when": [],
                        "message": {"text": "explicit notify"},
                        "notify": {"enabled": True, "channels": ["sound"], "title": "title", "text": "text"},
                    },
                    handle,
                )

            with patch("core.action_executor.send_notification", return_value=NotificationResult("sound", True)) as send_notification:
                response = run(
                    "Stop",
                    {
                        "cwd": cwd,
                        "agent_id": "agent-123",
                        "agent_type": "Explore",
                        "transcript_path": os.path.join(home, "agent-123.jsonl"),
                    },
                )

            self.assertEqual(response, {"systemMessage": "explicit notify"})
            send_notification.assert_not_called()

    def test_overbroad_post_tool_notify_rule_does_not_notify_regular_tool(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            rules_dir = os.path.join(home, ".claude", "hook-terr", "rules")
            os.makedirs(rules_dir)
            os.makedirs(cwd)
            with open(os.path.join(rules_dir, "post-tool.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "version": 1,
                        "id": "post-tool",
                        "enabled": True,
                        "event": "PostToolUse",
                        "priority": 200,
                        "decision": "warn",
                        "when": [],
                        "message": {"text": "tool used"},
                        "notify": {"enabled": True, "channels": ["sound"], "title": "title", "text": "text"},
                    },
                    handle,
                )

            with patch("core.action_executor.send_notification", return_value=NotificationResult("sound", True)) as send_notification:
                response = run("PostToolUse", {"cwd": cwd, "tool_name": "Edit", "tool_input": {"file_path": os.path.join(cwd, "app.py")}})

            self.assertEqual(response, {"systemMessage": "tool used"})
            send_notification.assert_not_called()

    def test_ask_user_question_sends_assistance_notification_using_stop_channels(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            config_dir = os.path.join(home, ".claude", "hook-terr")
            os.makedirs(config_dir)
            os.makedirs(cwd)
            with open(os.path.join(config_dir, "settings.json"), "w", encoding="utf-8") as handle:
                json.dump({"events": {"Stop": {"notifications": ["sound"]}, "PreToolUse": {"notifications": ["popup"]}}}, handle)

            with patch("core.action_executor.send_notification", return_value=NotificationResult("sound", True)) as send_notification:
                response = run("PreToolUse", {"cwd": cwd, "tool_name": "AskUserQuestion", "tool_input": {"question": "请选择"}})

            self.assertEqual(response, {})
            send_notification.assert_called_once()
            self.assertEqual(send_notification.call_args.args[0], "sound")

    def test_ask_user_question_does_not_notify_when_blocked(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            rules_dir = os.path.join(home, ".claude", "hook-terr", "rules")
            os.makedirs(rules_dir)
            os.makedirs(cwd)
            with open(os.path.join(rules_dir, "block-question.json"), "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "version": 1,
                        "id": "block-question",
                        "enabled": True,
                        "event": "PreToolUse",
                        "priority": 200,
                        "decision": "block",
                        "when": [{"field": "tool_name", "op": "equals", "value": "AskUserQuestion"}],
                        "message": {"text": "blocked"},
                        "notify": {"enabled": True, "channels": ["sound"]},
                    },
                    handle,
                )

            with patch("core.action_executor.send_notification", return_value=NotificationResult("sound", True)) as send_notification:
                response = run("PreToolUse", {"cwd": cwd, "tool_name": "AskUserQuestion"})

            self.assertEqual(response.get("hookSpecificOutput", {}).get("permissionDecision"), "deny")
            send_notification.assert_not_called()

    def test_ask_user_question_does_not_notify_subagent(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            os.makedirs(cwd)

            with patch("core.action_executor.send_notification", return_value=NotificationResult("sound", True)) as send_notification:
                response = run("PreToolUse", {"cwd": cwd, "tool_name": "AskUserQuestion", "isSidechain": True})

            self.assertEqual(response, {})
            send_notification.assert_not_called()

    def test_ask_user_question_with_official_agent_id_does_not_notify_subagent(self):
        with tempfile.TemporaryDirectory() as home, patch.dict(os.environ, {"USERPROFILE": home, "HOME": home, "CLAUDE_PLUGIN_ROOT": PLUGIN_ROOT}):
            cwd = os.path.join(home, "project")
            os.makedirs(cwd)

            with patch("core.action_executor.send_notification", return_value=NotificationResult("sound", True)) as send_notification:
                response = run(
                    "PreToolUse",
                    {
                        "cwd": cwd,
                        "tool_name": "AskUserQuestion",
                        "agent_id": "agent-123",
                        "agent_type": "Explore",
                    },
                )

            self.assertEqual(response, {})
            send_notification.assert_not_called()


if __name__ == "__main__":
    unittest.main()
