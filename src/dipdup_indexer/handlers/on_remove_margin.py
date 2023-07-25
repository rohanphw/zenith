from dipdup.context import HandlerContext
from dipdup.models import Transaction
from dipdup_indexer.types.vUSD.parameter.transfer import TransferParameter
from dipdup_indexer.types.vUSD.storage import VUSDStorage
from dipdup_indexer.types.zenith.parameter.remove_margin import RemoveMarginParameter
from dipdup_indexer.types.zenith.storage import ZenithStorage


async def on_remove_margin(
    ctx: HandlerContext,
    remove_margin: Transaction[RemoveMarginParameter, ZenithStorage],
    transfer: Transaction[TransferParameter, VUSDStorage],
) -> None:
    ...