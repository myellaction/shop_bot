from loader import dp, db
from aiogram import types
from aiogram.dispatcher.filters import CommandStart, Command
from keyboards.inline import menu_kb, back_to_menu


@dp.message_handler(commands = ['start', 'menu'])
async def cmd_start(message: types.Message):
    user = await db.get_buyer(message.from_user.id)
    if not user:
        try:
            await db.add_buyer(message.from_user.id, message.from_user.full_name,
                               message.from_user.username)
        except:
            pass
    await message.answer('🥁 Пиццерия "Yummy pizza"!\n🗒 Здесь вы можете сделать заказ.',
                         reply_markup=await menu_kb())



@dp.callback_query_handler(text='contacts')
async def contacts_cmd(callback: types.CallbackQuery):
    await callback.answer()
    text = '''<b>Наши контакты:</b> 
💼 <i>Разработка телеграм ботов для заведений, компаний и другие проекты.</i> 

<b>Еще одна работа:</b> @morskoi_boy_pythonbot
⛴ игра "Морской бой" с мультиплеером'''
    await callback.message.edit_text(text=text, reply_markup = await back_to_menu())