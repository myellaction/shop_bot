from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, db
from aiogram import types
from keyboards.inline import (chose_type_order, cb_type_order, show_orders_ikb,
                              cb_order_page, cb_show_order, order_ikb)
from utils.misc.commands import make_purchase_all


@dp.callback_query_handler(text='my_orders')
async def my_orders_cmd(callback: types.CallbackQuery):
    await callback.answer()
    text = 'Какие заказы вас интересуют?'
    markup = await chose_type_order()
    await callback.message.edit_text(text=text, reply_markup=markup)

@dp.callback_query_handler(cb_type_order.filter())
async def show_orders_cmd(callback: types.CallbackQuery, callback_data:dict):
    await callback.answer()
    type = callback_data.get('type')
    who = callback_data.get('who')
    td = {('user', 'Новый'):'📥 Новые заказы в работе',
          ('user', 'Все') : '📋 История ваших заказов',
          ('admin', 'Новый'): "📥 Новые заказы от клиентов",
          ('admin', 'В работе') : '⚙ Сейчас в работе заказы',
          ('admin', 'Готовый') : '✅ Уже приготовленные заказы',
          ('admin', 'Доставленный') : '🛍 Доставленные клиентам заказы',
          ('admin', 'Отменен') : '❎ Отмененные заказы без оплаты'}
    text = td[(who, type)]
    buyer_id = callback.from_user.id if who == 'user' else None
    orders = await db.get_order_purchases(buyer_id,type)
    if len(orders) == 0:
        text +='\n<i>На данный момент таких заказов нет</i>'
    markup = await show_orders_ikb(orders, type = type, who = who)
    await callback.message.edit_text(text=text, reply_markup = markup)

@dp.callback_query_handler(cb_order_page.filter())
async def cb_order_page_cmd(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    page = int(callback_data.get('page'))
    type = callback_data.get('type')
    who = callback_data.get('who')
    buyer_id = callback.from_user.id if who == 'user' else None
    orders = await db.get_order_purchases(buyer_id, type)
    markup = await show_orders_ikb(orders, page=page, type=type, who = who)
    await callback.message.edit_reply_markup(markup)

@dp.callback_query_handler(cb_show_order.filter())
async def show_detail_order_cmd(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    order_purchase_id = int(callback_data.get('id'))
    type =callback_data.get('type')
    who = callback_data.get('who')
    purchases = await db.get_purchases_by_order(order_purchase_id)
    order_purchase = await db.get_order_purchase(order_purchase_id)
    delivery = order_purchase.get('delivery')
    total = order_purchase.get('total')
    status = order_purchase.get('status')
    text_delivery = '<b>Доставка:</b> самовывоз' if delivery == 'Самовывоз' else "<b>Доставка:</b> курьером (+100 грн.)"
    text = (await make_purchase_all(purchases))[0]
    text = text.split('\n')
    while '' in text:
        text.remove('')
    text = [text[i] if i %2 else text[i] +'\n' for i in range(1,len(text))]
    text = [f'Заказ №{order_purchase_id}\nСтатус: {status}\n'] + text[0:len(text)-1] + [text_delivery] + [f'<b>Всего:</b> {total} грн.']
    text = '\n'.join(text)
    markup = await order_ikb(order_purchase_id, type, who)
    await callback.message.edit_text(text=text, reply_markup=markup)




