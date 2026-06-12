SLEEP_KEYWORDS = [
    "uxlash", "uxlashga", "uxlaydigan", "uxlamoq", "tunar", "mehmonxona",
    "qonaqxona", "hostel", "dam olish", "dam olish joyi", "yotoqxona", "uylash"
]

FOOD_KEYWORDS = [
    "ovqat", "restoran", "kafe", "oshxona", "osh", "nonvoyxona",
    "supermarket", "do'kon", "bog'cha", "taom", "ichimlik"
]


def classify_request(text: str) -> str:
    text_lower = text.lower()
    if any(keyword in text_lower for keyword in SLEEP_KEYWORDS):
        return "sleep"
    if any(keyword in text_lower for keyword in FOOD_KEYWORDS):
        return "food"
    return "general"


def get_system_prompt(category: str) -> str:
    if category == "sleep":
        return (
            "Siz foydalanuvchiga uxlash joylarini topishda yordam beradigan aqlli yordamchisiz. "
            "Foydalanuvchi uxlash joyi haqida so'rasa, mehmonxona, motel, hostel yoki qonaqxona haqida javob bering. "
            "Ovqatxona yoki restoran haqida gapirmang."
        )
    if category == "food":
        return (
            "Siz foydalanuvchiga ovqatlanish joylarini topishda yordam beradigan aqlli yordamchisiz. "
            "Foydalanuvchi ovqat, restoran yoki kafe haqida so'rasa, shunga mos javob bering. "
            "Uxlash joylari haqida gapirmang."
        )
    return (
        "Siz foydalanuvchiga yordam beradigan chat asistentsiz. "
        "Savollarni o'zbek tilida tushunib, aniq va foydali javob qaytaring."
    )
