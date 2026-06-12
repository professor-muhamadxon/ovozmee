"""Turli ASR (ovozni matnga o'girish) provayderlari uchun yagona interfeys.

Qo'llab-quvvatlanadigan provayderlar (ASR_PROVIDER):
  - groq    — Groq Whisper (OpenAI-mos audio.transcriptions API)
  - openai  — OpenAI Whisper (OpenAI-mos audio.transcriptions API)
  - gemini  — Google Gemini (audio faylni promptga qo'shib transkripsiya)
  - qwen    — Alibaba Qwen ASR (DashScope, OpenAI-mos chat completions + audio input)
"""

import base64

import config


async def transcribe_voice(audio_data: bytes) -> str:
    provider = config.ASR_PROVIDER

    if provider in ("groq", "openai"):
        return _transcribe_whisper(audio_data)
    if provider == "gemini":
        return _transcribe_gemini(audio_data)
    if provider == "qwen":
        return _transcribe_qwen(audio_data)

    raise ValueError(f"Noma'lum ASR_PROVIDER: {provider}")


def _transcribe_whisper(audio_data: bytes) -> str:
    from groq import Groq

    if config.ASR_PROVIDER == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=config.ASR_API_KEY, base_url=config.ASR_BASE_URL)
    else:
        client = Groq(api_key=config.ASR_API_KEY, base_url=config.ASR_BASE_URL)

    transcription = client.audio.transcriptions.create(
        file=("voice.ogg", audio_data, "audio/ogg"),
        model=config.ASR_MODEL,
        language=config.ASR_LANGUAGE,
    )
    return transcription.text.strip()


def _transcribe_gemini(audio_data: bytes) -> str:
    import google.generativeai as genai

    genai.configure(api_key=config.ASR_API_KEY)
    model = genai.GenerativeModel(config.ASR_MODEL)

    response = model.generate_content([
        {"mime_type": "audio/ogg", "data": audio_data},
        "Ushbu audio xabarni so'zma-so'z transkripsiya qil. "
        "Faqat transkripsiya matnini qaytar, izoh qo'shma.",
    ])
    return response.text.strip()


def _transcribe_qwen(audio_data: bytes) -> str:
    from openai import OpenAI

    base_url = config.ASR_BASE_URL or "https://dashscope.aliyuncs.com/compatible-mode/v1"
    client = OpenAI(api_key=config.ASR_API_KEY, base_url=base_url)

    audio_b64 = base64.b64encode(audio_data).decode("utf-8")
    response = client.chat.completions.create(
        model=config.ASR_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {"data": audio_b64, "format": "ogg"},
                    },
                ],
            }
        ],
    )
    return response.choices[0].message.content.strip()
