from loader import dp, bot, db
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline import (menu_kb, categories_kb,subcategories_kb,
                              items_kb, item_kb, cb_menu, cb_empty, cb_item, back_to_menu,
                              purchase_menu, cb_purchase, edit_purchase, cb_change_page,
                              cb_edit_purchase, edit_purchase_item, chose_delivery)
from utils.misc.commands import make_purchase_text, make_purchase_all
import asyncio



@dp.callback_query_handler(cb_menu.filter())
async def get_menu(callback: types.CallbackQuery, callback_data:dict, state:FSMContext):
    await callback.answer()
    level = int(callback_data.get('level'))
    kwargs = {'level':level,
              'category_id': int(callback_data.get('category_id')),
              'subcategory_id':int(callback_data.get('subcategory_id')),
             'item_id':int(callback_data.get('item_id')),
             'purchase_id':int(callback_data.get('purchase_id'))}

    if level==3:
        purchase = await db.get_purchase(buyer_id = callback.from_user.id,
                                         item_id=kwargs['item_id'])
        if purchase:
            total = purchase.get('amount')
            if total == 0:
                total = 1
                await db.edit_purchase(purchase.get('purchase_id'), amount=total)
            kwargs['total']=total
        else:
            await db.add_purchase(callback.from_user.id, kwargs['item_id'])


    func = {0:categories_kb, 1: subcategories_kb, 2:items_kb, 3 : item_kb}
    markup = await func[level](**kwargs)
    if level==3:
        await callback.message.delete()
        user_id = callback.from_user.id
        img = (await db.get_item(kwargs['item_id'])).get('img')
        item_name = (await db.get_item(kwargs['item_id'])).get('item_name')
        price = (await db.get_item(kwargs['item_id'])).get('price')
        await asyncio.sleep(0.2)
        text = make_purchase_text(item_name, price, kwargs.get('total', 1))
        return await bot.send_photo(chat_id=user_id, caption= text, photo=img,
                                   reply_markup=markup)



    mes = callback_data.get('mes')
    if level ==2 and mes=='1':
        await callback.message.delete()
        await asyncio.sleep(0.2)
        return await callback.message.answer(text='📒 Меню заведения "Yummy pizza"', reply_markup=markup)

    await callback.message.edit_text(text='📒 Меню заведения "Yummy pizza"',reply_markup=markup)

@dp.callback_query_handler(text='main_menu')
async def get_menu(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text='🥁 Пиццерия "Yummy pizza"!\n'
                                          '🗒 Здесь вы можете сделать заказ.',
                                     reply_markup=await menu_kb())


@dp.callback_query_handler(cb_item.filter())
async def item_menu(callback: types.CallbackQuery, callback_data:dict):
    await callback.answer()
    kwargs = {'category_id': int(callback_data.get('category_id')),
              'subcategory_id': int(callback_data.get('subcategory_id')),
              'item_id': int(callback_data.get('item_id')),
              'purchase_id': int(callback_data.get('purchase_id')),
              'total': int(callback_data.get('total')),
              'mes': callback_data.get('mes')}
    purchase = await db.get_purchase(callback.from_user.id, kwargs['item_id'])
    if not purchase:
        await db.add_purchase(callback.from_user.id,kwargs['item_id'],kwargs['total'])
    else:
        await db.edit_purchase(purchase_id=purchase.get('purchase_id'), amount=kwargs['total'])


    markup = await item_kb(**kwargs)
    item_name = (await db.get_item(kwargs['item_id'])).get('item_name')
    price = (await db.get_item(kwargs['item_id'])).get('price')
    text = make_purchase_text(item_name, price, kwargs['total'])
    await callback.message.edit_caption(caption = text, reply_markup=markup)


@dp.callback_query_handler(text='my_order')
async def show_purchase(callback: types.CallbackQuery):
    await callback.answer()
    purchases = await db.get_purchase_all(callback.from_user.id)
    if not purchases:
        return await callback.message.edit_text(text='🛒 Ваша корзина покупок пустая',
                                         reply_markup = await back_to_menu())
    text, total = await make_purchase_all(purchases)
    await callback.message.edit_text(text=text,
                                     reply_markup=await purchase_menu(total))


@dp.callback_query_handler(cb_purchase.filter())
async def purchase_menu1(callback: types.CallbackQuery, callback_data:dict):
    await callback.answer()
    action = callback_data.get('action')
    buyer_id = callback.from_user.id
    if action == 'make':
        total = callback_data.get('total')
        markup = await chose_delivery(total)
        return await callback.message.edit_text(text='Выберите способ доставки 🛍',
                                                reply_markup=markup)

    elif action == 'delete':
        await db.delete_purchases_creating(buyer_id)
        return await callback.message.edit_text('🛒 Корзина покупок очищена',
                                                reply_markup=await back_to_menu())
    elif action == 'edit':
        purchase_ids = await db.get_purchase_all(buyer_id)
        purchase_ids = [i.get('purchase_id') for i in purchase_ids]
        markup = await edit_purchase(purchase_ids)
        await callback.message.edit_reply_markup(markup)


@dp.callback_query_handler(cb_change_page.filter())
async def cmd_change_page(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    mes = callback_data.get('mes')
    if mes=='1':
        buyer_id=callback.from_user.id
        await callback.message.delete()
        purchases = await db.get_purchase_all(buyer_id)
        purchase_ids = [i.get('purchase_id') for i in purchases]
        text = (await make_purchase_all(purchases))[0]
        markup = await edit_purchase(purchase_ids)
        await asyncio.sleep(0.2)
        return await callback.message.answer(text=text, reply_markup=markup)


    page = int(callback_data.get('page'))
    purchase_ids = await db.get_purchase_all(callback.from_user.id)
    purchase_ids = [i.get('purchase_id') for i in purchase_ids]
    markup = await edit_purchase(purchase_ids, page)
    await callback.message.edit_reply_markup(markup)


@dp.callback_query_handler(cb_empty.filter())
async def empty_place(callback: types.CallbackQuery):
    await callback.answer()








