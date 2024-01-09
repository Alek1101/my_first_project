import os

import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup
from dotenv import load_dotenv
from settings import token
from helping import survey, user_data, total_score

load_dotenv()

bot = telebot.TeleBot(token=token)
if token is None:
    raise ValueError('В файле .env отсутствует API_KEY')

question = 0


def base_questions(m: types.Message):
    global question
    message = m.text
    if message == '/end':
        bot.send_message(m.chat.id, 'Прохождение остановлено',
                         reply_markup=types.ReplyKeyboardRemove())
        return
    user_id = m.from_user.id
    try:
        for season, scores in survey[question]["answers"][message].items():
            total_score[season] += scores
        user_data[user_id] = dict(user_score=total_score)
        question += 1
        if question >= len(survey):
            question = 0
            bot.send_message(m.chat.id, 'Итоги анкеты:', reply_markup=types.ReplyKeyboardRemove())
            max_score = 0
            your_season = ''
            for season, scores in total_score.items():
                bot.send_message(m.chat.id, f"{season} - {scores}")
                if scores > max_score:
                    max_score = scores
                    your_season = season
            print(user_data)
            bot.send_message(m.chat.id, f"Наибольшее количество баллов у времени года: {your_season}")
            return
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for key in survey[question]['answers'].keys():
            markup.add(key)
        bot.send_message(m.chat.id, survey[question]["question"], reply_markup=markup)
        bot.register_next_step_handler(m, base_questions)
    except:
        bot.reply_to(m, 'Что-то сломалось... Попробуйте ещё раз')
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for key in survey[question]['answers'].keys():
            markup.add(key)
        bot.send_message(m.chat.id, survey[question]["question"], reply_markup=markup)
        bot.register_next_step_handler(m, base_questions)


@bot.message_handler(commands=['start'])
def profile_output(m: types.Message):
    bot.send_message(m.from_user.id, 'Запускаем анкету...')
    user_id = m.from_user.id
    user_name = m.from_user.first_name

    if user_id not in user_data:
        user_data[user_id] = dict(user_name=user_name)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for key in survey[question]['answers'].keys():
        markup.add(key)
    bot.send_message(m.chat.id, survey[question]["question"], reply_markup=markup)
    bot.register_next_step_handler(m, base_questions)


@bot.message_handler(commands=['help'])
def support(m):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('/start')
    markup.add('/help')
    bot.send_message(m.chat.id, 'Бот-анкета\n'
                                'Доступные функции: \n'
                                '/start - запускает анкету\n'
                                '/help - справка\n'
                                '/end - команда окончания опроса', reply_markup=markup)


@bot.message_handler(commands=['end'])
def explanation(m):
    bot.send_message(m.chat.id, 'Просто так это команда бесполезна\n'
                                'Используй её при опросе, если захочешь завершить его досрочно.',
                     reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['text'])
def rest(m):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('/start')
    markup.add('/help')
    markup.add('/end')
    bot.send_message(m.chat.id, 'К сожалению, пока что могу распознать только три команды:\n'
                                , reply_markup=markup)


bot.infinity_polling()
