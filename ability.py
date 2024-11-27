import random
from typing import TYPE_CHECKING, List
from attack import EnergyType
from action import Action, ActionType

if TYPE_CHECKING:
    from player import Player
    from card import Card


# TODO: fix multiple abilities
class Ability:
    class PsyShadow:
        def __init__(self):
            self.name = "Psy Shadow"

        def able_to_use(self, player: "Player") -> bool:
            return True

        def gather_actions(
            self, player: "Player", card_using_ability: "Card"
        ) -> List["Action"]:
            actions = []
            for card in player.bench + [player.active_card]:
                actions.append(
                    Action(
                        f"Use ability {self.name} on {card.name}",
                        lambda card=card, card_using_ability=card_using_ability, self=self: self.use(
                            card, card_using_ability
                        ),
                        ActionType.ABILITY,
                    )
                )
            return actions

        def use(self, target_card: "Card", using_card: "Card"):
            if using_card.has_used_ability:
                raise Exception(
                    f"{using_card.name} has already used {self.name} ability"
                )
            target_card.add_energy(EnergyType.PSYCHIC.value)
            target_card.has_used_ability = True
