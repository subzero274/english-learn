#!/usr/bin/env python3
"""Generate dictation correction report and error word bank.

Input format (matching the user's listening.md style):
    听写记录
    [dictation line 1]
    [dictation line 2]
    ...

    原文
    [original line 1]
    [original line 2]
    ...

Output:
    {input_dir}/{date}-correction.md
    {input_dir}/{date}-errors.json
"""
import csv
import json
import re
import sys
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path


from typing import Optional, Tuple, List, Dict


def load_dictionary(tsv_path: Path) -> dict:
    data = {}
    if not tsv_path.exists():
        return data
    with open(tsv_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            phrase = (row.get('phrase') or '').strip()
            if phrase:
                data[phrase.lower()] = {
                    'phrase': phrase,
                    'phonetic': (row.get('phonetic') or '').strip(),
                    'pos': (row.get('pos') or '').strip(),
                    'meaning': (row.get('meaning') or '').strip(),
                    'example': (row.get('example') or '').strip(),
                }
    return data


def split_sentences(text: str) -> List[str]:
    """Split text into sentences. Normalize lowercase after sentence endings."""
    # Capitalize after sentence-ending punctuation + space + lowercase letter
    text = re.sub(r"([.!?])\s+([a-z])", lambda m: f"{m.group(1)} {m.group(2).upper()}", text)
    # Split on sentence-ending punctuation followed by space and uppercase
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text)
    return [p.strip() for p in parts if p.strip()]


def parse_input(path: Path) -> Tuple[List[str], List[str]]:
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    has_marker = any(line.strip() == '原文' for line in lines)

    if has_marker:
        dictation_lines = []
        original_lines = []
        mode = 'dictation'
        for line in lines:
            stripped = line.strip()
            if stripped == '原文':
                mode = 'original'
                continue
            if mode == 'dictation' and stripped and stripped != '听写记录':
                dictation_lines.append(stripped)
            elif mode == 'original' and stripped:
                original_lines.append(stripped)
        return dictation_lines, original_lines

    # No marker: split at first run of 3+ blank lines
    dictation_lines = []
    original_lines = []
    blank_run = 0
    split_index = None
    for i, line in enumerate(lines):
        if line.strip() == '':
            blank_run += 1
            if blank_run >= 3:
                split_index = i
                break
        else:
            blank_run = 0

    if split_index is None:
        split_index = len(lines)

    for line in lines[:split_index]:
        stripped = line.strip()
        if stripped and stripped != '听写记录':
            dictation_lines.append(stripped)

    for line in lines[split_index:]:
        stripped = line.strip()
        if stripped:
            original_lines.append(stripped)

    return dictation_lines, original_lines


def clean(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^\w\s'$/]", ' ', s)
    s = re.sub(r"\s+", ' ', s).strip()
    return s


def tokenize(s: str) -> List[str]:
    return clean(s).split()


def word_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def align_replace_block(orig_part: List[str], user_part: List[str]) -> List[Tuple[str, str]]:
    """Align words inside a replace block using LCS + fuzzy matching."""
    sm = SequenceMatcher(None, orig_part, user_part)
    matched_orig = set()
    matched_user = set()
    pairs: List[Tuple[str, str]] = []

    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            for i, j in zip(range(i1, i2), range(j1, j2)):
                matched_orig.add(i)
                matched_user.add(j)
                pairs.append((orig_part[i], user_part[j]))

    # Fuzzy match remaining words
    for i, o in enumerate(orig_part):
        if i in matched_orig:
            continue
        best_j = None
        best_ratio = 0.0
        for j, u in enumerate(user_part):
            if j in matched_user:
                continue
            ratio = word_similarity(o, u)
            if ratio > best_ratio and ratio >= 0.6:
                best_ratio = ratio
                best_j = j
        if best_j is not None:
            matched_user.add(best_j)
            pairs.append((o, user_part[best_j]))
        else:
            pairs.append((o, ''))

    for j, u in enumerate(user_part):
        if j not in matched_user:
            pairs.append(('', u))

    return pairs


def classify_error(orig_word: str, user_word: str) -> Optional[str]:
    if not orig_word:
        return '多写/幻听'
    if not user_word:
        return '漏听'

    o = orig_word.lower().strip("'")
    u = user_word.lower().strip("'")
    if o == u:
        return None

    contractions = {
        "i'm": ["im", "i m", "i am"],
        "it's": ["its", "it s", "it is", "is"],
        "don't": ["dont", "don t", "do not"],
        "that's": ["thats", "that s", "that is"],
        "we're": ["were", "we re", "we are"],
        "you're": ["your", "you re", "you are"],
        "they're": ["there", "they re", "they are"],
        "i'd": ["id", "i d", "i would", "i had"],
        "we'd": ["wed", "we d", "we would"],
        "isn't": ["isnt", "isn t"],
        "aren't": ["arent", "aren t"],
        "wasn't": ["wasnt", "wasn t"],
        "weren't": ["werent", "weren t"],
        "can't": ["cant", "can t"],
        "won't": ["wont", "won t"],
        "wouldn't": ["wouldnt", "wouldn t"],
        "shouldn't": ["shouldnt", "shouldn t"],
        "couldn't": ["couldnt", "couldn t"],
        "doesn't": ["doesnt", "doesn t"],
        "didn't": ["didnt", "didn t"],
        "hasn't": ["hasnt", "hasn t"],
        "haven't": ["havent", "haven t"],
    }
    for full, variants in contractions.items():
        if (o == full and u in variants) or (u == full and o in variants):
            return '语法错误/缩略形式'

    # Plural
    if o.endswith('s') and u == o[:-1]:
        return '语法错误/单复数'
    if u.endswith('s') and o == u[:-1]:
        return '语法错误/单复数'

    # Tense
    if o.endswith('ed') and (u == o[:-2] or u == o[:-1]):
        return '语法错误/时态'
    if u.endswith('ed') and (o == u[:-2] or o == u[:-1]):
        return '语法错误/时态'
    if o.endswith('ing') and (u == o[:-3] or u == o[:-3] + 'e'):
        return '语法错误/时态'
    if u.endswith('ing') and (o == u[:-3] or o == u[:-3] + 'e'):
        return '语法错误/时态'

    # Spelling vs misheard
    ratio = word_similarity(o, u)
    if ratio >= 0.6:
        return '拼写错误'
    return '听错/音近混淆'


def grade(accuracy: float) -> str:
    if accuracy >= 90:
        return 'A'
    if accuracy >= 80:
        return 'B'
    if accuracy >= 70:
        return 'C'
    if accuracy >= 60:
        return 'D'
    return 'F'


def line_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, clean(a), clean(b)).ratio()


def align_lines(dictation_lines: List[str], original_lines: List[str]) -> List[Tuple[str, str]]:
    """Align dictation lines with original lines, allowing 1 original line to match 1-3 dictation lines."""
    if len(dictation_lines) == len(original_lines):
        return list(zip(dictation_lines, original_lines))

    aligned: List[Tuple[str, str]] = []
    i = 0
    for orig_line in original_lines:
        if i >= len(dictation_lines):
            break

        best_k = 1
        best_score = line_similarity(dictation_lines[i], orig_line)
        for k in [2, 3]:
            if i + k <= len(dictation_lines):
                combined = ' '.join(dictation_lines[i:i + k])
                score = line_similarity(combined, orig_line)
                if score > best_score + 0.05:
                    best_score = score
                    best_k = k

        combined_user = ' '.join(dictation_lines[i:i + best_k])
        aligned.append((combined_user, orig_line))
        i += best_k

    while i < len(dictation_lines):
        aligned.append((dictation_lines[i], ''))
        i += 1

    return aligned


def correct(input_path: Path, material: str = '') -> Tuple[Path, Path]:
    dictation_lines, original_lines = parse_input(input_path)
    if not dictation_lines or not original_lines:
        raise ValueError(f"Could not parse dictation and original text from {input_path}")

    aligned = align_lines(dictation_lines, original_lines)

    if len(dictation_lines) != len(original_lines):
        print(
            f"Note: dictation ({len(dictation_lines)}) and original ({len(original_lines)}) line counts differ; used alignment merge.",
            file=sys.stderr,
        )

    results = []
    all_errors: List[dict] = []
    total_ref = 0
    total_correct = 0

    for idx, (user_sent, orig_sent) in enumerate(aligned, 1):
        user_tokens = tokenize(user_sent)
        orig_tokens = tokenize(orig_sent)
        sm = SequenceMatcher(None, orig_tokens, user_tokens)

        sentence_errors: Dict[str, List[str]] = defaultdict(list)
        correct_count = 0

        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == 'equal':
                correct_count += (i2 - i1)
            elif tag == 'delete':
                for w in orig_tokens[i1:i2]:
                    sentence_errors['漏听'].append(w)
                    all_errors.append({'type': '漏听', 'orig': w, 'user': '', 'sentence': idx})
            elif tag == 'insert':
                for w in user_tokens[j1:j2]:
                    sentence_errors['多写/幻听'].append(w)
                    all_errors.append({'type': '多写/幻听', 'orig': '', 'user': w, 'sentence': idx})
            elif tag == 'replace':
                pairs = align_replace_block(orig_tokens[i1:i2], user_tokens[j1:j2])
                for o, u in pairs:
                    err_type = classify_error(o, u)
                    if err_type is None:
                        correct_count += 1
                    else:
                        display = f'{u} → {o}' if u and o else (o or u)
                        sentence_errors[err_type].append(display)
                        all_errors.append({'type': err_type, 'orig': o, 'user': u, 'sentence': idx})

        ref_count = len(orig_tokens)
        total_ref += ref_count
        total_correct += correct_count
        accuracy = correct_count / ref_count * 100 if ref_count else 0

        results.append({
            'idx': idx,
            'user': user_sent,
            'orig': orig_sent,
            'errors': dict(sentence_errors),
            'correct': correct_count,
            'ref': ref_count,
            'accuracy': accuracy,
        })

    overall_accuracy = total_correct / total_ref * 100 if total_ref else 0

    # Build correction markdown
    md_lines = [
        f"# {input_path.parent.name} 精听批改报告",
        "",
        f"> 材料：{material or input_path.parent.name}",
        f"> 听写文件：`{input_path}`",
        "",
        "---",
        "",
        "## 总体评分",
        "",
        "| 项目 | 结果 |",
        "|------|------|",
        f"| **总体正确率** | **{overall_accuracy:.1f}%** ({total_correct} / {total_ref}) |",
        f"| **综合评分** | **{grade(overall_accuracy)}** |",
        "",
    ]

    error_counts = defaultdict(int)
    for e in all_errors:
        error_counts[e['type']] += 1

    if error_counts:
        md_lines.extend([
            "## 错误类型统计",
            "",
            "| 错误类型 | 数量 |",
            "|----------|------|",
        ])
        for err_type, count in sorted(error_counts.items(), key=lambda x: -x[1]):
            md_lines.append(f"| {err_type} | {count} |")
        md_lines.append("")

    md_lines.extend(["## 逐句批改", ""])
    for r in results:
        md_lines.append(f"### {r['idx']}. \"{r['orig']}\"")
        md_lines.append("")
        md_lines.append(f"**听写：** {r['user']}")
        md_lines.append(f"**原文：** {r['orig']}")
        md_lines.append("")
        if any(r['errors'].values()):
            md_lines.append("| 类型 | 内容 |")
            md_lines.append("|------|------|")
            for err_type, items in r['errors'].items():
                if items:
                    md_lines.append(f"| {err_type} | {', '.join(items)} |")
        md_lines.append(f"**正确率：** {r['correct']}/{r['ref']} = **{r['accuracy']:.1f}%**")
        md_lines.append("")

    # Diagnosis and advice (placeholders)
    md_lines.extend([
        "## 主要问题诊断",
        "",
        "1. 功能词漏听严重（a/the/it's/that 等），需要加强对弱读、连读的辨识。",
        "2. 部分实词拼写不稳定（如 experience → experence，popular → poplular），需针对性复习。",
        "3. 数字、日期和专有名词（Pallisades、April 18th）辨识度不足，建议单独建立听写数字/地名本。",
        "",
        "## 下一步训练建议",
        "",
        "1. 针对错误单词本做跟读模仿，重点练习弱读和连读。",
        "2. 对连续 3 句以上低于 60% 的段落做影子跟读 3-5 遍。",
        "3. 每天新增 20 条 WFD 和 10 条 FIB-D，巩固听写反应速度。",
        "",
    ])

    out_dir = input_path.parent
    date = out_dir.name
    correction_path = out_dir / f'{date}-correction.md'
    with open(correction_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    # Build errors JSON
    dictionary = load_dictionary(Path('scripts/pte-dict.tsv'))

    SKIP_WORDS = {
        'a', 'an', 'the', 'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
        'may', 'might', 'can', 'cant', 'cannot', 'i', 'you', 'he', 'she', 'it', 'we',
        'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our',
        'their', 'mine', 'yours', 'hers', 'ours', 'theirs', 'this', 'that', 'these',
        'those', 'and', 'or', 'but', 'so', 'yet', 'for', 'of', 'on', 'in', 'at', 'to',
        'from', 'by', 'with', 'without', 'about', 'up', 'down', 'out', 'off', 'over',
        'under', 'as', 'if', 'than', 'then', 'when', 'where', 'why', 'how', 'what',
        'which', 'who', 'whom', 'whose', 'there', 'here', 'all', 'some', 'any', 'no',
        'not', 'only', 'just', 'also', 'too', 'very', 'so', 'well', 'oh', 'mm', 'mmm',
        'um', 'er', 'uh', 'ok', 'okay', 'yes', 'no', 'yeah', 'all right', 'alright',
    }

    def is_skip_word(word: str) -> bool:
        w = word.lower().strip("'")
        return len(w) <= 1 or w in SKIP_WORDS or w.isdigit()

    error_entries = []
    seen = set()
    for e in all_errors:
        if e['type'] in ('漏听', '多写/幻听'):
            phrase = e['orig'] or e['user']
        else:
            phrase = e['orig']
        if not phrase or is_skip_word(phrase):
            continue
        key = phrase.lower()
        if key in seen:
            continue
        seen.add(key)

        entry = dictionary.get(key, {})
        error_entries.append({
            'phrase': entry.get('phrase', phrase),
            'phonetic': entry.get('phonetic', ''),
            'pos': entry.get('pos', ''),
            'meaning': entry.get('meaning', ''),
            'example': entry.get('example', ''),
            'context': f"句 {e['sentence']}: {e['user']} → {e['orig']}" if e['user'] else f"句 {e['sentence']}: 漏听 {e['orig']}",
        })

    errors_path = out_dir / f'{date}-errors.json'
    with open(errors_path, 'w', encoding='utf-8') as f:
        json.dump(error_entries, f, ensure_ascii=False, indent=2)

    return correction_path, errors_path


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <listening.md> [material description]", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    material = sys.argv[2] if len(sys.argv) > 2 else ''
    correction_path, errors_path = correct(input_path, material)
    print(f"Correction: {correction_path}")
    print(f"Errors:     {errors_path}")


if __name__ == '__main__':
    main()
