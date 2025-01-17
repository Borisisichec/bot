
import random
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Загадки с уровнями сложности
riddles = {
    "easy": [
        {
            "question": "Что можно увидеть с закрытыми глазами?",
            "options": ["Сон", "Тень", "Мечту"],
            "answer": "Сон"
        },
        {
            "question": "Зимой и летом одним цветом. Что это?",
            "options": ["Ёлка", "Трава", "Лист"],
            "answer": "Ёлка"
        },
        {
            "question": "Что нельзя съесть на завтрак?",
            "options": ["Обед", "Яблоко", "Суп"],
            "answer": "Обед"
        },
        {
            "question": "Что принадлежит вам, но другие используют чаще, чем вы?",
            "options": ["Имя", "Речь", "Ключ"],
            "answer": "Имя"
        },
        {
            "question": "Какая вещь нужна вам, чтобы увидеть своё отражение?",
            "options": ["Зеркало", "Вода", "Стекло"],
            "answer": "Зеркало"
        },
        {
            "question": "Что становится мокрым, когда сушит?",
            "options": ["Полотенце", "Дождь", "Снег"],
            "answer": "Полотенце"
        },
        {
            "question": "Что не имеет начала, конца или середины?",
            "options": ["Круг", "Линия", "Вечность"],
            "answer": "Круг"
        },
        {
            "question": "Оно ходит, но никогда не двигается. Что это?",
            "options": ["Часы", "Время", "Тень"],
            "answer": "Часы"
        },
    ],
    "medium": [
        {
            "question": "Что всегда перед нами, но мы его не видим?",
            "options": ["Будущее", "Солнце", "Ночь"],
            "answer": "Будущее"
        },
        {
            "question": "Что становится больше, если из него брать?",
            "options": ["Яма", "Дыра", "Куб"],
            "answer": "Яма"
        },
        {
            "question": "Сто одежек и все без застежек. Что это?",
            "options": ["Капуста", "Лук", "Кукуруза"],
            "answer": "Капуста"
        },
        {
            "question": "Что можно удержать, не трогая?",
            "options": ["Слово", "Тень", "Мысль"],
            "answer": "Слово"
        },
        {
            "question": "Что всегда идёт, но никогда не приходит?",
            "options": ["Время", "Тень", "Ночь"],
            "answer": "Время"
        },
        {
            "question": "Что живёт только тогда, когда ест?",
            "options": ["Огонь", "Животное", "Дерево"],
            "answer": "Огонь"
        },

    ],
    "hard": [
        {
            "question": "Чем больше ее стираешь, тем больше она становится. Что это?",
            "options": ["Доска", "Дыра", "Пятно"],
            "answer": "Дыра"
        },
        {
            "question": "У какого животного всегда холодный нос?",
            "options": ["Собака", "Пингвин", "Кошка"],
            "answer": "Собака"
        },
        {
            "question": "Что падает, но никогда не поднимается?",
            "options": ["Дождь", "Снег", "Тень"],
            "answer": "Дождь"
        },
        {

            "question": "Что легче воды, но не удержится в ведре?",
            "options": ["Воздух", "Туман", "Пена"],
            "answer": "Воздух"
        },
        {
            "question": "Что можно удерживать только один раз?",
            "options": ["Дыхание", "Слово", "Мгновение"],
            "answer": "Дыхание"
        },
        {
            "question": "На каком месте в соревновании вы окажетесь, если обгоните того, кто второй?",
            "options": ["Первое", "Второе", "Третье"],
            "answer": "Второе"
        },
        {
            "question": "Летит — молчит, лежит — молчит, когда умрёт — кричит. Что это?",
            "options": ["Стрела", "Снег", "Лист"],
            "answer": "Снег"
        },
        {
            "question": "Что имеет зубы, но не кусает?",
            "options": ["Пила", "Гребень", "Вилка"],
            "answer": "Гребень"
        },
        {
            "question": "У какого месяца 28 дней?",
            "options": ["Февраль", "Все", "Январь"],
            "answer": "Все"
        },
        {
            "question": "Это не может быть использовано, пока не сломано. Что это?",
            "options": ["Яйцо", "Секрет", "Пазл"],
            "answer": "Яйцо"
        },
        {
            "question": "Что растёт вниз головой?",
            "options": ["Корни", "Пещера", "Лавина"],
            "answer": "Корни"
        },
        {
            "question": "Какое слово пишется неправильно во всех словарях?",
            "options": ["Неправильно", "Ошибочно", "Слово"],
            "answer": "Неправильно"
        },
        {
            "question": "Я существую только тогда, когда есть свет, но я исчезаю, если свет меня касается. Что я?",
            "options": ["Тень", "Радуга", "Сон"],
            "answer": "Тень"
        },
        {
            "question": "Что всегда в движении, но не меняет своего места?",
            "options": ["Река", "Время", "Ветер"],
            "answer": "Река"
        },
        {
            "question": "Что становится длиннее, когда его тянуть, но короче, когда его складывают?",
            "options": ["Резинка", "Рулетка", "Шнур"],
            "answer": "Резинка"
        },
        {
            "question": "Что может путешествовать по миру, оставаясь в одном и том же углу?",
            "options": ["Марка", "Карта", "Письмо"],
            "answer": "Марка"
        },
        {
            "question": "Чем больше ты берёшь, тем больше оставляешь. Что это?",
            "options": ["Шаги", "Долг", "Песок"],
            "answer": "Шаги"
        },
    ],


    "expert":
        [  # Новый уровень сложности
        {
            "question": "Что принадлежит тебе, но другие пользуются этим чаще?",
            "options": ["Имя", "Телефон", "Ключи", "Время", "Речь"],
            "answer": "Имя"},

        {
            "question": "Без языка, а говорит. Что это?",
            "options": ["Река", "Эхо", "Радио", "Колокол", "Ветер"],
            "answer": "Эхо"
        },
        {
            "question": "Что можно держать в руках, но нельзя потрогать?",
            "options": ["Мечту", "Мысль", "Тень", "Огонь", "Воздух"],
            "answer": "Мечту"
        },
        {
            "question": "Что всегда растет, но никогда не уменьшается?",
            "options": ["Возраст", "Дерево", "Знания", "Река", "Гора"],
            "answer": "Возраст"
        },
        {
            "question": "Что может бежать, но ног не имеет?",
            "options": ["Река", "Часы", "Тень", "Огонь", "Собака"],
            "answer": "Река"
        },
        {
            "question": "Что становится мокрым, когда сушит?",
            "options": ["Ткань", "Рука", "Полотенце", "Губка", "Огонь"],
            "answer": "Полотенце"
        },
        {
            "question": "Что всегда идёт, но никогда не стоит на месте?",
            "options": ["Река", "Ветер", "Часы", "Время", "Тень"],
            "answer": "Время"
        },
        {
            "question": "Что можно сломать, не касаясь?",
            "options": ["Огонь", "Мечту", "Тишину", "Обещание", "Кристалл"],
            "answer": "Обещание"
        },

    ]
}

# Хранение очков игроков
user_scores = {}


# Главное меню с кнопками
def main_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("🧩 Загадка")],
            [KeyboardButton("🏆 Рейтинг"), KeyboardButton("📊 Мой счёт")]
        ],
        resize_keyboard=True
    )


# Определение уровня сложности
def get_difficulty(score):
    if score < 3:
        return "easy"
    elif 3 <= score < 6:
        return "medium"
    elif 6 <= score < 10:
        return "hard"
    else:
        return "expert"  # Новый уровень сложности


# Стартовая команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_scores[user_id] = {"correct": 0, "wrong": 0}
    await update.message.reply_text("Добро пожаловать! Выбери действие ниже:", reply_markup=main_menu())


# Новая загадка
async def send_riddle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    score = user_scores.get(user_id, {"correct": 0})["correct"]
    difficulty = get_difficulty(score)

    riddle = random.choice(riddles[difficulty])
    context.user_data['answer'] = riddle['answer']

    reply_markup = ReplyKeyboardMarkup(
        [[option] for option in riddle['options']], one_time_keyboard=True, resize_keyboard=True
    )

    await update.message.reply_text(f"[{difficulty.capitalize()}] {riddle['question']}", reply_markup=reply_markup)


# Проверка ответа
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


# Проверка изменений в рейтинге
async def check_ranking_changes(context: ContextTypes.DEFAULT_TYPE, user_positions=None):
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
    if not user_scores:
        await update.message.reply_text("Пока нет участников в рейтинге.", reply_markup=main_menu())
        return

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
    TOKEN = '7973384839:AAHtI2UJrzNnRwWTJZo_-xCQdd1BcZkwLy4'
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))



