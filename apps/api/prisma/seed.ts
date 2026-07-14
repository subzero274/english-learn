import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

const ADMIN_EMAIL = 'admin@example.com';
const ADMIN_PASSWORD = 'admin123';

const seedWords = [
  {
    word: 'abandon',
    phonetic: '/əˈbændən/',
    meaning: '放弃，抛弃',
    partOfSpeech: 'verb',
    difficulty: 'B2',
    tags: 'ielts,common',
    exampleSentences: [
      { english: 'They had to abandon their car in the snow.', chinese: '他们不得不把汽车弃置在雪中。' },
      { english: 'The captain ordered the crew to abandon ship.', chinese: '船长命令船员弃船。' },
    ],
  },
  {
    word: 'accelerate',
    phonetic: '/əkˈseləreɪt/',
    meaning: '加速，促进',
    partOfSpeech: 'verb',
    difficulty: 'B2',
    tags: 'ielts,academic',
    exampleSentences: [
      { english: 'The car accelerated rapidly on the highway.', chinese: '汽车在高速公路上迅速加速。' },
      { english: 'We need to accelerate the pace of reform.', chinese: '我们需要加快改革步伐。' },
    ],
  },
  {
    word: 'ambiguous',
    phonetic: '/æmˈbɪɡjuəs/',
    meaning: '模棱两可的，含糊不清的',
    partOfSpeech: 'adjective',
    difficulty: 'C1',
    tags: 'ielts,academic',
    exampleSentences: [
      { english: 'The contract is ambiguous in several places.', chinese: '这份合同有几处措辞含糊。' },
      { english: 'His reply was deliberately ambiguous.', chinese: '他的回答故意模棱两可。' },
    ],
  },
  {
    word: 'comprehensive',
    phonetic: '/ˌkɒmprɪˈhensɪv/',
    meaning: '全面的，综合的',
    partOfSpeech: 'adjective',
    difficulty: 'B2',
    tags: 'ielts,academic',
    exampleSentences: [
      { english: 'We need a comprehensive review of the policy.', chinese: '我们需要全面审查这项政策。' },
      { english: 'The report provides a comprehensive analysis.', chinese: '该报告提供了全面的分析。' },
    ],
  },
  {
    word: 'demonstrate',
    phonetic: '/ˈdemənstreɪt/',
    meaning: '证明，展示，示威',
    partOfSpeech: 'verb',
    difficulty: 'B2',
    tags: 'ielts,common',
    exampleSentences: [
      { english: 'The study demonstrates a clear link between smoking and cancer.', chinese: '该研究证明了吸烟与癌症之间的明确联系。' },
      { english: 'She demonstrated how to use the software.', chinese: '她展示了如何使用该软件。' },
    ],
  },
  {
    word: 'explicit',
    phonetic: '/ɪkˈsplɪsɪt/',
    meaning: '明确的，清楚的',
    partOfSpeech: 'adjective',
    difficulty: 'C1',
    tags: 'ielts,academic',
    exampleSentences: [
      { english: 'He gave explicit instructions about what to do.', chinese: '他就该做什么给出了明确的指示。' },
      { english: 'The film contains explicit violence.', chinese: '这部电影包含露骨的暴力场面。' },
    ],
  },
  {
    word: 'feasible',
    phonetic: '/ˈfiːzəbl/',
    meaning: '可行的，行得通的',
    partOfSpeech: 'adjective',
    difficulty: 'C1',
    tags: 'ielts,academic',
    exampleSentences: [
      { english: 'It is not feasible to finish the project in one week.', chinese: '在一周内完成这个项目是不可行的。' },
      { english: 'We need to find a feasible solution.', chinese: '我们需要找到一个可行的解决方案。' },
    ],
  },
  {
    word: 'fluctuate',
    phonetic: '/ˈflʌktʃueɪt/',
    meaning: '波动，起伏',
    partOfSpeech: 'verb',
    difficulty: 'C1',
    tags: 'ielts,academic',
    exampleSentences: [
      { english: 'Prices fluctuate according to supply and demand.', chinese: '价格随供求关系波动。' },
      { english: 'His mood fluctuates throughout the day.', chinese: '他的情绪一整天都在起伏不定。' },
    ],
  },
  {
    word: 'hypothesis',
    phonetic: '/haɪˈpɒθəsɪs/',
    meaning: '假设，假说',
    partOfSpeech: 'noun',
    difficulty: 'C1',
    tags: 'ielts,academic',
    exampleSentences: [
      { english: 'The results support our original hypothesis.', chinese: '结果支持我们最初的假设。' },
      { english: 'Scientists tested the hypothesis through experiments.', chinese: '科学家通过实验验证了这个假设。' },
    ],
  },
  {
    word: 'implement',
    phonetic: '/ˈɪmplɪment/',
    meaning: '实施，执行',
    partOfSpeech: 'verb',
    difficulty: 'B2',
    tags: 'ielts,common',
    exampleSentences: [
      { english: 'The government plans to implement new policies.', chinese: '政府计划实施新政策。' },
      { english: 'We need to implement changes immediately.', chinese: '我们需要立即实施变革。' },
    ],
  },
  {
    word: 'incline',
    phonetic: '/ɪnˈklaɪn/',
    meaning: '倾向于，倾斜',
    partOfSpeech: 'verb',
    difficulty: 'C1',
    tags: 'ielts,academic',
    exampleSentences: [
      { english: 'I incline to the view that education should be free.', chinese: '我倾向于认为教育应该是免费的。' },
      { english: 'The road inclines steeply here.', chinese: '这条路在这里陡然倾斜。' },
    ],
  },
  {
    word: 'justifiable',
    phonetic: '/ˈdʒʌstɪfaɪəbl/',
    meaning: '有正当理由的，可辩护的',
    partOfSpeech: 'adjective',
    difficulty: 'C1',
    tags: 'ielts,academic',
    exampleSentences: [
      { english: 'Her anger was entirely justifiable.', chinese: '她的愤怒完全是合情合理的。' },
      { english: 'Is it justifiable to break the law in this case?', chinese: '在这种情况下违法是正当的吗？' },
    ],
  },
  {
    word: 'magnify',
    phonetic: '/ˈmæɡnɪfaɪ/',
    meaning: '放大，夸大',
    partOfSpeech: 'verb',
    difficulty: 'C1',
    tags: 'ielts,academic',
    exampleSentences: [
      { english: 'The microscope can magnify objects up to 1000 times.', chinese: '这台显微镜能把物体放大1000倍。' },
      { english: 'The media tends to magnify minor problems.', chinese: '媒体往往会夸大一些小问题。' },
    ],
  },
  {
    word: 'notion',
    phonetic: '/ˈnəʊʃn/',
    meaning: '概念，看法',
    partOfSpeech: 'noun',
    difficulty: 'B2',
    tags: 'ielts,common',
    exampleSentences: [
      { english: 'I have no notion of what you mean.', chinese: '我不明白你的意思。' },
      { english: 'The notion of equality is central to democracy.', chinese: '平等的概念是民主的核心。' },
    ],
  },
  {
    word: 'parallel',
    phonetic: '/ˈpærəlel/',
    meaning: '平行的；类似的',
    partOfSpeech: 'adjective',
    difficulty: 'B2',
    tags: 'ielts,common',
    exampleSentences: [
      { english: 'The road runs parallel to the railway.', chinese: '这条路与铁路平行。' },
      { english: 'There are clear parallels between the two cases.', chinese: '这两个案例之间有明显的相似之处。' },
    ],
  },
  {
    word: 'prerequisite',
    phonetic: '/priːˈrekwəzɪt/',
    meaning: '先决条件，前提',
    partOfSpeech: 'noun',
    difficulty: 'C1',
    tags: 'ielts,academic',
    exampleSentences: [
      { english: 'A degree is a prerequisite for this job.', chinese: '学位是这份工作的先决条件。' },
      { english: 'Trust is a prerequisite for a healthy relationship.', chinese: '信任是健康关系的前提。' },
    ],
  },
  {
    word: 'reluctant',
    phonetic: '/rɪˈlʌktənt/',
    meaning: '不情愿的，勉强的',
    partOfSpeech: 'adjective',
    difficulty: 'B2',
    tags: 'ielts,common',
    exampleSentences: [
      { english: 'She was reluctant to admit her mistake.', chinese: '她不愿意承认自己的错误。' },
      { english: 'He gave a reluctant apology.', chinese: '他勉强地道了歉。' },
    ],
  },
  {
    word: 'sustain',
    phonetic: '/səˈsteɪn/',
    meaning: '维持，支撑，遭受',
    partOfSpeech: 'verb',
    difficulty: 'B2',
    tags: 'ielts,academic',
    exampleSentences: [
      { english: 'The economy cannot sustain such rapid growth.', chinese: '经济无法维持如此快速的增长。' },
      { english: 'He sustained serious injuries in the accident.', chinese: '他在事故中受了重伤。' },
    ],
  },
  {
    word: 'tangible',
    phonetic: '/ˈtændʒəbl/',
    meaning: '有形的，可触摸的，明确的',
    partOfSpeech: 'adjective',
    difficulty: 'C1',
    tags: 'ielts,academic',
    exampleSentences: [
      { english: 'The policy produced tangible benefits.', chinese: '这项政策带来了实实在在的好处。' },
      { english: 'There is no tangible evidence against him.', chinese: '没有对他不利的实物证据。' },
    ],
  },
  {
    word: 'vulnerable',
    phonetic: '/ˈvʌlnərəbl/',
    meaning: '易受伤害的，脆弱的',
    partOfSpeech: 'adjective',
    difficulty: 'B2',
    tags: 'ielts,common',
    exampleSentences: [
      { english: 'The old bridge is vulnerable to flooding.', chinese: '这座旧桥容易受到洪水侵袭。' },
      { english: 'Children are particularly vulnerable to disease.', chinese: '儿童特别容易患病。' },
    ],
  },
];

async function main() {
  // Create admin user
  const hashedPassword = await bcrypt.hash(ADMIN_PASSWORD, 10);
  await prisma.adminUser.upsert({
    where: { email: ADMIN_EMAIL },
    update: {},
    create: {
      email: ADMIN_EMAIL,
      password: hashedPassword,
    },
  });
  console.log(`Seeded admin user: ${ADMIN_EMAIL}`);

  // Seed words if none exist
  const existingCount = await prisma.word.count();
  if (existingCount > 0) {
    console.log(`Database already contains ${existingCount} words, skipping word seed.`);
  } else {
    for (const item of seedWords) {
      await prisma.word.create({
        data: {
          word: item.word,
          phonetic: item.phonetic,
          meaning: item.meaning,
          partOfSpeech: item.partOfSpeech,
          difficulty: item.difficulty,
          tags: item.tags,
          exampleSentences: {
            create: item.exampleSentences.map((s, index) => ({
              english: s.english,
              chinese: s.chinese,
              order: index,
            })),
          },
        },
      });
    }
    console.log(`Seeded ${seedWords.length} words.`);
  }
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
