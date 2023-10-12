from keyboards.inline import (cb_edit_purchase, edit_purchase_item,
                              cb_edit_purchase_item, cb_delivery, make_order, cb_make_order, back_to_menu)
from loader import dp, bot, db
from aiogram import types
import asyncio
from decimal import Decimal
from utils.misc.commands import make_purchase_text


@dp.callback_query_handler(cb_edit_purchase.filter())
async def cmd_edit_purchase(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    await callback.message.delete()
    purchase_id = int(callback_data.get('purchase_id'))
    purchase = await db.get_purchase(purchase_id=purchase_id)
    amount = purchase.get('amount')
    total = purchase.get('amount')
    item_id = purchase.get('item_id')
    item = await db.get_item(item_id)
    item_name = item.get('item_name')
    price = item.get('price')
    img = item.get('img')
    markup = await edit_purchase_item(item_id, total)
    text = make_purchase_text(item_name, price, amount)
    await asyncio.sleep(0.5)
    await bot.send_photo(chat_id=callback.from_user.id,
                               photo=img, caption=text, reply_markup=markup)


@dp.callback_query_handler(cb_edit_purchase_item.filter())
async def item_menu(callback: types.CallbackQuery, callback_data:dict):
    await callback.answer()
    kwargs = {'item_id': int(callback_data.get('item_id')),
              'total': int(callback_data.get('total'))}
    purchase = await db.get_purchase(callback.from_user.id, kwargs['item_id'])
    if not purchase:
        await db.add_purchase(callback.from_user.id,kwargs['item_id'],kwargs['total'])
    else:
        await db.edit_purchase(purchase_id=purchase.get('purchase_id'), amount=kwargs['total'])
    markup = await edit_purchase_item(**kwargs)
    item_name = (await db.get_item(kwargs['item_id'])).get('item_name')
    price = (await db.get_item(kwargs['item_id'])).get('price')
    text = make_purchase_text(item_name, price, kwargs['total'])
    await callback.message.edit_caption(caption = text, reply_markup=markup)


@dp.callback_query_handler(cb_delivery.filter())
async def chose_delivery_cmd(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    delivery = callback_data.get('type')
    total = callback_data.get('total')
    if delivery == 'курьером':
        total = Decimal(total) +100
    text = f'🗒 Ваш заказ сформирован!\n' \
           f'<b>Сумма:</b> {total} грн.\n' \
           f'<b>Способ доставки:</b> {delivery}\n'
    markup = await make_order(total, delivery)
    await callback.message.edit_text(text=text, reply_markup=markup)

@dp.callback_query_handler(cb_make_order.filter())
async def make_order_cmd (callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    buyer_id = callback.from_user.id
    total = Decimal(callback_data.get('total'))
    delivery = callback_data.get('delivery').capitalize()
    id = await db.add_order_purchase(buyer_id, total, delivery)
    return await callback.message.edit_text(f'🥁 Поздравляем!\n'
                                                f'Заказ №{id} отправлен в обработку.\n'
                                                f'<b>Сумма заказа:</b> {total} грн.',
                                         reply_markup=await back_to_menu())
