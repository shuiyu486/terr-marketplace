import json
import os
import sys
import tempfile
import unittest


PLUGIN_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PLUGIN_ROOT not in sys.path:
    sys.path.insert(0, PLUGIN_ROOT)

from core.background_tasks import has_pending_background_tasks


class BackgroundTaskTests(unittest.TestCase):
    def test_agent_result_is_pending_when_request_omits_background_flag(self):
        records = [
            self.tool_result("call-agent", {"status": "async_launched", "isAsync": True, "agentId": "agent-one"}),
        ]

        self.assertTrue(self.pending(records))

    def test_agent_result_is_pending_when_request_explicitly_requested_foreground(self):
        records = [
            self.tool_use("call-agent", "Agent", {"run_in_background": False}),
            self.tool_result("call-agent", {"status": "async_launched", "agentId": "agent-one"}),
        ]

        self.assertTrue(self.pending(records))

    def test_command_timeout_result_is_pending(self):
        records = [
            self.tool_result("call-command", {"backgroundTaskId": "bash-one", "timedOutAfterMs": 120000}),
        ]

        self.assertTrue(self.pending(records))

    def test_workflow_result_is_pending_until_notification(self):
        records = [
            self.tool_result("call-workflow", {"status": "async_launched", "taskId": "workflow-one", "runId": "wf-one"}),
        ]

        self.assertTrue(self.pending(records))

        records.append(self.notification("call-workflow", "completed"))

        self.assertFalse(self.pending(records))

    def test_successful_task_stop_finishes_background_task(self):
        records = [
            self.tool_result("call-command", {"backgroundTaskId": "bash-one"}),
            self.tool_use("call-stop", "TaskStop", {"task_id": "bash-one"}),
            self.tool_result(
                "call-stop",
                {"message": "Successfully stopped task", "task_id": "bash-one", "task_type": "local_bash"},
            ),
        ]

        self.assertFalse(self.pending(records))

    def test_successful_task_stop_content_fallback_finishes_background_task(self):
        records = [
            self.tool_result("call-command", {"backgroundTaskId": "bash-one"}),
            self.tool_use("call-stop", "TaskStop", {"task_id": "bash-one"}),
            self.tool_result("call-stop", None, content=json.dumps({"task_id": "bash-one", "task_type": "local_bash"})),
        ]

        self.assertFalse(self.pending(records))

    def test_failed_task_stop_does_not_finish_background_task(self):
        records = [
            self.tool_result("call-command", {"backgroundTaskId": "bash-one"}),
            self.tool_use("call-stop", "TaskStop", {"task_id": "bash-one"}),
            self.tool_result("call-stop", "No task found", content="<tool_use_error>No task found</tool_use_error>", is_error=True),
        ]

        self.assertTrue(self.pending(records))

    def test_failed_launch_is_not_pending_even_when_requested_in_background(self):
        records = [
            self.tool_use("call-command", "Bash", {"run_in_background": True}),
            self.tool_result("call-command", "launch failed", content="launch failed", is_error=True),
        ]

        self.assertFalse(self.pending(records))

    def test_unknown_notification_status_does_not_finish_task(self):
        records = [
            self.tool_result("call-agent", {"status": "async_launched", "agentId": "agent-one"}),
            self.notification("call-agent", "paused"),
        ]

        self.assertTrue(self.pending(records))

    def test_duplicate_terminal_notifications_are_idempotent(self):
        records = [
            self.tool_result("call-agent", {"status": "async_launched", "agentId": "agent-one"}),
            self.notification("call-agent", "completed"),
            self.notification("call-agent", "completed"),
        ]

        self.assertFalse(self.pending(records))

    def test_resumed_agent_uses_send_message_tool_id_for_next_completion(self):
        records = [
            self.tool_result("call-agent", {"status": "async_launched", "agentId": "agent-one"}),
            self.notification("call-agent", "completed"),
            self.tool_result("call-message", {"success": True, "resumedAgentId": "agent-one"}),
        ]

        self.assertTrue(self.pending(records))

        records.append(self.notification("call-message", "completed"))

        self.assertFalse(self.pending(records))

    def test_queued_message_to_running_agent_does_not_create_new_pending_task(self):
        records = [
            self.tool_result("call-agent", {"status": "async_launched", "agentId": "agent-one"}),
            self.tool_result("call-message", {"success": True, "message": "Message queued for delivery"}),
            self.notification("call-agent", "completed"),
        ]

        self.assertFalse(self.pending(records))

    def test_quoted_notification_does_not_finish_task(self):
        records = [
            self.tool_result("call-agent", {"status": "async_launched", "agentId": "agent-one"}),
            {
                "type": "user",
                "message": {
                    "content": "quoted <task-notification><tool-use-id>call-agent</tool-use-id><status>completed</status></task-notification>"
                },
            },
        ]

        self.assertTrue(self.pending(records))

    def pending(self, records):
        with tempfile.TemporaryDirectory() as temp:
            transcript_path = os.path.join(temp, "transcript.jsonl")
            with open(transcript_path, "w", encoding="utf-8") as handle:
                for index, record in enumerate(records, 1):
                    record.setdefault("timestamp", "2026-08-08T10:00:{:02d}Z".format(index))
                    handle.write(json.dumps(record) + "\n")
            return has_pending_background_tasks(transcript_path)

    def tool_use(self, tool_use_id, name, tool_input):
        return {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "id": tool_use_id,
                        "name": name,
                        "input": tool_input,
                    }
                ]
            },
        }

    def tool_result(self, tool_use_id, result, content="", is_error=False):
        part = {
            "type": "tool_result",
            "tool_use_id": tool_use_id,
            "content": content,
        }
        if is_error:
            part["is_error"] = True
        record = {
            "type": "user",
            "message": {"content": [part]},
        }
        if result is not None:
            record["toolUseResult"] = result
        return record

    def notification(self, tool_use_id, status):
        return {
            "type": "queue-operation",
            "operation": "enqueue",
            "content": (
                "<task-notification>"
                "<task-id>task-one</task-id>"
                "<tool-use-id>{}</tool-use-id>"
                "<status>{}</status>"
                "</task-notification>"
            ).format(tool_use_id, status),
        }


if __name__ == "__main__":
    unittest.main()
