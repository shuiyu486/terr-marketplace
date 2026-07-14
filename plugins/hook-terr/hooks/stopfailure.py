#!/usr/bin/env python3
import json
import os
import sys

PLUGIN_ROOT = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PLUGIN_ROOT not in sys.path:
    sys.path.insert(0, PLUGIN_ROOT)

from core.event_runner import run
from core.utf8 import configure_stdio


def main():
    try:
        configure_stdio()
        raw_input = sys.stdin.read()
        if not raw_input or not raw_input.strip():
            print(json.dumps({}, ensure_ascii=False), file=sys.stdout)
            return
        input_data = json.loads(raw_input.lstrip("﻿"))
        result = run("StopFailure", input_data)
        print(json.dumps(result, ensure_ascii=False), file=sys.stdout)
    except Exception as exc:
        print(f"hook-terr StopFailure error: {exc}", file=sys.stderr)
        print(json.dumps({}, ensure_ascii=False), file=sys.stdout)
    finally:
        sys.exit(0)


if __name__ == "__main__":
    main()
