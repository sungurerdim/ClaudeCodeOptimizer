#!/usr/bin/env python3
"""Cross-platform hook script to load core rules at session start."""

import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
rules_path = os.path.join(script_dir, "core-rules.json")

try:
    with open(rules_path, encoding="utf-8") as f:
        sys.stdout.write(f.read())
except FileNotFoundError:
    print(f"core-rules.json not found at {rules_path}", file=sys.stderr)
    sys.exit(1)
except OSError as e:
    print(f"Failed to read core-rules.json: {e}", file=sys.stderr)
    sys.exit(1)
