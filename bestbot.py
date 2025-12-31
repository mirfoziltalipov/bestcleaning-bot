from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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
            InlineKeyboardButton("🧹 Уборка дома", callback_data="home_clean"),
            InlineKeyboardButton("🏢 Мойка фасада", callback_data="facade_clean"),
            InlineKeyboardButton("🚿 Чистка канализаций", callback_data="sewer_clean")
        )
    else:
        kb.add(
            InlineKeyboardButton("🧹 Uy tozalash", callback_data="home_clean"),
            InlineKeyboardButton("🏢 Fasad yuvish", callback_data="facade_clean"),
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
        "✨ *Best Cleaning* ✨\n\n"
        "Профессиональные клининговые услуги:\n\n"
        "🧹 Уборка дома\n"
        "🏢 Мойка фасада\n"
        "🚿 Чистка канализаций\n\n"
        "Выберите услугу 👇"
        if lang == "ru" else
        "✨ *Best Cleaning* ✨\n\n"
        "Professional tozalash xizmatlari:\n\n"
        "🧹 Uy tozalash\n"
        "🏢 Fasad yuvish\n"
        "🚿 Kanalizatsiya tozalash\n\n"
        "Xizmatni tanlang 👇"
    )

    await call.message.answer(
        text,
        reply_markup=main_menu(lang),
        parse_mode="Markdown"
    )

# ===== Выбор услуги =====
@dp.callback_query_handler(lambda c: c.data in ["home_clean", "facade_clean", "sewer_clean"])
async def service_selected(call: types.CallbackQuery):
    lang = user_lang.get(call.from_user.id, "ru")

    if call.data == "home_clean":
        photo = "https://best-cleaning.uz/images/bg_1.jpg"
        caption = (
            "🧹 *Уборка дома*\n"
            "Цена: *от 150 000 сум*\n\n"
            "✔️ Квартиры и дома\n"
            "✔️ Экологичные средства\n"
            "✔️ Аккуратная работа"
            if lang == "ru" else
            "🧹 *Uy tozalash*\n"
            "Narx: *150 000 so‘mdan*\n\n"
            "✔️ Kvartira va uylar\n"
            "✔️ Ekologik vositalar\n"
            "✔️ Toza va tartibli"
        )

    elif call.data == "facade_clean":
        photo = "https://best-cleaning.uz/images/moyka-fasadov.jpg"
        caption = (
            "🏢 *Мойка фасада*\n"
            "Цена: *от 10 000 сум / м²*\n\n"
            "✔️ Современные технологии\n"
            "✔️ Ухоженный внешний вид"
            if lang == "ru" else
            "🏢 *Fasad yuvish*\n"
            "Narx: *10 000 so‘m / m² dan*\n\n"
            "✔️ Zamonaviy texnologiyalar\n"
            "✔️ Chiroyli tashqi ko‘rinish"
        )

    else:
        photo = "https://best-cleaning.uz/images/canal-main.png"
        caption = (
            "🚿 *Чистка канализаций*\n"
            "Цена: *от 200 000 сум*\n\n"
            "✔️ Устранение засоров\n"
            "✔️ Безопасно для труб"
            if lang == "ru" else
            "🚿 *Kanalizatsiya tozalash*\n"
            "Narx: *200 000 so‘mdan*\n\n"
            "✔️ Tiqinlarni bartaraf etish\n"
            "✔️ Quvurlar uchun xavfsiz"
        )

    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton(
            "📩 Оставить заявку" if lang == "ru" else "📩 Buyurtma qoldirish",
            callback_data="order"
        ),
        InlineKeyboardButton(
            "⬅️ На главное" if lang == "ru" else "⬅️ Asosiy menyu",
            callback_data="back"
        )
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

    # Ответ пользователю
    await message.answer(
        "✅ Заявка принята! Мы скоро свяжемся с вами."
        if lang == "ru" else
        "✅ Buyurtmangiz qabul qilindi! Tez orada siz bilan bog‘lanamiz."
    )

    # Сброс языка и возврат к выбору
    user_lang.pop(message.from_user.id, None)
    await message.answer(
        "🌐 Выберите язык / Tilni tanlang:",
        reply_markup=language_menu()
    )

# ===== Запуск =====
if __name__ == "__main__":
    print("Bot started")
    executor.start_polling(dp, skip_updates=True)
