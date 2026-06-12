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

Sozlash ikki bosqichli: avval qaysi provayderni ishlatishni tanlaysiz
(`LLM_PROVIDER` / `ASR_PROVIDER`), so'ng shu provayder uchun API kalit va
model nomini **alohida o'zgaruvchilarda** beradisiz. Har bir provayder uchun
alohida maydon bo'lgani uchun, ularning hammasini oldindan to'ldirib qo'yib,
keyin xohlagan paytda faqat `LLM_PROVIDER`/`ASR_PROVIDER`ni o'zgartirib
provayderlar orasida almashishingiz mumkin.

| O'zgaruvchi | Tavsif |
| --- | --- |
| `BOT_TOKEN` | Telegram bot tokeni (@BotFather) |
| `LLM_PROVIDER` | Hozir ishlatiladigan chat provayderi: `groq` \| `openai` \| `gemini` |
| `ASR_PROVIDER` | Hozir ishlatiladigan ASR provayderi: `groq` \| `openai` \| `gemini` \| `qwen` |
| `GROQ_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, `QWEN_API_KEY` | Har bir provayder uchun alohida API kalit |
| `GROQ_LLM_MODEL`, `OPENAI_LLM_MODEL`, `GEMINI_LLM_MODEL` | Har bir provayder uchun chat modeli |
| `GROQ_ASR_MODEL`, `OPENAI_ASR_MODEL`, `GEMINI_ASR_MODEL`, `QWEN_ASR_MODEL` | Har bir provayder uchun ASR modeli |
| `GROQ_BASE_URL`, `OPENAI_BASE_URL`, `GEMINI_BASE_URL`, `QWEN_BASE_URL` | Ixtiyoriy — OpenAI-mos boshqa server manzillari |
| `ASR_LANGUAGE` | Transkripsiya tili kodi (masalan, `uz`) |

## Provayder va model parametrlari

Quyidagi jadvallar har bir provayder uchun joriy (2026 boshi holatiga) tavsiya
etiladigan model nomlarini ko'rsatadi (`.env.example` faylida standart
qiymatlar sifatida qo'yilgan). Eng so'nggi narx va modellar ro'yxatini
provayderning rasmiy hujjatlaridan tekshiring, chunki bu qiymatlar tez-tez
yangilanadi.

### LLM (chat) modellari

| Provayder (`LLM_PROVIDER`) | O'zgaruvchi | Tavsiya etilgan model | Izoh |
| --- | --- | --- | --- |
| `groq` | `GROQ_LLM_MODEL` | `llama-3.1-8b-instant` yoki `llama-3.3-70b-versatile` | Tezkor/arzon yoki sifatliroq, bepul limiti bor |
| `openai` | `OPENAI_LLM_MODEL` | `gpt-4o-mini` yoki `gpt-4o` | Arzon-tez yoki yuqori sifat |
| `gemini` | `GEMINI_LLM_MODEL` | `gemini-2.5-flash` yoki `gemini-flash-3.5` | Google'ning OpenAI-mos endpointi orqali, bepul kvotasi bor |

### ASR (ovozni matnga o'girish) modellari

| Provayder (`ASR_PROVIDER`) | O'zgaruvchi | Tavsiya etilgan model | API kalit manbasi | Izoh |
| --- | --- | --- | --- | --- |
| `gemini` (standart) | `GEMINI_ASR_MODEL` | `gemini-2.5-flash`, `gemini-flash-3.5` yoki `gemini-2.0-flash` | [aistudio.google.com](https://aistudio.google.com/app/apikey) | Audio promptga qo'shilib transkripsiya qilinadi, bepul kvotasi bor |
| `groq` | `GROQ_ASR_MODEL` | `whisper-large-v3` yoki `whisper-large-v3-turbo` | [console.groq.com](https://console.groq.com) | `turbo` versiyasi tezroq, biroz aniqligi past |
| `openai` | `OPENAI_ASR_MODEL` | `whisper-1` | [platform.openai.com](https://platform.openai.com) | OpenAI-mos audio.transcriptions API |
| `qwen` | `QWEN_ASR_MODEL` | `qwen-audio-asr` | [dashscope.console.aliyun.com](https://dashscope.console.aliyun.com) | DashScope OpenAI-mos endpoint orqali |

## Provayderlar orasida almashish

Provayderni o'zgartirish uchun faqat `LLM_PROVIDER` va/yoki `ASR_PROVIDER`ni
yangilang — tegishli `*_API_KEY`, `*_LLM_MODEL`/`*_ASR_MODEL` va ixtiyoriy
`*_BASE_URL` qiymatlari `.env`da allaqachon tayyor turadi, kodga tegish
shart emas (`config.py`, `ai.py`, `asr.py`):

```bash
# Misol: ASR'ni Gemini'dan Groq Whisper'ga o'tkazish
ASR_PROVIDER=groq

# Misol: chatni OpenAI'ga o'tkazish
LLM_PROVIDER=openai
```

## Ishga tushirish

```bash
python main.py
```

## Bot buyruqlari va foydalanish

| Buyruq / Xabar turi | Tavsif |
| --- | --- |
| `/start` | Botni ishga tushiradi, salomlashadi va lokatsiya yuborish tugmasini ko'rsatadi |
| 📍 Lokatsiya | Foydalanuvchi joylashuvini saqlaydi — keyingi qidiruvlar shu nuqta atrofida (3 km) bo'ladi |
| 💬 Matnli xabar | So'rovni tahlil qilib, kategoriyaga (uxlash/ovqat/umumiy) mos javob qaytaradi |
| 🎤 Ovozli xabar | Xabarni ASR orqali matnga o'giradi, so'ng matnli xabar kabi qayta ishlaydi |

**Foydalanish tartibi:**

1. `/start` buyrug'ini yuboring
2. 📍 tugmasi orqali lokatsiyangizni yuboring
3. Matnli yoki ovozli xabar bilan nima qidirayotganingizni ayting (masalan: "yaqin atrofda mehmonxona bor-mi?" yoki "ovqatlanadigan joy kerak")
