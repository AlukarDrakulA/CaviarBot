from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = '5081975494:AAHQkbKrHo0LCP936bbgemDM1D8JftB-MwE'
# PROXY_URL = 'http://proxy.server:3128'

storage = MemoryStorage()

# bot = Bot(token=API_TOKEN, proxy= PROXY_URL)
bot = Bot(token=API_TOKEN) # для локального запуска
dp = Dispatcher(bot, storage=storage)
