from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import executor
import logging

# ========= НАСТРОЙКИ =========
BOT_TOKEN = "8450463741:AAEEXMafe22Lb-YLQlgum7Mopmp3z90yHoE"
GROUP_ID = -1003432542399
# =============================

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# ===== Хранилище языка пользователей =====
user_lang = {}

# ===== Меню выбора языка =====
def language_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton("🇺🇿 O‘zbekcha", callback_data="lang_uz")
    )
    return kb

# ===== Главное меню услуг =====
def main_menu(lang):
    kb = InlineKeyboardMarkup(row_width=1)

    if lang == "ru":
        kb.add(
            InlineKeyboardButton("🧹 Уборка", callback_data="cleaning"),
            InlineKeyboardButton("🏢 Мойка фасадов", callback_data="facade_clean"),
            InlineKeyboardButton("🧼 Мойка ковров", callback_data="carpet_clean"),
            InlineKeyboardButton("🛋 Чистка мебели", callback_data="furniture_clean"),
            InlineKeyboardButton("🪑 Чистка стульев", callback_data="chair_clean"),
            InlineKeyboardButton("🚿 Чистка канализации", callback_data="sewer_clean")
        )
    else:
        kb.add(
            InlineKeyboardButton("🧹 Tozalash", callback_data="cleaning"),
            InlineKeyboardButton("🏢 Fasad yuvish", callback_data="facade_clean"),
            InlineKeyboardButton("🧼 Gilam yuvish", callback_data="carpet_clean"),
            InlineKeyboardButton("🛋 Mebel tozalash", callback_data="furniture_clean"),
            InlineKeyboardButton("🪑 Stul tozalash", callback_data="chair_clean"),
            InlineKeyboardButton("🚿 Kanalizatsiya tozalash", callback_data="sewer_clean")
        )

    return kb

# ===== /start =====
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_lang.pop(message.from_user.id, None)
    await message.answer(
        "🌐 Выберите язык / Tilni tanlang:",
        reply_markup=language_menu()
    )

# ===== Установка языка =====
@dp.callback_query_handler(lambda c: c.data.startswith("lang_"))
async def set_language(call: types.CallbackQuery):
    lang = call.data.split("_")[1]
    user_lang[call.from_user.id] = lang

    text = (
        "✨ *Best Cleaning* ✨\n\nВыберите услугу 👇"
        if lang == "ru" else
        "✨ *Best Cleaning* ✨\n\nXizmatni tanlang 👇"
    )

    await call.message.answer(
        text,
        reply_markup=main_menu(lang),
        parse_mode="Markdown"
    )

# ===== Выбор услуги =====
@dp.callback_query_handler(lambda c: c.data in ["cleaning","facade_clean","carpet_clean","furniture_clean","chair_clean","sewer_clean"])
async def service_selected(call: types.CallbackQuery):
    lang = user_lang.get(call.from_user.id, "ru")

    if call.data == "cleaning":
        photo = "https://best-cleaning.uz/images/bg_1.jpg"
        caption = (
            "🧹 *Уборка*\nЦена: *350 000 сум*\nЕсли уборщицы со своими средствами — *550 000 сум*"
            if lang == "ru" else
            "🧹 *Tozalash*\nNarx: *350 000 so‘m*\nAgar xodimlar o‘z vositalari bilan kelsa — *550 000 so‘m*"
        )
    elif call.data == "facade_clean":
        photo = "https://best-cleaning.uz/images/moyka-fasadov.jpg"
        caption = (
            "🏢 *Мойка фасадов*\nЦена: *15 000 сум / м²*"
            if lang == "ru" else
            "🏢 *Fasad yuvish*\nNarx: *15 000 so‘m / m²*"
        )
    elif call.data == "carpet_clean":
        photo = "https://www.afisha.uz/uploads/media/2020/06/0690269_m.jpeg"
        caption = (
            "🧼 *Мойка ковров*\nЦена: *20 000 сум*"
            if lang == "ru" else
            "🧼 *Gilam yuvish*\nNarx: *20 000 so‘m*"
        )
    elif call.data == "furniture_clean":
        photo = "https://newcleaner.uz/wp-content/uploads/2024/02/332018086_w640_h640_pylesos-karcher-puzzi.webp"
        caption = (
            "🛋 *Чистка мебели*\nЦена: *100 000 сум / 1 место*"
            if lang == "ru" else
            "🛋 *Mebel tozalash*\nNarx: *100 000 so‘m / 1 joy*"
        )
    elif call.data == "chair_clean":
        photo = "https://files.glotr.uz/company/000/015/035/products/2020/05/18/2020-05-18-10-31-24-207011-5c05beba1a1fc00a280b8bfc76fcb3fe.jpg?_=ozb9y"
        caption = (
            "🪑 *Чистка стульев*\nЦена: *до 50 000 сум*"
            if lang == "ru" else
            "🪑 *Stul tozalash*\nNarx: *50 000 so‘m*"
        )
    else:
        photo = "https://best-cleaning.uz/images/canal-main.png"
        caption = (
            "🚿 *Чистка канализации*\nЦена: *45 000 сум / м*"
            if lang == "ru" else
            "🚿 *Kanalizatsiya tozalash*\nNarx: *45 000 so‘m / m*"
        )

    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("📩 Оставить заявку" if lang == "ru" else "📩 Buyurtma qoldirish", callback_data="order"),
        InlineKeyboardButton("⬅️ На главное" if lang == "ru" else "⬅️ Asosiy menyu", callback_data="back")
    )

    await call.message.answer_photo(
        photo=photo,
        caption=caption,
        reply_markup=kb,
        parse_mode="Markdown"
    )

# ===== Оставить заявку =====
@dp.callback_query_handler(lambda c: c.data == "order")
async def leave_order(call: types.CallbackQuery):
    lang = user_lang.get(call.from_user.id, "ru")
    await call.message.answer(
        "📩 Отправьте заявку одним сообщением:\nИмя, телефон, адрес"
        if lang == "ru" else
        "📩 Buyurtmani bitta xabarda yuboring:\nIsm, telefon, manzil"
    )

# ===== Назад к услугам =====
@dp.callback_query_handler(lambda c: c.data == "back")
async def back(call: types.CallbackQuery):
    lang = user_lang.get(call.from_user.id, "ru")
    await call.message.answer(
        "Выберите услугу 👇" if lang == "ru" else "Xizmatni tanlang 👇",
        reply_markup=main_menu(lang)
    )

# ===== Приём заявки =====
@dp.message_handler()
async def forward_to_group(message: types.Message):
    lang = user_lang.get(message.from_user.id, "ru")
    group_text = (
        "📩 *Новая заявка*\n\n"
        f"👤 {message.from_user.full_name}\n"
        f"🆔 `{message.from_user.id}`\n\n"
        f"{message.text}"
    )
    await bot.send_message(GROUP_ID, group_text, parse_mode="Markdown")

    await message.answer(
        "✅ Заявка принята! Мы скоро свяжемся с вами."
        if lang == "ru" else
        "✅ Buyurtmangiz qabul qilindi! Tez orada siz bilan bog‘lanamiz."
    )

    user_lang.pop(message.from_user.id, None)
    await message.answer(
        "🌐 Выберите язык / Tilni tanlang:",
        reply_markup=language_menu()
    )

# ===== Запуск =====
if __name__ == "__main__":
    print("Bot started")
    executor.start_polling(dp, skip_updates=True)

