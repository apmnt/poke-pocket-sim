from pokepocketsim import Card, Deck, Player, Match, Item

"""

This test file runs one game where p1 is controlled on the terminal by the user

"""

# Create a deck object
test_deck1 = Deck(energy_types=["psychic"])

# Add cards to the deck
test_deck1.add(Card.create_card("Ralts"))
test_deck1.add(Card.create_card("Kirlia"))
test_deck1.add(Card.create_card("Gardevoir"))
test_deck1.add(Card.create_card("Mewtwo EX"))
test_deck1.add(Item.Potion)
test_deck1.add(Item.Potion)

# Create another deck with cards
test_deck2 = Deck(energy_types=["psychic"])
test_deck2.add(Card.create_card("Ralts"))
test_deck2.add(Card.create_card("Kirlia"))
test_deck2.add(Card.create_card("Gardevoir"))
test_deck2.add(Card.create_card("Mewtwo EX"))

# Create players
test_player1 = Player("p1", test_deck1, is_bot=False)
test_player2 = Player("p2", test_deck2)

# Create a match object and pass the players as parameters
test_match = Match(test_player1, test_player2)

# Start the match
test_match.play_one_match()
