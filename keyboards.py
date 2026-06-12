from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_location_keyboard() -> ReplyKeyboardMarkup:
    button = KeyboardButton(text="📍 Lokatsiyani yuborish", request_location=True)
    return ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)
