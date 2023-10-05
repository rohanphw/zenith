from dipdup.context import HandlerContext
from dipdup.models import Transaction
from dipdup_indexer.types.vUSD.parameter.transfer import TransferParameter
from dipdup_indexer.types.vUSD.storage import VUSDStorage
from dipdup_indexer.types.zenith.parameter.remove_margin import RemoveMarginParameter
from dipdup_indexer.types.zenith.storage import ZenithStorage
from dipdup_indexer import models
from tortoise.exceptions import DoesNotExist


async def on_remove_margin(
    ctx: HandlerContext,
    remove_margin: Transaction[RemoveMarginParameter, ZenithStorage],
    transfer: Transaction[TransferParameter, VUSDStorage],
) -> None:
    user_address = remove_margin.data.sender_address
    user_balance = transfer.storage.balances.get(user_address, '0').balance
    try:
        user = await models.User.get(address=user_address)
    except DoesNotExist:
        user = await models.User.create(address=user_address, balance=user_balance)

    marked_price = remove_margin.storage.current_mark_price
    await models.MarkedPrice.create(
        timestamp=remove_margin.data.timestamp,
        price=marked_price,
    )
    
    try:
        removeMargin = await models.RemoveMargin.get(id=remove_margin.data.id)
    except DoesNotExist:
        removeMargin = await models.RemoveMargin.create(
            id=remove_margin.data.id,
            user=user,
            amount=remove_margin.parameter.__root__,
        )

    user.balance = user_balance
    await user.save()
    await removeMargin.save()
