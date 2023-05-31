from datetime import datetime, date, timedelta

from yoomoney import Client
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

    if not vpn_active:
        client = Client(WALLET_TOKEN)
        history = client.operation_history(label=telegram_user_id)

        latest_payment = None
        for operation in history.operations:
            if operation.status == 'success':
                latest_payment = operation.datetime
                if latest_payment < operation.datetime:
                    latest_payment = operation.datetime

        attrs = {'last_payment': latest_payment,
                 'vpn_active': True,
                 'subscribe_to': (latest_payment + timedelta(days=31)).replace(hour=0, minute=0, second=0)}

        if latest_payment is not None:
            await u.set_user_attrs(telegram_user_id=telegram_user_id,
                                   attrs=attrs)
