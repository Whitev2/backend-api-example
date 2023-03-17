from __future__ import annotations
from datetime import datetime

from api_exceptions.transaction_exc import BadBalance
from models import Transaction, User

from utils.rounding import rounding
from schemas import TransactionBase


class TransactionCrud:

    @staticmethod
    async def get_user(uid: str) -> User | None:
        user: User = await User.query.where(User.uid == uid).gino.first()
        return user

    async def update_user_balance(self, uid: str, number_sum: float):
        user = await self.get_user(uid)

        new_balance = sum([user.balance, float(number_sum)])
        if new_balance < float(0):
            raise BadBalance

        await user.update(balance=new_balance).apply()

    async def create(self, hash: str, uid: str, type: str, amount: float, timestamp: datetime.timestamp) -> TransactionBase | None:

        try:
            date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        except:
            date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")

        transaction: Transaction = await Transaction.create(trn_hash=hash,
                                                            type=type,
                                                            amount=float(amount),
                                                            timestamp=date, uid=uid)
        if type == "WITHDRAW":
            print("ВЫВОД ", amount)
            number_sum = -float(amount)
        else:
            print("ПОПОЛНЕНИЕ ", amount)
            number_sum = float(amount)

        try:
            await self.update_user_balance(uid=uid, number_sum=number_sum)
        except BadBalance:
            print("НЕДОСТАТОЧНО БАЛАНСА ДЛЯ ВЫВОДА СРЕДСТВ")
            return None

        amount = rounding(transaction.amount, 2)
        return TransactionBase(
            id=transaction.id,
            uid=transaction.uid,
            trn_hash=transaction.trn_hash,
            type=transaction.type,
            amount=amount,
            timestamp=str(transaction.timestamp)
        )

    async def get(self, hash: str) -> TransactionBase | None:
        transaction: Transaction = await Transaction.query.where(Transaction.trn_hash == hash).gino.all()

        if len(transaction) == 0:
            return None

        transaction = transaction[0]
        amount = rounding(transaction.amount, 2)

        return TransactionBase(
            id=transaction.id,
            uid=transaction.uid,
            trn_hash=transaction.trn_hash,
            type=transaction.type,
            amount=amount,
            timestamp=str(transaction.timestamp)
        )

    async def update(self):
        pass

    async def delete(self):
        pass
