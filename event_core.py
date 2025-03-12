# event_core.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import pandas as pd
from event import Event

def parse_event(text):
    list1 = text.split(' ')
    event_name = " ".join(list1[4:])
    date = list1[1].split('.')
    year, month, day = date[0], date[1], date[2]
    time_ = list1[2].split(':')
    hour, minute = time_[0], time_[1]
    return Event(year, month, day, hour, minute, event_name)

# event_core.py
async def check_event(vnt, context, update) -> bool:
    if int(vnt.year) < 2025:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Год указан неверно ({vnt.year})")
        return False
    elif int(vnt.month) <= 0 or int(vnt.month) > 12:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Месяц указан неверно ({vnt.month})")
        return False
    elif int(vnt.day) <= 0 or int(vnt.day) > 31:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"День указан неверно ({vnt.day})")
        return False
    elif int(vnt.hour) < 0 or int(vnt.hour) > 24:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Час указан неверно ({vnt.hour})")
        return False
    elif int(vnt.minute) < 0 or int(vnt.minute) > 60:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Минута указана неверно ({vnt.minute})")
        return False
    else:
        return True
def import_db():
    try:
        # Попытка прочитать файл
        dbase = pd.read_csv("db.csv")
        if dbase.empty:
            # Если файл пустой, создаем новый DataFrame с заголовками
            dbase = pd.DataFrame(columns=['year', 'month', 'day', 'hour', 'minute', 'event'])
            dbase.to_csv("db.csv", index=False)
            return []
    except pd.errors.EmptyDataError:
        # Если файл пустой, создаем новый DataFrame с заголовками
        dbase = pd.DataFrame(columns=['year', 'month', 'day', 'hour', 'minute', 'event'])
        dbase.to_csv("db.csv", index=False)
        return []
    except FileNotFoundError:
        # Если файл отсутствует, создаем новый файл с заголовками
        dbase = pd.DataFrame(columns=['year', 'month', 'day', 'hour', 'minute', 'event'])
        dbase.to_csv("db.csv", index=False)
        return []

    # Если файл успешно прочитан, преобразуем его в список событий
    events = []
    years = dbase['year'].tolist()
    months = dbase['month'].tolist()
    days = dbase['day'].tolist()
    hours = dbase['hour'].tolist()
    minutes = dbase['minute'].tolist()
    events_names = dbase['event'].tolist()
    for i in range(len(dbase)):
        x = Event(years[i], months[i], days[i], hours[i], minutes[i], events_names[i])
        events.append(x)
    return events
