# Запись ответов

import json


def save_progress(user_id, question_number):
    cur_progress = {str(user_id): question_number}
    try:
        with open('users_data.json', 'r') as file:
            progress = json.load(file)
        progress[str(user_id)] = question_number
        with open('users_data.json', 'w') as file:
            json.dump(cur_progress, file)
    except:
        with open('users_data.json', 'w') as file:
            json.dump(cur_progress, file)


# Загрузка прогресса пользователя из json


def load_progress(user_id):
    try:
        with open('users_data.json', 'r') as file:
            progress = json.load(file)
            return progress.get(str(user_id))
    except FileNotFoundError:
        return None


