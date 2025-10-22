from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime
from schedule import schedule  # импортируем расписание

def current_week_number():
    start_date = datetime(datetime.now().year, 9, 1)
    today = datetime.now()
    delta_days = (today - start_date).days
    return (delta_days // 7) % 2 + 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Понедельник", "Вторник", "Среда"], ["Четверг", "Пятница", "Суббота"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text("Выберите день недели:", reply_markup=reply_markup)

async def handle_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text in schedule:
        week = current_week_number()
        await update.message.reply_text(f"{text}, группа 10405223.\n\nТекущая неделя — {week}-я по счёту.\n{schedule[text]}")
    else:
        await update.message.reply_text("Выберите день недели из меню ниже.")

if __name__ == "__main__":
    TOKEN = "8243623540:AAHOsfoM37l3vXjUbx4MHYOF1cZErnf9DKQ"
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_day))

    print("Бот запущен...")
    app.run_polling()
