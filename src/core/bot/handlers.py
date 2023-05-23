import os

from telegram.constants import ParseMode
from telegram import (
    Update, InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import CallbackContext

from src.core import users as u
from src.core.payment import payment as p


async def start_handle(update: Update, context: CallbackContext):
    telegram_user_id = update.message.from_user.id
    text = f'Привет, {update.effective_user.first_name}!'
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)

    if not await u.user_is_registered(telegram_user_id):
        await u.register_user(telegram_user_id=str(update.effective_user.id),
                              username=str(update.effective_user.username),
                              first_name=str(update.effective_user.first_name),
                              last_name=str(update.effective_user.last_name))

    text, reply_markup = await get_general_menu()
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def show_general_menu_handle(update: Update, context: CallbackContext):
    text, reply_markup = await get_general_menu()
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def general_menu_callback_handle(update: Update, context: CallbackContext):
    query = update.callback_query

    if query.data == 'show_general_menu_handle':
        text, reply_markup = await get_general_menu()
    elif query.data == 'show_profile':
        text, reply_markup = await get_profile(update.effective_user.id)
    elif query.data == 'get_vpn_settings':
        text, reply_markup = await get_vpn_settings(update.effective_user.id)
    elif query.data == 'check_payment':
        text, reply_markup = await get_payment_info(update.effective_user.id)
    elif query.data == 'create_payment_link':
        text, reply_markup = await get_payment_link(update.effective_user.id)

    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def get_general_menu():
    text = 'Основное меню'

    # Кнопки
    keyboard = []
    keyboard.append([InlineKeyboardButton('✅ Подписка VPN', callback_data='show_profile')])
    keyboard.append([InlineKeyboardButton('❓ Помощь', callback_data='help')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    return text, reply_markup


async def get_profile(telegram_user_id):
    user = await u.get_user_attrs(telegram_user_id)
    keyboard = []

    if user['vpn_active'] in [None, False]:
        vpn_active = 'Не активна'
        keyboard.append([InlineKeyboardButton(text='🪙 Оплатить подписку',
                                              callback_data='create_payment_link')])
        keyboard.append([InlineKeyboardButton('🔄 Проверить оплату', callback_data="check_payment")])
    else:
        vpn_active = f"Активна до {user['subscribe_to']}"
        keyboard.append([InlineKeyboardButton('⚙️ Получить настройки', callback_data='get_vpn_settings')])

    text = f"Статус подписки: {vpn_active}\nЦена подписки на 30 дней: {os.getenv('SUBSCRIPTION_PRICE')}₽"

    keyboard.append([InlineKeyboardButton('⏪️', callback_data="show_general_menu_handle")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    return text, reply_markup


async def get_vpn_settings(telegram_user_id):
    text = 'Вот тут будут настройки для WireGuard'
    keyboard = [[InlineKeyboardButton('⏪️', callback_data="show_profile")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return text, reply_markup


async def get_payment_info(telegram_user_id):
    await p.chech_payment_status(telegram_user_id)

    text = 'АБВГД'
    keyboard = [[InlineKeyboardButton('⏪️', callback_data="show_profile")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return text, reply_markup


async def get_payment_link(telegram_user_id):
    link = await p.create_payment_link(telegram_user_id)
    text = f'После оплаты нажмите на кнопку "🔄 Проверить оплату"'

    keyboard = []
    keyboard.append([InlineKeyboardButton('🌐 Ссылка для оплаты', url=link)])
    keyboard.append([InlineKeyboardButton('🔄 Проверить оплату', callback_data="check_payment")])
    keyboard.append([InlineKeyboardButton('⏪️', callback_data="show_profile")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return text, reply_markup
