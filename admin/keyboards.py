from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.db_control import get_menu_data, get_item_from_menu_change

back_btn = InlineKeyboardButton(text='⬅️ назад', callback_data='back')


async def main_menu_kb():
    menu = InlineKeyboardButton(text='⚙️ Меню', callback_data='menu')
    statistics = InlineKeyboardButton(text='📊 Статистика', callback_data='statistics')
    find_user = InlineKeyboardButton(text='🔎 Найти', callback_data='find_user')
    newsletter = InlineKeyboardButton(text='📢 Рассылка', callback_data='newsletter')
    add_admin = InlineKeyboardButton(text='Добавить админ', callback_data='add_admin')
    return InlineKeyboardMarkup(inline_keyboard=[[find_user, statistics], [menu, newsletter], [add_admin]])


async def back_kb():
    return InlineKeyboardMarkup(inline_keyboard=[[back_btn]])


async def newsletter_kb():
    send = InlineKeyboardButton(text='Отправить', callback_data='send')
    return InlineKeyboardMarkup(inline_keyboard=[[back_btn, send]])


async def users_kb(data, loc=True, num=True, ords=True, canc_ord=True, accpt_ord=True, pers=True):
    kb = InlineKeyboardBuilder()
    match loc:
        case True:
            location = InlineKeyboardButton(text=f"📍 локация", callback_data=f"location {data}")
            kb.add(location)
    match num:
        case True:
            number = InlineKeyboardButton(text=f"👤 контакт", callback_data=f"contact {data}")
            kb.add(number)
    match ords:
        case True:
            orders = InlineKeyboardButton(text=f"ℹ️ заказы", callback_data=f"order {data}")
            kb.add(orders)
    match canc_ord:
        case True:
            cancel_order = InlineKeyboardButton(text=f"❌ отменить", callback_data=f"cancel_order {data}")
            kb.add(cancel_order)
    match accpt_ord:
        case True:
            accept_order = InlineKeyboardButton(text=f"✅ ПРИНЯТЬ", callback_data=f"accept_order {data}")
            kb.add(accept_order)
    match pers:
        case True:
            person_info = InlineKeyboardButton(text=f"ℹ️ назад", callback_data=f"person_info {data}")
            kb.add(person_info)

    return kb.adjust(2).as_markup()


async def change_menu_kb(cat=None):
    kb = InlineKeyboardBuilder()
    buttons = get_menu_data(cat)
    add_cat = InlineKeyboardButton(text='Добавить категорию', callback_data='add_category')
    for button in buttons:
        kb.add(InlineKeyboardButton(text=button, callback_data=button))
    kb.add(add_cat, back_btn)
    return kb.adjust(1).as_markup()


async def change_item_menu_kb():
    add = InlineKeyboardButton(text='Добавить', callback_data='add')
    remove = InlineKeyboardButton(text='Удалить', callback_data='remove')
    change = InlineKeyboardButton(text='Изменить', callback_data='change')
    return InlineKeyboardMarkup(inline_keyboard=[[add, remove], [back_btn, change]])


async def delete_item_from_menu(cat):
    kb = InlineKeyboardBuilder()
    buttons = get_menu_data(cat)[0]
    for button in buttons:
        kb.add(InlineKeyboardButton(text=button, callback_data=button))
    kb.add(back_btn)
    return kb.adjust(1).as_markup()


async def change_item_kb(cat=None):
    kb = InlineKeyboardBuilder()
    buttons = get_item_from_menu_change(cat)

    for button in buttons:
        kb.add(InlineKeyboardButton(text=button[1:], callback_data=button))
    kb.add(back_btn)
    return kb.adjust(1).as_markup()


async def change_info_kb():
    name = InlineKeyboardButton(text='название', callback_data='name')
    price = InlineKeyboardButton(text='цена', callback_data='price')
    photo = InlineKeyboardButton(text='фото',callback_data='photo')
    return InlineKeyboardMarkup(inline_keyboard=[[name, price, photo], [back_btn]])
