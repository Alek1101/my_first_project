import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup
import os
from dotenv import load_dotenv
from functions import save_progress, load_progress
from game import survey, plot

load_dotenv()
token = os.getenv('API_KEY')
if token is None:
    raise ValueError('в файле .env отсутствует API_KEY')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Это бот SeoMatrix!'
                                      '\nЧтобы узнать, что он может, напиши /help')


@bot.message_handler(commands=['help'])
def start(message):
    bot.send_message(message.chat.id, 'Тут есть команды:'
                                      '\n1. /start - запуск бота'
                                      '\n2. /help - узнать возможности бота'
                                      '\n3. /game - запустить игру'
                                      '\n4. /end - остановить игру'
                                      '\n5. /info - информация о сюжете')


@bot.message_handler(commands=['info'])
def info(m):
    bot.send_message(m.chat.id, 'Добро пожаловать в текстовый квест Algorythm!')
    with open(plot['photo'], 'rb') as f:
        bot.send_photo(m.chat.id, f)
    bot.send_message(m.chat.id, plot['text'])


question = -1


def menu(m):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('/game')
    markup.add('/info')
    markup.add('/help')
    bot.send_message(m.chat.id, '/game для начала новой игры\n'
                                '/info для информации о сюжете\n'
                                '/help для помощи', reply_markup=markup)


def base_questions(m: types.Message):
    global question
    user_id = m.from_user.id
    message = m.text
    if message == '/end':
        question = -1
        save_progress(user_id, question)
        menu(m)
        return
    if question == 0 and message == 'Активация':
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for key in survey[question]['choice'].keys():
            markup.add(key)
        with open(survey[question]['photo'], 'rb') as f:
            bot.send_photo(m.chat.id, f)
        markup.add('/end')
        bot.send_message(m.chat.id, survey[question]["text"], reply_markup=markup)
        bot.register_next_step_handler(m, base_questions)
    else:
        try:
            question = survey[question]['choice'][message]
            if survey[question]['choice'] == -1:
                print('-1, end')
                with open(survey[question]['photo'], 'rb') as f:
                    bot.send_photo(m.chat.id, f)
                bot.send_message(m.chat.id, survey[question]['text'])
                question = -1
                save_progress(user_id, question)
                if question == 15:
                    bot.send_message(m.chat.id, '<b>Вы прошли игру на лучшую концовку!</b>', parse_mode='html')
                bot.send_message(m.chat.id, 'Игра окончена.'
                                            '\nСпасибо за прохождение!', reply_markup=types.ReplyKeyboardRemove())
                menu(m)
                return

            markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for key in survey[question]['choice'].keys():
                markup.add(key)
            with open(survey[question]['photo'], 'rb') as f:
                bot.send_photo(m.chat.id, f)
            markup.add('/end')
            bot.send_message(m.chat.id, survey[question]["text"], reply_markup=markup)
            save_progress(user_id, question)
            bot.register_next_step_handler(m, base_questions)
        except:
            print('exc')
            bot.send_message(m.chat.id, 'Вводите ответ с клавиатуры\n')
            markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for key in survey[question]['choice'].keys():
                markup.add(key)
            with open(survey[question]['photo'], 'rb') as f:
                bot.send_photo(m.chat.id, f)
            markup.add('/end')
            bot.send_message(m.chat.id, survey[question]["text"], reply_markup=markup)
            bot.register_next_step_handler(m, base_questions)


@bot.message_handler(commands=['game'])
def profile_output(m: types.Message):
    global question
    bot.send_message(m.from_user.id, 'Запускаем игру')
    user_id = m.from_user.id
    try:
        question = load_progress(user_id)
    except:
        question = -1
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('Активация')
    with open(survey[question]['photo'], 'rb') as f:
        bot.send_photo(m.chat.id, f)
    markup.add('/end')
    bot.send_message(m.chat.id, survey[-1]['text'], reply_markup=markup)
    question = 0
    bot.register_next_step_handler(m, base_questions)


@bot.message_handler(commands=['end'])
def end(m):
    bot.send_message(m.chat.id, 'Функция end используется только в ходе игры\n'
                                'Используйте команды')
    menu(m)
    return

@bot.message_handler(content_types=['text'])
def text(m):
    bot.send_message(m.chat.id, "Жёсткая логика исполнения, I'm sorry\n"
                                "Используйте команды")
    menu(m)
    return


bot.infinity_polling()
