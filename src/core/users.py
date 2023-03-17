import pydantic
from datetime import datetime
from service.mongo_context_manager import MongoCollection


class User(pydantic.BaseModel):
    telegram_user_id: int
    name: str
    surname: str
    age: str
    date_registration: datetime

    last_payment: datetime
    subscription_status: str
    tariff: str





def register_user(telegram_user_id: int,
                  name: str,
                  surname: str,
                  age: str):

    user = User(telegram_user_id=int(telegram_user_id),
                name=str(name),
                surname=str(surname),
                age=int(age),
                date_registration = datetime.today()
                )

    with MongoCollection(uri='mongodb://localhost:27017/',
                         collection='new_fields',
                         database=db) as collection:
        pass

def check_registration(telegram_user_id):
    pass




