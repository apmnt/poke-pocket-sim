import builtins
from pokepocketsim import Player, Deck, Card, Item, Match

# Global list to record inputs
recorded_inputs = []

# Save the original input function
_original_input = builtins.input


def recording_input(prompt=""):
    user_input = _original_input(prompt)
    recorded_inputs.append(user_input)
    return user_input


# Override the built-in input with our recording version
builtins.input = recording_input

# Setup decks, players and match
test_deck1 = Deck(energy_types=["psychic"])
test_deck1.add_card(Card.create_card("Ralts"))
test_deck1.add_card(Card.create_card("Kirlia"))
test_deck1.add_card(Card.create_card("Gardevoir"))
test_deck1.add_card(Card.create_card("Mewtwo EX"))
test_deck1.add_card(Item.Potion)
test_deck1.add_card(Item.Potion)

test_deck2 = Deck(energy_types=["psychic"])
test_deck2.add_card(Card.create_card("Ralts"))
test_deck2.add_card(Card.create_card("Ralts"))
test_deck2.add_card(Card.create_card("Ralts"))

test_player1 = Player("p1", test_deck1, is_bot=False)
test_player2 = Player("p2", test_deck2, is_bot=False)

test_match = Match(test_player1, test_player2)

# Play the match
test_match.play_one_match()

# At end of the run, print out the recorded inputs on one row delimited by ", "
print("\nRecorded inputs during program runtime:")
print(", ".join(recorded_inputs))
