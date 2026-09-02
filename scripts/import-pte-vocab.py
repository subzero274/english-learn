#!/usr/bin/env python3
"""Import PTE junior/mid vocabulary into an ielts-listening SQLite database.

Each word becomes a card under a PTE deck, with a tag distinguishing
junior/mid.  The script is idempotent: existing (deck, english) pairs
are skipped rather than duplicated.
"""
import argparse
import sqlite3
import sys
from pathlib import Path


DECK_NAMES = {
    'junior': 'PTE::Junior',
    'mid': 'PTE::Mid',
}

TAGS = {
    'junior': 'pte-junior',
    'mid': 'pte-mid',
}


def parse_wordlist(path: Path) -> list[str]:
    words = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip()
            if word:
                words.append(word)
    return words


def get_or_create_deck(conn: sqlite3.Connection, name: str) -> int:
    cur = conn.cursor()
    cur.execute('SELECT id FROM decks WHERE name = ?', (name,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute('INSERT INTO decks (name) VALUES (?)', (name,))
    conn.commit()
    return cur.lastrowid


def import_words(conn: sqlite3.Connection, deck_id: int, tag: str, words: list[str]) -> tuple[int, int]:
    cur = conn.cursor()
    inserted = 0
    skipped = 0

    # Build a set of existing english words for this deck to avoid duplicates
    cur.execute('SELECT english FROM cards WHERE deck_id = ?', (deck_id,))
    existing = {row[0] for row in cur.fetchall()}

    for word in words:
        if word in existing:
            skipped += 1
            continue
        cur.execute(
            """
            INSERT INTO cards (deck_id, notetype, english, chinese, audio_filename, audio_path, tags)
            VALUES (?, 'basic', ?, NULL, '', NULL, ?)
            """,
            (deck_id, word, tag),
        )
        existing.add(word)
        inserted += 1

    conn.commit()
    return inserted, skipped


def main():
    parser = argparse.ArgumentParser(description='Import PTE vocabulary into ielts-listening DB')
    parser.add_argument('--db', required=True, help='Path to ielts_listening.db')
    parser.add_argument('--junior', required=True, help='Path to junior vocabulary markdown file')
    parser.add_argument('--mid', required=True, help='Path to mid vocabulary markdown file')
    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        print(f"Database not found: {db_path}", file=sys.stderr)
        sys.exit(1)

    junior_path = Path(args.junior)
    mid_path = Path(args.mid)

    conn = sqlite3.connect(db_path)
    try:
        for level, path in [('junior', junior_path), ('mid', mid_path)]:
            if not path.exists():
                print(f"File not found: {path}; skipping.", file=sys.stderr)
                continue

            words = parse_wordlist(path)
            deck_name = DECK_NAMES[level]
            tag = TAGS[level]
            deck_id = get_or_create_deck(conn, deck_name)
            inserted, skipped = import_words(conn, deck_id, tag, words)
            print(f"{level}: {len(words)} words, {inserted} inserted, {skipped} skipped (deck '{deck_name}', tag '{tag}')")
    finally:
        conn.close()


if __name__ == '__main__':
    main()
