from enum import Enum
import random
from .condition import Condition


class Supporter:

    class Erika:
        def card_able_to_use(card):
            return card.type == "grass"

        def use(card):
            card.hp = min(card.max_hp, card.hp + 50)

    class Giovanni:
        def use(player):
            player.active_card.add_condition(Condition.Plus10DamageDealed())
            for card in player.bench:
                card.add_condition(Condition.Plus10DamageDealed())

    class Sabrina:
        def player_able_to_use(player):
            return player.opponent.active_card and len(player.opponent.bench) > 0

        def use(player):
            player.opponent.move_active_card_to_bench()
