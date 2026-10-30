# # ============================================================
# #  1-DARS — Birinchi bot
# # #  Maqsad: bot Telegramda javob bersin
# # #
# # #  YOZISH TARTIBI (o'quvchi shu tartibda yozadi):
# # #    1-bosqich: importlar + main() + ishga tushirish  -> bot ishlaydi, lekin jim
# # #    2-bosqich: start() handler                        -> /start ga javob beradi
# # #    3-bosqich: help_cmd() handler                     -> /help ga javob beradi
# # #    4-bosqich: echo() handler                         -> hamma narsani takrorlaydi
# # #
# # #  ISHGA TUSHIRISH:  python main.py
# # # ============================================================
# #
# # import asyncio
# # import logging
# # import os
# #
# # from aiogram import Bot, Dispatcher, F
# # from aiogram.client.default import DefaultBotProperties
# # from aiogram.enums import ParseMode
# # from aiogram.filters import Command, CommandStart
# # from aiogram.types import Message
# # from dotenv import load_dotenv
# #
# # load_dotenv()
# #
# # logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
# #
# # dp = Dispatcher()
# #
# #
# # # ---------- 2-bosqich ----------
# # @dp.message(CommandStart())
# # async def start(message: Message):
# #     await message.answer(
# #         f"Salom, <b>{message.from_user.full_name}</b>!\n\n"
# #         f"Men birinchi botman. /help yozing."
# #     )
# #
# #
# # # ---------- 3-bosqich ----------
# # @dp.message(Command("help"))
# # async def help_cmd(message: Message):
# #     await message.answer(
# #         "<b>Buyruqlar:</b>\n"
# #         "/start — boshlash\n"
# #         "/help — yordam\n\n"
# #         "Yoki oddiy matn yozing — men takrorlayman."
# #     )
# #
# #
# # # ---------- 4-bosqich ----------
# # # DIQQAT: bu handler ENG OXIRIDA turishi shart!
# # # Yuqoriga ko'chiring — /start ishlamay qoladi. Sinab ko'ring.
# # @dp.message(F.text)
# # async def echo(message: Message):
# #     await message.answer(f"Siz yozdingiz: {message.text}")
# #
# #
# # # ---------- 1-bosqich ----------
# # async def main():
# #     bot = Bot(
# #         token=os.getenv("BOT_TOKEN"),
# #         default=DefaultBotProperties(parse_mode=ParseMode.HTML),
# #     )
# #     me = await bot.get_me()
# #     logging.info("Bot ishga tushdi: @%s", me.username)
# #     await dp.start_polling(bot)
# #
# #
# # if __name__ == "__main__":
# #     asyncio.run(main())
# import json
# import telebot
# from telebot import types, custom_filters
# from telebot.handler_backends import State, StatesGroup
# from telebot.storage import StateMemoryStorage
# from config import TOKEN
#
# state_storage = StateMemoryStorage()
# bot = telebot.TeleBot(TOKEN, state_storage=state_storage)
#
# MENYU = {
#     "pitsa": ("🍕 Pitsa", 45000),
#     "burger": ("🍔 Burger", 30000),
#     "lavash": ("🌯 Lavash", 25000),
#     "choy": ("🍵 Choy", 5000)
# }
#
# FAYL = "buyurtmalar.json"
#
# def yukla() -> dict:
#     try:
#         with open(FAYL, "r", encoding="utf-8") as f:
#             return json.load(f)
#     except FileNotFoundError:
#         return {}
#
# def saqla(data: dict):
#     with open(FAYL, "w", encoding="utf-8") as f:
#         json.dump(data, f, ensure_ascii=False, indent=2)
#
# def buyurtma_saqla(chat_id: int, matn: str):
#     data = yukla()
#     cid_str = str(chat_id)
#     data.setdefault(cid_str, []).append(matn)
#     saqla(data)
#
# def buyurtmalar_ol(chat_id: int) -> list:
#     data = yukla()
#     return data.get(str(chat_id), [])
#
# def buyurtma_ochir(chat_id: int, i: int):
#     data = yukla()
#     cid_str = str(chat_id)
#     royxat = data.get(cid_str, [])
#     if not (0 <= i < len(royxat)):
#         return None
#     ochirilgan = royxat.pop(i)
#     saqla(data)
#     return ochirilgan
#
# def asosiy_menyu():
#     m = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     m.row("🍽 Buyurtma berish", "🧾 Mening buyurtmam")
#     m.row("📋 Menyu", "ℹ️ Yordam")
#     return m
#
# def taom_tugmalari():
#     m = types.InlineKeyboardMarkup(row_width=2)
#     m.add(*[
#         types.InlineKeyboardButton(f"{nom} — {narx} so'm", callback_data=f"taom_{kod}")
#         for kod, (nom, narx) in MENYU.items()
#     ])
#     return m
#
# def tasdiq_tugmalari():
#     m = types.InlineKeyboardMarkup(row_width=2)
#     m.add(
#         types.InlineKeyboardButton("✅ Ha", callback_data="ha"),
#         types.InlineKeyboardButton("❌ Yo'q", callback_data="yoq")
#     )
#     return m
#
# def bekor_tugmalari(royxat: list):
#     m = types.InlineKeyboardMarkup(row_width=5)
#     m.add(*[
#         types.InlineKeyboardButton(f"❌ {i + 1}", callback_data=f"bekor_{i}")
#         for i in range(len(royxat))
#     ])
#     return m
#
# def royxat_matni(royxat: list) -> str:
#     matn = "🧾 Sizning buyurtmalaringiz:\n"
#     for idx, item in enumerate(royxat, 1):
#         matn += f"{idx}. {item}\n"
#     matn += "\nBekor qilish — raqamni bosing 👇"
#     return matn
#
# class Buyurtma(StatesGroup):
#     taom = State()
#     soni = State()
#     tasdiq = State()
#
# @bot.message_handler(commands=['start'])
# def start_cmd(message):
#     bot.delete_state(message.from_user.id, message.chat.id)
#     ism = message.from_user.first_name
#     bot.send_message(
#         message.chat.id,
#         f"Salom, {ism}! ☕ Ustudy kafega xush kelibsiz.\nPastdagi tugmalardan tanlang 👇",
#         reply_markup=asosiy_menyu()
#     )
#
# @bot.message_handler(state="*", commands=['cancel'])
# def cancel_cmd(message):
#     bot.delete_state(message.from_user.id, message.chat.id)
#     bot.send_message(
#         message.chat.id,
#         "❌ Bekor qilindi",
#         reply_markup=asosiy_menyu()
#     )
#
# @bot.message_handler(commands=['help'])
# @bot.message_handler(func=lambda m: m.text == "ℹ️ Yordam")
# def help_cmd(message):
#     matn = (
#         "🍽 Buyurtma berish — taom → soni → tasdiqlash\n"
#         "🧾 Mening buyurtmam — buyurtmalarim, ❌ bekor qilish\n"
#         "📋 Menyu — taomlar va narxlar\n"
#         "/cancel — dialogni bekor qilish"
#     )
#     bot.send_message(message.chat.id, matn)
#
# @bot.message_handler(commands=['menyu'])
# @bot.message_handler(func=lambda m: m.text == "📋 Menyu")
# def menyu_cmd(message):
#     qatorlar = [f"{nom} — {narx} so'm" for nom, narx in MENYU.values()]
#     matn = "📋 Menyu:\n" + "\n".join(qatorlar)
#     bot.send_message(message.chat.id, matn)
#
# @bot.message_handler(commands=['mening'])
# @bot.message_handler(func=lambda m: m.text == "🧾 Mening buyurtmam")
# def mening_cmd(message):
#     royxat = buyurtmalar_ol(message.chat.id)
#     if not royxat:
#         bot.send_message(
#             message.chat.id,
#             "Hali buyurtma yo'q. 🍽 Buyurtma berish tugmasini bosing"
#         )
#     else:
#         bot.send_message(
#             message.chat.id,
#             royxat_matni(royxat),
#             reply_markup=bekor_tugmalari(royxat)
#         )
#
# @bot.message_handler(commands=['buyurtma'])
# @bot.message_handler(func=lambda m: m.text == "🍽 Buyurtma berish")
# def buyurtma_boshlash(message):
#     bot.set_state(message.from_user.id, Buyurtma.taom, message.chat.id)
#     bot.send_message(
#         message.chat.id,
#         "Nima buyurasiz? 👇 (/cancel — bekor qilish)",
#         reply_markup=taom_tugmalari()
#     )
#
# @bot.callback_query_handler(func=lambda c: c.data.startswith("taom_"), state=Buyurtma.taom)
# def taom_tanlandi(call):
#     kod = call.data.split("_")[1]
#     nom, narx = MENYU[kod]
#     with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
#         data["taom"] = nom
#         data["narx"] = narx
#     bot.set_state(call.from_user.id, Buyurtma.soni, call.message.chat.id)
#     bot.answer_callback_query(call.id)
#     bot.edit_message_text(
#         f"Tanlandi: {nom}",
#         chat_id=call.message.chat.id,
#         message_id=call.message.message_id
#     )
#     bot.send_message(call.message.chat.id, "Nechta? (1–10)")
#
# @bot.message_handler(state=Buyurtma.taom)
# def taom_xato(message):
#     bot.send_message(message.chat.id, "Tugmalardan birini bosing 👆 (yoki /cancel)")
#
# @bot.message_handler(state=Buyurtma.soni)
# def soni_qabul(message):
#     if not message.text.isdigit() or not (1 <= int(message.text) <= 10):
#         bot.send_message(message.chat.id, "1 dan 10 gacha son kiriting")
#         return
#     soni = int(message.text)
#     with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#         data["soni"] = soni
#         data["jami"] = data["narx"] * soni
#         taom_nomi = data["taom"]
#         jami_narx = data["jami"]
#     bot.set_state(message.from_user.id, Buyurtma.tasdiq, message.chat.id)
#     bot.send_message(
#         message.chat.id,
#         f"🧾 {taom_nomi} × {soni} = {jami_narx} so'm\nTasdiqlaysizmi?",
#         reply_markup=tasdiq_tugmalari()
#     )
#
# @bot.callback_query_handler(func=lambda c: c.data in ("ha", "yoq"), state=Buyurtma.tasdiq)
# def tasdiq_qabul(call):
#     with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
#         matn = f"{data['taom']} × {data['soni']} = {data['jami']} so'm"
#     bot.delete_state(call.from_user.id, call.message.chat.id)
#     if call.data == "ha":
#         buyurtma_saqla(call.message.chat.id, matn)
#         bot.answer_callback_query(call.id, "Qabul qilindi ✅")
#         bot.edit_message_text(
#             f"✅ Buyurtma qabul qilindi:\n{matn}\n⏱ 15 daqiqada tayyor!",
#             chat_id=call.message.chat.id,
#             message_id=call.message.message_id
#         )
#     else:
#         bot.answer_callback_query(call.id, "Bekor qilindi")
#         bot.edit_message_text(
#             "❌ Buyurtma bekor qilindi",
#             chat_id=call.message.chat.id,
#             message_id=call.message.message_id
#         )
#     bot.send_message(
#         call.message.chat.id,
#         "Yana nimadir kerakmi? 👇",
#         reply_markup=asosiy_menyu()
#     )
#
# @bot.message_handler(state=Buyurtma.tasdiq)
# def tasdiq_xato(message):
#     bot.send_message(message.chat.id, "✅ Ha yoki ❌ Yo'q tugmasini bosing 👆")
#
# @bot.callback_query_handler(func=lambda c: c.data.startswith("bekor_"))
# def bekor_qilish_call(call):
#     i = int(call.data.split("_")[1])
#     ochirilgan = buyurtma_ochir(call.message.chat.id, i)
#     if ochirilgan is None:
#         bot.answer_callback_query(call.id, "Bu buyurtma topilmadi. 🧾 Ro'yxatni qayta oching")
#         return
#     bot.answer_callback_query(call.id, f"❌ Bekor qilindi: {ochirilgan}")