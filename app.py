from aiogram import executor
from handlers import dp
from loader import db
from utils.misc.commands import set_default_commands


async def on_startup(dp):
    await set_default_commands(dp)
    print('Подключение к БД')
    #await db.drop_tables()
    #await db.create_tables()
    print('Бот запущен!')



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates = True)