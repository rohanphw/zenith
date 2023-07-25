from dipdup.context import HandlerContext
from dipdup.models import Transaction
from dipdup_indexer.types.vUSD.parameter.transfer import TransferParameter
from dipdup_indexer.types.vUSD.storage import VUSDStorage
from dipdup_indexer.types.zenith.parameter.add_margin import AddMarginParameter
from dipdup_indexer.types.zenith.storage import ZenithStorage


async def on_add_margin(
    ctx: HandlerContext,
    add_margin: Transaction[AddMarginParameter, ZenithStorage],
    transfer: Transaction[TransferParameter, VUSDStorage],
) -> None:
    ...