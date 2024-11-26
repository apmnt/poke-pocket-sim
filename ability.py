import random
from attack import EnergyType
from action import Action, ActionType


class Ability:
    class PsyShadow:
        def __init__(self):
            self.name = "Psy Shadow"

        def able_to_use(self, player):
            return True

        def gather_actions(self, player, card_using_ability):
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

        def use(self, target_card, using_card):
            if using_card.has_used_ability:
                raise Exception(
                    f"{using_card.name} has already used {self.name} ability"
                )
            target_card.add_energy(EnergyType.PSYCHIC.value)
            target_card.has_used_ability = True
