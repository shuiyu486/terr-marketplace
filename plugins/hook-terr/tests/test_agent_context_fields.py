import os
import sys
import unittest

PLUGIN_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PLUGIN_ROOT not in sys.path:
    sys.path.insert(0, PLUGIN_ROOT)

from core.context_builder import build_context, get_field
from core.models import Rule
from core.rule_matcher import matches_rule


class AgentContextFieldsTests(unittest.TestCase):
    def test_subagent_stop_event_is_subagent(self):
        context = build_context("SubagentStop", {})

        self.assertEqual(get_field(context, "is_subagent"), "true")
        self.assertEqual(get_field(context, "agent_type"), "subagent")

    def test_explicit_is_subagent_true(self):
        context = build_context("Stop", {"is_subagent": True})

        self.assertEqual(get_field(context, "is_subagent"), "true")
        self.assertEqual(get_field(context, "agent_type"), "subagent")

    def test_explicit_is_subagent_false_string(self):
        context = build_context("Stop", {"is_subagent": "false"})

        self.assertEqual(get_field(context, "is_subagent"), "false")
        self.assertEqual(get_field(context, "agent_type"), "main")

    def test_explicit_agent_type_subagent(self):
        context = build_context("Stop", {"agent_type": "subagent"})

        self.assertEqual(get_field(context, "is_subagent"), "true")
        self.assertEqual(get_field(context, "agent_type"), "subagent")

    def test_is_sidechain_payload_field(self):
        context = build_context("Stop", {"isSidechain": True})

        self.assertEqual(get_field(context, "is_subagent"), "true")
        self.assertEqual(get_field(context, "agent_type"), "subagent")

    def test_agent_id_payload_field(self):
        context = build_context("Stop", {"agentId": "abc123"})

        self.assertEqual(get_field(context, "is_subagent"), "true")
        self.assertEqual(get_field(context, "agent_type"), "subagent")

    def test_snake_case_agent_id_payload_field(self):
        context = build_context("Stop", {"agent_id": "abc123", "agent_type": "Explore"})

        self.assertEqual(get_field(context, "is_subagent"), "true")
        self.assertEqual(get_field(context, "agent_type"), "subagent")

    def test_subagent_evidence_overrides_explicit_false(self):
        context = build_context("Stop", {"is_subagent": False, "agent_id": "abc123"})

        self.assertEqual(get_field(context, "is_subagent"), "true")
        self.assertEqual(get_field(context, "agent_type"), "subagent")

    def test_null_session_and_transcript_are_empty(self):
        context = build_context("Stop", {"session_id": None, "transcript_path": None})

        self.assertEqual(context.session_id, "")
        self.assertEqual(context.transcript_path, "")

    def test_windows_transcript_path_subagents_segment_fallback(self):
        context = build_context("Stop", {"transcript_path": r"C:\Users\u\.claude\projects\p\subagents\agent.jsonl"})

        self.assertEqual(get_field(context, "is_subagent"), "true")
        self.assertEqual(get_field(context, "agent_type"), "subagent")

    def test_posix_transcript_path_subagents_segment_fallback(self):
        context = build_context("Stop", {"transcript_path": "/home/u/.claude/projects/p/subagents/agent.jsonl"})

        self.assertEqual(get_field(context, "is_subagent"), "true")
        self.assertEqual(get_field(context, "agent_type"), "subagent")

    def test_subagents_substring_does_not_match(self):
        context = build_context("Stop", {"transcript_path": "/tmp/my-subagents-log.jsonl"})

        self.assertEqual(get_field(context, "is_subagent"), "false")
        self.assertEqual(get_field(context, "agent_type"), "main")

    def test_rule_can_match_json_boolean_condition_value(self):
        context = build_context("Stop", {"transcript_path": "/tmp/main.jsonl"})
        rule = Rule(
            id="main-only",
            event="Stop",
            enabled=True,
            decision="warn",
            when=[{"field": "is_subagent", "op": "equals", "value": False}],
        )

        self.assertTrue(matches_rule(rule, context))


if __name__ == "__main__":
    unittest.main()
