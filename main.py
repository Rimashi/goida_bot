import telebot
import time
import random
import re

token = "7038285388:AAFEyPahgAyCrNkAwUlmN_o6Dlas8DhBwL4"
bot = telebot.TeleBot(token)


users_id = set()
downs = []

slang_answers = {
    "сво": ["сво за наших гойда ура победа гооооол", "ГОЙДААААА", "ZZZZZZZZZZZZZZZZZZZ"],
    "z": "СЛАВА Z🙏❤️СЛАВА Z🙏❤️АНГЕЛА ХРАНИТЕЛЯ Z КАЖДОМУ ИЗ ВАС🙏❤️БОЖЕ ХРАНИ Z🙏❤️СПАСИБО ВАМ НАШИ Z🙏🏼❤️🇷🇺 ХРОНИ Z✊🇷🇺💯Слава Богу Z🙏❤️СЛАВА Z🙏❤️СЛАВА",
    "zv": "ZVZVZVZVZVZVZVZVZVZVZVZVZVZVZVZVZVZVZVZVZVZV",
    "zov": "ZOVVVVVVVVVVVVVVVVVVV",
    "гойда": [
        "CgACAgQAAxkBAAOOZ3KK6-gyRKw41lOlKM3i01yGKMIAAu8FAAJvw51QZ0GSnOguHOo2BA",
        "CgACAgQAAxkBAAOIZ3KKnFe1g3958pMIiCwJUoCE9z8AAugFAAI18zVS69uk2SLsWR02BA",
        "CgACAgQAAxkBAAOJZ3KKukZ1Qa-IBoDGMEf300JxMckAAm8GAALWy2xQX6iwzA4zVa82BA",
        "CgACAgQAAxkBAAOKZ3KKwAl5c2qZbJBG1GAN_x9RDaQAAjEEAAKmN41STzp5CTAydrs2BA",
        "CgACAgQAAxkBAAOLZ3KKyVP3I0qwYK-X_ZedniSAhEwAAgcGAAKvoTRTFIbTuzW5wxk2BA",
        "CgACAgQAAxkBAAOMZ3KK01DV097dDCmdLYZvH59hlDgAAsIFAAL7VD1R1KUnDFAwsjQ2BA",
        "CgACAgQAAxkBAAONZ3KK5Kyjwz8yVu7-VanHXTNu6BsAAjUGAAIFS2VQpQtNy1P6aro2BA",
    ],
    "да": "пизда",
    "пизда": "да",
    "нет": "пидора ответ",
    "не": "пидора отве....",
    "пидора ответ": "шлюхи аргумент",
    "шлюхи аргумент": "аргумент не нужен, пидор обнаружен",
    "аргумент не нужен, пидор обнаружен": "пидор засекречен, твой анал не вечен",
    "пидор засекречен, твой анал не вечен": "мой анал не вечен, твой анал помечен",

}


# connect to mongo


# Функция для удаления сообщения через заданное время
def delete_message(chat_id, message_id, delay):
    time.sleep(delay)
    bot.delete_message(chat_id, message_id)


# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    users_id.add(message.from_user.id)
    bot.reply_to(message, "Привет ✌️")


# вызов главного дауна
@bot.message_handler(commands=['main_down'])
def main_down(message):
    chat_id = message.chat.id
    down = 5283571568
    st = ""
    user_info = bot.get_chat_member(chat_id, down).user
    if user_info.username:
        st += f"@{user_info.username}\n"
    else:
        st += f"[даун без username](tg://user?id={down})\n"

    for i in range(25):
        sending_message = bot.send_message(chat_id, st, parse_mode="Markdown")
        message_id = sending_message.message_id
        delete_message(chat_id, message_id, 20)


# down commands
@bot.message_handler(commands=['downs'])
def help_message(message):
    st = "Главные дауны: \n"
    chat_id = message.chat.id
    for down in downs:
        try:
            user_info = bot.get_chat_member(chat_id, down).user
            if user_info.username:
                st += f"@{user_info.username}\n"
            else:
                st += f"[даун без username](tg://user?id={down})\n"
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Ошибка для пользователя {down}: {e}")
            st += f"[даун](tg://user?id={down})\n"

    l = []
    for i in range(25):
        sending_message = bot.send_message(chat_id, st, parse_mode="Markdown")
        message_id = sending_message.message_id
        l.append(message_id)

    for message_id in l:
        delete_message(chat_id, message_id, 60)


# Команда /all
@bot.message_handler(commands=['all'])
def all_message(message):
    users_id.add(message.from_user.id)
    chat_id = message.chat.id
    if users_id:
        st = "Эу, общий сбор: \n"
        for user in users_id:
            try:
                user_info = bot.get_chat_member(chat_id, user).user
                if user_info.username:
                    st += f"@{user_info.username}\n"
                else:
                    st += f"[даун без username](tg://user?id={user})\n"
            except telebot.apihelper.ApiTelegramException as e:
                print(f"Ошибка для пользователя {user}: {e}")
        bot.send_message(chat_id, st, parse_mode="Markdown")
    else:
        bot.send_message(chat_id, "Никого ещё нет в списке.", parse_mode="Markdown")


# help command
@bot.message_handler(commands=['help'])
def help_message(message):
    users_id.add(message.from_user.id)
    bot.reply_to(message, "эмммммммм, не")


# Получение всех сообщений
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    users_id.add(message.from_user.id)
    print(users_id)
    for key, value in slang_answers.items():
        # регулярное выражение для точного совпадения
        pattern = r'\b' + re.escape(key.lower()) + r'\b'
        if re.search(pattern, message.text.lower()):
            if type(value) is str:
                bot.reply_to(message, value)
            else:
                rand = random.randint(0, len(value) - 1)
                if value[0] == "CgACAgQAAxkBAAOOZ3KK6-gyRKw41lOlKM3i01yGKMIAAu8FAAJvw51QZ0GSnOguHOo2BA":
                    bot.send_animation(message.chat.id, value[rand])
                else:
                    bot.reply_to(message, value[rand])
            break


# Запуск бота
bot.infinity_polling()
