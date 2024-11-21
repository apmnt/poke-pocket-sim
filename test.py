from card import Card
from attack import Attack
from deck import Deck
from player import Player
from match import Match
import copy

test_attack1 = Attack("test attack 1", 30, {"fire": 1, "water": 0})
test_attack2 = Attack("test attack 2", 50, {"fire": 2, "water": 1})

test_card1 = Card("test card 1", 50, attacks=[test_attack1, test_attack2])
test_card2 = Card("test card 2", 50, attacks=[test_attack1, test_attack2])
test_card3 = Card("test card 3", 50, attacks=[test_attack1, test_attack2])
test_card4 = Card("test card 4", 50, attacks=[test_attack1, test_attack2])
test_card5 = Card("test card 5", 50, attacks=[test_attack1, test_attack2])
test_card6 = Card("test card 6", 50, attacks=[test_attack1, test_attack2])

test_deck1 = Deck(energy_types=["fire", "water"])
test_deck1.add_card(test_card1)
test_deck1.add_card(test_card2)
test_deck1.add_card(test_card3)
test_deck1.add_card(test_card4)
test_deck1.add_card(test_card5)
test_deck1.add_card(test_card6)

test_deck2 = copy.deepcopy(test_deck1)

test_player1 = Player("p1", test_deck1)
test_player2 = Player("p2", test_deck2)
test_match = Match(test_player1, test_player2)

game_over = False

while game_over is False:
    game_over = test_match.start_turn()
