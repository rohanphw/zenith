from dipdup.context import HandlerContext
from dipdup.models import Transaction
from dipdup_indexer.types.vUSD.parameter.transfer import TransferParameter
from dipdup_indexer.types.vUSD.storage import VUSDStorage
from dipdup_indexer.types.zenith.parameter.remove_margin import RemoveMarginParameter
from dipdup_indexer.types.zenith.storage import ZenithStorage
from dipdup_indexer import models


async def on_remove_margin(
    ctx: HandlerContext,
    remove_margin: Transaction[RemoveMarginParameter, ZenithStorage],
    transfer: Transaction[TransferParameter, VUSDStorage],
) -> None:
    user_address = remove_margin.data.sender_address
    user_balance = transfer.storage.balances.get(user_address, '0').balance
    user, _ = await models.RemoveMargin.get_or_create(address=user_address, balance=user_balance)
    removeMargin, _ = await models.RemoveMargin.get_or_create(
        id=remove_margin.data.id, 
        user=user, 
        amount=remove_margin.parameter.vUSD_amount
    )
    await user.save()
    await removeMargin.save()
