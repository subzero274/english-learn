import { prisma } from '../src'

async function main() {
  const sampleWords = [
    {
      word: 'serendipity',
      phonetic: '/ˌser.ənˈdɪp.ə.ti/',
      meaning: 'the fact of finding interesting or valuable things by chance',
      partOfSpeech: 'noun',
      difficulty: 'hard',
      tags: 'academic,ielts',
      exampleSentences: {
        create: [
          {
            english: 'Finding this restaurant was pure serendipity.',
            chinese: '发现这家餐厅纯粹是意外之喜。',
            order: 0,
          },
        ],
      },
    },
    {
      word: 'ubiquitous',
      phonetic: '/juːˈbɪk.wɪ.təs/',
      meaning: 'seeming to be everywhere',
      partOfSpeech: 'adjective',
      difficulty: 'hard',
      tags: 'academic,ielts',
      exampleSentences: {
        create: [
          {
            english: 'Smartphones have become ubiquitous in modern society.',
            chinese: '智能手机在现代社会已无处不在。',
            order: 0,
          },
        ],
      },
    },
    {
      word: 'ephemeral',
      phonetic: '/ɪˈfem.ər.əl/',
      meaning: 'lasting for only a short time',
      partOfSpeech: 'adjective',
      difficulty: 'hard',
      tags: 'academic,literature',
      exampleSentences: {
        create: [
          {
            english: 'Fashion trends are ephemeral by nature.',
            chinese: '时尚趋势本质上是短暂的。',
            order: 0,
          },
        ],
      },
    },
  ]

  for (const word of sampleWords) {
    await prisma.word.upsert({
      where: { word: word.word },
      update: {},
      create: word,
    })
  }

  console.log('✅ Seeded sample words')
}

main()
  .catch((e) => {
    console.error(e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })
