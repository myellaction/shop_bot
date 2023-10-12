from keyboards.inline import cb_menu
from loader import db
from aiogram import types

def make_cb(level=0, category_id=0, subcategory_id=0, item_id=0,purchase_id=0, mes=0):
    return cb_menu.new(level, category_id, subcategory_id, item_id, purchase_id, mes)

def make_purchase_text(name, price, amount=1):

    res = f'''✅ Добавлено: <b>{name}</b>
{price} грн. x {amount} шт. = {price*amount} грн.
<b>Всего: {price * amount} грн.</b>'''

    return res

async def make_purchase_all(purchases):
    text_list=[]
    total = 0
    for n,purchase in enumerate(purchases,1):
        item = await db.get_item(purchase.get('item_id'))
        name = item.get('item_name')
        price = item.get('price')
        amount = purchase.get('amount')
        tmp_total = price*amount
        text = f'''<b>{n}. {name}</b>
{price} грн. x {amount} шт. = {tmp_total} грн.'''
        text_list.append(text)
        total +=tmp_total
    res = '📦 В корзину покупок добавлено:\n\n'+ '\n\n'.join(text_list) + f'\n\n<b>Всего: {total} грн.</b>'
    return res, total


async def set_default_commands(dp):
    await dp.bot.set_my_commands([types.BotCommand('menu', "📋 Показать меню")])




