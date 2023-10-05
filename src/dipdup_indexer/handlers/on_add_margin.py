from dipdup.context import HandlerContext
from dipdup.models import Transaction
from dipdup_indexer.types.vUSD.parameter.transfer import TransferParameter
from dipdup_indexer.types.vUSD.storage import VUSDStorage
from dipdup_indexer.types.zenith.parameter.add_margin import AddMarginParameter
from dipdup_indexer.types.zenith.storage import ZenithStorage
from dipdup_indexer import models
from tortoise.exceptions import DoesNotExist


async def on_add_margin(
    ctx: HandlerContext,
    add_margin: Transaction[AddMarginParameter, ZenithStorage],
    transfer: Transaction[TransferParameter, VUSDStorage],
) -> None:
    user_address = add_margin.data.sender_address
    user_balance = transfer.storage.balances.get(user_address, '0').balance
    try:
        user = await models.User.get(address=user_address)
    except DoesNotExist:
        user = await models.User.create(address=user_address, balance=user_balance)

    marked_price = add_margin.storage.current_mark_price
    await models.MarkedPrice.create(
        timestamp=add_margin.data.timestamp,
        price=marked_price,
    )

    try:
        addMargin = await models.AddMargin.get(id=add_margin.data.id)
        print(addMargin)
    except DoesNotExist:
        addMargin = await models.AddMargin.create(
            id=add_margin.data.id,
            user=user,
            amount=add_margin.parameter.__root__,
        )

    user.balance = user_balance
    await user.save()
    await addMargin.save()
