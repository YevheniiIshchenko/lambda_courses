import telebot
bot = telebot.TeleBot('*token*')


@bot.message_handler(content_types=['text'])
def get_text_meassges(message):
    text = message.text
    text = text.replace('я ', 'ты ')
    text = text.replace('Я ', 'Ты ')
    bot.send_message(message.from_user.id, text)


bot.polling(none_stop=True, interval=0)
