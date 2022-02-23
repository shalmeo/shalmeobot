from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


def starting_kb():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔗 Подписаться', callback_data='sub_to_channel', url='https://t.me/shalmeoChannel'), 
         InlineKeyboardButton(text='✏️ Ввести код', callback_data='enter_referal')],
        [InlineKeyboardButton(text='✅ Проверить доступ', callback_data='check_allow')]
    ])
    
    return keyboard


def info_kb(user_email):
    text = '📧 Изменить почту' if user_email else '📧 Привязать почту'
    keyboard=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data='bind_email')],
        [InlineKeyboardButton(text='Закрыть', callback_data='close_info')]
    ])
    
    return keyboard


buy_cb = CallbackData('buy', 'action')
def buy_kb():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='💳 Купить товар', callback_data=buy_cb.new('buy_item'))],
        [InlineKeyboardButton(text='📍 Оплатить по баллам', callback_data=buy_cb.new('buy_with_points'))],
        [InlineKeyboardButton(text='🛒 Каталог', switch_inline_query_current_chat='')]
    ])
    
    return keyboard


confirmation_cb = CallbackData('confirmation', 'action')
def confirmation_kb(action):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Все верно!', callback_data=confirmation_cb.new(action))],
        [InlineKeyboardButton(text='⬅️ Назад', callback_data=confirmation_cb.new('cancel'))]
    ])
    
    return keyboard


def check_paid():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🛍 Проверить оплату', callback_data=confirmation_cb.new('check_paid'))],
        [InlineKeyboardButton(text='⬅️ Назад', callback_data=confirmation_cb.new('cancel'))]
    ])
    
    return keyboard


def successful_payment_kb():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🏠 Профиль', callback_data=confirmation_cb.new('to_profile'))],
        [InlineKeyboardButton(text='🛒 Каталог', switch_inline_query_current_chat='')],
    ])
    
    return keyboard


item_cb = CallbackData('item', 'action')


def del_item_kb():
    keyboard= InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🗑 Удалить товар', callback_data=item_cb.new('del'))],
        [InlineKeyboardButton(text='🛒 Каталог', switch_inline_query_current_chat='')]
    ])
    
    return keyboard
