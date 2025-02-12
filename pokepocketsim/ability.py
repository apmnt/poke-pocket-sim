import random
from typing import TYPE_CHECKING, List
import uuid
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
                lambda player, card_using_ability_id=card_using_ability.id, self=self: self.use(
                    player, card_using_ability_id
                ),
                ActionType.ABILITY,
            )
            return ab_action

        def use(self, player: "Player", using_card_id: uuid):
            target_card = player.active_card
            from player import Player

            using_card = Player.find_by_id(
                player.bench + [player.active_card], using_card_id
            )
            if using_card.has_used_ability:
                raise Exception(
                    f"{using_card.name} has already used {self.name} ability"
                )
            from card import Card

            Card.add_energy(player, target_card, EnergyType.PSYCHIC.value)
            using_card.has_used_ability = True
