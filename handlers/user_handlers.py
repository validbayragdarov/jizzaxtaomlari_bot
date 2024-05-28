from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import ADMIN, db
from db.db_control import insert_userdata, update_userdata
from keyboards.keyboards import language_kb, main_menu_kb, get_location, get_contact, complete_registration_kb
from lexicon.lexicon import text_func

router = Router()

router.message.filter(lambda x: x.from_user.id not in ADMIN)
router.callback_query.filter(lambda x: x.from_user.id not in ADMIN)


class SignUpUser(StatesGroup):
    name = State()
    surname = State()
    address = State()
    number = State()


def user_in_data(user_id):
    try:
        with db.cursor() as cursor:
            cursor.execute(f""" SELECT tg_id FROM user_data WHERE tg_id = {user_id} """)
            return user_id == cursor.fetchall()[0][0]
    except:
        return False


@router.message(CommandStart())
async def start_cmd(message: Message):
    print(message.chat.id)
    tg_id = message.from_user.id
    username = message.from_user.username
    if user_in_data(tg_id):
        await message.answer(await text_func(tg_id, 'main'), reply_markup=await main_menu_kb(tg_id))
    else:
        await message.answer('🇬🇧 Choose language \n🇷🇺 Выберите язык\n🇺🇿 Til tanlang\n🇹🇷 Dil seçiniz',
                             reply_markup=await language_kb())
        await insert_userdata(tg_id=tg_id, username=username)


@router.callback_query(F.data.in_(['e', 'r', 'u', 't']))
async def language_add(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    await update_userdata(user_id, lang=callback.data)
    await callback.message.delete()
    await callback.message.answer(await text_func(user_id, 'main'), reply_markup=await main_menu_kb(user_id))


@router.callback_query(F.data.in_(['back_to_menu']))
async def back_to_menu_func(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    if callback.data == 'complete_order':
        await callback.message.edit_text(await text_func(user_id, 'complete text'),
                                         reply_markup=await main_menu_kb(user_id))
        return
    await callback.message.edit_text(await text_func(user_id, 'main'), reply_markup=await main_menu_kb(user_id))


@router.callback_query(F.data == 'sign_up')
async def sign_up_func(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    await state.set_state(SignUpUser.name)
    await callback.message.edit_text(await text_func(user_id, 'register name'))


@router.message(SignUpUser.name)
async def signupname(message: Message, state: FSMContext):
    user_id = message.from_user.id
    name = message.text
    if name.isalpha() and 20 > len(name) > 2:
        await state.update_data(name=name.lower())
        await state.set_state(SignUpUser.surname)
        await message.answer(await text_func(user_id, 'register surname'))
    else:
        await state.clear()
        await state.set_state(SignUpUser.name)
        await message.answer(await text_func(user_id, 'register name'))


@router.message(SignUpUser.surname)
async def signupsurname(message: Message, state: FSMContext):
    user_id = message.from_user.id
    surname = message.text
    if surname.isalpha() and 20 > len(surname) > 2:
        await state.update_data(surname=surname.lower())
        await state.set_state(SignUpUser.address)
        await message.answer(await text_func(user_id, 'register address'), reply_markup=await get_location(user_id))
    else:
        await state.set_state(SignUpUser.surname)
        await message.answer(await text_func(user_id, 'register surname'))


@router.message(SignUpUser.address)
async def signuplocation(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text is None:

        latitude = message.location.latitude
        longitude = message.location.longitude

        await update_userdata(user_id, latitude=latitude)
        await update_userdata(user_id, longitude=longitude)
        await state.update_data(address='location')
    else:
        await state.update_data(address=message.text)

    await state.set_state(SignUpUser.number)
    await message.answer(await text_func(user_id, 'register number'), reply_markup=await get_contact(user_id))


@router.message(SignUpUser.number)
async def signupcontact(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text is None:
        number = message.contact.phone_number

    elif message.text.startswith('+') and len(message.text) > 10:
        number = message.text.strip()

    else:
        await state.set_state(SignUpUser.number)
        await message.answer(await text_func(user_id, 'register number'), reply_markup=await get_contact(user_id))
        return

    user_info = 'Info\n'
    await state.update_data(phone_number=number)
    data = await state.get_data()
    user_info += f"""👤 {data['name']} {data['surname']}
📍 {data['address']}  
📞 {data['phone_number']}
"""
    await message.answer(user_info, reply_markup=await complete_registration_kb())


@router.callback_query(F.data.in_(['yes_reg', 'no_reg']))
async def complete_registration(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id

    if callback.data == 'yes_reg':
        data = await state.get_data()
        try:
            await update_userdata(user_id, name=data['name'])
            await update_userdata(user_id, surname=data['surname'])
            await update_userdata(user_id, phone_number=data['phone_number'])
            await update_userdata(user_id, address=data['address'])
            await update_userdata(user_id, registered=1)
            await callback.message.answer(await text_func(user_id, 'after_sign_up'), reply_markup=ReplyKeyboardRemove())
        except:
            pass
    else:
        pass
    await back_to_menu_func(callback)
    await state.clear()


@router.callback_query(F.data == 'change_lang')
async def change_lang_func(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('🇬🇧 Choose language \n🇷🇺 Выберите язык\n🇺🇿 Til tanlang\n🇹🇷 Dil seçiniz',
                         reply_markup=await language_kb())



