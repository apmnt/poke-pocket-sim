from enum import Enum
import random
from typing import Any, Union, TYPE_CHECKING
from .condition import Condition, ConditionBase
from .protocols import ICard, IPlayer, ISupporter

if TYPE_CHECKING:
    from .attack import EnergyType


class Supporter:

    class Erika(ISupporter):
        def __init__(self) -> None:
            self.name: str = "Erika"

        def card_able_to_use(self, card: ICard) -> bool:
            # Check if card type is either the string "grass" or the EnergyType.GRASS
            card_type = str(card.type)
            return card_type.lower() == "grass"

        def use(self, card: ICard) -> None:
            card.hp = min(card.max_hp, card.hp + 50)

    class Giovanni(ISupporter):
        def __init__(self) -> None:
            self.name: str = "Giovanni"

        def card_able_to_use(self, card: ICard) -> bool:
            return True

        def use(self, player: IPlayer) -> None:
            player.active_card.add_condition(Condition.Plus10DamageDealed())
            for card in player.bench:
                card.add_condition(Condition.Plus10DamageDealed())

    class Sabrina(ISupporter):
        def __init__(self) -> None:
            self.name: str = "Sabrina"

        def card_able_to_use(self, card: ICard) -> bool:
            return True

        def player_able_to_use(self, player: IPlayer) -> bool:
            return bool(player.opponent.active_card) and len(player.opponent.bench) > 0

        def use(self, player: IPlayer) -> None:
            player.opponent.move_active_card_to_bench()
