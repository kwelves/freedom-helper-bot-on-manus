"""
Telegram-бот «Хелпер» для группы АН «Свобода»
Тихий помощник — 6-й игрок команды.
"""

import logging
import os
import json
import random
import datetime

import pytz
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ===== КОНФИГУРАЦИЯ =====
BOT_TOKEN = os.getenv("BOT_TOKEN", "8615058016:AAH2f7NLEsbrtKGMGdNxATPXky3fsHFSmCc")
OWNER_ID = int(os.getenv("OWNER_ID", "8142241137"))
CHAT_ID = int(os.getenv("CHAT_ID", "-1003764364716")) if os.getenv("CHAT_ID") else -1003764364716
ALLOWED_USERS = [int(uid.strip()) for uid in os.getenv("ALLOWED_USERS", "").split(",") if uid.strip()]

# Часовой пояс Бишкек
TIMEZONE = pytz.timezone("Asia/Bishkek")

# Файл для хранения списка юзернеймов
USERNAMES_FILE = "usernames.json"

# ===== СПИСОК ЮЗЕРНЕЙМОВ =====
DEFAULT_USERNAMES = [
    "@ajtzamir",
    "@AzizaBeishekeeva1",
    "@ayemnedeysin",
    "@Dennnise",
    "@TJ_5119",
    "@kikicaaa",
    "@Edumi09",
    "@ramil_19900",
    "@Iskennnn",
    "@Kikiki11100",
    "@Yourusernameexist",
    "@kerimbekox",
    "@Soveliy69",
    "@ayzhanymkaaa",
    "@Mauvaaiss",
    "@netnet01",
    "@Abdul1aevv_09",
    "@selforganized_xxx",
    "@leadandlike",
    "@dontbejud",
    "@autopomosh66",
    "@likyyla",
    "@bezmocni",
    "@Maria0669",
    "@D1ab0lus",
    "@aaaurorrs",
    "@boxing9511",
]


def load_usernames():
    """Загрузить список юзернеймов из файла."""
    if os.path.exists(USERNAMES_FILE):
        with open(USERNAMES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        save_usernames(DEFAULT_USERNAMES)
        return DEFAULT_USERNAMES.copy()


def save_usernames(usernames):
    """Сохранить список юзернеймов в файл."""
    with open(USERNAMES_FILE, "w", encoding="utf-8") as f:
        json.dump(usernames, f, ensure_ascii=False, indent=2)


# Загружаем юзернеймы при старте
usernames_list = load_usernames()


# ===== ПРИВЕТСТВИЯ =====
GREETINGS = [
    "Привет, {name}! Рады видеть тебя здесь. Ты не один — мы все здесь ради одной цели. Добро пожаловать в семью! 🤝",
    "Добро пожаловать, {name}! Здесь безопасное место, где тебя поймут и поддержат. Мы рады, что ты с нами! 💚",
    "Приветствуем тебя, {name}! Помни, что здесь тебя всегда выслушают и примут. Ты сделал важный шаг! 💪",
    "Рады, что ты нашёл дорогу к нам, {name}. Мы здесь, чтобы поддерживать друг друга на пути к свободе. Добро пожаловать! ✨",
    "{name}, привет! Ты в безопасности. Здесь нет осуждения, только поддержка и понимание. Рады твоему присутствию! 🤗",
    "Добро пожаловать в наше сообщество, {name}! Пусть этот чат станет для тебя источником сил и надежды. Мы вместе! 🙏",
    "Привет, {name}! Мы рады каждому новому участнику. Здесь ты найдёшь людей, которые понимают. Мы с тобой! 🫂",
    "{name}, добро пожаловать! Каждый из нас когда-то сделал первый шаг — и ты его уже сделал. Мы рядом! 🌱",
    "Привет, {name}! Здесь не нужно притворяться кем-то другим. Ты среди своих. Рады тебе! 🕊",
    "Рады тебе, {name}! Этот чат — место, где можно быть собой. Мы все идём одним путём. Добро пожаловать! 🛤",
    "{name}, привет! Ты пришёл в правильное место. Здесь тебя не осудят, а поддержат. Мы вместе! 💛",
    "Добро пожаловать, {name}! Не важно, откуда ты и что было раньше — важно, что ты здесь сейчас. Рады тебе! 🌟",
    "Привет, {name}! Мы — семья, и теперь ты часть неё. Здесь всегда выслушают и поддержат. Добро пожаловать! 🏠",
    "{name}, рады видеть тебя! Помни: ты не один в этом пути. Мы здесь друг для друга. 🤲",
    "Добро пожаловать, {name}! Каждый новый участник делает нас сильнее. Спасибо, что ты с нами! 🔥",
    "Привет, {name}! Здесь тебя ждут люди, которые знают, через что ты проходишь. Ты дома. 💚",
    "{name}, приветствуем! Сила в единстве — и мы рады, что ты теперь с нами. Вместе мы справимся! ✊",
    "Привет, {name}! Ты сделал смелый шаг. Здесь безопасно, здесь поймут. Добро пожаловать в нашу семью! 🌻",
    "Рады тебе, {name}! Не бойся — здесь все свои. Мы идём к свободе вместе. 🕊💚",
    "{name}, добро пожаловать! Ты больше не один. Мы здесь, чтобы поддерживать друг друга. Рады, что ты пришёл! 🙌",
]

# ===== НАПОМИНАНИЯ =====
REMINDERS = [
    "🕊 Друзья, собрание через 2 часа — в {time}. Ждём каждого из вас!",
    "💚 Напоминание: через 2 часа наше собрание ({time}). Приходите, мы вместе!",
    "🙏 До собрания осталось 2 часа (начало в {time}). Будем рады видеть всех!",
    "✨ Сегодня собрание в {time} — через 2 часа. Приходите, каждый голос важен!",
    "🕊 Не забудьте — собрание в {time}! Через 2 часа встречаемся. Ждём вас!",
    "💪 Собрание сегодня в {time} (через 2 часа). Вместе мы сильнее — приходите!",
    "🤝 Напоминаем: через 2 часа собрание ({time}). Ваше присутствие важно для всех нас!",
]


def is_authorized(user_id):
    """Проверить, авторизован ли пользователь."""
    return user_id == OWNER_ID or user_id in ALLOWED_USERS


# ===== ОБРАБОТЧИКИ =====

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка всех текстовых сообщений — сбор юзернеймов + реакция на 'хелпер'."""
    if not update.message or not update.message.text:
        return

    # Автоматический сбор юзернеймов
    user = update.effective_user
    if user and user.username:
        username = f"@{user.username}"
        if username not in usernames_list:
            usernames_list.append(username)
            save_usernames(usernames_list)
            logger.info(f"Добавлен новый юзернейм: {username}")

    # Реакция на обращение «хелпер» или по никнейму бота
    message_text = update.message.text.lower()
    bot_info = await context.bot.get_me()
    bot_username = bot_info.username.lower()

    if "хелпер" in message_text or f"@{bot_username}" in message_text:
        if is_authorized(update.effective_user.id):
            await update.message.reply_text("Я здесь, чем помочь? 🤝")


async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветствие новых участников группы + сбор юзернеймов."""
    if not update.message or not update.message.new_chat_members:
        return

    for new_member in update.message.new_chat_members:
        if new_member.is_bot:
            continue

        # Сохраняем юзернейм нового участника
        if new_member.username:
            username = f"@{new_member.username}"
            if username not in usernames_list:
                usernames_list.append(username)
                save_usernames(usernames_list)
                logger.info(f"Новый участник добавлен в список: {username}")

        # Отправляем приветствие
        name = new_member.first_name or "друг"
        greeting = random.choice(GREETINGS).format(name=name)
        await update.message.reply_text(greeting)


async def send_meeting_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Отправка напоминания о собрании с тегами в раскрываемой цитате."""
    meeting_time = context.job.data["time"]
    reminder_text = random.choice(REMINDERS).format(time=meeting_time)

    # Формируем теги
    tags = " ".join(usernames_list)

    # Сообщение с тегами в раскрываемой цитате
    message_text = (
        f"{reminder_text}\n\n"
        f"<blockquote expandable>📢 {tags}</blockquote>"
    )

    try:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=message_text,
            parse_mode="HTML"
        )
        logger.info(f"Напоминание о собрании в {meeting_time} отправлено.")
    except Exception as e:
        logger.error(f"Ошибка отправки напоминания: {e}")


# ===== КОМАНДЫ ВЛАДЕЛЬЦА =====

async def cmd_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавить юзернейм в список. Использование: /add @username"""
    if not is_authorized(update.effective_user.id):
        return

    if not context.args:
        await update.message.reply_text("Использование: /add @username")
        return

    for username in context.args:
        if not username.startswith("@"):
            username = f"@{username}"
        if username not in usernames_list:
            usernames_list.append(username)
            save_usernames(usernames_list)
            await update.message.reply_text(f"✅ {username} добавлен в список.")
        else:
            await update.message.reply_text(f"ℹ️ {username} уже в списке.")


async def cmd_remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удалить юзернейм из списка. Использование: /remove @username"""
    if not is_authorized(update.effective_user.id):
        return

    if not context.args:
        await update.message.reply_text("Использование: /remove @username")
        return

    for username in context.args:
        if not username.startswith("@"):
            username = f"@{username}"
        if username in usernames_list:
            usernames_list.remove(username)
            save_usernames(usernames_list)
            await update.message.reply_text(f"✅ {username} удалён из списка.")
        else:
            await update.message.reply_text(f"ℹ️ {username} не найден в списке.")


async def cmd_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать текущий список юзернеймов."""
    if not is_authorized(update.effective_user.id):
        return

    if usernames_list:
        text = f"📋 Список участников ({len(usernames_list)}):\n\n" + "\n".join(usernames_list)
    else:
        text = "Список пуст."
    await update.message.reply_text(text)


async def cmd_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправить тестовое напоминание. Использование: /test"""
    if not is_authorized(update.effective_user.id):
        return

    # Отправляем тестовое напоминание
    tags = " ".join(usernames_list)
    reminder_text = random.choice(REMINDERS).format(time="21:00")
    message_text = (
        f"[ТЕСТ] {reminder_text}\n\n"
        f"<blockquote expandable>📢 {tags}</blockquote>"
    )

    try:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=message_text,
            parse_mode="HTML"
        )
        await update.message.reply_text("✅ Тестовое напоминание отправлено в группу.")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать список команд."""
    if not is_authorized(update.effective_user.id):
        return

    help_text = (
        "🤖 Команды бота:\n\n"
        "/add @username — добавить в список тегов\n"
        "/remove @username — удалить из списка тегов\n"
        "/list — показать список участников\n"
        "/test — отправить тестовое напоминание\n"
        "/help — показать эту справку"
    )
    await update.message.reply_text(help_text)


# ===== ЗАПУСК =====

def main():
    """Запуск бота."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Команды владельца
    application.add_handler(CommandHandler("start", cmd_help))
    application.add_handler(CommandHandler("help", cmd_help))
    application.add_handler(CommandHandler("add", cmd_add))
    application.add_handler(CommandHandler("remove", cmd_remove))
    application.add_handler(CommandHandler("list", cmd_list))
    application.add_handler(CommandHandler("test", cmd_test))

    # Обработчик новых участников
    application.add_handler(MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member
    ))

    # Обработчик текстовых сообщений (сбор юзернеймов + реакция на «хелпер»)
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message
    ))

    # ===== РАСПИСАНИЕ НАПОМИНАНИЙ =====
    job_queue = application.job_queue

    # Понедельник: напоминание в 19:00 о собрании в 21:00
    job_queue.run_daily(
        send_meeting_reminder,
        time=datetime.time(hour=19, minute=0, tzinfo=TIMEZONE),
        days=(0,),  # 0 = понедельник
        data={"time": "21:00"}
    )

    # Четверг: напоминание в 19:00 о собрании в 21:00
    job_queue.run_daily(
        send_meeting_reminder,
        time=datetime.time(hour=19, minute=0, tzinfo=TIMEZONE),
        days=(3,),  # 3 = четверг
        data={"time": "21:00"}
    )

    # Суббота: напоминание в 17:00 о собрании в 19:00
    job_queue.run_daily(
        send_meeting_reminder,
        time=datetime.time(hour=17, minute=0, tzinfo=TIMEZONE),
        days=(5,),  # 5 = суббота
        data={"time": "19:00"}
    )

    logger.info("Бот запущен! Расписание напоминаний активно.")
    logger.info(f"OWNER_ID: {OWNER_ID}")
    logger.info(f"CHAT_ID: {CHAT_ID}")
    logger.info(f"Участников в списке: {len(usernames_list)}")

    # Запуск бота (drop_pending_updates=True — игнорируем старые обновления при запуске)
    application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    main()
