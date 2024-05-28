import aiogram.types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.db_basket_control import db_basket_get_items
from db.db_control import get_menu_data
from lexicon.lexicon import text_func


async def back_kb(user_id):
    btn = InlineKeyboardButton(text=await text_func(user_id, 'back_to_menu_kb'), callback_data='back_to_menu')
    return InlineKeyboardMarkup(inline_keyboard=[[btn]])


# ============================ LANGUAGE KB ===============================

async def language_kb():
    e = InlineKeyboardButton(text='🇬🇧', callback_data='e')
    r = InlineKeyboardButton(text='🇷🇺', callback_data='r')
    u = InlineKeyboardButton(text='🇺🇿', callback_data='u')
    t = InlineKeyboardButton(text='🇹🇷', callback_data='t')

    kb = InlineKeyboardMarkup(inline_keyboard=[[e, r, ], [u, t]])
    return kb


# ============================ MAIN MENU KB ===============================


async def main_menu_kb(user_id):
    menu = InlineKeyboardButton(text=await text_func(user_id, 'menu_kb'), callback_data='menu')
    basket = InlineKeyboardButton(text=await text_func(user_id, 'basket_kb'), callback_data='basket')
    profile = InlineKeyboardButton(text=await text_func(user_id, 'write_us_kb'), callback_data='write_us')
    lang = InlineKeyboardButton(text=await text_func(user_id, 'change_lang_kb'), callback_data='change_lang')

    kb = InlineKeyboardMarkup(inline_keyboard=[[menu, basket], [lang, profile]])
    return kb


# ============================ CATEGORIES KB ===============================


async def categories_kb(user_id):
    kb = InlineKeyboardBuilder()
    for button in get_menu_data():
        kb.add(InlineKeyboardButton(text=button, callback_data=button))
    kb.add(InlineKeyboardButton(text=await text_func(user_id, 'basket_kb'), callback_data='basket'),
           InlineKeyboardButton(text=await text_func(user_id, 'back_to_menu_kb'), callback_data='back_to_menu'))
    return kb.adjust(2).as_markup()


# ============================ IN CATEGORIES KB ===============================


async def in_categories_kb(category, user_id):
    kb = InlineKeyboardBuilder()
    for button in get_menu_data(cat=category)[0]:
        kb.add(InlineKeyboardButton(text=button, callback_data=button))
    kb.add(InlineKeyboardButton(text=await text_func(user_id, 'basket_kb'), callback_data='basket'))
    kb.add(InlineKeyboardButton(text=await text_func(user_id, 'back_cat_kb'), callback_data='back_cat_kb'))

    return kb.adjust(2).as_markup()


# ============================ CHOSEN ITEM KB ===============================


async def chosen_item_kb(item, user_id=None):
    item = InlineKeyboardButton(text=f'{item[0]} {item[1]}', callback_data=f'chosen_{item[0]}')
    add = InlineKeyboardButton(text='+', callback_data='add')
    remove = InlineKeyboardButton(text='-', callback_data='remove')
    done = InlineKeyboardButton(text=await text_func(user_id, 'done_kb'), callback_data='done')

    kb = InlineKeyboardMarkup(inline_keyboard=[[remove, item, add], [done]])
    return kb


# ============================ BASKET KB ===============================


async def basket_kb(user_id):
    change = InlineKeyboardButton(text=await text_func(user_id, 'change_kb'), callback_data='change')
    menu = InlineKeyboardButton(text=await text_func(user_id, 'menu_kb'), callback_data='menu')
    clear = InlineKeyboardButton(text=await text_func(user_id, 'clear_kb'), callback_data='clear')
    complete = InlineKeyboardButton(text=await text_func(user_id, 'complete_kb'), callback_data='complete')

    kb = InlineKeyboardMarkup(inline_keyboard=[[change, clear], [menu, complete]])
    return kb


# ============================ CHANGE ITEM IN BASKET KB ===============================


async def change_in_basket_kb(callback):
    user_id = callback.from_user.id
    kb = InlineKeyboardBuilder()
    for button in await db_basket_get_items(user_id, 'item'):
        kb.add(InlineKeyboardButton(text=button[0], callback_data=button[0]))
    kb.add(InlineKeyboardButton(text=await text_func(user_id, 'back_basket_kb'), callback_data='back_basket'))
    return kb.adjust(1).as_markup()


# ============================ REGISTRATION KB ===============================


async def registration_kb(user_id):
    sign_up = InlineKeyboardButton(text=await text_func(user_id, 'sign_up_kb'), callback_data='sign_up')
    skip = InlineKeyboardButton(text=await text_func(user_id, 'cancel_kb'), callback_data='cancel')

    kb = InlineKeyboardMarkup(inline_keyboard=[[sign_up], [skip]])
    return kb


# ============================ GET LOCATION AND CONTACT KB ===============================

async def get_location(user_id) -> aiogram.types.ReplyKeyboardMarkup:
    location = KeyboardButton(text=await text_func(user_id, 'location_kb'), request_location=True)
    return ReplyKeyboardMarkup(keyboard=[[location]], resize_keyboard=True)


async def get_contact(user_id):
    contact = KeyboardButton(text=await text_func(user_id, 'contact_kb'), request_contact=True)
    kb = ReplyKeyboardMarkup(keyboard=[[contact]], one_time_keyboard=True, resize_keyboard=True)
    return kb


# ============================ COMPLETE REGISTRATION KB ===============================


async def complete_registration_kb():
    yes = InlineKeyboardButton(text='✅', callback_data='yes_reg')
    no = InlineKeyboardButton(text='❌', callback_data='no_reg')
    return InlineKeyboardMarkup(inline_keyboard=[[no, yes]])


# ============================ COMPLETE ORDER KB ===============================

async def complete_order_kb(user_id):
    yes = InlineKeyboardButton(text=await text_func(user_id, 'complete_kb'), callback_data='complete_order')
    no = InlineKeyboardButton(text=await text_func(user_id, 'cancel_order_kb'), callback_data='cancel')
    return InlineKeyboardMarkup(inline_keyboard=[[no, yes]])


# ============================ PAYMENT METHOD KB ===============================

async def payment_method_kb(user_id):
    cash = InlineKeyboardButton(text=await text_func(user_id, 'payment_cash_kb'), callback_data='cash')
    card = InlineKeyboardButton(text=await text_func(user_id, 'payment_card_kb'), callback_data='card')
    return InlineKeyboardMarkup(inline_keyboard=[[cash, card]])


# ============================ ABOUT US KB ===============================

async def about_us_kb(user_id):
    cafe_contact1 = InlineKeyboardButton(text=await text_func(user_id, 'contact_kb') + ' 1',
                                         callback_data='cafe_contact1')
    cafe_contact2 = InlineKeyboardButton(text=await text_func(user_id, 'contact_kb') + ' 2',
                                         callback_data='cafe_contact2')
    cafe_location = InlineKeyboardButton(text=await text_func(user_id, 'location_kb'), callback_data='cafe_location')
    back_btn = InlineKeyboardButton(text=await text_func(user_id, 'back_to_menu_kb'), callback_data='back_to_menu')

    return InlineKeyboardMarkup(inline_keyboard=[[cafe_contact1, cafe_contact2], [cafe_location], [back_btn]])


async def back_to_write_us_kb(user_id):
    back_btn = InlineKeyboardButton(text=await text_func(user_id, 'back_to_menu_kb'), callback_data='back_to_write_us')
    return InlineKeyboardMarkup(inline_keyboard=[[back_btn]])


async def choose_address_kb(user_id, address):
    kb = InlineKeyboardBuilder()
    for button in address:
        kb.add(InlineKeyboardButton(text=button, callback_data=f"my-{button}"))
    kb.add(InlineKeyboardButton(text=await text_func(user_id, 'add_new_address_kb'), callback_data='add_new_address'))
    return kb.adjust(1).as_markup()