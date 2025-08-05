#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Centralized hook scripts directory (relative to repo root)
HOOKS_SRC = Path("hooks")

# Git hooks directory
HOOKS_DEST = Path(".git/hooks")


def create_symlink(src: Path, dest: Path):
    """Create or replace symlink on Linux/macOS"""
    if dest.exists() or dest.is_symlink():
        dest.unlink()
    os.symlink(src.resolve(), dest)
    print(f"Symlink created: {dest} -> {src}")


def create_batch_wrapper(src: Path, dest: Path):
    """
    Create a Windows batch file wrapper pointing to the Python hook script.
    Path is relative: .git/hooks -> ../hooks/<hook_name>
    """
    hook_name = src.name
    batch_content = f"""@echo off
REM Auto-generated Git hook wrapper
python "%~dp0..\\hooks\\{hook_name}" %*
"""
    wrapper_path = dest.with_suffix(".bat")
    with open(wrapper_path, "w") as f:
        f.write(batch_content)
    print(f"Batch wrapper created: {wrapper_path}")


def install_hooks():
    if not HOOKS_SRC.exists():
        print(f"Error: {HOOKS_SRC} directory does not exist.")
        sys.exit(1)

    HOOKS_DEST.mkdir(parents=True, exist_ok=True)

    for hook_script in HOOKS_SRC.iterdir():
        if not hook_script.is_file():
            continue

        dest = HOOKS_DEST / hook_script.name

        if sys.platform.startswith(("linux", "darwin")):
            create_symlink(hook_script, dest)
        elif sys.platform.startswith("win"):
            create_batch_wrapper(hook_script, dest)
        else:
            print(f"Unsupported platform: {sys.platform}")
            sys.exit(1)


if __name__ == "__main__":
    install_hooks()
