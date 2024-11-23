from enum import Enum
import random


class Supporter:

    class Erika:
        def __init__(self):
            pass
        
        def act(player):
            cards = [player.active_card] + player.bench
            green_cards = [card for card in cards if card.type == "Grass"]
            card = random.choice(green_cards) if green_cards else None
            if card is None:
                return
            card.hp = min(card.max_hp, card.hp + 50)

    class Giovanni:
        def act(player):
            pass