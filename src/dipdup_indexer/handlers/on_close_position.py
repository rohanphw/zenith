from dipdup.context import HandlerContext
from dipdup.models import Transaction
from dipdup_indexer.types.vUSD.parameter.transfer import TransferParameter
from dipdup_indexer.types.vUSD.storage import VUSDStorage
from dipdup_indexer.types.zenith.parameter.close_position import ClosePositionParameter
from dipdup_indexer.types.zenith.storage import ZenithStorage
from dipdup_indexer import models


async def on_close_position(
    ctx: HandlerContext,
    close_position: Transaction[ClosePositionParameter, ZenithStorage],
    transfer: Transaction[TransferParameter, VUSDStorage],
) -> None:
    user_address = close_position.data.sender_address
    user_balance = transfer.storage.balances.get(user_address, '0').balance
    user, _ = await models.User.get_or_create(address=user_address, balance=user_balance)
    closePosition = await models.ClosePosition.get_or_create(id=close_position.data.id, user=user)
    await user.save()
    await closePosition.save()
