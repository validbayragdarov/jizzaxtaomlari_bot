from config import db


async def text_func(user_id, text):
    with db.cursor() as cursor:
        cursor.execute(f""" SELECT lang FROM user_data WHERE tg_id = {user_id} """)
        l = cursor.fetchall()[0][0]
    lang = {
        't': {
            'main': 'Hoşgeldin',
            'category': 'Ne istiyorsun?',
            'in_category': 'Aşağıdan birini seçin',
            'need_sign_up': 'Siparişi tamamlamak için kayıt olmanız gerekmektedir.',
            'complete text': 'Siparişiniz kabul edildi\nLütfen yanıt bekleyin',
            'precomplete_order': '‼️Siparişi kontrol ettim ve yerine getirmek istiyorum‼️',
            'register name': "1/4 Adınızı yazın\nisim yalnızca bir dize olmalıdır",
            'register surname': '2/4 Şimdi soyadınızı yazın\nsoyadınız yalnızca bir dize olmalıdır',
            'register address': '3/4 Tam gönderim adresinizi girin\nYada aşağıdaki düğmeye tıklayın',
            'register number': "4/4 Telgram/whatsapp numaranızı gönderin\nMesela +90 *** *** ** **\nYada aşağıdaki "
                               "düğmeye tıklayın",
            'empty_basket': 'Kafa Sepeti',
            'order_canceled': 'Siparişiniz iptal edildi. Sorularınız varsa bize yazın.',
            'order_accepted': 'Siparişiniz alınmıştır, lütfen kuryemizi bekleyin',
            'after_sign_up': 'Şimdi siparişinizi tamamlayabilirsiniz',
            'item_name': 'Yiyecek',
            'price': 'Fiyat',
            'count': 'Adet',
            'new_address_write': 'Yeni adresinizi yaziniz yada konum gonderiniz',

            'menu_kb': '🍽 Menü',
            'basket_kb': '🧺 Sepet',
            'write_us_kb': '📲 İletişim',
            'done_kb': ' ✅ Hazır',
            'change_kb': '🔄 Feğiştir',
            'clear_kb': '🧹 Temizle',
            'complete_kb': '✅ Bitir',
            'back_cat_kb': '⬅️ Geri',
            'back_to_menu_kb': '⬅️ Geri',
            'back_basket_kb': '⬅️ Geri',
            'sign_up_kb': '✍️ Kayıt ol',
            'cancel_kb': '🚫 Iptal',
            'cancel_order_kb': '🚫 Iptal',
            'location_kb': '📍 Konum',
            'contact_kb': '📞 Numara',
            'change_lang_kb': '🏳️ Dil',
            'payment_cash_kb': '💵 Nakit',
            'payment_card_kb': '💳 Banka kart',
            'add_new_address_kb': 'Yeni adres ekle'

        },
        'e': {
            'main': 'Welcome to main menu',
            'category': 'Choose the category',
            'in_category': 'Choose one below',
            'need_sign_up': 'To complete the order you need to sign up',
            'precomplete_order': '‼️ I`m checked my order and want to complete it ‼️',
            'complete text': 'We got your order\nOur support will contact you',
            'register name': '1/4 First write your name\nname should be only string',
            'register surname': '2/4 Then write your surname\nsurname should be only string',
            'register address': '3/4 Write your full adress or push the button below',
            'register number': '4/4 Send your telegram/whatsapp number\nExample +90 *** *** ** **\nOr push the button below',
            'empty_basket': 'Empty basket',
            'order_canceled': 'Your order was canceled, if you have any questions please write us',
            'order_accepted': 'Your order is accepted, wait our courier to contact you',
            'after_sign_up': 'You can now complete the order',
            'new_address_write': 'Write new address or send location',

            'menu_kb': '🍽 Menu',
            'basket_kb': '🧺 Basket',
            'write_us_kb': '📲 Write us',
            'done_kb': '✅ Done',
            'change_kb': '🔄 Change',
            'clear_kb': '🧹 Clear',
            'complete_kb': '✅ Complete',
            'back_cat_kb': '⬅️ Back',
            'back_to_menu_kb': '⬅️ Back',
            'back_basket_kb': '⬅️ Back',
            'sign_up_kb': '✍️ Sign up',
            'cancel_kb': '🚫 Skip',
            'cancel_order_kb': '🚫 Cancel',
            'contact_kb': '📞 Number',
            'location_kb': '📍 Location',
            'change_lang_kb': '🏳️ Language',
            'payment_cash_kb': '💵 Cash',
            'payment_card_kb': '💳 Bank card',
            'item_name': 'Food',
            'price': 'Price',
            'count': 'Amount',
            'add_new_address_kb': 'New address'

        },

        'r': {
            'main': 'Добро пожаловать в главное меню',
            'category': 'Выберите категорию',
            'in_category': 'Выберите одну ниже',
            'need_sign_up': 'Чтобы завершить заказ вы должны пройти регистрацию',
            'complete text': 'Ваш заказ был получен\nОжидайте ответа',
            'precomplete_order': '‼️ Я проверил заказ и хочу его завершить ‼️',
            'register name': '1/4 Начнем с имени, как вас зовут ?',
            'register surname': '2/4 Теперь фамилия',
            'register address': '3/4 Напишите полный адрес доставки или нажмите на кнопку ниже',
            'register number': '4/4 Отправьте свой telegram/whatsapp номер\nПример +90 *** *** ** **\nИли нажмите на кнопку ниже',
            'empty_basket': 'Пустая корзинка',
            'order_canceled': 'Ваш заказ был отменен, пожалуйста напишите нам если у вас возникли вопросы',
            'order_accepted': 'Ваш заказ был принят, ожидайте нашего курьера',
            'after_sign_up': 'Теперь вы можете завершить заказ',
            'new_address_write': 'Напишите новый адресс или отправьте локацию',

            'menu_kb': '🍽 Меню',
            'basket_kb': '🧺 Корзина',
            'done_kb': '✅ Готово',
            'write_us_kb': '📲 Связаться',
            'change_kb': '🔄 Изменить',
            'clear_kb': '🧹 Очистить',
            'complete_kb': '✅ Завершить',
            'back_cat_kb': '⬅️ Назад',
            'back_to_menu_kb': '⬅️ Назад',
            'back_basket_kb': '⬅️ Назад',
            'sign_up_kb': '✍️ Регистрация',
            'cancel_kb': '🚫 Отмена',
            'cancel_order_kb': '🚫 Отменить',
            'contact_kb': '📞 Номер',
            'location_kb': '📍 Локация',
            'change_lang_kb': '🏳️ Язык',
            'payment_cash_kb': '💵 Наличка',
            'payment_card_kb': '💳 Картой',
            'item_name': 'Блюдо',
            'price': 'Цена',
            'count': 'Кол-во',
            'add_new_address_kb': 'Новый адресс'

        },

        'u': {
            'main': 'Menuga xush kelibsiz',
            'category': 'Nima xohlaysiz?',
            'in_category': 'Pastan bittasini tanlang',
            'need_sign_up': 'Buyurtmani bajarish uchun ro`yxatdan o`tishingiz kerak.',
            'complete text': 'Buyurtmangiz qabul qilindi\nJavobni kuting',
            'precomplete_order': '‼️ Buyurtmani tekshirib chiqdim va uni bajarmoqchiman ‼️',
            'register name': "1/4 Birinchi ismingizni yozing\nism faqat satr bo'lishi kerak",
            'register surname': '2/4 Endi esa familyangizni yozing\nfamiliya faqat satr bo`lishi kerak',
            'register address': '3/4 To`liq yetkazib berish manzilingizni yozing yoki pastdagi tugmani bosing',
            'register number': '4/4 Telegram/whatsapp raqamingizni yuboring\nMisol +90 *** *** ** **\nYoki pasdagi tugmani bosing',
            'empty_basket': 'Bosh savatcha',
            'order_canceled': 'Buyurtmangiz bekor qilindi. Savollaringiz bo`lsa, bizga yozing.',
            'order_accepted': 'Buyurtmangiz qabul qilindi, iltimos bizning kurerimizni kuting',
            'after_sign_up': 'Endi siz buyurtmani bajarishingiz mumkin',
            'new_address_write': 'Yangi adresni yozing yoki lokatsiyani jonating',

            'menu_kb': '🍽 Menu',
            'basket_kb': '🧺 Savatcha',
            'write_us_kb': '📲 Aloqa',
            'done_kb': '✅ Tayor',
            'change_kb': '🔄 Almashtirmoq',
            'clear_kb': '🧹 Tozalash',
            'complete_kb': '✅ Bitirish',
            'back_cat_kb': '⬅️ Orqaga',
            'back_to_menu_kb': '⬅️ Orqaga',
            'back_basket_kb': '⬅️ Orqaga',
            'sign_up_kb': '✍️ Ro`yxatga olish',
            'cancel_kb': '🚫 Bekor qilish',
            'cancel_order_kb': '🚫 Bekor qilish',
            'location_kb': '📍 Locatsiya',
            'contact_kb': '📞 Nomer',
            'change_lang_kb': '🏳️ Til',
            'payment_cash_kb': '💵 Naqd',
            'payment_card_kb': '💳 Bank karta',
            'item_name': 'Ismi',
            'price': 'Narx',
            'count': 'Miqdori',
            'add_new_address_kb': 'Yangi adres'

        }}
    return lang[l][text]
