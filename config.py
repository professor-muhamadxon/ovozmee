import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]

# Har bir provayder uchun standart modellar (agar alohida *_MODEL berilmasa)
DEFAULT_LLM_MODELS = {
    "groq": "llama-3.1-8b-instant",
    "openai": "gpt-4o-mini",
    "gemini": "gemini-2.5-flash",
}

DEFAULT_ASR_MODELS = {
    "groq": "whisper-large-v3",
    "openai": "whisper-1",
    "gemini": "gemini-2.5-flash",
    "qwen": "qwen-audio-asr",
}

# Chat (LLM) sozlamalari
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")  # groq | openai | gemini

LLM_API_KEY = os.getenv(f"{LLM_PROVIDER.upper()}_API_KEY") or os.getenv("LLM_API_KEY")
LLM_MODEL = (
    os.getenv(f"{LLM_PROVIDER.upper()}_LLM_MODEL")
    or os.getenv("LLM_MODEL")
    or DEFAULT_LLM_MODELS.get(LLM_PROVIDER, "")
)
LLM_BASE_URL = os.getenv(f"{LLM_PROVIDER.upper()}_BASE_URL") or os.getenv("LLM_BASE_URL")

# ASR (ovozni matnga o'girish) sozlamalari
ASR_PROVIDER = os.getenv("ASR_PROVIDER", "gemini")  # groq | openai | gemini | qwen

ASR_API_KEY = (
    os.getenv(f"{ASR_PROVIDER.upper()}_API_KEY")
    or os.getenv("ASR_API_KEY")
    or LLM_API_KEY
)
ASR_MODEL = (
    os.getenv(f"{ASR_PROVIDER.upper()}_ASR_MODEL")
    or os.getenv("ASR_MODEL")
    or DEFAULT_ASR_MODELS.get(ASR_PROVIDER, "")
)
ASR_BASE_URL = os.getenv(f"{ASR_PROVIDER.upper()}_BASE_URL") or os.getenv("ASR_BASE_URL")
ASR_LANGUAGE = os.getenv("ASR_LANGUAGE", "uz")
