# Nulufar — Yaqin joylarni topuvchi Telegram bot

Foydalanuvchi lokatsiyasini va matnli/ovozli xabarini tahlil qilib, eng yaqin
mehmonxona, hostel, restoran, kafe va shunga o'xshash joylarni (OpenStreetMap
Overpass API orqali) topib beradi. Aniq natija topilmasa, AI yordamida
qidiruv tavsiyalari beradi.

## Imkoniyatlar

- 📍 Lokatsiya orqali yaqin joylarni qidirish (Overpass API)
- 💬 Matnli so'rovlarni tushunish va kategoriya bo'yicha javob berish
- 🎤 Ovozli xabarlarni matnga o'girish (ASR) va shu bo'yicha javob berish
- 🔁 Turli LLM va ASR provayderlarini almashtirish imkoniyati (Groq, OpenAI va OpenAI-mos boshqa servislar)

## O'rnatish

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

`.env.example` faylidan nusxa olib `.env` faylini yarating va o'z
qiymatlaringizni kiriting:

```bash
copy .env.example .env
```

### Muhim sozlamalar (`.env`)

| O'zgaruvchi | Tavsif |
| --- | --- |
| `BOT_TOKEN` | Telegram bot tokeni (@BotFather) |
| `LLM_PROVIDER` | Chat modeli provayderi: `groq` yoki `openai` |
| `LLM_API_KEY` | LLM provayder uchun API kalit |
| `LLM_MODEL` | Chat modeli nomi (pastdagi jadvalga qarang) |
| `LLM_BASE_URL` | Ixtiyoriy — OpenAI-mos boshqa server manzili |
| `ASR_PROVIDER` | Ovozni matnga o'girish provayderi: `groq` \| `openai` \| `gemini` \| `qwen` |
| `ASR_API_KEY` | ASR uchun API kalit (bo'sh bo'lsa `LLM_API_KEY` ishlatiladi) |
| `ASR_MODEL` | ASR modeli nomi (pastdagi jadvalga qarang) |
| `ASR_BASE_URL` | Ixtiyoriy — OpenAI-mos boshqa server manzili |
| `ASR_LANGUAGE` | Transkripsiya tili kodi (masalan, `uz`) |

## Provayder va model parametrlari

Quyidagi jadvallar har bir provayder uchun joriy (2026 boshi holatiga) tavsiya
etiladigan model nomlarini ko'rsatadi. Eng so'nggi narx va modellar ro'yxatini
provayderning rasmiy hujjatlaridan tekshiring, chunki bu qiymatlar tez-tez
yangilanadi.

### LLM (chat) modellari — `LLM_MODEL`

| Provayder (`LLM_PROVIDER`) | Tavsiya etilgan `LLM_MODEL` | Izoh |
| --- | --- | --- |
| `groq` | `llama-3.3-70b-versatile` | Tezkor va sifatli, bepul limiti bor |
| `groq` | `llama-3.1-8b-instant` | Eng tez/arzon, oddiy vazifalar uchun |
| `openai` | `gpt-4o-mini` | Arzon va tez, ko'p tilni yaxshi tushunadi |
| `openai` | `gpt-4o` | Yuqori sifat, narxi qimmatroq |

### ASR (ovozni matnga o'girish) modellari — `ASR_MODEL`

| Provayder (`ASR_PROVIDER`) | Tavsiya etilgan `ASR_MODEL` | `ASR_API_KEY` manbasi | Izoh |
| --- | --- | --- | --- |
| `groq` (standart) | `whisper-large-v3` yoki `whisper-large-v3-turbo` | [console.groq.com](https://console.groq.com) | `turbo` versiyasi tezroq, biroz aniqligi past |
| `openai` | `whisper-1` | [platform.openai.com](https://platform.openai.com) | OpenAI-mos audio.transcriptions API |
| `gemini` | `gemini-1.5-flash` yoki `gemini-2.0-flash` | [aistudio.google.com](https://aistudio.google.com/app/apikey) | Audio promptga qo'shilib transkripsiya qilinadi |
| `qwen` | `qwen-audio-asr` | [dashscope.console.aliyun.com](https://dashscope.console.aliyun.com) | DashScope OpenAI-mos endpoint orqali |

## Boshqa ASR modeliga o'tish

ASR qismi `ASR_PROVIDER`, `ASR_MODEL`, `ASR_API_KEY` va `ASR_BASE_URL`
o'zgaruvchilari orqali sozlanadi, kod o'zgartirilishi shart emas (`asr.py`):

- **Groq Whisper** (standart): `ASR_PROVIDER=groq`, `ASR_MODEL=whisper-large-v3`
- **OpenAI Whisper**: `ASR_PROVIDER=openai`, `ASR_MODEL=whisper-1`, `ASR_API_KEY=<openai_key>`
- **OpenAI-mos boshqa server** (masalan, lokal Whisper serveri): `ASR_PROVIDER=openai`, `ASR_BASE_URL=http://localhost:PORT/v1`
- **Google Gemini**: `ASR_PROVIDER=gemini`, `ASR_MODEL=gemini-1.5-flash`, `ASR_API_KEY=<google_api_key>`
- **Qwen (Alibaba DashScope)**: `ASR_PROVIDER=qwen`, `ASR_MODEL=qwen-audio-asr`, `ASR_API_KEY=<dashscope_api_key>`

## Ishga tushirish

```bash
python main.py
```
