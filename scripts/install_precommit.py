#!/usr/bin/env python3
import os
import sys
from pathlib import Path
import textwrap

# Centralized hook scripts directory
HOOKS_SRC = Path("hooks")  # e.g., hooks/pre-commit, hooks/pre-push

# Git hooks directory
HOOKS_DEST = Path(".git/hooks")

# Windows batch wrapper template
BATCH_TEMPLATE = textwrap.dedent(r"""
    @echo off
    REM Auto-generated Git hook wrapper
    python "%~dp0..\..\{hook_path}" %*
""")


def create_symlink(src: Path, dest: Path):
    """Create or replace symlink on Linux/macOS"""
    if dest.exists() or dest.is_symlink():
        dest.unlink()
    os.symlink(src.resolve(), dest)
    print(f"Symlink created: {dest} -> {src}")


def create_batch_wrapper(src: Path, dest: Path):
    """Create Windows batch file wrapper"""
    content = BATCH_TEMPLATE.format(hook_path=src.as_posix())
    with open(dest.with_suffix(".bat"), "w") as f:
        f.write(content.strip() + "\n")
    print(f"Batch wrapper created: {dest.with_suffix('.bat')}")


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
