import datetime
from datetime import timedelta

from yoomoney import Quickpay
from yoomoney import Client

import src.core.users as u
from src.core.config import WALLET_TOKEN, SUBSCRIPTION_PRICE


async def get_account_number():
    client = Client(WALLET_TOKEN)
    user = client.account_info()
    return user.account


async def create_payment_link(telegram_user_id):
    quickpay = Quickpay(
        receiver=await get_account_number(),
        quickpay_form="shop",
        targets="Sponsor this project",
        paymentType="SB",
        sum=int(SUBSCRIPTION_PRICE),
        label=telegram_user_id
    )
    return quickpay.redirected_url


async def chech_payment_status(telegram_user_id):
    # Проверяет статус подписки по последнему платежу
    user_info = await u.get_user_attrs(telegram_user_id)
    vpn_active = user_info['vpn_active']
    last_payment = user_info['last_payment']

    # Рассматриваем только отключенных
    if not vpn_active:

        # Получаем историю поступлений от клиента
        client = Client(WALLET_TOKEN)
        history = client.operation_history(label=telegram_user_id)

        # Получаем самую последнюю оплату
        for operation in history.operations:
            if operation.status == 'success':
                last_payment = operation.datetime
                if last_payment < operation.datetime:
                    last_payment = operation.datetime

        # Получаем день окончания подписки
        subscribe_to = (last_payment + timedelta(days=31)).replace(hour=0, minute=0, second=0)

        # Если это позже, чем сегодня, то меняем vpn_active на True
        if subscribe_to >= datetime.datetime.today():
            vpn_active = True

        # Обновляем данные в базе
        new_attrs = {'last_payment': last_payment, 'vpn_active': vpn_active, 'subscribe_to': subscribe_to}
        await u.set_user_attrs(telegram_user_id=telegram_user_id, attrs=new_attrs)

    return subscribe_to, vpn_active
