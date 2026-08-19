# English Learn · 英语学习记录

> 个人英语学习仓库，围绕 **听、说、读、写** 四个维度记录课程笔记、生词整理、同义替换、影音语料与作业复盘。
> 当前以 **IELTS 备考** 为主线，所有资料按技能维度分类归档，便于复习时按弱项快速定位。

---

## 目录结构

```
english-learn/
├── listening/          # 听力：精听训练、课堂笔记、生词与同义替换、音频材料
├── speaking/           # 口语：课堂纪要/笔记、Part 1/2/3 素材、句型库、词汇自测
├── reading/            # 阅读：文章、课堂笔记、生词整理、长难句与答案解析
├── writing/            # 写作：课程要点、范文、作业、语法批改与写作复盘
├── movies/             # 影音语料：电影字幕/台词，用于听口输入与地道表达积累
├── notes/              # 通用跨技能笔记（同义替换汇总、答题分析等）
├── scripts/            # 辅助脚本：PDF/HTML 导出、音标加注、听写抽查等
└── README.md           # 本文件
```

### 各目录说明

| 目录 | 用途 | 典型文件 |
|------|------|---------|
| `listening/` | 听力训练全流程资料 | `精听训练/` 原文与答案、`class-N/` 课堂笔记、`audio/` 音频与同替整理 |
| `speaking/` | 口语话题素材与课堂复盘 | `口语准备.md`、课堂纪要 PDF、`class-N/` 笔记与句型 |
| `reading/` | 阅读文章与精读笔记 | `class-N/` 文章与笔记、`homework/` 作业与答案解析 |
| `writing/` | 写作方法论与练习 | 课程要点 MD/PDF、范文、作业批改、写作复盘 |
| `movies/` | 影视语料输入 | 电影字幕（SRT/TXT）、台词文本 |
| `notes/` | 跨维度通用知识库 | `paraphrase.md` 同义替换总库、答案解析 |
| `scripts/` | 辅助脚本 | `md_to_pdf.py`、`add_phonetics.py`、`statistic.bash.js` |

---

## 内容规范

### 1. 文件名与附件约定

- 主笔记使用 **Markdown**（`.md`），便于版本管理与全文检索。
- 同一主题的导出文件（PDF / HTML / 图片 / 音频）统一放入该主题目录的 `_assets/` 子目录：
  - `主题.md` — 源文件（放在目录根）
  - `主题/_assets/` — 导出物与附件
- 避免空格：英文文件名用 `-` 连接，中文文件名保持简洁。

### 2. 生词整理模板

每个技能维度下的 `生词整理.md` / `vocabulary.md` 建议统一使用以下表格：

```markdown
| 单词 / 短语 | 词性 | 音标 | 中文 | 简单解释 | 例句 |
|------------|------|------|------|---------|------|
| initiative | n. | /ɪˈnɪʃətɪv/ | 新举措 | 想出来的新点子、新项目 | The idea for these initiatives came from the public. |
```

### 3. 同义替换记录模板

雅思各科的核心考点之一是同义替换（Paraphrase）。跨技能通用替换汇总到 `notes/paraphrase.md`；各技能目录下只保留本技能课堂/练习专属同替。统一使用以下表格：

```markdown
| 题目表达 | 原文表达 | 说明 |
|----------|----------|------|
| local people | the public | 当地居民 → 公众 |
| method of water treatment | recycling system enables seawater to be used | 水处理方法 → 海水回收利用系统 |
```

### 4. 课堂笔记命名

- 按课程顺序：`class-2/`、`class-3/`、`class-5/`
- 统一使用 **class-N** 格式（带连字符），避免 `class2` 与 `class-3` 混用。

---

## 快速查找

| 想找什么 | 去哪里 |
|----------|--------|
| 同义替换总库 | `notes/paraphrase.md` |
| 听力生词 | `listening/class-N/vocabulary.md` 或 `listening/class-3/10-2-2-New-city-developments-生词整理.md` |
| 口语 Part 2 素材 | `speaking/口语准备.md`、`speaking/class-N/note.md` |
| 阅读生词与同替 | `reading/class-N/生词整理.md`、`reading/class-N/note.md` |
| 写作动态图方法 | `writing/雅思小作文动态图-课程要点与作业指南.md` |
| 电影台词语料 | `movies/The.Pursuit.of.Happyness/` |
| 辅助脚本 | `scripts/` |

---

## 维护建议

1. **定期合并同类项**：生词、同替不要散落在多个 `vocabulary.md` 里，复习阶段可汇总到 `notes/`。
2. **源文件优先**：以 `.md` 为唯一 truth source，`.pdf`/`.html`/图片等导出物放入对应 `_assets/` 目录。
3. **音频/图片轻量管理**：大文件建议只放网盘链接或压缩包，避免仓库膨胀。
4. **统一 class 编号**：所有课堂目录已统一为 `class-N` 格式，新增时也遵循此规则。
5. **脚本集中管理**：新增辅助脚本统一放到 `scripts/`，避免散落在课堂目录中。

---

## License

个人学习用途，谢绝商用转载。
