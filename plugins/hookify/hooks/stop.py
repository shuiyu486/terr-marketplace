#!/usr/bin/env python3
"""Stop hook executor for hookify plugin.

This script is called by Claude Code when agent wants to stop.
It reads .claude/hookify.*.local.md files and evaluates stop rules.
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


def main():
    """Main entry point for Stop hook."""
    try:
        # Reconfigure stdio for UTF-8 — the harness always sends/receives UTF-8
        sys.stdin.reconfigure(encoding='utf-8')
        sys.stdout.reconfigure(encoding='utf-8')

        # Read input from stdin
        raw_input = sys.stdin.read()

        if not raw_input or not raw_input.strip():
            print(json.dumps({}), file=sys.stdout)
            return

        try:
            input_data = json.loads(raw_input)
        except json.JSONDecodeError as e:
            # Dump malformed input to debug file for diagnosis
            debug_dir = os.path.join(os.path.expanduser('~'), '.claude', 'hookify-debug')
            os.makedirs(debug_dir, exist_ok=True)
            import time
            debug_path = os.path.join(debug_dir, f'stop-input-error-{int(time.time())}.json')
            try:
                with open(debug_path, 'w', encoding='utf-8') as f:
                    f.write(raw_input)
            except (UnicodeEncodeError, UnicodeDecodeError, OSError):
                # If UTF-8 encoding fails (e.g., raw bytes that can't be represented),
                # write as raw bytes instead
                try:
                    with open(debug_path, 'wb') as f:
                        f.write(raw_input.encode('utf-8', errors='surrogateescape'))
                except Exception:
                    pass  # Last resort: accept debug data loss
            # Show clean error pointing to debug file
            error_output = {
                "systemMessage": (
                    f"Hookify Stop: JSON parse error at column {e.colno}. "
                    f"Raw input saved to {debug_path} for diagnosis."
                )
            }
            print(json.dumps(error_output), file=sys.stdout)
            return

        # Load stop rules
        rules = load_rules(event='stop')

        # Evaluate rules
        engine = RuleEngine()
        result = engine.evaluate_rules(rules, input_data)

        # Always output JSON (even if empty)
        print(json.dumps(result), file=sys.stdout)

    except Exception as e:
        # On any error, allow the operation
        error_output = {
            "systemMessage": f"Hookify error: {str(e)}"
        }
        print(json.dumps(error_output), file=sys.stdout)

    finally:
        # ALWAYS exit 0
        sys.exit(0)


if __name__ == '__main__':
    main()
