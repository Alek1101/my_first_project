import os

import telebot
from dotenv import load_dotenv
from telebot import types
from info import functions

load_dotenv()

token = os.getenv('API_KEY')
if token is None:
    raise ValueError('в файле .env отсутствует API_KEY')

bot = telebot.TeleBot(token=token)


def title_screen():
    @bot.message_handler(content_types=['text'])
    def title_text(message: types.Message):
        bot.send_message(message.chat.id, f'{functions["title_screen"]}')


def base_func():
    def hello_filter(message: types.Message) -> bool:
        return 'привет' in message.text.lower()

    def bye_filter(message: types.Message) -> bool:
        return 'пока' in message.text.lower()

    @bot.message_handler(content_types=['text'], commands=['start'])
    def start_command(message: types.Message):
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
        bot.send_message(message.chat.id, f'{functions["start_info"]}')
        bot.send_message(message.chat.id, f'{functions["start_commands"]}')

    @bot.message_handler(content_types=['text'], commands=['help'])
    def help_command(message: types.Message):
        bot.send_message(message.chat.id, f'{functions["help"]}')

    #
    @bot.message_handler(content_types=['text'], func=hello_filter)
    def send_hello(message: types.Message):
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')

    #
    #
    @bot.message_handler(content_types=['text'], func=bye_filter)
    def send_bye(message: types.Message):
        bot.send_message(message.chat.id, f'Пока, {message.from_user.first_name}!')


base_func()
title_screen()

#
# @bot.message_handler(content_types=['text'])
# def echo_handler(message: types.Message):
#     bot.send_message(message.chat.id, f'Ты прислал(а) сообщение с текстом "{message.text}"')
#
#
# bot.send_message(chat_id, "Привет")
#
bot.polling()
