import random
from card import Card


class Deck:
    def __init__(self, energy_types, cards=[]):
        self.energy_types = energy_types
        self.cards = cards

    def add_card(self, card):
        self.cards.append(card)

    def draw_card(self):
        if self.cards:
            return self.cards.pop(0)
        else:
            return None

    def draw_energy(self):
        return random.choice(self.energy_types)

    def __repr__(self):
        return "Deck:\n" + "\n".join(str(card) for card in self.cards)
