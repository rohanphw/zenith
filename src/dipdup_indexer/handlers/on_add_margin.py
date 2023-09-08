from dipdup.context import HandlerContext
from dipdup.models import Transaction
from dipdup_indexer.types.vUSD.parameter.transfer import TransferParameter
from dipdup_indexer.types.vUSD.storage import VUSDStorage
from dipdup_indexer.types.zenith.parameter.add_margin import AddMarginParameter
from dipdup_indexer.types.zenith.storage import ZenithStorage
from dipdup_indexer import models


async def on_add_margin(
    ctx: HandlerContext,
    add_margin: Transaction[AddMarginParameter, ZenithStorage],
    transfer: Transaction[TransferParameter, VUSDStorage],
) -> None:
    user_address = add_margin.data.sender_address
    user_balance = transfer.storage.balances.get(user_address, '0').balance
    user, _ = await models.User.get_or_create(address=user_address, balance=user_balance)
    addMargin, _ = await models.AddMargin.get_or_create(
        id=add_margin.data.id, user=user, amount=add_margin.parameter.vUSD_amount
    )
    await user.save()
    await addMargin.save()
