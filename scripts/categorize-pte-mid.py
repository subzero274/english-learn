#!/usr/bin/env python3
"""Categorize PTE mid vocabulary by meaning using WordNet.

Outputs grouped markdown files under PTE/vocabulary-mid/.
Each group contains at most 200 words.
"""
import os
from collections import defaultdict
from pathlib import Path

from nltk.corpus import wordnet as wn


MID_VOCAB = Path(__file__).resolve().parent.parent / "PTE" / "vocabulary-mid.md"
OUT_DIR = Path(__file__).resolve().parent.parent / "PTE" / "vocabulary-mid"

OCCUPATION_HYPERNYMS = {
    'professional', 'worker', 'employee', 'employer', 'skilled_worker', 'leader',
    'expert', 'artist', 'musician', 'politician', 'student', 'patient', 'official',
    'athlete', 'writer', 'scientist', 'teacher', 'doctor', 'engineer', 'candidate',
    'client', 'buyer', 'consumer', 'partner', 'delegate', 'manager', 'director',
    'officer', 'minister', 'agent', 'interpreter', 'translator', 'scholar', 'lecturer',
    'editor', 'analyst', 'archaeologist', 'retailer', 'historian', 'speaker', 'author',
    'pilot', 'developer', 'programmer', 'psychologist', 'volunteer', 'physician', 'nurse',
    'hunter', 'farmer', 'cook', 'painter', 'actor', 'novelist', 'poet', 'philosopher',
    'judge', 'lawyer', 'criminal', 'immigrant', 'settler', 'tourist', 'traveler',
    'visitor', 'resident', 'teenager', 'teen', 'adult', 'infant', 'newborn', 'senior',
    'peer', 'colleague', 'parent', 'mother', 'father', 'sibling', 'brother', 'sister',
    'daughter', 'child', 'baby'
}

# Prefer concrete noun senses over person/abstract senses for ambiguous words.
PREFERRED_LEX = {'noun.animal', 'noun.plant', 'noun.food', 'noun.body', 'noun.substance'}

CATEGORY_ORDER = [
    'noun.communication',
    'adj.all',
    'noun.act',
    'noun.artifact',
    'noun.person_identity',
    'noun.cognition',
    'verb_communication_cognition',
    'adv.all',
    'verb_change_action',
    'noun.substance',
    'noun.group',
    'noun.attribute',
    'noun.state',
    'noun.person_occupation',
    'noun.location',
    'noun.animal',
    'noun.body',
    'noun.food',
    'noun.time',
    'adj.pert',
    'unknown',
    'noun.event',
    'noun.object',
    'noun.plant',
    'noun.quantity',
    'noun.possession',
    'abstract_misc',
]

CATEGORY_TITLES = {
    'noun.communication': '交流与语言',
    'adj.all': '描述与特征（形容词）',
    'noun.act': '行为与活动',
    'noun.artifact': '物品与器具',
    'noun.person_identity': '人物 / 身份与群体',
    'noun.cognition': '认知与思维',
    'verb_communication_cognition': '交流与认知动词',
    'adv.all': '程度与方式（副词）',
    'verb_change_action': '变化与动作动词',
    'noun.substance': '物质与材料',
    'noun.group': '群体与组织',
    'noun.attribute': '属性与特征（名词）',
    'noun.state': '状态与情况',
    'noun.person_occupation': '人物 / 职业与角色',
    'noun.location': '地点与方位',
    'noun.animal': '动物',
    'noun.body': '身体部位',
    'noun.food': '食物',
    'noun.time': '时间与时间相关',
    'adj.pert': '关联与派生形容词',
    'unknown': '专有名词与特殊词汇',
    'noun.event': '事件',
    'noun.object': '自然物体',
    'noun.plant': '植物',
    'noun.quantity': '数量与度量',
    'noun.possession': '拥有与财产',
    'abstract_misc': '抽象、现象与总称',
}

ABSTRACT_MISC_KEYS = {
    'noun.phenomenon', 'noun.process', 'noun.feeling', 'noun.Tops',
    'noun.shape', 'noun.motive', 'noun.relation'
}


def load_words(path: Path) -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


def person_subcategory(word: str, syn) -> str:
    hypernyms = set()
    for h in syn.hypernyms():
        hypernyms.update(l.name().lower() for l in h.lemmas())
        for hh in h.hypernyms():
            hypernyms.update(l.name().lower() for l in hh.lemmas())
    if hypernyms & OCCUPATION_HYPERNYMS:
        return 'noun.person_occupation'
    return 'noun.person_identity'


def categorize(word: str) -> str:
    synsets = wn.synsets(word)
    if not synsets:
        return 'unknown'

    nouns = [s for s in synsets if s.pos() == 'n']
    for s in nouns:
        if s.lexname() in PREFERRED_LEX:
            return s.lexname()

    chosen = nouns or [s for s in synsets if s.pos() == 'a'] or [s for s in synsets if s.pos() == 'v'] or synsets
    s = chosen[0]
    lexname = s.lexname()

    if lexname == 'noun.person':
        return person_subcategory(word, s)
    if lexname.startswith('verb.'):
        if lexname in (
            'verb.communication', 'verb.cognition', 'verb.social', 'verb.emotion', 'verb.perception'
        ):
            return 'verb_communication_cognition'
        return 'verb_change_action'
    if lexname in ABSTRACT_MISC_KEYS:
        return 'abstract_misc'
    return lexname


def main():
    words = load_words(MID_VOCAB)
    groups: dict[str, list[str]] = defaultdict(list)
    for word in words:
        groups[categorize(word)].append(word)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Clear previous files to avoid stale categories
    for old in OUT_DIR.glob('*.md'):
        old.unlink()

    summary_lines = ['# PTE 中级词汇分类\n']

    for idx, key in enumerate(CATEGORY_ORDER, 1):
        if key not in groups:
            continue
        items = sorted(groups[key], key=str.lower)
        title = CATEGORY_TITLES[key]
        filename = f"{idx:02d}-{title.replace(' / ', '-').replace('（', '').replace('）', '').replace(' ', '-')}.md"
        filepath = OUT_DIR / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            f.write(f"> 本组共 {len(items)} 个词\n\n")
            for w in items:
                f.write(f"- {w}\n")
        summary_lines.append(f"- **{title}**：{len(items)} 词 → [{filename}]({filename})")

    readme = OUT_DIR / 'README.md'
    with open(readme, 'w', encoding='utf-8') as f:
        f.write('\n'.join(summary_lines) + '\n')

    print(f"Categorized {len(words)} words into {len(summary_lines)-1} groups under {OUT_DIR}")


if __name__ == '__main__':
    main()
