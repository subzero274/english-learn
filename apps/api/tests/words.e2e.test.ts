import request from 'supertest';
import { createApp } from '@/app';

const app = createApp();

async function getAdminToken() {
  const res = await request(app)
    .post('/api/auth/login')
    .send({ email: 'admin@test.com', password: 'test123' });
  return res.body.data.token;
}

function sampleWord() {
  return {
    word: 'ephemeral',
    phonetic: '/ɪˈfemərəl/',
    meaning: '短暂的，瞬息即逝的',
    partOfSpeech: 'adjective',
    difficulty: 'C1',
    tags: 'ielts,literary',
    exampleSentences: [
      { english: 'Fashions are ephemeral, changing with every season.', chinese: '时尚是短暂的，每个季节都在变化。' },
      { english: 'The beauty of cherry blossoms is ephemeral.', chinese: '樱花的美是转瞬即逝的。' },
    ],
  };
}

describe('GET /api/health', () => {
  it('returns ok', async () => {
    const res = await request(app).get('/api/health');
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('ok');
  });
});

describe('GET /api/words', () => {
  it('returns empty paginated list', async () => {
    const res = await request(app).get('/api/words');
    expect(res.status).toBe(200);
    expect(res.body.data).toEqual([]);
    expect(res.body.pagination.total).toBe(0);
  });
});

describe('POST /api/words', () => {
  it('returns 401 without token', async () => {
    const res = await request(app).post('/api/words').send(sampleWord());
    expect(res.status).toBe(401);
  });

  it('creates a word when authenticated', async () => {
    const token = await getAdminToken();
    const res = await request(app)
      .post('/api/words')
      .set('Authorization', `Bearer ${token}`)
      .send(sampleWord());

    expect(res.status).toBe(201);
    expect(res.body.data.word).toBe('ephemeral');
    expect(res.body.data.exampleSentences).toHaveLength(2);
  });
});

describe('GET /api/words/:id', () => {
  it('returns a word by id', async () => {
    const token = await getAdminToken();
    const createRes = await request(app)
      .post('/api/words')
      .set('Authorization', `Bearer ${token}`)
      .send(sampleWord());

    const id = createRes.body.data.id;
    const res = await request(app).get(`/api/words/${id}`);

    expect(res.status).toBe(200);
    expect(res.body.data.id).toBe(id);
    expect(res.body.data.exampleSentences).toHaveLength(2);
  });

  it('returns 404 for missing word', async () => {
    const res = await request(app).get('/api/words/99999');
    expect(res.status).toBe(404);
  });
});

describe('PATCH /api/words/:id', () => {
  it('updates word and sentences when authenticated', async () => {
    const token = await getAdminToken();
    const createRes = await request(app)
      .post('/api/words')
      .set('Authorization', `Bearer ${token}`)
      .send(sampleWord());

    const id = createRes.body.data.id;
    const res = await request(app)
      .patch(`/api/words/${id}`)
      .set('Authorization', `Bearer ${token}`)
      .send({
        meaning: '极其短暂的',
        exampleSentences: [
          { english: 'The moment was ephemeral.', chinese: '那一刻极其短暂。' },
        ],
      });

    expect(res.status).toBe(200);
    expect(res.body.data.meaning).toBe('极其短暂的');
    expect(res.body.data.exampleSentences).toHaveLength(1);
  });
});

describe('DELETE /api/words/:id', () => {
  it('deletes a word when authenticated', async () => {
    const token = await getAdminToken();
    const createRes = await request(app)
      .post('/api/words')
      .set('Authorization', `Bearer ${token}`)
      .send(sampleWord());

    const id = createRes.body.data.id;
    const deleteRes = await request(app)
      .delete(`/api/words/${id}`)
      .set('Authorization', `Bearer ${token}`);

    expect(deleteRes.status).toBe(204);

    const getRes = await request(app).get(`/api/words/${id}`);
    expect(getRes.status).toBe(404);
  });
});

describe('POST /api/auth/login', () => {
  it('returns token for valid credentials', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({ email: 'admin@test.com', password: 'test123' });

    expect(res.status).toBe(200);
    expect(res.body.data.token).toBeDefined();
    expect(res.body.data.admin.email).toBe('admin@test.com');
  });

  it('returns 401 for invalid credentials', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({ email: 'admin@test.com', password: 'wrong' });

    expect(res.status).toBe(401);
  });
});
