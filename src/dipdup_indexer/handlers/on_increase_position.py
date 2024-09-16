from dipdup.context import HandlerContext
from dipdup.models import Transaction

from dipdup_indexer import models
from dipdup_indexer.types.vUSD.parameter.transfer import TransferParameter
from dipdup_indexer.types.vUSD.storage import VUSDStorage
from dipdup_indexer.types.zenith.parameter.increase_position import IncreasePositionParameter
from dipdup_indexer.types.zenith.storage import ZenithStorage
from tortoise.exceptions import DoesNotExist

async def on_increase_position(
    ctx: HandlerContext,
    increase_position: Transaction[IncreasePositionParameter, ZenithStorage],
    transfer: Transaction[TransferParameter, VUSDStorage],
) -> None:
    user_address = increase_position.data.sender_address
    user_balance = transfer.storage.balances.get(user_address, '0').balance
    
    try:
        user = await models.User.get(address=user_address)
        user.balance = user_balance
    except DoesNotExist:
        user = await models.User.create(address=user_address, balance=user_balance)

    marked_price = increase_position.storage.current_mark_price
    await models.MarkedPrice.create(
        timestamp=increase_position.data.timestamp,
        price=marked_price,
    )


    try:
        increasePosition = await models.IncreasePosition.get(id=increase_position.data.id)
    except DoesNotExist:
        increasePosition = await models.IncreasePosition.create(
            id=increase_position.data.id,
            user=user,
            amount=increase_position.parameter.vUSD_amount,
        )

    position = increase_position.storage.positions[user_address]
    pnl_exist = await models.PnL.filter(user=user, status='open').first()
    if pnl_exist:
        pnl_exist.collateral = position.collateral_amount
        pnl_exist.position_size = position.vUSD_amount
        await pnl_exist.save()
    else:
        await models.PnL.create(
            user=user,
            timestamp=increase_position.data.timestamp,
            direction=position.position,
            collateral=position.collateral_amount,
            position_size=position.vUSD_amount,
            realized_pnl='0',
            status='open',
        )

    user.balance = user_balance
    await user.save()
    await increasePosition.save()

