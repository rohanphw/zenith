from dipdup.context import HandlerContext
from dipdup.models import Transaction
from dipdup_indexer.types.zenith.parameter.decrease_position import DecreasePositionParameter
from dipdup_indexer.types.zenith.storage import ZenithStorage
from dipdup_indexer import models
from tortoise.exceptions import DoesNotExist
from dipdup_indexer.types.vUSD.parameter.transfer import TransferParameter
from dipdup_indexer.types.vUSD.storage import VUSDStorage


async def on_decrease_position(
    ctx: HandlerContext,
    decrease_position: Transaction[DecreasePositionParameter, ZenithStorage],
) -> None:
    user_address = decrease_position.data.sender_address

    try:
        user = await models.User.get(address=user_address)
    except DoesNotExist:
        user = await models.User.create(address=user_address, balance='0')
        print(user)

    marked_price = decrease_position.storage.current_mark_price
    await models.MarkedPrice.create(
        timestamp=decrease_position.data.timestamp,
        price=marked_price,
    )

    try:
        decreasePosition = await models.DecreasePosition.get(id=decrease_position.data.id)
    except DoesNotExist:
        decreasePosition = await models.DecreasePosition.create(
            id=decrease_position.data.id,
            user=user,
            amount=decrease_position.parameter.vUSD_amount,
        )

    await user.save()
    await decreasePosition.save()
