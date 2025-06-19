from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes


TOKEN = "7430127739:AAGja3SxBUvvd2Shd913BmH4D5h88nxE0c0"
CHANNEL_ID = "@qKzesSXCvq5iOTli"  # канал Лолы

LANGUAGES = {
    "🇷🇺 Русский": "ru",
    "🇬🇧 English": "en",
    "🇺🇿 O‘zbek": "uz"
}

WELCOME_MESSAGES = {
    "ru": "Привет, я Лола 💋\nЯ твоя виртуальная подруга. Готова показать тебе что-то интересное 😉",
    "en": "Hi, I'm Lola 💋\nYour virtual girlfriend. Ready to show you something fun 😉",
    "uz": "Salom, men Lola 💋\nMen sizning virtual dugonangizman. Qiziqarli narsalarni ko'rsatishga tayyorman 😉"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(lang, callback_data=f"lang_{code}")] for lang, code in LANGUAGES.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Выберите язык / Choose a language / Tilni tanlang:", reply_markup=reply_markup)

async def handle_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang_code = query.data.split("_")[1]
    context.user_data['lang'] = lang_code

    user_id = query.from_user.id
    chat_member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
    if chat_member.status in ["member", "administrator", "creator"]:
        await query.edit_message_text(WELCOME_MESSAGES[lang_code] + "\n\nТы уже подписан на канал 💖")
    else:
        await send_subscription_prompt(query, lang_code)

async def send_subscription_prompt(entity, lang_code):
    keyboard = [[
        InlineKeyboardButton("Подписаться 🔐", url="https://t.me/+qKzesSXCvq5iOTli")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = {
        "ru": "🔐 Чтобы получить доступ, сначала подпишись на мой приватный канал:",
        "en": "🔐 To get access, first subscribe to my private channel:",
        "uz": "🔐 Kirish uchun avval maxfiy kanalga obuna bo'ling:"
    }
    await entity.edit_message_text(text[lang_code], reply_markup=reply_markup)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^(🇷🇺|🇬🇧|🇺🇿)"), start))
app.add_handler(CommandHandler("lang", start))
app.add_handler(CallbackQueryHandler(handle_language, pattern="^lang_"))
app.run_polling()
