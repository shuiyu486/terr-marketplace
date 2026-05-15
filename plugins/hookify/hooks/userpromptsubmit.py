#!/usr/bin/env python3
"""UserPromptSubmit hook executor for hookify plugin.

This script is called by Claude Code when user submits a prompt.
It reads .claude/hookify.*.local.md files and evaluates rules.
"""

import os
import sys
import json

# Add plugin root to Python path for imports
PLUGIN_ROOT = os.environ.get('CLAUDE_PLUGIN_ROOT')
if PLUGIN_ROOT and PLUGIN_ROOT not in sys.path:
    sys.path.insert(0, PLUGIN_ROOT)

try:
    from core.config_loader import load_rules
    from core.rule_engine import RuleEngine
except ImportError as e:
    error_msg = {"systemMessage": f"Hookify import error: {e}"}
    print(json.dumps(error_msg), file=sys.stdout)
    sys.exit(0)


def _dump_debug(hook_name, raw_input, error):
    """Save malformed JSON input for diagnosis, then output clean error."""
    import time
    debug_dir = os.path.join(os.path.expanduser('~'), '.claude', 'hookify-debug')
    os.makedirs(debug_dir, exist_ok=True)
    debug_path = os.path.join(debug_dir, f'{hook_name}-input-error-{int(time.time())}.json')
    with open(debug_path, 'w', encoding='utf-8') as f:
        f.write(raw_input)
    error_output = {
        "systemMessage": (
            f"Hookify {hook_name}: JSON parse error at column {error.colno}. "
            f"Raw input saved to {debug_path}"
        )
    }
    print(json.dumps(error_output), file=sys.stdout)


def main():
    """Main entry point for UserPromptSubmit hook."""
    try:
        # Read input from stdin
        raw_input = sys.stdin.read()

        if not raw_input or not raw_input.strip():
            print(json.dumps({}), file=sys.stdout)
            return

        try:
            input_data = json.loads(raw_input)
        except json.JSONDecodeError as e:
            _dump_debug("UserPromptSubmit", raw_input, e)
            return

        # Load user prompt rules
        rules = load_rules(event='prompt')

        # Evaluate rules
        engine = RuleEngine()
        result = engine.evaluate_rules(rules, input_data)

        # Always output JSON (even if empty)
        print(json.dumps(result), file=sys.stdout)

    except Exception as e:
        error_output = {
            "systemMessage": f"Hookify error: {str(e)}"
        }
        print(json.dumps(error_output), file=sys.stdout)

    finally:
        # ALWAYS exit 0
        sys.exit(0)


if __name__ == '__main__':
    main()
