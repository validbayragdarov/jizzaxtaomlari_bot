from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import ADMIN, TOKEN
from admin.keyboards import main_menu_kb, back_kb, newsletter_kb, users_kb, change_menu_kb, \
    change_item_menu_kb, delete_item_from_menu, change_item_kb, change_info_kb
from db.db_basket_control import show_orders
from db.db_control import get_db_for_admin, get_menu_data, set_db_for_admin, del_db_for_admin, get_item_from_menu_change
from lexicon.lexicon import text_func

router = Router()
bot = Bot(token=TOKEN)

router.message.filter(lambda message: message.from_user.id in ADMIN)
router.callback_query.filter(lambda callback: callback.from_user.id in ADMIN)


class NewsLetter(StatesGroup):
    text = State()


class FindUser(StatesGroup):
    fullname = State()


class FoodControl(StatesGroup):
    category = State()
    item = State()
    change_item = State()
    new_price = State()
    new_name = State()
    photo_id = State()
    new_photo_id = State()


class AddWorker(StatesGroup):
    worker = State()


class AddCategory(StatesGroup):
    category = State()


@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('ПРИВЕТ АДМИН', reply_markup=await main_menu_kb())


@router.callback_query(F.data == 'back')
async def back_func(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        await callback.message.edit_text('ПРИВЕТ АДМИН', reply_markup=await main_menu_kb())
    except:
        await callback.message.delete()
        await callback.message.answer('ПРИВЕТ АДМИН', reply_markup=await main_menu_kb())
    await callback.answer()


@router.callback_query(F.data == 'statistics')
async def statistics_func(callback: CallbackQuery):
    statistics = await get_db_for_admin("SELECT SUM(sum_order), SUM(order_count), COUNT(id) "
                                        "FROM user_data ")
    show_statistics = "  📊Статистика📊\n\n"
    for item in statistics:
        show_statistics += f"""💰 Сумма: {item[0]} TL
🧺 заказы: {item[1]}
👤 клиенты: {item[2]}"""
    await callback.message.edit_text(show_statistics, reply_markup=await back_kb())
    await callback.answer()


@router.callback_query(F.data == 'newsletter')
async def newsletter_func(callback: CallbackQuery, state: FSMContext):
    await state.set_state(NewsLetter.text)
    await callback.message.edit_text("Напишите текст", reply_markup=await back_kb())


@router.message(NewsLetter.text)
async def newsletter_text_func(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await message.answer(data['text'], reply_markup=await newsletter_kb())


@router.callback_query(F.data == 'send')
async def newsletter_send_func(callback: CallbackQuery, state: FSMContext):
    user_ids = await get_db_for_admin("""SELECT tg_id FROM user_data""")
    data = await state.get_data()

    active_user = []
    for user_id in user_ids:
        try:
            await bot.send_message(chat_id=user_id[0], text=data['text'])
            active_user.append(user_id[0])
        except:
            pass

    await callback.message.edit_text(f"Получили: {len(active_user)} клиентов", reply_markup=await main_menu_kb())
    await callback.answer()
    await state.clear()


@router.callback_query(F.data == 'find_user')
async def find_user_func(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FindUser.fullname)
    await callback.message.edit_text(
        "имя-фамилия для точного поиска\nимя- поик по имени\n-фамилия поиск по фамилии", reply_markup=await back_kb())
    await callback.answer()


@router.message(FindUser.fullname)
async def get_fullname_func(message: Message, state: FSMContext):
    match '-' in message.text:
        case False:
            await state.clear()
            await state.set_state(FindUser.fullname)
            await message.answer(f"""Вы забыли "-"\nПодсказка: {message.text}- """, reply_markup=await back_kb())
            return

    await state.update_data(fullname=message.text.lower().split('-'))
    data = await state.get_data()
    users = ''
    if len(data['fullname'][0]) > 0 and len(data['fullname'][1]) == 0:
        names = await get_db_for_admin(
            f"SELECT * FROM user_data WHERE name = '{data['fullname'][0]}'")
    elif len(data['fullname'][1]) > 0 and len(data['fullname'][0]) == 0:
        names = await get_db_for_admin(
            f"SELECT * FROM user_data WHERE surname = '{data['fullname'][1]}' ")
    else:
        names = await get_db_for_admin(
            f"SELECT * FROM user_data WHERE name = '{data['fullname'][0]}' AND surname = '{data['fullname'][1]}' ")

    for user in names:
        users += (f"🆔 data: [{user[0]}]\n"
                  f"👤 Имя: {user[3]}\n"
                  f"👤 Фамилия: {user[4]}\n"
                  f"☎️ Телефон: +{user[12]}\n"
                  f"🆔 Телеграм: {user[1]}\n"
                  f"#️⃣ Никнэйм: @{user[2]}\n"
                  f"🏚 Адресс: {user[5]}\n"
                  f"🧺 Заказов: {user[6]}\n"
                  f"💰 Сумма: {user[7]} tl\n"
                  f"🏁 Язык: {user[8]}\n\n")
        await message.answer(users, reply_markup=await users_kb(user[0], canc_ord=False, accpt_ord=False, pers=False))
        users = ''


@router.callback_query(lambda c: c.data.startswith('person_info '))
async def person_info(callback: CallbackQuery):
    users = ''
    names = await get_db_for_admin(
        f"SELECT * FROM user_data WHERE id = '{callback.data.split()[-1]}'")
    for user in names:
        users += (f"🆔 data: [{user[0]}]\n"
                  f"👤 Имя: {user[3]}\n"
                  f"👤 Фамилия: {user[4]}\n"
                  f"☎️ Телефон: +{user[12]}\n"
                  f"🆔 Телеграм: {user[1]}\n"
                  f"#️⃣ Никнэйм: @{user[2]}\n"
                  f"🏚 Адресс: {user[5]}\n"
                  f"🧺 Заказов: {user[6]}\n"
                  f"💰 Сумма: {user[7]} tl\n"
                  f"🏁 Язык: {user[8]}\n\n")
        await callback.message.edit_text(users, reply_markup=await users_kb(user[0], accpt_ord=False, canc_ord=False,
                                                                            pers=False))
        users = ''
    await callback.answer()


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


@router.callback_query(lambda c: c.data.startswith('order '))
async def get_orders(callback: CallbackQuery):
    data_id = callback.data.split()[-1]
    user_id = await get_db_for_admin(f"SELECT tg_id FROM user_data WHERE id = {data_id}")
    count = await get_db_for_admin(f'SELECT order_count FROM user_data WHERE id = {data_id}')
    try:
        await callback.message.edit_text(await show_orders(user_id[0][0], count[0][0]),
                                         reply_markup=await users_kb(data_id, ords=False, canc_ord=False,
                                                                     accpt_ord=False))
        await callback.answer()
    except:
        await callback.answer('Попробуйте заново')


@router.callback_query(lambda c: c.data == 'menu')
async def menu_settgings_func(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FoodControl.category)
    await callback.message.edit_text('Выберите категорию', reply_markup=await change_menu_kb())
    await callback.answer()


@router.callback_query(lambda c: c.data == 'add_category')
async def add_category_func(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddCategory.category)
    await callback.message.edit_text('Напишите название категории', reply_markup=await back_kb())
    await callback.answer()


@router.message(AddCategory.category)
async def set_new_category_func(message: Message, state: FSMContext):
    await set_db_for_admin(f""" INSERT INTO menu (category) VALUES ('{message.text}') """)
    await state.clear()
    await message.answer(f"Новая категория {message.text} добавлена ", reply_markup=await change_menu_kb())


@router.callback_query(lambda c: c.data in get_menu_data(), FoodControl.category)
async def item_settings_func(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data)
    menu = await get_db_for_admin(f""" SELECT item,price,category FROM menu WHERE category = '{callback.data}' """)
    show_menu = """название | цена | категория
-----------------------------"""
    for info in menu:
        show_menu += f"""
{info[0]} | {info[1]} TL | {info[2]}
"""

    await callback.message.edit_text(f'{show_menu}\nЧто будем делать?',
                                     reply_markup=await change_item_menu_kb())
    await callback.answer()


@router.callback_query(F.data == 'add')
async def add_food_menu(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FoodControl.item)
    await callback.message.answer("""Напишите название-цену
    сомса-150""", reply_markup=await back_kb())
    await callback.answer()


@router.message(FoodControl.item)
async def adding_food(message: Message, state: FSMContext):
    await state.update_data(item=message.text.split('-'))
    await state.set_state(FoodControl.photo_id)

    data = await state.get_data()

    if len(data['item']) != 2:
        await state.set_state(FoodControl.item)
        await message.answer("""‼️ОШИБКА‼️
    Напишите НАЗВАНИЕ-ЦЕНУ
    сомса-150-hot""", reply_markup=await back_kb())
        return

    await message.answer("Отправьте фото еды", reply_markup=await back_kb())


@router.message(FoodControl.photo_id, F.photo)
async def adding_photo(message: Message, state: FSMContext):
    await state.update_data(photo_id=message.photo[-1].file_id)
    data = await state.get_data()

    await set_db_for_admin(f""" INSERT INTO menu (item, price, category, photo_id)
                                VALUES ('{data['item'][0]}', {data['item'][1]}, '{data['category']}', '{data['photo_id']}')""")
    await message.answer_photo(photo=data['photo_id'],
                               caption=f"✅ Добавлено ✅\n[{data['item'][0]} | {data['item'][1]} tl | {data['category']}]\n\n"
                                       f"Добавьте еще 👇\n'Назад' для выхода", reply_markup=await back_kb())
    await state.set_state(FoodControl.item)


@router.callback_query(F.data == 'remove')
async def remove_item_menu(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text("Выберите блюдо", reply_markup=await delete_item_from_menu(data['category']))
    await callback.answer()


@router.callback_query(F.data.in_(get_menu_data(all_items=True)))
async def delete_item_from_menu_func(callback: CallbackQuery):
    item = await get_db_for_admin(f""" SELECT item FROM menu WHERE item = '{callback.data}' """)
    await del_db_for_admin(f""" DELETE FROM menu WHERE item = '{callback.data}' """)
    await callback.message.edit_text(f"✅ {item[0]} Удалено", reply_markup=await main_menu_kb())
    await callback.answer()


@router.callback_query(F.data == 'change')
async def change_item_info(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(FoodControl.change_item)
    await callback.message.edit_text("Выберите блюдо", reply_markup=await change_item_kb(data['category']))
    await callback.answer()


@router.callback_query(FoodControl.change_item, F.data.in_(get_item_from_menu_change()))
async def change_item_info_process(callback: CallbackQuery, state: FSMContext):
    await state.update_data(change_item=callback.data[1:])
    data = await state.get_data()
    try:
        item = await get_db_for_admin(
            f""" SELECT item,price,category,photo_id FROM menu WHERE item = '{data['change_item']}' """)
        name = item[0][0]
        price = item[0][1]
        category = item[0][2]
        photo_id = item[0][3]
        await callback.message.answer_photo(photo=photo_id, caption=f"{name} {price}tl {category}\nЧто будем менять ?",
                                            reply_markup=await change_info_kb())
        await callback.message.delete()
    except:
        item = await get_db_for_admin(
            f""" SELECT item,price,category FROM menu WHERE item = '{data['change_item']}' """)
        name = item[0][0]
        price = item[0][1]
        category = item[0][2]
        await callback.message.edit_text(f"🖼 Нет фото\n{name} {price}tl {category}\nЧто будем менять ?",
                                         reply_markup=await change_info_kb())
    await callback.answer()


@router.callback_query(F.data.in_(['name', 'price', 'photo']))
async def change_name(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'name':
        await state.set_state(FoodControl.new_name)
    elif callback.data == 'price':
        await state.set_state(FoodControl.new_price)
    elif callback.data == 'photo':
        await state.set_state(FoodControl.new_photo_id)
    await callback.message.answer('Отправьте новое значение', reply_markup=await back_kb())
    await callback.answer()


@router.message(FoodControl.new_name)
async def set_new_foodname(message: Message, state: FSMContext):
    new_name = message.text
    data = await state.get_data()
    await set_db_for_admin(f""" UPDATE menu
                                SET item = '{new_name}' WHERE item = '{data['change_item']}' """)
    item = await get_db_for_admin(f""" SELECT item,price,category FROM menu WHERE item = '{new_name}'""")
    name = item[0][0]
    price = item[0][1]
    category = item[0][2]
    await message.answer(f"✅ Готово ✅ \n{name} {price}tl {category}",
                         reply_markup=await main_menu_kb())
    await state.clear()


@router.message(FoodControl.new_price)
async def set_new_foodname(message: Message, state: FSMContext):
    new_price = message.text
    data = await state.get_data()
    await set_db_for_admin(f""" UPDATE menu
                                SET price = {new_price} WHERE item = '{data['change_item']}' """)
    item = await get_db_for_admin(f""" SELECT item,price,category FROM menu WHERE item = '{data['change_item']}'""")
    name = item[0][0]
    price = item[0][1]
    category = item[0][2]
    await message.answer(f"✅ Готово ✅ \n{name} {price}tl {category}",
                         reply_markup=await main_menu_kb())
    await state.clear()


@router.message(FoodControl.new_photo_id, F.photo)
async def set_new_foodname(message: Message, state: FSMContext):
    new_photo_id = message.photo[-1].file_id
    data = await state.get_data()
    await set_db_for_admin(f""" UPDATE menu
                                SET photo_id = '{new_photo_id}' WHERE item = '{data['change_item']}' """)
    item = await get_db_for_admin(f""" SELECT item,price,category FROM menu WHERE item = '{data['change_item']}'""")
    name = item[0][0]
    price = item[0][1]
    category = item[0][2]
    await message.answer_photo(photo=new_photo_id, caption=f"✅ Готово ✅ \n{name} {price}tl {category}",
                               reply_markup=await back_kb())
    await state.clear()


@router.callback_query(F.data == 'add_admin')
async def add_worker_func(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddWorker.worker)
    await callback.message.edit_text('Отправьте ID пользователя', reply_markup=await back_kb())


@router.message(AddWorker.worker)
async def adding_new_worker(message: Message, state: FSMContext):
    if message.text.isdigit():
        await set_db_for_admin(f"INSERT INTO workers (id) VALUES ({message.text})")
        await message.answer('✅Готово✅', reply_markup=await back_kb())
    else:
        await message.answer('Неправильно, отправьте айди', reply_markup=await back_kb())



@router.message()
async def trash_message(message: Message):
    await message.delete()
