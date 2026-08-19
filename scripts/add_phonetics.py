#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add phonetics to vocabulary-test-audio.html by merging data from vocabulary.md
"""
import re
import json
from pathlib import Path


def parse_vocabulary_md(md_path):
    """Parse vocabulary.md to extract word -> phonetic mapping"""
    text = Path(md_path).read_text(encoding='utf-8')

    # Match table rows: | **word** | /phonetic/ | ... |
    pattern = r'\|\s*\*\*([^*|]+)\*\*\s*\|\s*([^|]+)\s*\|'
    matches = re.findall(pattern, text)

    phonetics = {}
    for word, phonetic in matches:
        word = word.strip()
        phonetic = phonetic.strip()
        if phonetic and phonetic.startswith('/'):
            phonetics[normalize_word(word)] = phonetic

    return phonetics


def normalize_word(word):
    return word.lower().strip().replace('​', '')


def parse_html_words(html_path):
    """Parse current HTML to extract word objects"""
    text = Path(html_path).read_text(encoding='utf-8')

    # Find the words array
    match = re.search(r'const words = \[(.*?)\];', text, re.DOTALL)
    if not match:
        raise ValueError("Could not find words array in HTML")

    words_text = match.group(1)

    # Parse individual word objects
    word_pattern = r"\{\s*word:\s*'([^']+)'\s*,\s*meaning:\s*'([^']+)'\s*,\s*example:\s*\"([^\"]+)\"\s*\}"
    words = []
    for m in re.finditer(word_pattern, words_text):
        words.append({
            'word': m.group(1),
            'meaning': m.group(2),
            'example': m.group(3)
        })

    return words


def merge_phonetics(words, phonetics):
    """Add phonetic to each word if found"""
    missing = []
    for word in words:
        key = normalize_word(word['word'])
        if key in phonetics:
            word['phonetic'] = phonetics[key]
        else:
            word['phonetic'] = ''
            missing.append(word['word'])

    return missing


def generate_html(words, template_path, output_path):
    """Generate new HTML with phonetics"""
    template = Path(template_path).read_text(encoding='utf-8')

    # Generate new words array with phonetic field
    word_lines = []
    for w in words:
        word = w['word'].replace("'", "\\'")
        meaning = w['meaning'].replace("'", "\\'")
        example = w['example'].replace('\\', '\\\\').replace('"', '\\"')
        phonetic = w.get('phonetic', '').replace("'", "\\'")

        if phonetic:
            line = f"            {{ word: '{word}', phonetic: '{phonetic}', meaning: '{meaning}', example: \"{example}\" }}"
        else:
            line = f"            {{ word: '{word}', meaning: '{meaning}', example: \"{example}\" }}"
        word_lines.append(line)

    words_array = "const words = [\n" + ",\n".join(word_lines) + "\n        ];"

    # Replace old words array
    new_html = re.sub(r'const words = \[.*?\];', words_array, template, flags=re.DOTALL)

    # Update learn card template to show phonetic
    old_card = '''<div class="card-meaning">${item.meaning}</div>'''
    new_card = '''<div class="card-phonetic">${item.phonetic || ''}</div>
                    <div class="card-meaning">${item.meaning}</div>'''
    new_html = new_html.replace(old_card, new_card)

    # Add CSS for phonetic
    css_addition = '''
        .learn-card .card-phonetic {
            font-size: 13px;
            color: #888;
            font-family: "Arial Unicode MS", "Lucida Sans Unicode", sans-serif;
            margin: 4px 0;
            padding: 3px 10px;
            background: #f0f0f0;
            border-radius: 4px;
            display: inline-block;
        }'''

    # Insert before .learn-card .card-meaning CSS
    new_html = new_html.replace('.learn-card .card-meaning {', css_addition + '\n        .learn-card .card-meaning {', 1)

    Path(output_path).write_text(new_html, encoding='utf-8')


if __name__ == '__main__':
    base_dir = Path('/Users/qianduoduo/.openclaw/workspace/english-listening/listening/class-4')

    md_path = base_dir / 'vocabulary.md'
    html_path = base_dir / 'vocabulary-test-audio.html'
    output_path = html_path

    phonetics = parse_vocabulary_md(md_path)
    words = parse_html_words(html_path)
    missing = merge_phonetics(words, phonetics)

    generate_html(words, html_path, output_path)

    print(f"Processed {len(words)} words")
    if missing:
        print(f"Missing phonetics for {len(missing)} words:")
        for w in missing:
            print(f"  - {w}")
    else:
        print("All words have phonetics")
