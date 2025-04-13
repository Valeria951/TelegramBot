import os
import requests
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

TOKEN = "7751933750:AAGlvaf2Ue79LHcLIdEDpD8W7mgUzFmKV8A"
DEEPSEEK_API = "sk-70337bd08fd84abdbc5ef51e58f90e08"
YANDEX_API = "aje8s4mem40cul2f37g4"
ADMIN_CONTACT = "CardMagicBot@yandex.com"  # Ваша почта для жалоб

# Логирование
def log(user_id, text):
    with open("logs.txt", "a") as f:
        f.write(f"{datetime.now()} | Пользователь {user_id}: {text}\n")

# Команда /start
async def start(update: Update, context):
    warning = "⚠️ Изображения созданы ИИ. Не используйте их в коммерческих целях без разрешения!"
    await update.message.reply_text(f"Привет! Напиши текст для открытки.\n\n{warning}")

# Жалобы через /report
async def report(update: Update, context):
    user_id = update.message.from_user.id
    with open("reports.txt", "a") as f:
        f.write(f"Жалоба от {user_id}: {update.message.text}\n")
    await update.message.reply_text("Жалоба отправлена. Контакты для связи: " + ADMIN_CONTACT)

# Генерация открытки
async def generate_card(update: Update, context):
    user_id = update.message.from_user.id
    user_text = update.message.text
    log(user_id, user_text)  # Сохраняем логи

    try:
        # Генерация текста через DeepSeek
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {DEEPSEEK_API}"},
            json={"messages": [{"role": "user", "content": user_text}]}
        )
        card_text = response.json()['choices'][0]['message']['content']

        # Генерация картинки через Яндекс (пример API)
        image_response = requests.post(
            "https://vision.yandex.net/api/v1/analyze",
            headers={"Authorization": f"Api-Key {YANDEX_API}"},
            json={"text": user_text}
        )
        with open("card.jpg", "wb") as f:
            f.write(image_response.content)

        await update.message.reply_photo(photo=open("card.jpg", "rb"), caption=card_text)
    except Exception as e:
        await update.message.reply_text("Ошибка. Попробуйте позже.")

# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_card))
    app.run_polling() async def donate(update: Update, context):
    await update.message.reply_text("Оплатите 100 руб: https://www.donationalerts.com/widget/goal/8696196?token=xGrjipJxWhxvxaNMYIT3")
# И добавьте обработчик в блок __main__:
app.add_handler(CommandHandler("donate", donate))# Добавьте эту функцию ДО блока if __name__ == "__main__":
async def donate(update: Update, context):
    await update.message.reply_text("Оплатите 50 руб: ВАША_ССЫЛКА_ОТ_DONATEBOT")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("donate", donate))  # Добавьте эту строку
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_card))
    app.run_polling()
    from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
async def donate(update: Update, context):
    await update.message.reply_text("...")  # ← отступ здесь
