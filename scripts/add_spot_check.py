#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add spot check mode to vocabulary-test-audio.html
"""
from pathlib import Path

HTML_PATH = Path('/Users/qianduoduo/.openclaw/workspace/english-listening/listening/class-4/vocabulary-test-audio.html')

html = HTML_PATH.read_text(encoding='utf-8')

# 1. Update mode switch buttons
old_mode_switch = '''    <div class="mode-switch">
        <button class="mode-btn active" onclick="switchMode('learn')" id="learnModeBtn">📖 学习模式</button>
        <button class="mode-btn" onclick="switchMode('test')" id="testModeBtn">✏️ 测试模式</button>
    </div>'''

new_mode_switch = '''    <div class="mode-switch">
        <button class="mode-btn active" onclick="switchMode('learn')" id="learnModeBtn">📖 学习模式</button>
        <button class="mode-btn" onclick="switchMode('test')" id="testModeBtn">✏️ 测试模式</button>
        <button class="mode-btn" onclick="switchMode('spot')" id="spotModeBtn">🎯 抽检模式</button>
    </div>'''

html = html.replace(old_mode_switch, new_mode_switch)

# 2. Add spot check section after test mode section
old_test_section_end = '''    <div id="result" class="result"></div>
    </div>

    <script>'''

new_spot_section = '''    <div id="result" class="result"></div>
    </div>

    <!-- 抽检模式 -->
    <div id="spotMode" class="section hidden">
        <div class="learn-controls">
            <button onclick="generateSpotCheck()"">🎲 重新抽检</button>
            <button onclick="playSpotAll()">▶️ 顺序播放</button>
            <button onclick="stopSpotPlay()">⏹ 停止</button>
        </div>
        <div class="progress" id="spotInfo">本次抽检 0 题 · 已答：0 / 0</div>
        <div class="progress-bar">
            <div class="progress-fill" id="spotProgressFill" style="width: 0%"></div>
        </div>
        <div id="spotWordList"></div>

        <button class="submit" onclick="checkSpotAnswers()">提交抽检答案</button>

        <div id="spotResult" class="result"></div>
    </div>

    <script>'''

html = html.replace(old_test_section_end, new_spot_section)

# 3. Update excluded words and spot check variables after YOUDAO_AUDIO_URL declaration
old_youdao = '''        const YOUDAO_AUDIO_URL = 'https://dict.youdao.com/dictvoice';
        let currentMode = 'learn';
        let playAllInterval = null;
        let examplesHidden = false;'''

new_youdao = '''        const YOUDAO_AUDIO_URL = 'https://dict.youdao.com/dictvoice';
        const EXCLUDED_WORDS = [
            'acting spaces',
            'put on a production',
            'available for hire',
            'show round',
            'adult-only times',
            'running machines',
            'booking preferences'
        ];
        const SPOT_CHECK_COUNT = 10;
        let currentMode = 'learn';
        let playAllInterval = null;
        let spotPlayInterval = null;
        let examplesHidden = false;
        let spotCheckWords = [];'''

html = html.replace(old_youdao, new_youdao)

# 4. Update switchMode function
old_switch_mode = '''        function switchMode(mode) {
            currentMode = mode;
            document.getElementById('learnModeBtn').classList.toggle('active', mode === 'learn');
            document.getElementById('testModeBtn').classList.toggle('active', mode === 'test');
            document.getElementById('learnMode').classList.toggle('hidden', mode !== 'learn');
            document.getElementById('testMode').classList.toggle('hidden', mode !== 'test');
            stopPlayAll();
            if (mode === 'test') {
                renderTestList();
            }
        }'''

new_switch_mode = '''        function switchMode(mode) {
            currentMode = mode;
            document.getElementById('learnModeBtn').classList.toggle('active', mode === 'learn');
            document.getElementById('testModeBtn').classList.toggle('active', mode === 'test');
            document.getElementById('spotModeBtn').classList.toggle('active', mode === 'spot');
            document.getElementById('learnMode').classList.toggle('hidden', mode !== 'learn');
            document.getElementById('testMode').classList.toggle('hidden', mode !== 'test');
            document.getElementById('spotMode').classList.toggle('hidden', mode !== 'spot');
            stopPlayAll();
            stopSpotPlay();
            if (mode === 'test') {
                renderTestList();
            } else if (mode === 'spot') {
                generateSpotCheck();
            }
        }'''

html = html.replace(old_switch_mode, new_switch_mode)

# 5. Update stopPlayAll to also stop spot play
old_stop_play_all = '''        function stopPlayAll() {
            if (playAllInterval) {
                clearTimeout(playAllInterval);
                playAllInterval = null;
            }
            document.getElementById('progressFill').style.width = '0%';
        }'''

new_stop_play_all = '''        function stopPlayAll() {
            if (playAllInterval) {
                clearTimeout(playAllInterval);
                playAllInterval = null;
            }
            document.getElementById('progressFill').style.width = '0%';
        }

        function stopSpotPlay() {
            if (spotPlayInterval) {
                clearTimeout(spotPlayInterval);
                spotPlayInterval = null;
            }
            document.getElementById('spotProgressFill').style.width = '0%';
        }'''

html = html.replace(old_stop_play_all, new_stop_play_all)

# 6. Add spot check functions before checkAnswers function
spot_check_functions = '''
        function getAvailableWords() {
            return words.filter(w => !EXCLUDED_WORDS.includes(w.word));
        }

        function generateSpotCheck() {
            const available = getAvailableWords();
            const shuffled = [...available].sort(() => Math.random() - 0.5);
            spotCheckWords = shuffled.slice(0, SPOT_CHECK_COUNT);
            renderSpotCheckList();
            document.getElementById('spotResult').style.display = 'none';
        }

        function renderSpotCheckList() {
            document.getElementById('spotInfo').textContent = `本次抽检 ${spotCheckWords.length} 题 · 已答：0 / ${spotCheckWords.length * 2}`;
            const container = document.getElementById('spotWordList');
            container.innerHTML = spotCheckWords.map((item, index) => `
                <div class="word-item" data-spot-index="${index}" data-word="${item.word}" data-meaning="${item.meaning}">
                    <div class="number">${index + 1}</div>
                    <button class="play-btn" onclick="playAudio(${words.indexOf(item)})" title="播放">🔊</button>
                    <div class="input-group">
                        <div class="input-label">英文</div>
                        <input type="text" placeholder="英文" data-type="word" data-index="${index}" oninput="updateSpotProgress()">
                    </div>
                    <div class="input-group">
                        <div class="input-label">中文</div>
                        <input type="text" placeholder="中文意思" data-type="meaning" data-index="${index}" oninput="updateSpotProgress()">
                    </div>
                </div>
            `).join('');
            updateSpotProgress();
        }

        function updateSpotProgress() {
            const total = spotCheckWords.length * 2;
            let count = 0;
            document.querySelectorAll('#spotWordList input[type="text"]').forEach(input => {
                if (input.value.trim()) count++;
            });
            document.getElementById('spotInfo').textContent = `本次抽检 ${spotCheckWords.length} 题 · 已答：${count} / ${total}`;
        }

        function playSpotAll() {
            stopSpotPlay();
            let index = 0;
            const playNext = () => {
                if (index >= spotCheckWords.length) {
                    document.getElementById('spotProgressFill').style.width = '100%';
                    return;
                }
                playAudio(words.indexOf(spotCheckWords[index]));
                document.getElementById('spotProgressFill').style.width = `${((index + 1) / spotCheckWords.length) * 100}%`;
                index++;
                spotPlayInterval = setTimeout(playNext, 3000);
            };
            playNext();
        }

        function checkSpotAnswers() {
            let wordCorrect = 0;
            let meaningCorrect = 0;
            let total = spotCheckWords.length;
            let fullyCorrect = 0;

            document.querySelectorAll('#spotWordList .word-item').forEach(item => {
                const correctWord = item.getAttribute('data-word');
                const correctMeaning = item.getAttribute('data-meaning');
                const wordInput = item.querySelector('input[data-type="word"]');
                const meaningInput = item.querySelector('input[data-type="meaning"]');
                const userWord = normalize(wordInput.value);
                const userMeaning = meaningInput.value.trim();

                const isWordCorrect = userWord === normalize(correctWord);
                const isMeaningCorrectResult = isMeaningCorrect(userMeaning, correctMeaning);

                if (isWordCorrect) wordCorrect++;
                if (isMeaningCorrectResult) meaningCorrect++;
                if (isWordCorrect && isMeaningCorrectResult) fullyCorrect++;

                item.classList.remove('correct-item', 'wrong-item');
                const existingReveal = item.querySelector('.answer-reveal');
                if (existingReveal) existingReveal.remove();

                if (isWordCorrect && isMeaningCorrectResult) {
                    item.classList.add('correct-item');
                } else {
                    item.classList.add('wrong-item');
                    const reveal = document.createElement('div');
                    reveal.className = 'answer-reveal';
                    reveal.innerHTML = `正确答案：<strong>${correctWord}</strong> — ${correctMeaning}`;
                    item.appendChild(reveal);
                }
            });

            const wordPercentage = Math.round((wordCorrect / total) * 100);
            const meaningPercentage = Math.round((meaningCorrect / total) * 100);
            const totalPercentage = Math.round((fullyCorrect / total) * 100);

            const resultDiv = document.getElementById('spotResult');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = `
                <div class="score-box">${fullyCorrect} / ${total}</div>
                <p>英文拼写：${wordCorrect}/${total}（${wordPercentage}%）</p>
                <p>中文意思：${meaningCorrect}/${total}（${meaningPercentage}%）</p>
                <p>完全正确：${totalPercentage}%</p>
                <p>${totalPercentage >= 80 ? '🎉 抽检通过！' : totalPercentage >= 60 ? '👍 还可以，再抽一批试试。' : '💪 这批掌握不牢，先去学习模式复习。'}</p>
            `;
            resultDiv.className = 'result ' + (totalPercentage >= 60 ? 'correct' : 'wrong');

            window.scrollTo(0, document.body.scrollHeight);
        }

'''

# Insert before function checkAnswers()
html = html.replace('        function checkAnswers() {', spot_check_functions + '        function checkAnswers() {')

# 7. Update initialization to not auto-generate spot check (it will be generated when mode switched)
old_init = '''        // Initialize
        document.getElementById('totalCount').textContent = words.length;
        renderLearnList();
        renderTestList();'''

new_init = '''        // Initialize
        document.getElementById('totalCount').textContent = words.length;
        renderLearnList();
        renderTestList();'''

# No change needed for init

HTML_PATH.write_text(html, encoding='utf-8')
print("Spot check mode added successfully")
