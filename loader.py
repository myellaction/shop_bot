from aiogram import Bot, Dispatcher
from data.config import TOKEN_API
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from utils.db_api.postgres import Database

storage = MemoryStorage()
bot = Bot(token = TOKEN_API, parse_mode = 'HTML')
dp = Dispatcher(bot = bot, storage=storage)

loop = asyncio.get_event_loop()
db = loop.run_until_complete(Database.create())


