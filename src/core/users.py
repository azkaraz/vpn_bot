from datetime import datetime
from typing import Optional

import pydantic

from src.core.service.mongo_context_manager import MongoCollection
from src.core.config import MONGO_DB, MONGO_DB_URL


class User(pydantic.BaseModel):
    telegram_user_id: int
    username: str
    first_name: str
    last_name: str

    date_registration: datetime

    last_payment: Optional[datetime]
    vpn_active: Optional[bool]
    subscribe_to: Optional[datetime]


async def get_user_attrs(telegram_user_id):
    with MongoCollection(uri=MONGO_DB_URL,
                         collection='users',
                         database=MONGO_DB) as collection:
        return collection.find_one({'telegram_user_id': telegram_user_id})


async def set_user_attrs(telegram_user_id, attrs):
    filter_for_mongo = {'telegram_user_id': telegram_user_id}
    new_values = {'$set': attrs}
    with MongoCollection(uri=MONGO_DB_URL,
                         collection='users',
                         database=MONGO_DB) as collection:
        collection.update_one(filter_for_mongo, new_values)


async def register_user(telegram_user_id, username, first_name, last_name,
                        date_registration=datetime.today(), last_payment=None,
                        vpn_active=None, subscribe_to=None, balance=0):

    user = User(telegram_user_id=telegram_user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                date_registration=date_registration,
                last_payment=last_payment,
                vpn_active=vpn_active,
                subscribe_to=subscribe_to,
                balance=balance).dict()

    with MongoCollection(uri=MONGO_DB_URL,
                         collection='users',
                         database=MONGO_DB) as collection:
        collection.insert_one(user)


async def user_is_registered(telegram_user_id):
    with MongoCollection(uri=MONGO_DB_URL,
                         collection='users',
                         database=MONGO_DB) as collection:
        user = collection.find_one({'telegram_user_id': telegram_user_id})

        if user is None:
            return False
        else:
            return True


def subscription_is_paid(telegram_user_id):
    pass
