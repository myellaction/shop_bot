from loader import dp, db
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline import admin_panel_ikb, cb_admin_order, cb_type_order

@dp.callback_query_handler(text='admin_panel')
async def admin_panel(callback: types.CallbackQuery):
    await callback.answer()
    text = '🔐 Панель для работы с заказами'
    markup = await admin_panel_ikb()
    await callback.message.edit_text(text=text, reply_markup = markup)

@dp.callback_query_handler(cb_admin_order.filter())
async def admin_order_cmd(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    order_purchase_id = int(callback_data.get('order_purchase_id'))
    type = callback_data.get('type')
    action = callback_data.get('action')
    await db.edit_order_status_or_delete(order_purchase_id, action)
    dct = {'В работе': f"Заказ №{order_purchase_id} добавлен в работу",
        'Готовый': f'Заказ №{order_purchase_id} перемещен в готовые',
        'Доставленный': f'Заказ №{order_purchase_id} перемещен в доставленные',
        'cancel': f'Заказ №{order_purchase_id} успешно отменен',
        'delete': f'Заказ №{order_purchase_id} успешно удален'}
    text = dct[action]
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data=cb_type_order.new(type, who='admin'))]
    ])
    await callback.message.edit_text(text=text, reply_markup = markup)










