#!/usr/bin/env python3
"""Verify that a daily training commit meets the required quotas.

Requirements for a training commit:
  1. At least one new/modified intensive listening practice.
  2. At least 20 new Write From Dictation (WFD) records.
  3. At least 10 new Fill in the Blanks - Drag & Drop (FIB-D) records.

Supported locations:
  - 精听练习：listening/精听训练/ 或 daily-trainning/YYYYMMDD/
  - WFD：PTE/wfd.md 或 daily-trainning/YYYYMMDD/wfd.md
  - FIB-D：PTE/fib-d.md 或 daily-trainning/YYYYMMDD/fib-d.md

If no training files are staged, the commit is allowed (useful for docs/infra commits).
"""
import subprocess
import sys
from pathlib import Path

WFD_MIN = 20
FIBD_MIN = 10

INTENSIVE_LISTENING_PREFIXES = [
    'listening/精听训练/',
    'daily-trainning/',
]

WFD_CANDIDATES = [
    Path('PTE/wfd.md'),
]

FIBD_CANDIDATES = [
    Path('PTE/fib-d.md'),
]


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout


def staged_files() -> list[str]:
    return run(['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM']).splitlines()


def file_content_at(path: Path, ref: str) -> str:
    """Read file content from a git ref (e.g. 'HEAD' or ':0')."""
    try:
        return run(['git', 'show', f'{ref}:{path}'])
    except subprocess.CalledProcessError:
        return ''


def count_records(text: str) -> int:
    """Count records. One record = two consecutive non-empty content lines.

    Only lines after the first '## 训练记录' heading are counted.
    Markdown syntax lines (headings, blockquotes, fences, separators) are ignored.
    """
    lines = text.splitlines()
    start_index = 0
    for i, line in enumerate(lines):
        if line.strip() == '## 训练记录':
            start_index = i + 1
            break

    content_lines = []
    for line in lines[start_index:]:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('#'):
            continue
        if stripped.startswith('>'):
            continue
        if stripped.startswith('```'):
            continue
        if stripped in ('---', '***', '___'):
            continue
        content_lines.append(stripped)

    return len(content_lines) // 2


def find_daily_trainning_files(pattern: str) -> list[Path]:
    """Find files matching pattern under daily-trainning/YYYYMMDD/ directories."""
    base = Path('daily-trainning')
    if not base.exists():
        return []
    return sorted(p for p in base.rglob(pattern) if p.is_file())


def wfd_paths() -> list[Path]:
    return WFD_CANDIDATES + find_daily_trainning_files('wfd.md')


def fibd_paths() -> list[Path]:
    return FIBD_CANDIDATES + find_daily_trainning_files('fib-d.md')


def check_intensive_listening(staged: list[str]) -> bool:
    return any(p.startswith(prefix) for p in staged for prefix in INTENSIVE_LISTENING_PREFIXES)


def count_added_records(path: Path, staged: list[str]) -> int:
    key = str(path)
    if key not in staged:
        return 0
    before = count_records(file_content_at(path, 'HEAD'))
    after = count_records(file_content_at(path, ':0'))
    return max(0, after - before)


def total_added_records(candidates: list[Path], staged: list[str]) -> tuple[int, list[Path]]:
    total = 0
    updated = []
    for path in candidates:
        added = count_added_records(path, staged)
        if added > 0:
            total += added
            updated.append(path)
    return total, updated


def is_training_commit(staged: list[str]) -> bool:
    prefixes = INTENSIVE_LISTENING_PREFIXES + [str(p) for p in wfd_paths() + fibd_paths()]
    return any(p.startswith(prefix) for p in staged for prefix in prefixes)


def main() -> int:
    staged = staged_files()

    if not staged:
        print('No staged changes. Skip daily-commit verification.')
        return 0

    if not is_training_commit(staged):
        print('Not a training commit. Skip daily-commit verification.')
        return 0

    errors = []

    # 1. Intensive listening
    if not check_intensive_listening(staged):
        errors.append(
            '缺少新的精听练习：请在 listening/精听训练/ 或 daily-trainning/YYYYMMDD/ 下新增或修改听写材料。'
        )

    # 2. WFD
    wfd_total, wfd_updated = total_added_records(wfd_paths(), staged)
    if wfd_updated and wfd_total < WFD_MIN:
        errors.append(
            f'WFD 训练记录不足：本次提交新增 {wfd_total} 条，要求至少 {WFD_MIN} 条。'
        )
    elif not wfd_updated:
        errors.append(
            f'未更新 WFD 记录：请在 PTE/wfd.md 或 daily-trainning/YYYYMMDD/wfd.md 中新增 {WFD_MIN} 条。'
        )

    # 3. FIB-D
    fibd_total, fibd_updated = total_added_records(fibd_paths(), staged)
    if fibd_updated and fibd_total < FIBD_MIN:
        errors.append(
            f'FIB-D 训练记录不足：本次提交新增 {fibd_total} 条，要求至少 {FIBD_MIN} 条。'
        )
    elif not fibd_updated:
        errors.append(
            f'未更新 FIB-D 记录：请在 PTE/fib-d.md 或 daily-trainning/YYYYMMDD/fib-d.md 中新增 {FIBD_MIN} 条。'
        )

    if errors:
        print('❌ 每日提交校验未通过：')
        for e in errors:
            print(f'  • {e}')
        print()
        print('提示：如本次为非训练类提交，可使用 git commit --no-verify 跳过校验。')
        return 1

    print('✅ 每日提交校验通过：')
    print(f'  • 精听练习：已更新')
    print(f'  • WFD 新增：{wfd_total} 条')
    print(f'  • FIB-D 新增：{fibd_total} 条')
    return 0


if __name__ == '__main__':
    sys.exit(main())
