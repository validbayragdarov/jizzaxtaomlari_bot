from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from admin.keyboards import users_kb
from config import ADMIN, WORKERS, TOKEN
from db.db_control import get_db_for_admin
from lexicon.lexicon import text_func

router = Router()
bot = Bot(token=TOKEN)

router.message.filter(lambda message: message.from_user.id in ADMIN + WORKERS)
router.callback_query.filter(lambda callback: callback.from_user.id in ADMIN + WORKERS)



@router.callback_query(lambda c: c.data.startswith('cancel_order '))
async def cancel_order_func(callback: CallbackQuery):
    user_id = await get_db_for_admin(f""" SELECT tg_id FROM user_data WHERE id = {callback.data.split()[-1]} """)
    data_id = callback.data.split()[-1]
    await bot.send_message(chat_id=user_id[0][0], text=await text_func(user_id[0][0], 'order_canceled'))
    await callback.message.edit_text(callback.message.text + "\n❌ЗАКАЗ ОТМЕНЁН❌",
                                     reply_markup=await users_kb(data_id, canc_ord=False, pers=False, ords=False))
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith('accept_order '))
async def accept_order_func(callback: CallbackQuery):
    user_id = await get_db_for_admin(f""" SELECT tg_id FROM user_data WHERE id = {callback.data.split()[-1]} """)
    data_id = callback.data.split()[-1]
    await bot.send_message(chat_id=user_id[0][0], text=await text_func(user_id[0][0], 'order_accepted'))
    await callback.message.edit_text(callback.message.text + "\n✅ЗАКАЗ ПРИНЯТ✅",
                                     reply_markup=await users_kb(data_id, accpt_ord=False, pers=False, ords=False))
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith('contact '))
async def get_contact_func(callback: CallbackQuery):
    try:
        contact = await get_db_for_admin(
            f"SELECT name, surname, phone_number FROM user_data WHERE id={callback.data.split()[-1]}")
        await bot.send_contact(chat_id=callback.from_user.id, first_name=contact[0][0], last_name=contact[0][1],
                               phone_number=str(contact[0][2]))
    except:
        await bot.send_message(chat_id=callback.from_user.id, text='🚫 Нет телеграм номера')

    await callback.answer()


@router.callback_query(lambda c: c.data.startswith('location '))
async def get_location_func(callback: CallbackQuery):
    try:
        user_id = int(callback.data.split()[1])
        location = await get_db_for_admin(f"SELECT latitude, longitude FROM user_data WHERE id= {user_id} ")
        await bot.send_location(chat_id=callback.from_user.id, latitude=location[0][0],
                                longitude=location[0][1])
    except:
        await bot.send_message(chat_id=callback.from_user.id, text='🚫 Локации нету')
    await callback.answer()
