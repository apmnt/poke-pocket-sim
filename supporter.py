from enum import Enum
import random


class Supporter:

    class Erika:
        def card_able_to_use(card):
            return card.type == "grass"

        def use(card):
            card.hp = min(card.max_hp, card.hp + 50)

    class Giovanni:
        def use(player):
            pass
