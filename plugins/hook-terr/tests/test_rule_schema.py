import os
import sys
import unittest

PLUGIN_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PLUGIN_ROOT not in sys.path:
    sys.path.insert(0, PLUGIN_ROOT)

from core.schema import validate_rule, validate_settings


class RuleSchemaTests(unittest.TestCase):
    def base_rule(self):
        return {
            "version": 1,
            "id": "test-rule",
            "enabled": True,
            "event": "Stop",
            "decision": "warn",
            "priority": 100,
            "match": "all",
            "when": [],
            "message": {"text": "message"},
            "notify": {"enabled": False},
        }

    def errors_for(self, **updates):
        rule = self.base_rule()
        rule.update(updates)
        return validate_rule(rule, "rule.json")

    def test_enabled_must_be_boolean(self):
        errors = self.errors_for(enabled="false")

        self.assertIn("rule.json: enabled must be a boolean", errors)

    def test_priority_must_be_integer(self):
        errors = self.errors_for(priority="high")

        self.assertIn("rule.json: priority must be an integer", errors)

    def test_event_and_decision_must_be_strings(self):
        errors = self.errors_for(event=[], decision=[])

        self.assertIn("rule.json: event must be a string", errors)
        self.assertIn("rule.json: decision must be a string", errors)

    def test_match_must_be_known_value(self):
        errors = self.errors_for(match="ayn")

        self.assertIn("rule.json: match must be one of all, any", errors)

    def test_match_must_be_string(self):
        errors = self.errors_for(match=[])

        self.assertIn("rule.json: match must be a string", errors)

    def test_message_and_notify_must_be_objects(self):
        errors = self.errors_for(message="message", notify="notify")

        self.assertIn("rule.json: message must be an object", errors)
        self.assertIn("rule.json: notify must be an object", errors)

    def test_notify_enabled_must_be_boolean(self):
        errors = self.errors_for(notify={"enabled": "true"})

        self.assertIn("rule.json: notify.enabled must be a boolean", errors)

    def test_notify_channels_must_contain_strings(self):
        errors = self.errors_for(notify={"channels": [[]]})

        self.assertIn("rule.json: notify.channels must contain only strings", errors)

    def test_agent_context_fields_are_allowed_in_conditions(self):
        rule = self.base_rule()
        rule["when"] = [
            {"field": "is_subagent", "op": "equals", "value": False},
            {"field": "agent_type", "op": "equals", "value": "main"},
        ]

        self.assertEqual(validate_rule(rule, "rule.json"), [])

    def test_condition_operator_must_be_string(self):
        rule = self.base_rule()
        rule["when"] = [{"field": "cwd", "op": [], "value": "x"}]

        errors = validate_rule(rule, "rule.json")

        self.assertIn("rule.json: condition 0 operator must be a string", errors)

    def test_stop_failure_rule_event_is_allowed(self):
        self.assertEqual(self.errors_for(event="StopFailure"), [])

    def test_api_error_recovery_settings_are_allowed(self):
        settings = {
            "features": {
                "apiErrorRecovery": {
                    "enabled": True,
                    "terminal": "wezterm",
                    "strategy": "escalate_then_restore",
                    "windowSeconds": 600,
                    "restoreAfterSeconds": 600,
                    "sendDelayMs": 800,
                    "match": ["cybersecurity risk"],
                    "primaryModelCommand": "/model opus",
                    "fallbackModelCommand": "/model sonnet",
                    "continueCommand": "continue",
                    "maxEscalations": 1,
                    "lockTimeoutSeconds": 30,
                    "dedupeSeconds": 5,
                    "requireSamePaneForRestore": True,
                }
            }
        }

        self.assertEqual(validate_settings(settings), [])

    def test_api_error_recovery_rejects_invalid_settings(self):
        settings = {
            "features": {
                "apiErrorRecovery": {
                    "enabled": "yes",
                    "terminal": "windows_terminal",
                    "strategy": "always_switch",
                    "windowSeconds": 0,
                    "sendDelayMs": -1,
                    "match": [1],
                    "requireSamePaneForRestore": "true",
                }
            }
        }

        errors = validate_settings(settings)

        self.assertIn("settings.features.apiErrorRecovery.enabled must be a boolean", errors)
        self.assertIn("settings.features.apiErrorRecovery.terminal must be wezterm", errors)
        self.assertIn("settings.features.apiErrorRecovery.strategy must be escalate_then_restore", errors)
        self.assertIn("settings.features.apiErrorRecovery.windowSeconds must be a positive integer", errors)
        self.assertIn("settings.features.apiErrorRecovery.sendDelayMs must be a non-negative number", errors)
        self.assertIn("settings.features.apiErrorRecovery.match must contain only strings", errors)
        self.assertIn("settings.features.apiErrorRecovery.requireSamePaneForRestore must be a boolean", errors)


if __name__ == "__main__":
    unittest.main()
