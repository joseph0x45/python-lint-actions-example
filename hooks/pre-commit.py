#!/usr/bin/env python3
import subprocess
import sys

checks = [
    ["ruff", "check", "."],
    ["mypy", "--install-types", "--non-interactive", "."],
    ["pyright"],
]

print("Running pre-commit checks...\n")

for cmd in checks:
    print(f"> {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"✖ {' '.join(cmd)} failed. Aborting commit.")
        sys.exit(result.returncode)

print("\n✔ All checks passed. Proceeding with commit.")
