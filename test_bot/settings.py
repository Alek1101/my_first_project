import os
import json
from pathlib import Path
from helping import user_data

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent

load_dotenv(BASE_DIR / '.env')  # take environment variables from .env.

token = os.getenv('API_KEY')

MEDIA_DIR = BASE_DIR / 'users_data.json'
API_KEY = os.getenv('API_KEY')

print(BASE_DIR)
print(MEDIA_DIR)


# def dump(data):
#     with open(MEDIA_DIR, 'w') as f:
#         json.dump(data, f)
#
#
# dump(user_data)
#
#
# def load(data):
#     with open(MEDIA_DIR, 'w') as f:
#         data = json.load(f)
#         return data
#
#
# load(user_data)