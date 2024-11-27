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
            ab_action = Action(
                        f"Use ability {self.name} on {player.active_card.name}",
                        lambda card=player.active_card, card_using_ability=card_using_ability, self=self: self.use(
                            card, card_using_ability
                        ),
                        ActionType.ABILITY,
                    )
            return ab_action

        def use(self, target_card: "Card", using_card: "Card"):
            if using_card.has_used_ability:
                raise Exception(
                    f"{using_card.name} has already used {self.name} ability"
                )
            target_card.add_energy(EnergyType.PSYCHIC.value)
            target_card.has_used_ability = True
