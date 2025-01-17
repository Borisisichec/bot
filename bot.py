
import random
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Загадки с уровнями сложности
riddles = {
    "easy": [
        {"question": "Что можно увидеть с закрытыми глазами?", "options": ["Сон", "Тень", "Мечту"], "answer": "Сон"},
        {"question": "Зимой и летом одним цветом. Что это?", "options": ["Ёлка", "Трава", "Лист"], "answer": "Ёлка"}
    ],
    "medium": [
        {"question": "Что становится больше, если из него брать?", "options": ["Яма", "Дыра", "Куб"], "answer": "Яма"},
        {"question": "Сто одежек и все без застежек. Что это?", "options": ["Капуста", "Лук", "Кукуруза"],
         "answer": "Капуста"}
    ],
    "hard": [
        {"question": "Летит — молчит, лежит — молчит, когда умрёт — кричит. Что это?",
         "options": ["Стрела", "Снег", "Лист"], "answer": "Снег"},
        {"question": "У какого месяца 28 дней?", "options": ["Февраль", "Все", "Январь"], "answer": "Все"}
    ]
}

# Хранение очков игроков и их позиций
user_scores = {}
user_positions = {}


# Главное меню с кнопками
def main_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("🧩 Загадка")],
            [KeyboardButton("🏆 Рейтинг"), KeyboardButton("📊 Мой счёт")]
        ],
        resize_keyboard=True
    )


# Стартовая команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_scores[user_id] = {"correct": 0, "wrong": 0}
    user_positions[user_id] = None
    await update.message.reply_text("Добро пожаловать! Выбери действие ниже:", reply_markup=main_menu())


# Новая загадка
async def send_riddle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    riddle = random.choice(riddles["easy"])
    context.user_data['answer'] = riddle['answer']

    reply_markup = ReplyKeyboardMarkup(
        [[option] for option in riddle['options']], one_time_keyboard=True, resize_keyboard=True
    )

    await update.message.reply_text(f"{riddle['question']}", reply_markup=reply_markup)


# Проверка ответа и уведомления
async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_answer = update.message.text
    correct_answer = context.user_data.get('answer')

    if user_answer == correct_answer:
        user_scores[user_id]["correct"] += 1
        await update.message.reply_text("Правильно! 👍", reply_markup=main_menu())
    else:
        user_scores[user_id]["wrong"] += 1
        await update.message.reply_text(f"Неправильно. Правильный ответ: {correct_answer}.", reply_markup=main_menu())

    await check_ranking_changes(context)


# Проверка изменений в рейтинге
async def check_ranking_changes(context: ContextTypes.DEFAULT_TYPE):
    sorted_scores = sorted(user_scores.items(), key=lambda x: x[1]["correct"], reverse=True)
    current_positions = {user_id: position for position, (user_id, _) in enumerate(sorted_scores, start=1)}

    for user_id, new_position in current_positions.items():
        previous_position = user_positions.get(user_id)

        # Уведомление о первом месте
        if new_position == 1 and previous_position != 1:
            await context.bot.send_message(user_id, "🎉 Поздравляем! Ты поднялся на 1 место!")

        # Уведомление о потере позиции
        if previous_position and new_position > previous_position:
            await context.bot.send_message(user_id, "⚠️ Кто-то обогнал тебя в рейтинге. Догоняй!")

        user_positions[user_id] = new_position



# Показ рейтинга
async def show_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sorted_scores = sorted(user_scores.items(), key=lambda x: x[1]["correct"], reverse=True)
    leaderboard = "🏆 *Таблица лидеров:*\n\n"

    for i, (user_id, score) in enumerate(sorted_scores, start=1):
        user_name = (await context.bot.get_chat(user_id)).first_name
        leaderboard += f"{i}. {user_name}: {score['correct']} правильных ответов\n"

    await update.message.reply_text(leaderboard, parse_mode='Markdown', reply_markup=main_menu())


# Показ личного счёта
async def show_score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    score = user_scores.get(user_id, {"correct": 0, "wrong": 0})
    await update.message.reply_text(
        f"📊 Твой счёт:\n✅ Правильных: {score['correct']}\n❌ Ошибок: {score['wrong']}",
        reply_markup=main_menu()
    )


# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🧩 Загадка":
        await send_riddle(update, context)
    elif text == "🏆 Рейтинг":
        await show_leaderboard(update, context)
    elif text == "📊 Мой счёт":
        await show_score(update, context)
    else:
        await check_answer(update, context)


# Запуск бота
def main():
    TOKEN = '7973384839:AAHtI2UJrzNnRwWTJZo_-xCQdd1BcZkwLy4'  # Замени на свой токен
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


    app.run_polling()


if __name__ == "__main__":
    main()

