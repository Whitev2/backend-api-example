import uuid

from models import User

from utils.rounding import rounding
from schemas import UserBase


class UserCrud:

    async def create(self, name) -> UserBase:
        user: User = await User.create(uid=str(uuid.uuid4()), name=name)
        return UserBase(id=user.id, uid=user.uid, name=user.name)

    @staticmethod
    async def get_balance(uid: str, date):

        user: User = await User.query.where(User.uid == uid).gino.first()
        if user is None:
            return None

        if date:
            user_balance = await user.user_balance_date(date)
            balance = rounding(user_balance, 2)
        else:
            balance = rounding(user.balance, 2)

        return balance

    async def update(self):
        pass

    async def delete(self):
        pass
