

questions = [
    {"q": "Python'da ro'yxat qaysi qavsda yoziladi?", "opts": ["( )", "[ ]", "{ }"], "a": 1},
    {"q": "2 ** 3 nechaga teng?", "opts": ["6", "8", "9"], "a": 1},
    {"q": "Bot tokenini kim beradi?", "opts": ["@BotFather", "@Python", "Google"], "a": 0}
]


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🎮 Boshlash", "ℹ️ Yordam")
    await message.answer("Salom! 🧠 Mini viktorinaga xush kelibsiz.", reply_markup=kb)

print("hello world")

print("prpr")