import datetime

from src.core.config import MONGO_DB_URL, MONGO_DB
from src.core.service.mongo_context_manager import MongoCollection


def payment_check_job():
    with MongoCollection(uri=MONGO_DB_URL,
                         collection='users',
                         database=MONGO_DB) as collection:
        users = collection.find()
        today = datetime.date.today()
        user_ids_with_expired_subscription = [user['_id'] for user in users if user['subscribe_to'].date() < today]

        filter_for_mongo = {"_id": {"$in": user_ids_with_expired_subscription}}
        new_value = {"$set": {"vpn_active": False}}
        result = collection.update_many(filter_for_mongo, new_value)

        print("Обновлено записей:", result.modified_count)


if __name__ == '__main__':
    payment_check_job()
