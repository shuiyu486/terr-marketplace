import os
import sys
import unittest

PLUGIN_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PLUGIN_ROOT not in sys.path:
    sys.path.insert(0, PLUGIN_ROOT)

from core.schema import validate_rule


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

    def test_condition_operator_must_be_string(self):
        rule = self.base_rule()
        rule["when"] = [{"field": "cwd", "op": [], "value": "x"}]

        errors = validate_rule(rule, "rule.json")

        self.assertIn("rule.json: condition 0 operator must be a string", errors)


if __name__ == "__main__":
    unittest.main()
