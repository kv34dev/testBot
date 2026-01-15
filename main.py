import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from io import BytesIO

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message with inline buttons"""
    keyboard = [
        [InlineKeyboardButton("Button 1", callback_data='btn1')],
        [InlineKeyboardButton("Button 2", callback_data='btn2')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        'Hello. I am a test bot.\n\n'
        'Available commands:\n'
        '/start - start the bot\n'
        '/help - show help\n'
        '/keyboard - show reply keyboard\n'
        '/photo - send a photo\n'
        '/document - send a document\n'
        '/poll - create a poll',
        reply_markup=reply_markup
    )


# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help information"""
    await update.message.reply_text(
        'This is a test bot with basic functions:\n\n'
        'Text sending\n'
        'Keyboards (inline and reply)\n'
        'Photo sending\n'
        'File sending\n'
        'Poll creation\n'
        'Message handling\n\n'
        'Try different commands to test functionality.'
    )


# /keyboard command - Reply keyboard
async def keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show reply keyboard"""
    keyboard = [
        ['Option 1', 'Option 2'],
        ['Option 3', 'Option 4'],
        ['Remove keyboard']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        'Select an option from the keyboard:',
        reply_markup=reply_markup
    )


# Handle inline button presses
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callbacks from inline buttons"""
    query = update.callback_query
    await query.answer()

    if query.data == 'btn1':
        await query.edit_message_text('You pressed Button 1')
    elif query.data == 'btn2':
        await query.edit_message_text('You pressed Button 2')


# /photo command - send photo
async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a test photo"""
    photo_url = 'https://picsum.photos/400/300'

    await update.message.reply_photo(
        photo=photo_url,
        caption='This is a test photo'
    )


# /document command - send document
async def send_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a test document"""
    # Create a simple text file in memory
    content = 'This is a test document.\nCreated by the test bot.\n\nContent line 1\nContent line 2\nContent line 3'
    document = BytesIO(content.encode('utf-8'))
    document.name = 'test_document.txt'

    await update.message.reply_document(
        document=document,
        filename='test_document.txt',
        caption='Test document file'
    )


# /poll command - create poll
async def create_poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create a poll"""
    questions = ['Python', 'JavaScript', 'Java', 'C++']

    await update.message.reply_poll(
        question='What is your favorite programming language?',
        options=questions,
        is_anonymous=False
    )


# Handle text messages
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages"""
    text = update.message.text

    if text == 'Remove keyboard':
        await update.message.reply_text(
            'Keyboard removed',
            reply_markup=ReplyKeyboardRemove()
        )
    elif text in ['Option 1', 'Option 2', 'Option 3', 'Option 4']:
        await update.message.reply_text(f'You selected: {text}')
    else:
        await update.message.reply_text(f'You wrote: {text}\n\nSend /help for command list')


# Handle photos from user
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle received photos"""
    await update.message.reply_text('Photo received successfully')


# Handle documents from user
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle received documents"""
    file_name = update.message.document.file_name
    await update.message.reply_text(f'Document received: {file_name}')


def main():
    """Start the bot"""
    # Insert your bot token from @BotFather here
    TOKEN = 'token'

    # Create application
    application = Application.builder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('keyboard', keyboard))
    application.add_handler(CommandHandler('photo', send_photo))
    application.add_handler(CommandHandler('document', send_document))
    application.add_handler(CommandHandler('poll', create_poll))

    # Inline button handler
    application.add_handler(CallbackQueryHandler(button_callback))

    # Message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # Start the bot
    print('Bot started...')
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
