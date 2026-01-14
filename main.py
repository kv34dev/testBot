import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветственное сообщение с inline-кнопками"""
    keyboard = [
        [InlineKeyboardButton("Кнопка 1", callback_data='btn1')],
        [InlineKeyboardButton("Кнопка 2", callback_data='btn2')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        'Привет! Я тестовый бот.\n\n'
        'Доступные команды:\n'
        '/start - начать\n'
        '/help - помощь\n'
        '/keyboard - показать клавиатуру\n'
        '/photo - отправить фото\n'
        '/document - отправить документ\n'
        '/poll - создать опрос',
        reply_markup=reply_markup
    )


# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Помощь"""
    await update.message.reply_text(
        'Это тестовый бот с базовыми функциями:\n\n'
        '📝 Отправка текста\n'
        '⌨️ Клавиатуры (inline и reply)\n'
        '📷 Отправка фото\n'
        '📄 Отправка файлов\n'
        '📊 Создание опросов\n'
        '💬 Обработка сообщений\n\n'
        'Попробуйте разные команды!'
    )


# Команда /keyboard - Reply клавиатура
async def keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать reply-клавиатуру"""
    keyboard = [
        ['Опция 1', 'Опция 2'],
        ['Опция 3', 'Опция 4'],
        ['Убрать клавиатуру']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        'Выберите опцию из клавиатуры:',
        reply_markup=reply_markup
    )


# Обработка нажатий inline-кнопок
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка callback от inline-кнопок"""
    query = update.callback_query
    await query.answer()

    if query.data == 'btn1':
        await query.edit_message_text('Вы нажали Кнопку 1! 👍')
    elif query.data == 'btn2':
        await query.edit_message_text('Вы нажали Кнопку 2! 🎉')


# Команда /photo - отправка фото
async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправить тестовое фото"""
    # URL тестового изображения
    photo_url = 'https://picsum.photos/400/300'

    await update.message.reply_photo(
        photo=photo_url,
        caption='Это тестовое фото 📷'
    )


# Команда /document - отправка документа
async def send_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправить тестовый документ"""
    # Создаем простой текстовый файл в памяти
    from io import BytesIO

    document = BytesIO('Hello! This is a test document.\nЭто тестовый документ.')
    document.name = 'test.txt'

    await update.message.reply_document(
        document=document,
        caption='Тестовый документ 📄'
    )


# Команда /poll - создание опроса
async def create_poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Создать опрос"""
    questions = ['Python', 'JavaScript', 'Java', 'C++']

    await update.message.reply_poll(
        question='Какой ваш любимый язык программирования?',
        options=questions,
        is_anonymous=False
    )


# Обработка текстовых сообщений
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений"""
    text = update.message.text

    if text == 'Убрать клавиатуру':
        await update.message.reply_text(
            'Клавиатура убрана ✅',
            reply_markup=ReplyKeyboardRemove()
        )
    elif text in ['Опция 1', 'Опция 2', 'Опция 3', 'Опция 4']:
        await update.message.reply_text(f'Вы выбрали: {text}')
    else:
        await update.message.reply_text(f'Вы написали: {text}\n\nОтправьте /help для списка команд')


# Обработка фото от пользователя
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка полученных фото"""
    await update.message.reply_text('Получил ваше фото! 📸')


# Обработка документов от пользователя
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка полученных документов"""
    file_name = update.message.document.file_name
    await update.message.reply_text(f'Получил документ: {file_name} 📎')


def main():
    """Запуск бота"""
    # Вставьте сюда токен вашего бота от @BotFather
    TOKEN = '8430334122:AAGmy7cxzIQddp2TlAYYkO-iNR1mRzCXmTE'

    # Создание приложения
    application = Application.builder().token(TOKEN).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('keyboard', keyboard))
    application.add_handler(CommandHandler('photo', send_photo))
    application.add_handler(CommandHandler('document', send_document))
    application.add_handler(CommandHandler('poll', create_poll))

    # Обработчик inline-кнопок
    application.add_handler(CallbackQueryHandler(button_callback))

    # Обработчики сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # Запуск бота
    print('Бот запущен...')
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()