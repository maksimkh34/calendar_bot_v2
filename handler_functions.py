# handler_functions.py
from event_core import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import pandas as pd
from event import Event

path_to_db = 'D:\\Work\\Python\\calendar_bot_new\\db.csv'

async def start(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Это бот-календарь. Он может планировать события, изменять уже запланированные, и удалять их, но пока не может оповещать о их наступлении...\n"
             "Команды бота:\n"
             "/add - Бот добавит событие\n"
             "/check - Бот выводит все запланированные события\n"
             "/edit - Бот выводит все события, а затем можно изменить текст выбранного события\n"
             "/delete - Бот удаляет выбранное событие\n"
             "/about - Описание бота\n"
             "/help или /start - Вывести этот список еще раз"
    )

async def show_events(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Загрузка событий...")
    events = import_db()
    for event in events:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Событие на {event.year}.{event.month}.{event.day}, {event.hour}:{event.minute} - {event.event_name}"
        )
    if not events:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="События не найдены!")
    keyboard = [[InlineKeyboardButton("Добавить события", callback_data='3')]]
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Чтобы добавить новые события, введите /add",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def callback_handler(update, context):
    query = update.callback_query
    await query.answer()
    if query.data == '1':
        await start(update, context)
    elif query.data == '2':
        await show_events(update, context)
    elif query.data == '3':
        await add_event(update, context)
    elif query.data.startswith('del_'):
        index = int(query.data[4:])
        db_df = pd.read_csv('db.csv')
        db_df.drop(index=index, inplace=True)
        db_df.to_csv('db.csv', index=False)
        keyboard = [[InlineKeyboardButton("Показать запланированные события", callback_data='2')]]
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Событие удалено. Введите /check для просмотра текущих событий",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data.startswith('edt_'):
        data = query.data.split('_')
        index = int(data[1])
        new_name = "_".join(data[2:])
        db = pd.read_csv('db.csv')
        db.at[index, 'event'] = new_name
        db.to_csv('db.csv', index=False)
        keyboard = [[InlineKeyboardButton("Показать запланированные события", callback_data='2')]]
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Событие изменено. Введите /check для просмотра текущих событий",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def unknown_command(update, context):
    keyboard = [[InlineKeyboardButton("Показать команды", callback_data='1')]]
    await update.message.reply_text(
        "Команда не распознана. Введите /help, чтобы просмотреть все команды",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def add_event(update, context):
    if not update.message or update.message.text == '/add':
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Введите данные нового события в формате:\n"
                 "/add YYYY.MM.DD HH:MM - Событие\n"
                 "Например: /add 2012.12.20 14:00 - День рождения"
        )
    else:
        vnt = parse_event(update.message.text)
        if len(update.message.text) < 25:
            await update.message.reply_text("Событие задано неверно. Введите /add для справки")
        elif not await check_event(vnt, context, update):
            await update.message.reply_text("Событие задано неверно. Введите /add для справки")
        else:
            dict_event = {
                'year': vnt.year,
                'month': vnt.month,
                'day': vnt.day,
                'hour': vnt.hour,
                'minute': vnt.minute,
                'event': vnt.event_name
            }
            old_db = pd.read_csv('db.csv')
            new_db = pd.concat([old_db, pd.DataFrame([dict_event])], ignore_index=True)
            new_db.to_csv('db.csv', index=False)
            keyboard = [[InlineKeyboardButton("Показать запланированные события", callback_data='2')]]
            await update.message.reply_text(
                "Событие успешно добавлено. Введите /check для просмотра текущих событий",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )


async def delete_event(update, context):
    events = import_db()
    keyboard = []
    if not events:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="События не найдены!")
    else:
        for i, event in enumerate(events):
            keyboard.append([InlineKeyboardButton(
                f"{event.event_name} ({event.year}.{event.month}.{event.day}, {event.hour}:{event.minute})",
                callback_data=f'del_{i}'
            )])
        await update.message.reply_text(
            "Какое событие требуется удалить?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def about(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Developed by https://github.com/maksimkh34\nGitHub: https://github.com/maksimkh34/calendar_bot"
    )

async def edit_event(update, context):
    events = import_db()
    keyboard = []
    new_event_name = update.message.text[6:]
    if update.message.text == '/edit':
        await update.message.reply_text("Команда используется в формате /edit 'Новый текст.")
    else:
        if not events:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="События не найдены!")
        else:
            for i, event in enumerate(events):
                keyboard.append([InlineKeyboardButton(
                    f"{event.event_name} ({event.year}.{event.month}.{event.day}, {event.hour}:{event.minute})",
                    callback_data=f"edt_{i}_{new_event_name}"
                )])
            await update.message.reply_text(
                "Какое событие требуется изменить?",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
