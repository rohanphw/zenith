from dipdup.context import HandlerContext
from dipdup.models import Transaction

from dipdup_indexer import models
from dipdup_indexer.types.vUSD.parameter.transfer import TransferParameter
from dipdup_indexer.types.vUSD.storage import VUSDStorage
from dipdup_indexer.types.zenith.parameter.increase_position import IncreasePositionParameter
from dipdup_indexer.types.zenith.storage import ZenithStorage


async def on_increase_position(
    ctx: HandlerContext,
    increase_position: Transaction[IncreasePositionParameter, ZenithStorage],
    transfer: Transaction[TransferParameter, VUSDStorage],
) -> None:
    user_address = increase_position.data.sender_address
    user_balance = transfer.storage.balances.get(user_address, '0').balance
    user, _ = await models.User.get_or_create(address=user_address, balance=user_balance)
    increasePosition, _ = await models.IncreasePosition.get_or_create(
        id=increase_position.data.id,
        user=user,
        amount=increase_position.parameter.vUSD_amount,
    )
    await user.save()
    await increasePosition.save()
