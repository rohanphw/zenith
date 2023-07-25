from dipdup.context import HandlerContext
from dipdup.models import Transaction
from dipdup_indexer.types.zenith.parameter.decrease_position import DecreasePositionParameter
from dipdup_indexer.types.zenith.storage import ZenithStorage


async def on_decrease_position(
    ctx: HandlerContext,
    decrease_position: Transaction[DecreasePositionParameter, ZenithStorage],
) -> None:
    ...