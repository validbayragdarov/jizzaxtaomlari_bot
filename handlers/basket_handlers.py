from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from datetime import datetime
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from admin.keyboards import users_kb
from db.db_basket_control import db_basket_get, db_basket_clear, db_basket_update, db_basket_get_items
from db.db_control import create_basket, update_userdata, get_userdata, get_all_userdata, get_db_for_admin
from handlers.user_handlers import back_to_menu_func
from keyboards.keyboards import basket_kb, change_in_basket_kb, registration_kb, complete_order_kb, payment_method_kb
from handlers.menu_handlers import ChosenItem, menu_func
from lexicon.lexicon import text_func
from config import GROUP_ID, TOKEN, ADMIN, db

router = Router()
bot = Bot(token=TOKEN)

router.message.filter(lambda x: x.from_user.id not in ADMIN)
router.callback_query.filter(lambda x: x.from_user.id not in ADMIN)


class PaymentMethod(StatesGroup):
    method = State()


def user_registered(user_id):
    try:
        with db.cursor() as cursor:
            cursor.execute(f""" SELECT registered FROM user_data WHERE tg_id = {user_id} """)
            return 1 == int(cursor.fetchall()[0][0])
    except:
        return False


@router.callback_query(F.data.in_(['basket', 'back_basket']))
async def basket_func(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    await create_basket(user_id)
    await callback.message.edit_text(
        await db_basket_get(callback.from_user.id, 'item,price,count, time'),
        reply_markup=await basket_kb(user_id))


@router.callback_query(F.data == 'clear')
async def clear_basket_func(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    await db_basket_clear(user_id)
    await basket_func(callback)


@router.callback_query(F.data == 'change')
async def change_in_basket(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(ChosenItem.item)
    await callback.message.edit_text(
        await db_basket_get(callback.from_user.id, 'id,item,price,count,time'),
        reply_markup=await change_in_basket_kb(callback))


@router.callback_query(F.data == 'complete')
async def complete_order_func(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await callback.answer()
    if user_registered(user_id):
        if await db_basket_get(user_id, '*') == await text_func(user_id, 'empty_basket'):
            await menu_func(callback)
        else:
            await state.set_state(PaymentMethod.method)
            await callback.message.edit_text('payment', reply_markup=await payment_method_kb(user_id))
    else:
        await callback.message.edit_text(await text_func(user_id, 'need_sign_up'),
                                         reply_markup=await registration_kb(user_id))


@router.callback_query(F.data.in_(['cash', 'card']))
async def choose_payment_func(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await callback.answer()
    match callback.data:
        case 'cash':
            await state.update_data(payment_method='💵 Наличка')
        case 'card':
            await state.update_data(payment_method='💳 Карта')
    await callback.message.edit_text(await text_func(user_id, 'precomplete_order'),
                                     reply_markup=await complete_order_kb(user_id))


@router.callback_query(F.data == 'complete_order')
async def complete_order_process(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    user_id = callback.from_user.id
    data_id = await get_db_for_admin(f""" SELECT id FROM user_data WHERE tg_id = {user_id} """)
    await back_to_menu_func(callback)
    await db_basket_update(user_id, time=str(datetime.now())[:-7])
    order_info = (await get_all_userdata(user_id, 'name, '
                                                  'surname, '
                                                  'address, '
                                                  'username, '
                                                  'tg_id, '
                                                  'phone_number') +
                  await db_basket_get(user_id, 'item,price,count,time') + data['payment_method'])

    await bot.send_message(chat_id=GROUP_ID, text=order_info,
                           reply_markup=await users_kb(data_id[0][0], ords=False, pers=False))

    get_total = await db_basket_get_items(user_id, 'SUM(count*price)')
    for total in get_total:
        get_total = total[0]
    sum_order = await get_userdata(user_id, 'sum_order') + get_total
    order_count = await get_userdata(user_id, 'order_count') + 1

    await update_userdata(user_id, sum_order=sum_order)
    await update_userdata(user_id, order_count=order_count)


@router.callback_query(F.data == 'cancel')
async def cancel_sign_up_func(callback: CallbackQuery):
    await callback.answer()
    await back_to_menu_func(callback)
