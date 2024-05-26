import psycopg

from config import db


def create_userdata():
    with db.cursor() as cursor:
        cursor.execute(""" CREATE TABLE IF NOT EXISTS user_data (
        id SERIAL PRIMARY KEY,
        tg_id BIGINT,
        username TEXT,
        name TEXT,
        surname TEXT,
        address TEXT,
        order_count INTEGER DEFAULT 0,
        sum_order BIGINT DEFAULT 0,
        lang TEXT DEFAULT 0,
        registered TEXT DEFAULT 0,
        longitude REAL,
        latitude REAL,
        phone_number BIGINT
        ) """)


def create_menu():
    with db.cursor() as cursor:
        cursor.execute(""" CREATE TABLE IF NOT EXISTS menu (
            id SERIAL PRIMARY KEY,
            item TEXT,
            price BIGINT,
            category TEXT,
            photo_id TEXT
            ) """)


def create_workers():
    with db.cursor() as cursor:
        cursor.execute(""" CREATE TABLE IF NOT EXISTS workers (
            id BIGINT) """)


async def create_basket(user_id):
    with db.cursor() as cursor:
        count = await get_userdata(user_id, 'order_count')
        cursor.execute(f""" CREATE TABLE IF NOT EXISTS "{user_id}_{count}" (
            id SERIAL PRIMARY KEY,
            item TEXT,
            price BIGINT,
            count INTEGER DEFAULT 0,
            time TEXT,
            photo_id TEXT
            ) """)


async def insert_userdata(**kwargs):
    columns = ''
    values = ''
    for column, value in kwargs.items():
        columns += f"{column},"
        values += f"'{value}',"

    with db.cursor() as cursor:
        cursor.execute(f""" INSERT INTO user_data ({columns[:-1]}) VALUES ({values[:-1]})""")


async def get_userdata(user_id, *args):
    columns = ''
    for column in args:
        columns += f"{column},"
    try:
        with db.cursor() as cursor:
            cursor.execute(f""" SELECT {columns[:-1]} FROM user_data WHERE tg_id = {user_id} """)
            return cursor.fetchall()[0][0]
    except Exception as ex:
        print(ex)


async def get_db_for_admin(request):
    with db.cursor() as cursor:
        cursor.execute(f""" {request} """)
        result = cursor.fetchall()
        return result


async def set_db_for_admin(request):
    with db.cursor() as cursor:
        cursor.execute(f""" {request} """)


async def del_db_for_admin(request):
    with db.cursor() as cursor:
        cursor.execute(f""" {request} """)


async def get_all_userdata(user_id, *args):
    columns = ''
    for column in args:
        columns += f"{column},"
    try:
        with db.cursor() as cursor:
            cursor.execute(f""" SELECT {columns[:-1]} FROM user_data WHERE tg_id = {user_id} """)
            res = cursor.fetchall()[0]
            show = f"""🔔НОВЫЙ ЗАКАЗ🔔
 🧍‍♂️ {res[0]} - {res[1]}
----------------------------
 📍 адрес: {res[2]}
 📞 номер: +{res[5]}
 👤 юзернейм: @{res[3]}
 🆔 айди: [{res[4]}]
----------------------------
"""
            return show
    except Exception as ex:
        print(ex)


async def update_userdata(user_id, **kwargs):
    columns = ''
    values = ''
    for column, value in kwargs.items():
        columns += f"{column},"
        if isinstance(value, str):
            values += f"'{value}',"
        else:
            values += f"{value},"

    with db.cursor() as cursor:
        cursor.execute(f""" UPDATE user_data
                            SET {columns[:-1]} = {values[:-1]} WHERE tg_id = {user_id}""")


def get_menu_data(cat=None, all_items=False, price_item=None, request=None) -> list:
    items = []
    item_price = {}
    with db.cursor() as cursor:
        if all_items is True:
            cursor.execute(f""" SELECT item FROM menu """)
            for item in cursor.fetchall():
                items.append(item[0])
            return items
        elif request is not None:
            cursor.execute(request)
            for item in cursor.fetchall():
                items.append(item[0])
            return items
        elif cat is not None:
            cursor.execute(f""" SELECT item, price FROM menu WHERE category = '{cat}' """)
            res = cursor.fetchall()
            for item in res:
                items.append(item[0])
            for item in res:
                item_price[item[0]] = item[1]
            return [items, item_price]
        elif price_item is not None:
            cursor.execute(f""" SELECT price FROM menu WHERE item = '{price_item}' """)
            return cursor.fetchall()[0][0]
        else:
            cursor.execute(f""" SELECT category FROM menu GROUP BY category """)
            for item in cursor.fetchall():
                items.append(item[0])
            return items


def get_item_from_menu_change(cat=None):
    buttons = []
    with db.cursor() as cursor:
        if cat is not None:
            cursor.execute(f""" SELECT item FROM menu WHERE category = '{cat}' """)
            result = cursor.fetchall()
            for item in result:
                buttons.append(f"c{item[0]}")
            return buttons
        else:
            cursor.execute(f""" SELECT item FROM menu""")
            result = cursor.fetchall()
            for item in result:
                buttons.append(f"c{item[0]}")
            return buttons


async def basket_add_count(user_id, item):
    with db.cursor() as cursor:
        count = await get_userdata(user_id, 'order_count')
        cursor.execute(f""" UPDATE "{user_id}_{count}"
                                SET count = count + 1 WHERE item = '{item[0]}' """)


async def basket_remove_count(user_id, item):
    with db.cursor() as cursor:
        count = await get_userdata(user_id, 'order_count')
        cursor.execute(f""" UPDATE "{user_id}_{count}"
                                SET count = count - 1 WHERE item = '{item[0]}' """)


async def basket_insert(user_id, **kwargs):
    columns = ''
    values = ''
    for column, value in kwargs.items():
        columns += f"{column},"
        values += f"'{value}',"

    with db.cursor() as cursor:
        count = await get_userdata(user_id, 'order_count')
        cursor.execute(f""" INSERT INTO "{user_id}_{count}" ({columns[:-1]}) VALUES({values[:-1]}) """)


async def basket_get(user_id, item, *args):
    columns = ''
    for column in args:
        columns += f"{column},"

    with db.cursor() as cursor:
        count = await get_userdata(user_id, 'order_count')
        cursor.execute(f""" SELECT {columns[:-1]} FROM "{user_id}_{count}" WHERE item = '{item}' """)
        return cursor.fetchall()[0][0]


async def basket_delete_zero_count(user_id):
    with db.cursor() as cursor:
        count = await get_userdata(user_id, 'order_count')
        cursor.execute(f"""DELETE FROM "{user_id}_{count}" WHERE count=0""")




