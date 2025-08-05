#!/usr/bin/env python3
import os
import sys
import shutil
from pathlib import Path

HOOKS_SRC = Path("hooks")

HOOKS_DEST = Path(".git/hooks")


def create_symlink(src: Path, dest: Path):
    """Create or replace symlink on Linux/macOS"""
    if dest.exists() or dest.is_symlink():
        dest.unlink()
    os.symlink(src.resolve(), dest)
    print(f"Symlink created: {dest} -> {src}")


def copy_hook(src: Path, dest: Path):
    """Copy hook file on Windows"""
    if dest.exists():
        dest.unlink()
    shutil.copyfile(src, dest)
    print(f"Copied hook to {dest}")


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
            copy_hook(hook_script, dest)
        else:
            print(f"Unsupported platform: {sys.platform}")
            sys.exit(1)


if __name__ == "__main__":
    install_hooks()
