from card import Card, Cards
from deck import Deck
from player import Player
from match import Match
from item import Item

"""

This test file runs one game where p1 is controlled on the terminal by the user

"""

# Create a deck object
test_deck1 = Deck(energy_types=["psychic"])

# Add cards to the deck
test_deck1.add_card(Card.create_card(Cards.RALTS))
test_deck1.add_card(Card.create_card(Cards.KIRLIA))
test_deck1.add_card(Card.create_card(Cards.GARDEVOIR))
test_deck1.add_card(Card.create_card(Cards.MEWTWO_EX))
test_deck1.add_card(Item.Potion)
test_deck1.add_card(Item.Potion)

# Create another deck with cards
test_deck2 = Deck(energy_types=["psychic"])
test_deck2.add_card(Card.create_card(Cards.RALTS))
test_deck2.add_card(Card.create_card(Cards.KIRLIA))
test_deck2.add_card(Card.create_card(Cards.GARDEVOIR))
test_deck2.add_card(Card.create_card(Cards.MEWTWO_EX))

# Create players
test_player1 = Player("p1", test_deck1, is_bot=False)
test_player2 = Player("p2", test_deck2)

# Create a match object and pass the players as parameters
test_match = Match(test_player1, test_player2)

# Start the match
test_match.play_one_match()
