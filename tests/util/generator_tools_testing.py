from typing import List, Tuple

from chaingreen.full_node.mempool_check_conditions import get_name_puzzle_conditions
from chaingreen.types.blockchain_format.coin import Coin
from chaingreen.types.blockchain_format.sized_bytes import bytes32
from chaingreen.types.full_block import FullBlock
from chaingreen.types.generator_types import BlockGenerator
from chaingreen.util.generator_tools import additions_for_npc


def run_and_get_removals_and_additions(
    block: FullBlock, max_cost: int, safe_mode=False
) -> Tuple[List[bytes32], List[Coin]]:
    removals: List[bytes32] = []
    additions: List[Coin] = []

    assert len(block.transactions_generator_ref_list) == 0
    if not block.is_transaction_block():
        return [], []

    if block.transactions_generator is not None:
        npc_result = get_name_puzzle_conditions(BlockGenerator(block.transactions_generator, []), max_cost, safe_mode)
        # build removals list
        for npc in npc_result.npc_list:
            removals.append(npc.coin_name)
        additions.extend(additions_for_npc(npc_result.npc_list))

    rewards = block.get_included_reward_coins()
    additions.extend(rewards)
    return removals, additions
