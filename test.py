from card import Card, Cards
from attack import Attack
from deck import Deck
from player import Player
from match import Match
from item import Item
from supporter import Supporter

test_deck1 = Deck(energy_types=["water"])
test_deck1.add_card(Card.create_card(Cards.GARDEVOIR))
test_deck1.add_card(Card.create_card(Cards.GARDEVOIR))
test_deck1.add_card(Item.Potion())
test_deck1.add_card(Item.Potion())
test_deck1.add_card(Item.Potion())
test_deck1.add_card(Supporter.Giovanni())
test_deck1.add_card(Supporter.Giovanni())
test_deck1.add_card(Supporter.Giovanni())
test_deck1.add_card(Supporter.Giovanni())
test_deck1.add_card(Supporter.Giovanni())


test_deck2 = Deck(energy_types=["water"])
test_deck2.add_card(Card.create_card(Cards.GARDEVOIR))
test_deck2.add_card(Card.create_card(Cards.GARDEVOIR))
test_deck2.add_card(Item.Potion())


test_player1 = Player("p1", test_deck1)
test_player2 = Player("p2", test_deck2)
test_match = Match(test_player1, test_player2)

game_over = False

while game_over is False:
    game_over = test_match.start_turn()
