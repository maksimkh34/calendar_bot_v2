# main.py
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from const import bot_token
from handler_functions import *
from datetime import datetime

# Initializing bot
# Текущее время
d = datetime.now()
print(f"Bot init finished. ({d.time().hour}:{d.time().minute}:{d.time().second})")

# Создаем объект приложения
application = Application.builder().token(bot_token).build()

# Handlers
button_help_handler = CallbackQueryHandler(callback_handler)
start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', start)
unknown_handler = MessageHandler(filters.COMMAND, unknown_command)
show_events_handler = CommandHandler('check', show_events)
add_handler = CommandHandler('add', add_event)
delete_event_handler = CommandHandler('delete', delete_event)
about_handler = CommandHandler('about', about)
edit_event_handler = CommandHandler('edit', edit_event)

# Adding handlers
application.add_handler(start_handler)
application.add_handler(help_handler)
application.add_handler(button_help_handler)
application.add_handler(show_events_handler)
application.add_handler(add_handler)
application.add_handler(delete_event_handler)
application.add_handler(about_handler)
application.add_handler(edit_event_handler)
application.add_handler(unknown_handler)  # Default handler

# Starting polling
print("Polling started... ")
application.run_polling()
print("Stopped.")