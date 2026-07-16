import os
import sys
import unittest
from unittest.mock import patch

PLUGIN_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PLUGIN_ROOT not in sys.path:
    sys.path.insert(0, PLUGIN_ROOT)

from core.action_executor import execute, resolve_channels, stop_channels
from core.models import HookContext, Rule
from core.response_builder import build_response


class ResponseBuilderTests(unittest.TestCase):
    def block_rule(self):
        return Rule(id="block", event="PreToolUse", enabled=True, decision="block")

    def test_pre_tool_use_block_uses_permission_protocol(self):
        response = build_response("PreToolUse", self.block_rule(), "denied")

        output = response["hookSpecificOutput"]
        self.assertEqual(output["hookEventName"], "PreToolUse")
        self.assertEqual(output["permissionDecision"], "deny")
        self.assertEqual(output["permissionDecisionReason"], "denied")

    def test_post_tool_use_block_uses_top_level_protocol(self):
        response = build_response("PostToolUse", self.block_rule(), "stop turn")

        self.assertEqual(response["decision"], "block")
        self.assertEqual(response["reason"], "stop turn")
        self.assertNotIn("hookSpecificOutput", response)

    def test_user_prompt_submit_block_uses_top_level_protocol(self):
        response = build_response("UserPromptSubmit", self.block_rule(), "reject prompt")

        self.assertEqual(response["decision"], "block")
        self.assertEqual(response["reason"], "reject prompt")

    def test_popup_config_title_is_used_when_rule_has_no_title(self):
        rule = Rule(
            id="notify",
            event="Stop",
            enabled=True,
            decision="allow",
            notify={"enabled": True, "channels": ["popup"], "text": "message"},
        )
        settings = {"notifications": {"popup": {"enabled": True, "title": "Configured Title"}}}

        with patch("core.action_executor.send_notification") as send_notification:
            execute(rule, HookContext("Stop"), settings)

        self.assertEqual(send_notification.call_args.args[1], "Configured Title")

    def test_rule_title_overrides_popup_config_title(self):
        rule = Rule(
            id="notify",
            event="Stop",
            enabled=True,
            decision="allow",
            notify={"enabled": True, "channels": ["popup"], "title": "Rule Title"},
        )
        settings = {"notifications": {"popup": {"enabled": True, "title": "Configured Title"}}}

        with patch("core.action_executor.send_notification") as send_notification:
            execute(rule, HookContext("Stop"), settings)

        self.assertEqual(send_notification.call_args.args[1], "Rule Title")

    def test_notification_channels_are_stably_deduplicated(self):
        rule = self.block_rule()
        rule.notify = {"channels": ["sound", "sound", "popup"]}
        settings = {"events": {"Stop": {"notifications": ["popup", "popup", "sound"]}}}

        self.assertEqual(resolve_channels(rule, HookContext("Stop"), settings), ["sound", "popup"])
        self.assertEqual(stop_channels(settings), ["popup", "sound"])


if __name__ == "__main__":
    unittest.main()
