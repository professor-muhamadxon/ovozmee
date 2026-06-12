from groq import Groq

import config
from classifier import classify_request, get_system_prompt


GEMINI_OPENAI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"


def _make_client(provider: str, api_key: str | None, base_url: str | None):
    """OpenAI-mos (Groq, OpenAI, Gemini va boshqalar) klient yaratadi."""
    if provider == "openai":
        from openai import OpenAI
        return OpenAI(api_key=api_key, base_url=base_url)
    if provider == "gemini":
        from openai import OpenAI
        return OpenAI(api_key=api_key, base_url=base_url or GEMINI_OPENAI_BASE_URL)
    # default: groq (OpenAI-mos API)
    return Groq(api_key=api_key, base_url=base_url)


llm_client = _make_client(config.LLM_PROVIDER, config.LLM_API_KEY, config.LLM_BASE_URL)


async def ask_ai(question: str) -> str:
    category = classify_request(question)
    system_prompt = get_system_prompt(category)
    response = llm_client.chat.completions.create(
        model=config.LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        max_tokens=512,
        temperature=0.2
    )
    return response.choices[0].message.content.strip()


async def fallback_with_ai(lat: float, lon: float, category: str, user_query: str | None = None) -> str:
    # Ask AI to provide helpful fallback suggestions and search links
    user_desc = f"Foydalanuvchi so'rov: {user_query}" if user_query else ""
    prompt = (
        f"Siz yordamchisiz. Foydalanuvchi joy qidiryapti (kategoriya: {category}). "
        f"Foydalanuvchi taxminiy koordinatalar: {lat},{lon}. {user_desc} \n\n"
        "Agar aniq OSM ma'lumot topilmasa, foydalanuvchiga quyidagilarni bering (o'zbekcha):\n"
        "1) Qanday Google Maps yoki Telegram qidiruv so'rovi yozish kerak (misol bilan).\n"
        "2) Qisqa maslahatlar — qayerlarni tekshirish (mehmonxona, hostel, motel yoki restoran, kafe).\n"
        "3) Bitta Google Maps qidiruv linkini shakllantiring (misol: https://www.google.com/maps/search/?api=1&query=hotel+near+LAT+LON).\n"
        "Javobni 3-6 qatorgacha qisqa va aniq qilib yozing."
    )

    response = llm_client.chat.completions.create(
        model=config.LLM_MODEL,
        messages=[
            {"role": "system", "content": "Siz foydalanuvchiga yordam beradigan aqlli yordamchisiz."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.2
    )
    return response.choices[0].message.content.strip()
