#!/usr/bin/env python3
"""Generate vocabulary/pte-roots.md by grouping PTE words by prefixes, suffixes and Latin/Greek roots."""
import json
from collections import defaultdict
from pathlib import Path


def main():
    pte_path = Path('pte.json')
    out_path = Path('vocabulary/pte-roots.md')

    with open(pte_path, 'r', encoding='utf-8') as f:
        entries = json.load(f)

    entry_map = {e['phrase'].lower(): e for e in entries}

    PREFIXES = [
        ('un-', '不；相反', ['un']),
        ('re-', '再；回', ['re']),
        ('in-/im-/il-/ir-', '不；进入', ['in', 'im', 'il', 'ir']),
        ('dis-', '不；分开', ['dis']),
        ('en-/em-', '使；进入', ['en', 'em']),
        ('over-', '超过；在…之上', ['over']),
        ('out-', '向外；超过', ['out']),
        ('under-', '在…之下；不足', ['under']),
        ('pre-', '在前；预先', ['pre']),
        ('pro-', '向前；支持', ['pro']),
        ('post-', '在后', ['post']),
        ('sub-', '在下；次要', ['sub']),
        ('super-', '超过；在上', ['super']),
        ('trans-', '跨越；转变', ['trans']),
        ('inter-', '在…之间', ['inter']),
        ('anti-', '反对', ['anti']),
        ('co-/con-/com-/col-/cor-', '共同；一起', ['co', 'con', 'com', 'col', 'cor']),
        ('de-', '向下；去除', ['de']),
        ('ex-/e-/ef-', '向外；出', ['ex', 'ef']),
        ('mis-', '错误；坏', ['mis']),
        ('non-', '非；不', ['non']),
        ('semi-', '半', ['semi']),
        ('micro-', '微小', ['micro']),
        ('multi-', '多', ['multi']),
        ('bi-', '二', ['bi']),
        ('tri-', '三', ['tri']),
        ('mono-', '单一', ['mono']),
        ('poly-', '多', ['poly']),
        ('hyper-', '超过', ['hyper']),
        ('hypo-', '不足', ['hypo']),
        ('auto-', '自动；自己', ['auto']),
        ('bio-', '生命', ['bio']),
        ('geo-', '地球', ['geo']),
        ('photo-', '光', ['photo']),
        ('therm-', '热', ['therm']),
        ('hydr-', '水', ['hydr']),
        ('chrono-', '时间', ['chron']),
        ('tele-', '远', ['tele']),
        ('counter-', '相反；对应', ['counter']),
        ('extra-', '额外', ['extra']),
        ('fore-', '在前', ['fore']),
        ('self-', '自己', ['self']),
        ('up-', '向上', ['up']),
        ('down-', '向下', ['down']),
        ('well-', '好', ['well']),
    ]

    SUFFIXES = [
        ('-tion/-sion/-ation', '行为；状态；结果', ['tion', 'sion', 'ation']),
        ('-ment', '行为；状态；结果', ['ment']),
        ('-ness', '状态；性质', ['ness']),
        ('-ity/-ety', '状态；性质', ['ity', 'ety']),
        ('-able/-ible', '能够…的', ['able', 'ible']),
        ('-ous/-ious', '充满…的', ['ous', 'ious']),
        ('-ive', '倾向于…的', ['ive']),
        ('-al', '与…有关的', ['al']),
        ('-ic/-ical', '与…有关的', ['ic', 'ical']),
        ('-ful', '充满…的', ['ful']),
        ('-less', '没有…的', ['less']),
        ('-ize/-ise/-ify', '使…化', ['ize', 'ise', 'ify']),
        ('-er/-or/-ar', '做…的人/物', ['er', 'or', 'ar']),
        ('-ist', '从事…的人', ['ist']),
        ('-ism', '主义；学说', ['ism']),
        ('-age', '状态；集合', ['age']),
        ('-ance/-ence', '状态；性质', ['ance', 'ence']),
        ('-dom', '状态；领域', ['dom']),
        ('-hood', '状态', ['hood']),
        ('-ship', '状态；身份', ['ship']),
        ('-ward', '方向', ['ward']),
        ('-wise', '方式', ['wise']),
        ('-logy', '学科', ['logy']),
        ('-meter/-metry', '测量', ['meter', 'metry']),
        ('-scope', '观察仪器', ['scope']),
        ('-phone', '声音设备', ['phone']),
        ('-graph/-graphy', '写/画/记录', ['graph', 'graphy']),
        ('-gram', '写/画', ['gram']),
        ('-lingual', '语言的', ['lingual']),
        ('-cracy/-crat', '统治', ['cracy', 'crat']),
    ]

    ROOTS = [
        ('spect/spic', '看', ['spect', 'spic']),
        ('vis/vid', '看', ['vis', 'vid']),
        ('scope', '看；仪器', ['scope']),
        ('struct', '建造', ['struct']),
        ('port', '携带', ['port']),
        ('form', '形状', ['form']),
        ('mit/miss', '送', ['mit', 'miss']),
        ('fect/fact/fic', '做', ['fect', 'fact', 'fic']),
        ('duc/duct', '引导', ['duc', 'duct']),
        ('pos/pon/pound', '放置', ['pos', 'pon', 'pound']),
        ('vert/vers', '转', ['vert', 'vers']),
        ('tract', '拉', ['tract']),
        ('fer', '携带；产生', ['fer']),
        ('cap/capt/cept/ceive', '拿；取', ['cap', 'capt', 'cept', 'ceive']),
        ('ced/ceed/cess', '走', ['ced', 'ceed', 'cess']),
        ('ten/tin/tent/tain', '保持', ['ten', 'tin', 'tent', 'tain']),
        ('press', '压', ['press']),
        ('ject', '投掷', ['ject']),
        ('cur/curs/cour', '跑；发生', ['cur', 'curs', 'cour']),
        ('clud/clus/clos', '关闭', ['clud', 'clus', 'clos']),
        ('grad/gress', '走；步', ['grad', 'gress']),
        ('mot/mov/mob', '移动', ['mot', 'mov', 'mob']),
        ('flu/flux', '流', ['flu', 'flux']),
        ('fus', '倒；流', ['fus']),
        ('rupt', '断裂', ['rupt']),
        ('fract/frag', '破碎', ['fract', 'frag']),
        ('pel/puls', '推；驱', ['pel', 'puls']),
        ('spir', '呼吸；精神', ['spir']),
        ('viv/vit', '生命', ['viv', 'vit']),
        ('mort', '死', ['mort']),
        ('gen', '出生；种类', ['gen']),
        ('cred', '相信', ['cred']),
        ('dict', '说', ['dict']),
        ('locu/loqu/log', '说；学问', ['locu', 'loqu', 'log']),
        ('voc/vok', '喊；叫', ['voc', 'vok']),
        ('nom/nym', '名字', ['nom', 'nym']),
        ('scrib/script', '写', ['scrib', 'script']),
        ('graph/gram', '写；画', ['graph', 'gram']),
        ('liter/letter', '文字', ['liter', 'letter']),
        ('numer', '数字', ['numer']),
        ('oper', '工作', ['oper']),
        ('labor', '工作', ['labor']),
        ('fort', '强', ['fort']),
        ('val/vail', '强；价值', ['val', 'vail']),
        ('dyn', '力量', ['dyn']),
        ('pot', '力量', ['pot']),
        ('arm', '武器', ['arm']),
        ('bell', '战争', ['bell']),
        ('pac', '和平', ['pac']),
        ('polis/polit', '城市；公民', ['polis', 'polit']),
        ('dem', '人民', ['dem']),
        ('popul/publ', '人民', ['popul', 'publ']),
        ('reg/rect', '直；统治', ['reg', 'rect']),
        ('leg', '法律；读', ['leg']),
        ('jur/jus', '法律；正义', ['jur', 'jus']),
        ('mon/moni', '警告；单独', ['mon', 'moni']),
        ('path/pati', '感情；痛苦', ['path', 'pati']),
        ('pass', '感情；忍受', ['pass']),
        ('sens/sent', '感觉', ['sens', 'sent']),
        ('audi/audit', '听', ['audi', 'audit']),
        ('phon', '声音', ['phon']),
        ('son', '声音', ['son']),
        ('lumin/luc/lus', '光', ['lumin', 'luc', 'lus']),
        ('rad/ras/ray', '光线；根', ['rad', 'ras', 'ray']),
        ('therm', '热', ['therm']),
        ('aqua/aque', '水', ['aqua', 'aque']),
        ('mar/mer', '海', ['mar', 'mer']),
        ('terr', '土地', ['terr']),
        ('sol', '太阳；单独', ['sol']),
        ('luna', '月亮', ['luna']),
        ('stella/aster/astr', '星星', ['stella', 'aster', 'astr']),
        ('cosm', '宇宙', ['cosm']),
        ('urb', '城市', ['urb']),
        ('rur/rus', '乡村', ['rur', 'rus']),
        ('agri', '农田', ['agri']),
        ('flor/fleur', '花', ['flor', 'fleur']),
        ('faun', '动物群', ['faun']),
        ('zo', '动物', ['zo']),
        ('bot', '植物', ['bot']),
        ('eco', '家；环境', ['eco']),
        ('phys', '自然；身体', ['phys']),
        ('psych', '心理', ['psych']),
        ('neur', '神经', ['neur']),
        ('cardi', '心脏', ['cardi']),
        ('derm', '皮肤', ['derm']),
        ('oste', '骨', ['oste']),
        ('dent', '牙齿', ['dent']),
        ('ocul', '眼睛', ['ocul']),
        ('lingu', '舌头；语言', ['lingu']),
        ('mania', '狂热', ['mania']),
        ('phob', '恐惧', ['phob']),
        ('therap', '治疗', ['therap']),
        ('med/medic', '治疗', ['med', 'medic']),
        ('san', '健康', ['san']),
        ('tox', '毒', ['tox']),
        ('vir', '毒；男人', ['vir']),
        ('organ', '器官；组织', ['organ']),
        ('cell', '细胞', ['cell']),
        ('molec', '分子', ['molec']),
        ('atom', '原子', ['atom']),
        ('electr', '电', ['electr']),
        ('magnet', '磁', ['magnet']),
        ('mechan', '机械', ['mechan']),
        ('techn', '技术', ['techn']),
        ('chem', '化学', ['chem']),
        ('mathemat', '数学', ['mathemat']),
        ('astronom', '天文', ['astronom']),
        ('biolog', '生物', ['biolog']),
        ('geolog', '地质', ['geolog']),
        ('psycholog', '心理', ['psycholog']),
        ('sociolog', '社会', ['sociolog']),
        ('anthropolog', '人类', ['anthropolog']),
        ('archaeolog', '考古', ['archaeolog']),
        ('histor', '历史', ['histor']),
        ('philos', '爱；智慧', ['philos']),
        ('linguist', '语言', ['linguist']),
        ('phonet', '语音', ['phonet']),
        ('morph', '形状', ['morph']),
        ('etym', '词源', ['etym']),
        ('cogn/gnos', '知道', ['cogn', 'gnos']),
        ('sci', '知道', ['sci']),
        ('theor', '理论', ['theor']),
        ('pract', '实践', ['pract']),
        ('method', '方法', ['method']),
        ('centr/center', '中心', ['centr', 'center']),
        ('velop', '包裹；发展', ['velop']),
        ('volv/volu', '卷；转', ['volv', 'volu']),
        ('pend/pens', '悬挂；称重', ['pend', 'pens']),
        ('spond/spons', '承诺', ['spond', 'spons']),
        ('stat/stan', '站立', ['stat', 'stan']),
        ('sist', '站立', ['sist']),
        ('stinct/sting', '刺', ['stinct', 'sting']),
        ('sum/sumpt', '拿', ['sum', 'sumpt']),
        ('trib', '给予', ['trib']),
        ('turb', '扰乱', ['turb']),
        ('vac', '空', ['vac']),
        ('van', '空', ['van']),
        ('ven/vent', '来', ['ven', 'vent']),
        ('vict/vinc', '征服', ['vict', 'vinc']),
        ('vor', '吃', ['vor']),
        ('zoo', '动物', ['zoo']),
    ]

    def starts_with(phrase, prefix):
        return phrase.lower().startswith(prefix.lower())

    def ends_with(phrase, suffix):
        return phrase.lower().endswith(suffix.lower())

    def contains(phrase, root):
        return root.lower() in phrase.lower()

    root_words = defaultdict(list)

    for phrase in entry_map:
        for root_name, root_meaning, patterns in PREFIXES:
            for pat in patterns:
                if starts_with(phrase, pat):
                    root_words[root_name].append(phrase)
                    break
        for root_name, root_meaning, patterns in SUFFIXES:
            for pat in patterns:
                if ends_with(phrase, pat):
                    root_words[root_name].append(phrase)
                    break
        for root_name, root_meaning, patterns in ROOTS:
            for pat in patterns:
                if len(pat) >= 3 and contains(phrase, pat):
                    root_words[root_name].append(phrase)
                    break

    categorized_words = set()
    for words in root_words.values():
        categorized_words.update(words)
    uncategorized = [p for p in entry_map if p not in categorized_words]

    lines = []
    lines.append("# PTE 单词 · 按词根/词缀分类记忆\n")
    lines.append("> 基于 `pte.json` 中的 725 个 PTE 高频词，按常见前缀、后缀、拉丁/希腊词根归类。\n")
    lines.append("> 目标：通过词根串记，举一反三。同一单词可能同时出现在前缀、后缀和词根下。\n")
    lines.append("---\n")

    lines.append("## 使用建议\n")
    lines.append("1. **先看前缀/后缀**：它们出现频率最高，能帮你快速判断词性和方向。\n")
    lines.append("2. **再攻克核心词根**：每个词根下的单词一起背，更容易建立联系。\n")
    lines.append("3. **最后扫未归类**：多为高频基础词或外来词，单独强化。\n")
    lines.append("")

    lines.append("## 目录\n")
    lines.append("1. [前缀 Prefixes](#前缀-prefixes)\n")
    lines.append("2. [后缀 Suffixes](#后缀-suffixes)\n")
    lines.append("3. [核心词根 Core Roots](#核心词根-core-roots)\n")
    lines.append("4. [未归类 Uncategorized](#未归类-uncategorized)\n")
    lines.append("")

    def write_section(title, groups, min_count=1):
        lines.append(f"---\n## {title}\n")
        for root_name, root_meaning, patterns in groups:
            if root_name not in root_words:
                continue
            words = sorted(set(root_words[root_name]), key=lambda x: x.lower())
            if len(words) < min_count:
                continue
            lines.append(f"### {root_name} = {root_meaning}\n")
            for w in words:
                e = entry_map[w]
                lines.append(
                    f"- **{e['phrase']}** {e.get('phonetic', '')} *{e.get('pos', '')}* — {e.get('meaning', '')}"
                )
            lines.append("")

    write_section('前缀 Prefixes', PREFIXES)
    write_section('后缀 Suffixes', SUFFIXES)
    write_section('核心词根 Core Roots', ROOTS, min_count=3)

    if uncategorized:
        lines.append("---\n")
        lines.append("## 未归类 Uncategorized\n")
        lines.append(f"以下 {len(uncategorized)} 个单词暂未找到合适的词根/词缀归类，建议单独记忆：\n")
        for w in sorted(set(uncategorized)):
            e = entry_map[w]
            lines.append(
                f"- **{e['phrase']}** {e.get('phonetic', '')} *{e.get('pos', '')}* — {e.get('meaning', '')}"
            )
        lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"Total words: {len(entry_map)}")
    print(f"Categorized: {len(categorized_words)}")
    print(f"Uncategorized: {len(uncategorized)}")
    print(f"Groups written: {out_path}")


if __name__ == '__main__':
    main()
