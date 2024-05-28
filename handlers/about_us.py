from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from config import TOKEN
from keyboards.keyboards import about_us_kb, back_to_write_us_kb

router = Router()
bot = Bot(token=TOKEN)


@router.callback_query(F.data == 'write_us')
async def about_us_func(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    await callback.message.edit_text(
        "📍 Katip Kasım, Mahallesi, Güvenlik Cd. No:14, 34130 Fatih/İstanbul\n📞 +902124582231",
        reply_markup=await about_us_kb(user_id))


@router.callback_query(F.data == 'cafe_location')
async def cafe_location_get(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    await callback.message.delete()
    await bot.send_location(chat_id=user_id, longitude=28.955838664106412, latitude=41.006900295315035,
                            reply_markup=await back_to_write_us_kb(user_id))


@router.callback_query(F.data == 'cafe_contact1')
async def cafe_contact_get1(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    await callback.message.delete()
    await bot.send_contact(chat_id=user_id, first_name='Jizzakh', last_name='Taomlari', phone_number='+902124582231',
                           reply_markup=await back_to_write_us_kb(user_id))


@router.callback_query(F.data == 'cafe_contact2')
async def cafe_contact_get2(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    await callback.message.delete()
    await bot.send_contact(chat_id=user_id, first_name='Jizzakh', last_name='Taomlari', phone_number='+905318157707',
                           reply_markup=await back_to_write_us_kb(user_id))


@router.callback_query(F.data == 'back_to_write_us')
async def back_to_write_us_func(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    await callback.message.delete()
    await callback.message.answer(
        "📍 Katip Kasım, Mahallesi, Güvenlik Cd. No:14, 34130 Fatih/İstanbul\n📞 +902124582231",
        reply_markup=await about_us_kb(user_id))


@router.message()
async def error_message(message: Message):
    from config import TOKEN
    bot = Bot(token=TOKEN)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)