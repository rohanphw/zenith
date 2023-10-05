from dipdup.context import HandlerContext
from dipdup.models import Transaction
from dipdup_indexer.types.vUSD.parameter.transfer import TransferParameter
from dipdup_indexer.types.vUSD.storage import VUSDStorage
from dipdup_indexer.types.zenith.parameter.close_position import ClosePositionParameter
from dipdup_indexer.types.zenith.storage import ZenithStorage
from dipdup_indexer import models
from tortoise.exceptions import DoesNotExist


async def on_close_position(
    ctx: HandlerContext,
    close_position: Transaction[ClosePositionParameter, ZenithStorage],
    transfer: Transaction[TransferParameter, VUSDStorage],
) -> None:
    user_address = close_position.data.sender_address
    user_balance = transfer.storage.balances.get(user_address, '0').balance

    try:
        user = await models.User.get(address=user_address)
    except DoesNotExist:
        user = await models.User.create(address=user_address, balance=user_balance)

    marked_price = close_position.storage.current_mark_price
    await models.MarkedPrice.create(
        timestamp=close_position.data.timestamp,
        price=marked_price,
    )
    
    try:
        closePosition = await models.ClosePosition.get(id=close_position.data.id)
    except DoesNotExist:
        closePosition = await models.ClosePosition.create(
            id=close_position.data.id,
            user=user,
        )

    user.balance = user_balance
    await user.save()
