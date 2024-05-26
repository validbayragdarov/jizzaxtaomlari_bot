from config import db
from db.db_control import get_userdata
from lexicon.lexicon import text_func


async def user_basket(user_id) -> str:
    """
    Возвращает название корзинки-таблицы пользователя
    :param user_id: телеграм айди
    :return: str
    """
    or_co = await get_userdata(user_id, 'order_count')
    return f"{user_id}_{or_co}"


async def db_basket_get(user_id, *args) -> str:
    """
    Возвращает информацию о корзинке пользователя
    :param user_id: телеграм айди
    :param args: столбцы
    :return: str
    """
    columns = ''
    for column in args:
        columns += f"{column},"
    with db.cursor() as cursor:
        cursor.execute(f""" SELECT {columns[:-1]}, price*count FROM "{await user_basket(user_id)}" """)
        res = cursor.fetchall()
        match len(res):
            case 0:
                return await text_func(user_id, 'empty_basket')
            case _:
                total = cursor.execute(f""" SELECT SUM(price*count) FROM "{await user_basket(user_id)}" """)
                if res[0][3] is None:
                    basket = f"----------------------------\n"
                else:
                    basket = f"🕓 {res[0][3]}\n----------------------------\n"
                for info in res:
                    basket += f"{info[0]} | {info[1]} tl | {info[2]} | = {info[4]} tl\n"
                basket += f"----------------------------\ntotal = {total.fetchall()[0][0]} tl"
                return basket


async def db_basket_update(user_id, **kwargs):
    columns = ''
    values = ''
    for column, value in kwargs.items():
        columns += f"{column},"
        if isinstance(value, str):
            values += f"'{value}',"
        else:
            values += f"{value},"

    with db.cursor() as cursor:
        cursor.execute(f""" UPDATE "{await user_basket(user_id)}"
                                SET {columns[:-1]} = {values[:-1]}""")


async def db_basket_clear(user_id):
    with db.cursor() as cursor:
        cursor.execute(f""" DELETE FROM "{await user_basket(user_id)}" """)


async def db_basket_get_items(user_id, item):
    with db.cursor() as cursor:
        cursor.execute(f""" SELECT {item} FROM "{await user_basket(user_id)}" """)
        return cursor.fetchall()


async def show_orders(user_id, order_count):
    show_order = ''
    with db.cursor() as cursor:
        for count in range(order_count):

            time = cursor.execute(f""" SELECT time from "{user_id}_{count}" LIMIT 1""").fetchall()[0][0]
            show_order += f"""------------------------
ДАТА -- {time} --
------------------------\n"""
            order = cursor.execute(f""" SELECT id, item, price, count FROM "{user_id}_{count}" """)

            for info in order.fetchall():
                show_order += f""" {info[0]} | {info[1]} | {info[2]} tl | {info[3]} \n"""

            total = cursor.execute(f""" SELECT SUM(price*count) FROM "{user_id}_{count}" """).fetchall()
            show_order += f"Итоговая сумма = {total[0][0]}\n\n"

        return show_order
