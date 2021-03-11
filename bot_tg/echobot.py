from datetime import datetime
from pymongo import MongoClient

from telebot import types, util
import telebot
import psycopg2
import time

# postgres
connection = psycopg2.connect(user="user",
                              password="password",
                              host="host",
                              port="port",
                              database="database")

cursor = connection.cursor()

# telegram bot
bot = telebot.TeleBot('token')

# mongodb
client = MongoClient()
db = client['echobot513test']
posts = db.posts


def isint(x):
    try:
        a = int(x)
        return True
    except ValueError:
        return False


@bot.message_handler(commands=['start'])
def start(message):
    message_text = '''
    /show_all_messages - покзать все сообщения\n
    /show_my_messages - показать все мои сообщения\n
    /talk - бот познакомится с тобой \n'''
    bot.send_message(message.from_user.id, message_text)


@bot.message_handler(commands=['show_all_messages'])
def show_all_messages(message):
    result = posts.find({})
    message_text = ''
    for post in result:
        message_text += f"User = {post['user-id']} \n"
        message_text += f"Date = {post['datetime']} \n"
        message_text += f"Text = {post['text']} \n"
        message_text += '\n'

    splitted_text = util.split_string(message_text, 3000)
    for text in splitted_text:
        bot.send_message(message.from_user.id, text)


@bot.message_handler(commands=['show_my_messages'])
def show_my_messages(message):
    result = posts.find({'user-id': message.from_user.id})
    message_text = ''
    for post in result:
        message_text += f"Date = {post['datetime']} \n"
        message_text += f"Text = {post['text']} \n"
        message_text += '\n'

    splitted_text = util.split_string(message_text, 3000)
    for text in splitted_text:
        bot.send_message(message.from_user.id, text)


# общение
chat = {}


@bot.message_handler(commands=['talk'])
def talk(message):
    user = {}
    id = message.chat.id
    chat[id] = user

    bot.send_message(message.from_user.id, "Hello! What's your name?")
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    if message.content_type == 'text':
        if message.text in commands:
            return commands[message.text](message)
        chat[message.chat.id]['name'] = message.text
        bot.send_message(message.from_user.id, "Nice to meet you! How old are you?")
        bot.register_next_step_handler(message, get_age)
        if message.text in commands:
            bot.clear_step_handler(message)
    else:
        bot.send_message(message.from_user.id, "Oooops, something goes wrong =( ")


@bot.callback_query_handler(func=lambda m: True)
def answer(call):
    chatid = call.message.chat.id
    if call.data == 'y':
        name = chat[chatid]['name']
        age = chat[chatid]['age']
        sql_request = f'''
        INSERT INTO USERS (ChatID, Name, Age)
        VALUES ({chatid}, '{name}', {age});
        '''
        cursor.execute(sql_request)
        connection.commit()
        bot.send_message(call.message.chat.id, "Ok, remembered")
    if call.data == 'n':
        bot.send_message(call.message.chat.id, "Мда, даже данные заполнить не можешь, калека")
    bot.edit_message_reply_markup(message_id=call.message.message_id, chat_id=chatid, reply_markup=())
    answer_get = True


def get_age(message):
    if message.content_type == 'text':
        if message.text in commands:
            return commands[message.text](message)
        if isint(message.text):
            chat[message.chat.id]['age'] = message.text
            markup = types.InlineKeyboardMarkup()
            btn_yes = types.InlineKeyboardButton('Yes', callback_data='y')
            btn_no = types.InlineKeyboardButton('No', callback_data='n')
            markup.row(btn_yes, btn_no)

            msg = bot.send_message(message.from_user.id,
                                   f"Your name is {chat[message.chat.id]['name']} and you are {chat[message.chat.id]['age']} years old?",
                                   reply_markup=markup)
            time.sleep(5)
            bot.edit_message_reply_markup(message_id=msg.message_id, chat_id=msg.chat.id,
                                          reply_markup=())
        else:
            bot.send_message(message.from_user.id, "No! Enter a number!")
            bot.register_next_step_handler(message, get_age)
    else:
        bot.send_message(message.from_user.id, "Oooops, something goes wrong =( ")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    text = message.text
    post = {
        'user-id': message.from_user.id,
        'text': text,
        'datetime': datetime.now(),
    }
    posts.insert_one(post)

    sql_request = f'''
    INSERT INTO messages (userID, text)
    VALUES ({message.from_user.id}, '{text}');
    '''
    cursor.execute(sql_request)
    connection.commit()
    bot.send_message(message.from_user.id, text)


commands = {
    '/start': start,
    '/talk': talk,
    '/show_my_messages': show_my_messages,
    '/show_all_messages': show_all_messages,
}

bot.polling(none_stop=True, interval=0)
