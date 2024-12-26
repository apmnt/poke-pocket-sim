import pytest
from player import Player
from deck import Deck
from card import Card, Cards
from item import Item
from supporter import Supporter
from action import Action, ActionType
from match import Match

class TestPlayer:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.test_deck1 = Deck(energy_types=["psychic"])
        self.test_deck1.add_card(Card.create_card(Cards.RALTS))
        self.test_deck1.add_card(Card.create_card(Cards.KIRLIA))
        self.test_deck1.add_card(Card.create_card(Cards.GARDEVOIR))
        self.test_deck1.add_card(Card.create_card(Cards.MEWTWO_EX))
        self.test_deck1.add_card(Item.Potion)
        self.test_deck1.add_card(Item.Potion)


        self.test_deck2 = Deck(energy_types=["psychic"])
        self.test_deck2.add_card(Card.create_card(Cards.RALTS))
        self.test_deck2.add_card(Card.create_card(Cards.KIRLIA))
        self.test_deck2.add_card(Card.create_card(Cards.GARDEVOIR))
        self.test_deck2.add_card(Card.create_card(Cards.MEWTWO_EX))


        self.test_player1 = Player("p1", self.test_deck1)
        self.test_player1.evaluate_actions = True
        self.test_player2 = Player("p2", self.test_deck2)

        self.test_match = Match(self.test_player1, self.test_player2)

    def test_knock_card_out(self):
        # Add your test logic here
        pass

if __name__ == '__main__':
    pytest.main()