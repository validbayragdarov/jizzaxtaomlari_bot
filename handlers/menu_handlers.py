from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import ADMIN
from db.db_basket_control import db_basket_update, user_basket
from db.db_control import get_menu_data, create_basket, basket_add_count, basket_insert, basket_get, \
    basket_remove_count, \
    basket_delete_zero_count, set_db_for_admin
from keyboards.keyboards import categories_kb, in_categories_kb, chosen_item_kb
from lexicon.lexicon import text_func

router = Router()

router.message.filter(lambda x: x.from_user.id not in ADMIN)
router.callback_query.filter(lambda x: x.from_user.id not in ADMIN)


class ChosenItem(StatesGroup):
    item = State()


@router.callback_query(F.data.in_(['menu', 'back_cat_kb']))
async def menu_func(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    match callback.data:
        case 'done':
            await callback.message.delete()
            await callback.message.answer(await text_func(callback.from_user.id, 'category'),
                                          reply_markup=await categories_kb(user_id))
            return
    await callback.message.edit_text(await text_func(callback.from_user.id, 'category'),
                                     reply_markup=await categories_kb(user_id))


@router.callback_query(F.data.in_(get_menu_data()))
async def in_categories_func(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    await create_basket(user_id)
    await state.set_state(ChosenItem.item)
    await callback.message.edit_text(await text_func(user_id, 'in_category'),
                                     reply_markup=await in_categories_kb(callback.data, user_id))


@router.callback_query(ChosenItem.item, F.data.in_(get_menu_data(all_items=True)))
async def item_in_process_func(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    try:
        await basket_get(callback.from_user.id, callback.data, 'item')
    except:
        photo_id = get_menu_data(request=f"SELECT photo_id FROM menu WHERE item = '{callback.data}' ")
        await basket_insert(callback.from_user.id, item=callback.data, price=get_menu_data(price_item=callback.data),
                            photo_id=photo_id[0])
    count = await basket_get(callback.from_user.id, callback.data, 'count')
    price = await basket_get(callback.from_user.id, callback.data, 'price')

    await state.update_data(item=f"{callback.data},{count}".split(','))
    data = await state.get_data()

    item_name = await text_func(user_id, 'item_name')
    item_count = await text_func(user_id, 'count')
    item_price = await text_func(user_id, 'price')

    try:
        photo_id = await basket_get(callback.from_user.id, callback.data, 'photo_id')
        await callback.message.answer_photo(photo=photo_id,
                                            caption=f"🧺 {item_name}: {callback.data}\n"
                                                    f"💰 {item_price}: {price} tl\n"
                                                    f"🧮 {item_count}: {count}",
                                            reply_markup=await chosen_item_kb(data['item'], callback.from_user.id))
        await callback.message.delete()
    except Exception as e:
        print(e)
        await callback.message.edit_text(f"🧺 {callback.data}\n💰 {price} tl",
                                         reply_markup=await chosen_item_kb(data['item'], callback.from_user.id))


@router.callback_query(F.data == "add")
async def add_func(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        user_id = callback.from_user.id
        data = await state.get_data()
        await basket_add_count(user_id, item=data['item'])
        count = await basket_get(callback.from_user.id, data['item'][0], 'count')
        price = await basket_get(callback.from_user.id, data['item'][0], 'price')
        data['item'][1] = count
        item_name = await text_func(user_id, 'item_name')
        item_count = await text_func(user_id, 'count')
        item_price = await text_func(user_id, 'price')
        try:
            await callback.message.edit_caption(caption=f"🧺 {item_name}: {data['item'][0]}\n"
                                                        f"💰 {item_price}: {price} tl\n"
                                                        f"🧮 {item_count}: {count}",
                                                reply_markup=await chosen_item_kb(data['item'], user_id))
        except Exception as ex:
            await callback.answer(f"ERROR {ex}")
    except Exception as ex:
        await callback.answer(f"try again {ex}")


@router.callback_query(F.data == "remove")
async def add_func(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        user_id = callback.from_user.id
        data = await state.get_data()
        await basket_remove_count(user_id, item=data['item'])
        count = await basket_get(callback.from_user.id, data['item'][0], 'count')
        match count < 0:
            case True:
                await db_basket_update(user_id, count=0)
                count = 0
        price = await basket_get(callback.from_user.id, data['item'][0], 'price')
        data['item'][1] = count
        item_name = await text_func(user_id, 'item_name')
        item_count = await text_func(user_id, 'count')
        item_price = await text_func(user_id, 'price')
        try:
            await callback.message.edit_caption(caption=f"🧺 {item_name}: {data['item'][0]}\n"
                                                        f"💰 {item_price}: {price} tl\n"
                                                        f"🧮 {item_count}: {count}",
                                                reply_markup=await chosen_item_kb(data['item'], user_id))
        except Exception as ex:
            await callback.answer(f"ERROR {ex}")
    except Exception as ex:
        await callback.answer(f"try again {ex}")


@router.callback_query(lambda c: c.data.startswith('chosen_'))
async def delete_chosen_item(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    data = await state.get_data()
    data['item'][1] = 0
    await set_db_for_admin(
        f""" UPDATE "{await user_basket(user_id)}" 
             SET count = 0 
             WHERE item = '{data['item'][0]}' """)

    count = await basket_get(callback.from_user.id, data['item'][0], 'count')
    price = await basket_get(callback.from_user.id, data['item'][0], 'price')


    item_name = await text_func(user_id, 'item_name')
    item_count = await text_func(user_id, 'count')
    item_price = await text_func(user_id, 'price')

    await callback.message.edit_caption(caption=f"🧺 {item_name}: {data['item'][0]}\n"
                                                f"💰 {item_price}: {price} tl\n"
                                                f"🧮 {item_count}: {count} ",
                                        reply_markup=await chosen_item_kb(data['item'], callback.from_user.id))


@router.callback_query(F.data == 'done')
async def done_item(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await basket_delete_zero_count(callback.from_user.id)
    await state.clear()
    await menu_func(callback)
