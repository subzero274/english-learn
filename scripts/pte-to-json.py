#!/usr/bin/env python3
"""Convert pte.md to pte.json using pte-dict.tsv as the meaning source."""
import csv
import json
import sys
from pathlib import Path


def load_dict(tsv_path: Path) -> dict:
    """Load phrase dictionary from TSV."""
    data = {}
    with open(tsv_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            phrase = row.get('phrase', '').strip()
            if not phrase:
                continue
            data[phrase.lower()] = {
                'phrase': phrase,
                'pos': (row.get('pos') or '').strip(),
                'meaning': (row.get('meaning') or '').strip(),
                'phonetic': (row.get('phonetic') or '').strip(),
                'example': (row.get('example') or '').strip(),
            }
    return data


def read_pte_tokens(path: Path) -> list:
    """Read pte.md and return unique tokens in original order."""
    tokens = []
    seen = set()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            for raw in line.split():
                raw = raw.strip()
                key = raw.lower()
                if raw and key not in seen:
                    seen.add(key)
                    tokens.append(raw)
    return tokens


def main():
    pte_path = Path('pte.md')
    dict_path = Path('scripts/pte-dict.tsv')
    out_path = Path('pte.json')

    if not pte_path.exists():
        print(f"{pte_path} not found", file=sys.stderr)
        sys.exit(1)

    if not dict_path.exists():
        print(f"{dict_path} not found", file=sys.stderr)
        sys.exit(1)

    dictionary = load_dict(dict_path)
    tokens = read_pte_tokens(pte_path)

    entries = []
    for token in tokens:
        entry = dictionary.get(token.lower(), {
            'phrase': token,
            'pos': '',
            'meaning': '',
            'phonetic': '',
            'example': '',
        })
        entries.append(entry)

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    print(f"Converted {len(entries)} entries to {out_path}")
    missing = sum(1 for e in entries if not e.get('meaning'))
    print(f"Entries with meaning: {len(entries) - missing}/{len(entries)}")


if __name__ == '__main__':
    main()
