from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from loader import db


cb_menu = CallbackData('menu', 'level', 'category_id', 'subcategory_id', 'item_id','purchase_id', 'mes')
cb_item = CallbackData('item','category_id', 'subcategory_id','item_id', 'total','purchase_id','mes')
cb_purchase = CallbackData('purchase', 'action', 'total')
cb_change_page=CallbackData('my_order', 'page','mes')
cb_empty = CallbackData('empty')

cb_edit_purchase = CallbackData('edit_purchase', 'purchase_id')
cb_edit_purchase_item = CallbackData('edit_purchase_item','item_id', 'total','mes')

cb_delivery = CallbackData('delivery','type','total')
cb_make_order = CallbackData('make_order', 'total', 'delivery')

cb_type_order = CallbackData('cb_type_order', 'type', 'who')
cb_show_order = CallbackData('cb_show_order', 'id', 'type', 'who')
cb_order_page = CallbackData('cb_order_page', 'page', 'type', 'who')

cb_admin_order = CallbackData('cb_admin_order', 'order_purchase_id', 'type', 'action')

from utils.misc.commands import make_cb

async def menu_kb():
    markup = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='📒 Меню', callback_data=make_cb())],
        [InlineKeyboardButton(text='📦 Моя корзина', callback_data='my_order')],
        [InlineKeyboardButton(text='🗂 Мои заказы', callback_data='my_orders')],
        [InlineKeyboardButton(text='📱 Контакты', callback_data='contacts')],
        [InlineKeyboardButton(text='🔐 Админ панель', callback_data='admin_panel')],
    ])
    return markup

async def back_to_menu():
    markup=InlineKeyboardMarkup(row_width=1,inline_keyboard=[
        [InlineKeyboardButton(text='⬅ Назад', callback_data='main_menu')]
        ])
    return markup

async def purchase_menu(total=0):
    markup = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='✅ Сделать заказ',
                              callback_data=cb_purchase.new(action='make', total=total))],
        [InlineKeyboardMarkup(text='📝 Редактировать заказ',
                              callback_data=cb_purchase.new(action='edit', total=0))],
        [InlineKeyboardButton(text='❌ Очистить корзину',
                              callback_data=cb_purchase.new(action='delete', total=0))],
        [InlineKeyboardButton(text='⬅ Назад', callback_data='main_menu')]
       ])
    return markup

async def edit_purchase(purchase_ids, page=0,mes=0):
    total = 5
    markup = InlineKeyboardMarkup(row_width=total)
    len_list= len(purchase_ids)
    start = page * total
    end = start + total
    max_page=len_list//total if len_list%total==0 else len_list//total +1
    current_ids = purchase_ids[start:end]
    for n,i in enumerate(current_ids,start):
        markup.insert(InlineKeyboardButton(text=str(n+1),
                                        callback_data=cb_edit_purchase.new(i)))
    n = len (current_ids)
    while n<total:
        markup.insert(InlineKeyboardButton(text='-',
                                           callback_data=cb_empty.new()))
        n+=1
    if len_list>total:
        if page >0:
            markup.row(InlineKeyboardButton(text='<', callback_data=cb_change_page.new(page-1,mes)))
        else:
            markup.row(InlineKeyboardButton(text='...', callback_data=cb_empty.new()))
        if page<max_page-1:
            markup.insert(InlineKeyboardButton(text='>', callback_data=cb_change_page.new(page + 1, mes)))
        else:
            markup.insert(InlineKeyboardButton(text='...', callback_data=cb_empty.new()))
    markup.add(InlineKeyboardButton(text='⬅ Назад', callback_data='my_order'))
    return markup


async def edit_purchase_item(item_id, total, mes=1):
    if total == 0:
        maybe_empty = InlineKeyboardButton(text='🔻', callback_data=cb_empty.new())
    else:
        maybe_empty = InlineKeyboardButton(text='🔻',
                                           callback_data=cb_edit_purchase_item.new(item_id,
                                                                                   total - 1,
                                                                                   mes))

    markup = InlineKeyboardMarkup(row_width=3)
    markup.insert(maybe_empty)
    buttons = [InlineKeyboardButton(text=f'{total} шт.', callback_data=cb_empty.new()),
               InlineKeyboardButton(text='🔺', callback_data=cb_edit_purchase_item.new(item_id, total + 1,
                                                                                      mes))]
    for i in buttons:
        markup.insert(i)

    markup.add(InlineKeyboardButton(text='⬅ Назад', callback_data=cb_change_page.new(page=0,mes=mes)))
    return markup


async def chose_delivery(total):
    markup = InlineKeyboardMarkup(inline_keyboard = [
        [InlineKeyboardButton('🛵 Курьером (+100 грн.)', callback_data=cb_delivery.new('курьером', total))],
        [InlineKeyboardButton('💪 Самовывоз', callback_data=cb_delivery.new('самовывоз', total))]])
    markup.add(InlineKeyboardButton(text='⬅ Назад', callback_data='my_order'))
    return markup


async def make_order(total, delivery):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✅ Готово', callback_data=cb_make_order.new(total, delivery))],
        [InlineKeyboardButton(text='⬅ Назад', callback_data='my_order')]
    ])
    return markup


async def chose_type_order():
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('📥 Новые', callback_data = cb_type_order.new('Новый', 'user'))],
        [InlineKeyboardButton('📋 История заказов', callback_data=cb_type_order.new('Все', 'user'))]
    ])
    markup.add(InlineKeyboardButton(text='⬅ Назад', callback_data='main_menu'))
    return markup


async def show_orders_ikb (orders, type, who, page=1):
    total_pages = 5
    start = (page-1) * total_pages
    end = start + total_pages
    l = len(orders)
    if l%total_pages:
        last_page = l//total_pages +1
    else:
        last_page = l//total_pages
    slice = orders[start:end]
    markup = InlineKeyboardMarkup()
    for i in slice:
        id = i.get("order_purchase_id")
        total = i.get("total")
        text = f'№{id} - {total} грн.'
        markup.add(InlineKeyboardButton(text=text, callback_data=cb_show_order.new(id, type, who)))
    if l>total_pages:
        ls = len(slice)
        while ls < total_pages:
            markup.add(InlineKeyboardButton(text='-', callback_data=cb_empty.new()))
            ls+=1

        if page == 1:
            markup.add(InlineKeyboardButton(text='...', callback_data=cb_empty.new()))
        else:
            markup.add(InlineKeyboardButton(text='<', callback_data=cb_order_page.new(page-1, type, who)))

        if page == last_page:
            markup.insert(InlineKeyboardButton(text = '...', callback_data=cb_empty.new()))
        else:
            markup.insert(InlineKeyboardButton(text='>', callback_data=cb_order_page.new(page+1, type, who)))
    if who == 'user':
        markup.add(InlineKeyboardButton(text='⬅ Назад', callback_data='my_orders'))
    else:
        markup.add(InlineKeyboardButton(text='⬅ Назад', callback_data='admin_panel'))

    return markup

async def admin_panel_ikb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='📥 Новые заказы', callback_data=cb_type_order.new('Новый', 'admin'))],
        [InlineKeyboardButton(text='⚙ В работе', callback_data=cb_type_order.new('В работе','admin'))],
        [InlineKeyboardButton(text='✅ Готовые заказы', callback_data=cb_type_order.new('Готовый','admin'))],
        [InlineKeyboardButton(text='🛍 Доставленные заказы',
                              callback_data=cb_type_order.new('Доставленный', 'admin'))],
        [InlineKeyboardButton(text='❎ Отмененные заказы', callback_data=cb_type_order.new('Отменен', 'admin'))],
        [InlineKeyboardButton(text='⬅ Назад', callback_data="main_menu")]
    ])

async def order_ikb(order_purchase_id=None, type=None, who=None):
    if who == 'user':
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='⬅ Назад', callback_data=cb_type_order.new(type, who))]
        ])
    else:
        dct = {'Новый':['В работу', 'В работе'],
          'В работе' : ['Готовый', "Готовый"],
          'Готовый' : ['Доставленный', "Доставленный"]}

        markup =  InlineKeyboardMarkup(inline_keyboard = [
            [InlineKeyboardButton(text='Удалить',
                                 callback_data = cb_admin_order.new(order_purchase_id, type, 'delete'))]])
        if type not in ('Доставленный', "Отменен"):
            markup.insert(InlineKeyboardButton(text='Отменить',
                                               callback_data=cb_admin_order.new(order_purchase_id, type, 'cancel')))
            markup.insert(InlineKeyboardButton(text=dct[type][0],
                                               callback_data= cb_admin_order.new(order_purchase_id,
                                                                                 type, dct[type][1])))
        markup.add(InlineKeyboardButton(text='⬅ Назад', callback_data=cb_type_order.new(type,who)))
        return markup











async def categories_kb(**kwargs):
    LEVEL = 0
    cats = await db.get_cats()
    markup = InlineKeyboardMarkup(row_width = 1)
    for i in cats:
        name = i.get('category_name')
        name_id = i.get('category_id')
        markup.add(InlineKeyboardButton(text=name,
                                        callback_data=make_cb(LEVEL+1, name_id)))
    markup.add(InlineKeyboardButton(text='⬅ Назад', callback_data='main_menu'))
    return markup

async def subcategories_kb(category_id=0, **kwargs):
    LEVEL = 1
    subcats = await db.get_subcats(category_id)
    markup = InlineKeyboardMarkup(row_width=1)
    for i in subcats:
        name = i.get('subcategory_name')
        name_id = i.get('subcategory_id')
        markup.add(InlineKeyboardButton(text=name,
                                        callback_data = make_cb(LEVEL+1, category_id, name_id)))
    markup.add(InlineKeyboardButton(text='⬅ Назад',
                                    callback_data=make_cb(LEVEL - 1)))
    return markup

async def items_kb(category_id=0, subcategory_id=0, **kwargs):
    LEVEL = 2
    items = await db.get_items(category_id=category_id, subcategory_id=subcategory_id)
    markup = InlineKeyboardMarkup(row_width=1)
    for i in items:
        text = f"{i.get('item_name')} - {i.get('price')} грн."
        id = i.get('item_id')
        markup.add(InlineKeyboardButton(text=text,
                                        callback_data= make_cb(LEVEL+1, category_id, subcategory_id, id)))
    markup.add(InlineKeyboardButton(text = '⬅ Назад',
                                    callback_data = make_cb(LEVEL-1, category_id)))
    return markup

async def item_kb(category_id, subcategory_id, item_id, purchase_id=0, total=1,mes=1, **kwargs):
    LEVEL = 3
    if total ==0:
        maybe_empty = InlineKeyboardButton(text='🔻', callback_data=cb_empty.new())
    else:
        maybe_empty = InlineKeyboardButton(text='🔻',
                                           callback_data=cb_item.new(category_id,
                                                                     subcategory_id,item_id,
                                                                     total-1, purchase_id, mes))

    markup = InlineKeyboardMarkup(row_width=3)
    markup.insert(maybe_empty)
    buttons=[InlineKeyboardButton(text=f'{total} шт.', callback_data=cb_empty.new()),
         InlineKeyboardButton(text='🔺', callback_data=cb_item.new(category_id,
                                                                  subcategory_id,
                                                                  item_id,total+1, purchase_id, mes))]
    for i in buttons:
        markup.insert(i)

    markup.add(InlineKeyboardButton(text='⬅ Назад', callback_data=make_cb(LEVEL-1,
                                                                      category_id, subcategory_id,
                                                                             purchase_id=purchase_id,
                                                                        mes=mes)))
    return markup










