from datetime import datetime

from sqlalchemy.dialects.postgresql import TIMESTAMP

from gino import Gino

db = Gino()


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String, db.ForeignKey('users.uid'))
    trn_hash = db.Column(db.String)
    type = db.Column(db.String)
    amount = db.Column(db.Float)

    timestamp = db.Column(TIMESTAMP)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    balance = db.Column(db.Float, default=float(0))

    async def user_balance_date(self, date: str):
        date = datetime.strptime(date[:-2], "%Y-%m-%dT%H:%M:%S.%f")

        query = Transaction.query.where(Transaction.timestamp <= date).where(Transaction.uid == self.uid)

        transactions = await query.gino.all()

        list_transaction = list()
        for transaction in transactions:
            if transaction.type == "WITHDRAW":
                list_transaction.append(-transaction.amount)
            elif transaction.type == "DEPOSIT":
                list_transaction.append(transaction.amount)
        return sum(list_transaction)
