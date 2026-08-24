#!/usr/bin/env python3
"""Install git hooks from .githooks into .git/hooks."""
import shutil
import stat
import sys
from pathlib import Path


def main():
    source_dir = Path('.githooks')
    target_dir = Path('.git/hooks')

    if not source_dir.exists():
        print(f"{source_dir} not found", file=sys.stderr)
        sys.exit(1)

    if not target_dir.exists():
        print("Not a git repository or .git/hooks missing", file=sys.stderr)
        sys.exit(1)

    installed = []
    for hook in source_dir.iterdir():
        if hook.name.startswith('.'):
            continue
        target = target_dir / hook.name
        shutil.copy2(hook, target)
        target.chmod(target.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        installed.append(hook.name)

    if installed:
        print(f"Installed git hooks: {', '.join(installed)}")
    else:
        print("No hooks to install.")


if __name__ == '__main__':
    main()
