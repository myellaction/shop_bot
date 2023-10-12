from loader import dp
from aiogram import types
from pprint import pprint
from data.const import menu_dict



'''
@dp.message_handler(content_types = types.ContentType.PHOTO)
async def get_dict(message: types.Message):
    photo = message.photo[0].file_id
    text = message.caption
    menu_dict[text] = {'price':200, 'img':photo, 'category_id': 4,'subcategory_id':13}

@dp.message_handler(text='/end')
async def end(message: types.Message):
    pprint(menu_dict)
'''


















