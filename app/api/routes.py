from aiohttp import web
from aiohttp.web import Request

from api_exceptions.transaction_exc import TransactionAlreadyExist
from crud import get_user_crud, get_transaction_crud


async def create_user(request: Request):
    user_crud = get_user_crud()

    data = await request.json()
    name = data.get("name", "anon")
    user = await user_crud.create(name)
    return web.json_response(user.__dict__, status=201)


async def create_transaction(request: Request):
    transaction_crud = get_transaction_crud()

    data = await request.json()
    hash, uid, type, amount, timestamp = data.get("hash"), data.get("uid"), data.get("type"), data.get("amount"), data.get("timestamp")

    try:
        transaction = await transaction_crud.create(hash=hash, type=type, amount=amount, timestamp=timestamp, uid=uid)

    except TransactionAlreadyExist:
        return web.json_response(status=409)

    if transaction is None:
        return web.json_response(status=402)

    resp_data = {'uid': transaction.uid,
                 'hash': transaction.trn_hash,
                 'type': transaction.type,
                 'amount': transaction.amount,
                 'timestamp': str(transaction.timestamp)}

    return web.json_response(resp_data, status=200)


async def get_user_balance(request: Request):
    user_crud = get_user_crud()

    uid = request.match_info['uid']
    date = request.rel_url.query.get('date')
    balance = await user_crud.get_balance(uid, date)
    return web.json_response({"balance": balance}, status=200)


async def get_transaction(request: Request):
    transaction_crud = get_transaction_crud()

    hash = request.match_info['hash']
    transaction = await transaction_crud.get(hash)
    resp_data = {'uid': transaction.uid,
                 'hash': transaction.trn_hash,
                 'type': transaction.type,
                 'amount': transaction.amount,
                 'timestamp': str(transaction.timestamp)}
    return web.json_response(resp_data, status=201)


def add_routes(app):
    app.router.add_route('POST', r'/v1/transaction', create_transaction, name='add_transaction')
    app.router.add_route('POST', r'/v1/user', create_user, name='create_user')
    app.router.add_route('GET', r'/v1/user/{uid}/balance', get_user_balance, name='get_user_balance')
    app.router.add_route('GET', r'/v1/transaction/{hash}', get_transaction, name='incoming_transaction')
    ...
