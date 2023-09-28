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
    # user_balance = decrease_position.storage.balances.get(user_address, '0').balance
    # print(user_balance)

    try:
        user = await models.User.get(address=user_address)
        # user.balance = user_balance
    except DoesNotExist:
        user = await models.User.create(address=user_address, balance='0')
        print(user)
    # print(decrease_position.data.id)
    # print(user)
    # print(decrease_position.storage.balances.get(user_address, '0'))

    try:
        decreasePosition = await models.DecreasePosition.get(id=decrease_position.data.id)
    except DoesNotExist:
        decreasePosition = await models.DecreasePosition.create(
            id=decrease_position.data.id,
            user=user,
            amount=decrease_position.parameter.vUSD_amount,
        )

    # user.balance = user_balance
    await user.save()
    await decreasePosition.save()
