import uuid
from typing import (
    TYPE_CHECKING,
    List,
)

from .action import Action, ActionType
from .attack import EnergyType

if TYPE_CHECKING:
    from ..core.card import Card
    from ..core.player import Player


# TODO: fix multiple abilities
class Ability:
    class PsyShadow:
        def __init__(self) -> None:
            self.name: str = "Psy Shadow"

        def able_to_use(self, player: "Player") -> bool:
            return True

        def gather_actions(self, player: "Player", card_using_ability: "Card") -> List[Action]:
            if player.active_card is None:
                return []  # Return empty list if active_card is None

            ab_action = Action(
                f"Use ability {self.name} on {player.active_card.name}",
                lambda player, card_using_ability_id=card_using_ability.uuid, self=self: self.use(
                    player, card_using_ability_id
                ),
                ActionType.ABILITY,
            )
            return [ab_action]  # Return a list containing the action

        def use(self, player: "Player", using_card_id: uuid.UUID) -> None:
            from ..core.card import Card

            if player.active_card is None:
                return  # Early return if active_card is None

            target_card = player.active_card  # Now we know it's not None

            using_card = player.find_by_id(  # Use the method from Player instance
                player.bench + ([player.active_card] if player.active_card else []),
                using_card_id,
            )

            if using_card is None:
                return  # Early return if using_card is None

            if using_card.has_used_ability:
                raise Exception(f"{using_card.name} has already used {self.name} ability")

            # Now we know both cards are not None
            Card.add_energy(player, target_card, EnergyType.Psychic.value)
            using_card.has_used_ability = True
