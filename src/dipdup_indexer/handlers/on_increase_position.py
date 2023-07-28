from dipdup.context import HandlerContext
from dipdup.models import Transaction
from dipdup_indexer.types.zenith.parameter.increase_position import IncreasePositionParameter
from dipdup_indexer.types.zenith.storage import ZenithStorage
from dipdup_indexer.types.vUSD.parameter.transfer import TransferParameter
from dipdup_indexer.types.vUSD.storage import VUSDStorage


async def on_increase_position(
    ctx: HandlerContext,
    increase_position: Transaction[IncreasePositionParameter, ZenithStorage],
    transfer: Transaction[TransferParameter, VUSDStorage],
) -> None:
    ...
