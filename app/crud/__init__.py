from crud.transaction_crud import TransactionCrud
from crud.user_crud import UserCrud


def get_user_crud() -> UserCrud:
    return UserCrud()


def get_transaction_crud() -> TransactionCrud:
    return TransactionCrud()
