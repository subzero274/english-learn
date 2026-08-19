const fs = require('fs');
const path = require('path');

/**
 * 解析 SRT 文件，提取每条字幕的对话内容
 * @param {string} content - SRT 文件原始内容
 * @returns {Array<{index: number, time: string, text: string}>} - 字幕条目数组
 */
function parseSRT(content) {
    const blocks = content.split(/\r?\n\s*\r?\n/).filter(b => b.trim());
    const subtitles = [];

    for (const block of blocks) {
        const lines = block.trim().split(/\r?\n/);
        if (lines.length < 3) continue;

        const index = parseInt(lines[0].trim(), 10);
        const time = lines[1].trim();
        
        const text = lines.slice(2)
            .join(' ')
            .replace(/<[^>]+>/g, '')
            .trim();

        if (text) {
            subtitles.push({ index, time, text });
        }
    }

    return subtitles;
}

/**
 * 提取纯文本内容（用于单词统计）
 * @param {Array} subtitles - 解析后的字幕数组
 * @returns {string} - 所有文本拼接
 */
function extractAllText(subtitles) {
    return subtitles.map(s => s.text).join(' ');
}

/**
 * 将对话保存到文件（仅保留文字，无时间戳）
 * @param {Array} subtitles - 字幕数组
 * @param {string} outputPath - 输出文件路径
 */
function saveDialogues(subtitles, outputPath) {
    const lines = subtitles.map(s => s.text);
    const content = lines.join('\n\n');
    fs.writeFileSync(outputPath, content, 'utf-8');
}

/**
 * 提取单词并统计频率
 * @param {string} text - 纯文本
 * @returns {Array<{word: string, count: number}>} - 按频率降序排列的单词列表
 */
function countWords(text) {
    const cleaned = text
        .toLowerCase()
        .replace(/[^\w\s']/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();

    const words = cleaned.split(' ').filter(w => w.length > 0);
    const freqMap = {};

    for (const word of words) {
        const cleanWord = word.replace(/^'+|'+$/g, '');
        if (cleanWord.length === 0) continue;
        freqMap[cleanWord] = (freqMap[cleanWord] || 0) + 1;
    }

    const result = Object.entries(freqMap).map(([word, count]) => ({ word, count }));
    result.sort((a, b) => b.count - a.count);
    return result;
}

/**
 * 主函数
 */
function main() {
    const inputFile = process.argv[2] || 'subtitle.srt';
    const outputDir = process.argv[3] || '.';

    if (!fs.existsSync(inputFile)) {
        console.error(`❌ 文件不存在: ${inputFile}`);
        console.log('用法: node script.js <srt文件路径> [输出目录]');
        process.exit(1);
    }

    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }

    const baseName = path.basename(inputFile, path.extname(inputFile));
    const dialogueFile = path.join(outputDir, `${baseName}-dialogues.txt`);
    const jsonFile = path.join(outputDir, `${baseName}-word-frequency.json`);

    console.log(`📖 正在读取: ${inputFile}`);

    const content = fs.readFileSync(inputFile, 'utf-8');
    const subtitles = parseSRT(content);

    console.log(`📝 共提取 ${subtitles.length} 条字幕`);

    saveDialogues(subtitles, dialogueFile);
    console.log(`💬 对话已保存至: ${path.resolve(dialogueFile)}`);

    const text = extractAllText(subtitles);
    const wordStats = countWords(text);
    const totalWords = wordStats.reduce((sum, item) => sum + item.count, 0);
    const uniqueWords = wordStats.length;

    const output = {
        source: path.resolve(inputFile),
        generatedAt: new Date().toISOString(),
        summary: {
            totalWords,
            uniqueWords,
            subtitleCount: subtitles.length
        },
        words: wordStats
    };

    fs.writeFileSync(jsonFile, JSON.stringify(output, null, 2), 'utf-8');

    console.log(`\n📊 统计结果：共 ${totalWords} 个单词，${uniqueWords} 个不重复单词\n`);
    console.log('🔥 出现频率最高的 20 个单词：');
    console.log('─'.repeat(45));
    wordStats.slice(0, 20).forEach((item, index) => {
        const bar = '█'.repeat(Math.min(item.count, 20));
        console.log(`${(index + 1).toString().padStart(2)}. ${item.word.padEnd(15)} ${item.count.toString().padStart(4)} ${bar}`);
    });

    console.log(`\n✅ 单词频率已保存至: ${path.resolve(jsonFile)}`);
}

main();