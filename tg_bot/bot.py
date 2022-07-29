import telebot
from django.conf import settings


bot = telebot.TeleBot(token=settings.TOKEN)


def send_order(chat_id, text):
    bot.send_message(chat_id=chat_id, text=text)

