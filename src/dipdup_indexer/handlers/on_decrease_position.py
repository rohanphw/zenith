from dipdup.context import HandlerContext
from dipdup.models import Transaction
from dipdup_indexer.types.zenith.parameter.decrease_position import DecreasePositionParameter
from dipdup_indexer.types.zenith.storage import ZenithStorage
from dipdup_indexer import models


async def on_decrease_position(
    ctx: HandlerContext,
    decrease_position: Transaction[DecreasePositionParameter, ZenithStorage],
) -> None:
    user_address = decrease_position.data.sender_address
    user, _ = await models.User.get_or_create(address=user_address)
    decreasePosition, _ = await models.DecreasePosition.get_or_create(id=decrease_position.data.id, user=user)
    await user.save()
    await decreasePosition.save()
