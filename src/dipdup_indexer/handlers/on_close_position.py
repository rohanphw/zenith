from dipdup.context import HandlerContext
from dipdup.models import Transaction
from dipdup_indexer.types.vUSD.parameter.transfer import TransferParameter
from dipdup_indexer.types.vUSD.storage import VUSDStorage
from dipdup_indexer.types.zenith.parameter.close_position import ClosePositionParameter
from dipdup_indexer.types.zenith.storage import ZenithStorage


async def on_close_position(
    ctx: HandlerContext,
    close_position: Transaction[ClosePositionParameter, ZenithStorage],
    transfer: Transaction[TransferParameter, VUSDStorage],
) -> None:
    ...