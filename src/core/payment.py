from yoomoney import Client
from yoomoney import Quickpay
from yoomoney import Client

token = "4100118145719086.18141EF20A6D0D082CEB490FCD456B3B2AD067F15A33218A79FF8256EFEE605AA67C6B26CD484C50326FEC87DF75F2DE46267D457C70198ADD69EC3B8D54225426AE1F16C77D2A9F1FFEE891807B6DD291BAB5D1E53E610201FA1AACE82356FB44EE8651FCBEB2922466EC6298F8FA0C59D503D40AE0B4F840503DD7A3E0C0C1"


def get_account_number():
    client = Client(token)
    user = client.account_info()
    return user.account


def create_payment_link(telegram_user_id):
    quickpay = Quickpay(
        receiver=get_account_number(),
        quickpay_form="shop",
        targets="Sponsor this project",
        paymentType="SB",
        sum=2,
        label=telegram_user_id
    )
    print(quickpay.base_url)
    print(quickpay.redirected_url)
    return quickpay.redirected_url


def chech_payment_status(telegram_user_id):
    client = Client(token)
    history = client.operation_history(label=telegram_user_id)
    print("List of operations:")
    print("Next page starts with: ", history.next_record)
    for operation in history.operations:
        print()
        print("Operation:", operation.operation_id)
        print("\tStatus     -->", operation.status)
        print("\tDatetime   -->", operation.datetime)
        print("\tTitle      -->", operation.title)
        print("\tPattern id -->", operation.pattern_id)
        print("\tDirection  -->", operation.direction)
        print("\tAmount     -->", operation.amount)
        print("\tLabel      -->", operation.label)
        print("\tType       -->", operation.type)

    if not history.operations:
        return False
    else:
        return True
