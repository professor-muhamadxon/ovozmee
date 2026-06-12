import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]

# Chat (LLM) sozlamalari
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")  # groq | openai
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
LLM_BASE_URL = os.getenv("LLM_BASE_URL")

# ASR (ovozni matnga o'girish) sozlamalari
ASR_PROVIDER = os.getenv("ASR_PROVIDER", "groq")  # groq | openai | gemini | qwen
ASR_API_KEY = os.getenv("ASR_API_KEY", LLM_API_KEY)
ASR_MODEL = os.getenv("ASR_MODEL", "whisper-large-v3")
ASR_BASE_URL = os.getenv("ASR_BASE_URL")
ASR_LANGUAGE = os.getenv("ASR_LANGUAGE", "uz")
