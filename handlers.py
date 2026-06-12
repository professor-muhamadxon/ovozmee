import httpx
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

import config
from ai import ask_ai, fallback_with_ai
from asr import transcribe_voice
from classifier import classify_request
from keyboards import get_location_keyboard
from places import search_places

router_dp = Dispatcher()

# store user locations after they send location
user_locations: dict = {}


async def handle_place_search(bot: Bot, message: Message, category: str, query_text: str) -> None:
    """Lokatsiyaga asoslanib yaqin joylarni topib, foydalanuvchiga yuboradi."""
    loc = user_locations.get(message.from_user.id)
    if not loc:
        await message.answer("❗️ Avval lokatsiyangizni yuboring (📍). Keyin yaqin joylarni qidiraman.")
        return

    places = await search_places(loc["lat"], loc["lon"], category)
    if not places:
        fallback = await fallback_with_ai(loc["lat"], loc["lon"], category, query_text)
        await message.answer(fallback)
        return

    await message.answer(f"📍 Yaqin joylar ({category}):")
    for i, p in enumerate(places, 1):
        latp = p.get("lat")
        lonp = p.get("lon")
        name = p.get("name")
        if latp and lonp:
            try:
                await bot.send_location(chat_id=message.chat.id, latitude=latp, longitude=lonp)
            except Exception:
                pass
            maps_link = f"https://www.google.com/maps?q={latp},{lonp}"
            await message.answer(f"{i}. {name}\n🗺 {maps_link}")
        else:
            await message.answer(f"{i}. {name}")


async def process_query(bot: Bot, message: Message, text: str) -> None:
    """Matn (yoki transkripsiya qilingan ovoz) bo'yicha javob beradi."""
    category = classify_request(text)
    if category in ("sleep", "food"):
        await handle_place_search(bot, message, category, text)
    else:
        answer = await ask_ai(text)
        await message.answer(answer)


@router_dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        f"Assalomu alaykum, {message.from_user.first_name}!\n\n"
        "Avval lokatsiyangizni yuboring (📍), so'ng ovozli yoki matnli xabar yuboring.",
        reply_markup=get_location_keyboard()
    )


@router_dp.message(F.location)
async def handle_location(message: Message):
    user_locations[message.from_user.id] = {
        "lat": message.location.latitude,
        "lon": message.location.longitude
    }
    await message.answer(
        "✅ Lokatsiya qabul qilindi!\n\n"
        "Endi ovozli yoki matnli xabar yuboring — meni nima topishimni ayting!"
    )


@router_dp.message(F.text)
async def handle_text(message: Message, bot: Bot):
    user_text = message.text.strip()
    if not user_text:
        return
    await message.answer("🔄 So'rovingiz tahlil qilinmoqda...")
    try:
        await process_query(bot, message, user_text)
    except Exception as exc:
        await message.answer("❗️ Kechirasiz, hozir javob bera olmayapman. Iltimos, keyinroq qayta urinib ko'ring.")
        print(f"AI javob xatosi: {exc}")


@router_dp.message(F.voice)
async def handle_voice(message: Message, bot: Bot):
    await message.answer("🔄 Ovozingizni transkripsiya qilayapman...")

    voice_file = await bot.get_file(message.voice.file_id)
    file_url = f"https://api.telegram.org/file/bot{config.BOT_TOKEN}/{voice_file.file_path}"

    async with httpx.AsyncClient() as client:
        audio_response = await client.get(file_url, timeout=30)
        audio_response.raise_for_status()
        audio_data = audio_response.content

    try:
        text = await transcribe_voice(audio_data)
    except Exception as exc:
        await message.answer("❗️ Ovozni transkripsiya qilishda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
        print(f"Transcription error: {exc}")
        return

    if not text:
        await message.answer("❗️ Ovozdan matn olish imkoni bo'lmadi. Iltimos, yana bir bor sinab ko'ring.")
        return

    await message.answer(f"🎤 Siz dedingiz: {text}")
    try:
        await process_query(bot, message, text)
    except Exception as exc:
        await message.answer("❗️ AI javob berishda xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring.")
        print(f"AI javob xatosi: {exc}")
