# Pokemon TCG Pocket Simulator

Under development!

Currently features include almost every mechanic. Most of the implementations need improvement to be bug free and faster, and a lot of single items, supporters, and pokemon still need to be added. Adding them is manual work, but the framework to support them is there. Pokemon can be added by scraping the pokemon list and generating necessary code.

Currently under development and featuring only separate files, but it will soon be available as a library in PyPI.

Welcoming collaboration! If you clone this repo and find something that should be added or doesn't work (most things do not work flawlessly as of right now), just [create an issue](https://github.com/apmnt/poke-pocket-sim/issues)!

Roadmap:

- [x] Add attacks, cards and basic turn mechanics
- [x] Add items
- [x] Add supporters
- [x] Add abilities
- [x] Add evolutions
- [x] Add data collection for match analysis
- [x] Add simulation of one turn and evaluation of the action sequences
- [ ] Add simulation of multiple turns and evaluate the action sequences
- [x] Add user based inputs to make it user/bot playable
- [ ] Add better text based user interface for playing

To play one game against an opponent, run the test_single_player.py. The script creates an example deck and takes in user inputs for actions for player one.

test_single_player.py file:

```python

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

```

Possible actions for each turn can be simulated and each sequence can be evaluated to find the best sequence based on evolutions, damage done, and knocked out cards. Example:

```python
from card import Card, Cards
from deck import Deck
from player import Player
from match import Match
from item import Item
from supporter import Supporter
from action import Action
from typing import List, Tuple

test_deck1 = Deck(energy_types=["psychic"])
test_deck1.add_card(Card.create_card(Cards.RALTS))
test_deck1.add_card(Card.create_card(Cards.KIRLIA))
test_deck1.add_card(Card.create_card(Cards.GARDEVOIR))
test_deck1.add_card(Card.create_card(Cards.MEWTWO_EX))
test_deck1.add_card(Card.create_card(Cards.MEWTWO_EX))
test_deck1.add_card(Item.Potion)
test_deck1.add_card(Item.Potion)


test_deck2 = Deck(energy_types=["psychic"])
test_deck2.add_card(Card.create_card(Cards.RALTS))
test_deck2.add_card(Card.create_card(Cards.KIRLIA))
test_deck2.add_card(Card.create_card(Cards.GARDEVOIR))
test_deck2.add_card(Card.create_card(Cards.MEWTWO_EX))
test_deck2.add_card(Card.create_card(Cards.MEWTWO_EX))


test_player1 = Player("p1", test_deck1)
test_player2 = Player("p2", test_deck2)
test_match = Match(test_player1, test_player2)

# test_match.play_one_match()

# Collect all possible sequences of actions for player1's turn
test_match.start_turn()
test_match.start_turn()
test_match.start_turn()
test_match.start_turn()
test_match.start_turn()
test_match.start_turn()
sequences: List[Tuple[int, List[Action]]] = test_match.simulate_turn_actions(
    test_player1
)

# Sort the list by the evaluation
sequences.sort(key=lambda x: x[0])

# Print sequences
print("Unique possible sequences:")
for sequence in sequences:
    print(
        "Evaluation: ",
        sequence[0],
        "Actions: ",
        [action.name for action in sequence[1]],
    )
```

Output:

```
Unique possible sequences:
Evaluation:  10.0 Actions:  ['Evolve Kirlia to Gardevoir', 'Retreat active card (Card(Mewtwo EX with 150 hp, Energies: psychic: 2))', 'Add psychic energy to Card(Mewtwo EX with 150 hp, Energies: )']
Evaluation:  10.0 Actions:  ['Evolve Kirlia to Gardevoir', 'Retreat active card (Card(Mewtwo EX with 150 hp, Energies: psychic: 2))', 'Add psychic energy to Card(Kirlia with 80 hp, Energies: )']
Evaluation:  10.0 Actions:  ['Evolve Kirlia to Gardevoir', 'Retreat active card (Card(Mewtwo EX with 150 hp, Energies: psychic: 2))', 'Add psychic energy to Card(Mewtwo EX with 150 hp, Energies: psychic: 0)']
Evaluation:  10.0 Actions:  ['Evolve Kirlia to Gardevoir', 'Add psychic energy to Card(Mewtwo EX with 150 hp, Energies: psychic: 2)', 'Retreat active card (Card(Mewtwo EX with 150 hp, Energies: psychic: 2))']
Evaluation:  10.0 Actions:  ['Evolve Kirlia to Gardevoir', 'Add psychic energy to Card(Kirlia with 80 hp, Energies: )', 'Retreat active card (Card(Mewtwo EX with 150 hp, Energies: psychic: 3))']
Evaluation:  10.0 Actions:  ['Evolve Kirlia to Gardevoir', 'Add psychic energy to Card(Mewtwo EX with 150 hp, Energies: )', 'Retreat active card (Card(Mewtwo EX with 150 hp, Energies: psychic: 3))']
Evaluation:  10.0 Actions:  ['Retreat active card (Card(Mewtwo EX with 150 hp, Energies: psychic: 2))', 'Use ability Psy Shadow on Mewtwo EX', 'Add psychic energy to Card(Mewtwo EX with 150 hp, Energies: psychic: 1)']
Evaluation:  10.0 Actions:  ['Retreat active card (Card(Mewtwo EX with 150 hp, Energies: psychic: 2))', 'Use ability Psy Shadow on Mewtwo EX', 'Add psychic energy to Card(Gardevoir with 110 hp, Energies: )', 'Retreat active card (Card(Mewtwo EX with 150 hp, Energies: psychic: 2))']
Evaluation:  10.0 Actions:  ['Retreat active card (Card(Mewtwo EX with 150 hp, Energies: psychic: 2))', 'Use ability Psy Shadow on Mewtwo EX', 'Add psychic energy to Card(Mewtwo EX with 150 hp, Energies: psychic: 0)', 'Retreat active card (Card(Mewtwo EX with 150 hp, Energies: psychic: 2))']
Evaluation:  10.0 Actions:  ['Retreat active card (Card(Mewtwo EX with 150 hp, Energies: psychic: 2))', 'Add psychic energy to Card(Mewtwo EX with 150 hp, Energies: )']
Evaluation:  10.0 Actions:  ['Retreat active card (Card(Mewtwo EX with 150 hp, Energies: psychic: 2))', 'Add psychic energy to Card(Gardevoir with 110 hp, Energies: )']
Evaluation:  10.0 Actions:  ['Retreat active card (Card(Mewtwo EX with 150 hp, Energies: psychic: 2))', 'Add psychic energy to Card(Mewtwo EX with 150 hp, Energies: psychic: 0)']
Evaluation:  10.0 Actions:  ['Add psychic energy to Card(Mewtwo EX with 150 hp, Energies: psychic: 2)', 'Use ability Psy Shadow on Mewtwo EX', 'Retreat active card (Card(Mewtwo EX with 150 hp, Energies: psychic: 3))']
Evaluation:  10.0 Actions:  ['Add psychic energy to Card(Mewtwo EX with 150 hp, Energies: psychic: 2)', 'Retreat active card (Card(Mewtwo EX with 150 hp, Energies: psychic: 2))']
Evaluation:  10.0 Actions:  ['Add psychic energy to Card(Kirlia with 80 hp, Energies: )', 'Use ability Psy Shadow on Mewtwo EX', 'Retreat active card (Card(Mewtwo EX with 150 hp, Energies: psychic: 4))']
Evaluation:  10.0 Actions:  ['Add psychic energy to Card(Kirlia with 80 hp, Energies: )', 'Retreat active card (Card(Mewtwo EX with 150 hp, Energies: psychic: 3))']
Evaluation:  10.0 Actions:  ['Add psychic energy to Card(Mewtwo EX with 150 hp, Energies: )', 'Use ability Psy Shadow on Mewtwo EX', 'Retreat active card (Card(Mewtwo EX with 150 hp, Energies: psychic: 4))']
Evaluation:  10.0 Actions:  ['Add psychic energy to Card(Mewtwo EX with 150 hp, Energies: )', 'Retreat active card (Card(Mewtwo EX with 150 hp, Energies: psychic: 3))']
Evaluation:  15.0 Actions:  ['Evolve Kirlia to Gardevoir', 'Mewtwo EX use psychic_sphere']
Evaluation:  15.0 Actions:  ['Evolve Kirlia to Gardevoir', 'Add psychic energy to Card(Mewtwo EX with 150 hp, Energies: psychic: 2)', 'Mewtwo EX use psychic_sphere']
Evaluation:  15.0 Actions:  ['Evolve Kirlia to Gardevoir', 'Add psychic energy to Card(Kirlia with 80 hp, Energies: )', 'Mewtwo EX use psychic_sphere']
Evaluation:  15.0 Actions:  ['Evolve Kirlia to Gardevoir', 'Add psychic energy to Card(Mewtwo EX with 150 hp, Energies: )', 'Mewtwo EX use psychic_sphere']
Evaluation:  15.0 Actions:  ['Mewtwo EX use psychic_sphere']
Evaluation:  15.0 Actions:  ['Retreat active card (Card(Mewtwo EX with 150 hp, Energies: psychic: 2))', 'Use ability Psy Shadow on Mewtwo EX', 'Add psychic energy to Card(Gardevoir with 110 hp, Energies: )', 'Mewtwo EX use psychic_sphere']
Evaluation:  15.0 Actions:  ['Retreat active card (Card(Mewtwo EX with 150 hp, Energies: psychic: 2))', 'Use ability Psy Shadow on Mewtwo EX', 'Add psychic energy to Card(Mewtwo EX with 150 hp, Energies: psychic: 0)', 'Mewtwo EX use psychic_sphere']
Evaluation:  15.0 Actions:  ['Add psychic energy to Card(Mewtwo EX with 150 hp, Energies: psychic: 2)', 'Use ability Psy Shadow on Mewtwo EX', 'Mewtwo EX use psychic_sphere']
Evaluation:  15.0 Actions:  ['Add psychic energy to Card(Mewtwo EX with 150 hp, Energies: psychic: 2)', 'Mewtwo EX use psychic_sphere']
Evaluation:  15.0 Actions:  ['Add psychic energy to Card(Kirlia with 80 hp, Energies: )', 'Use ability Psy Shadow on Mewtwo EX', 'Mewtwo EX use psychic_sphere']
Evaluation:  15.0 Actions:  ['Add psychic energy to Card(Kirlia with 80 hp, Energies: )', 'Mewtwo EX use psychic_sphere']
Evaluation:  15.0 Actions:  ['Add psychic energy to Card(Mewtwo EX with 150 hp, Energies: )', 'Use ability Psy Shadow on Mewtwo EX', 'Mewtwo EX use psychic_sphere']
Evaluation:  15.0 Actions:  ['Add psychic energy to Card(Mewtwo EX with 150 hp, Energies: )', 'Mewtwo EX use psychic_sphere']
Evaluation:  25.0 Actions:  ['Add psychic energy to Card(Kirlia with 80 hp, Energies: )', 'Use ability Psy Shadow on Mewtwo EX', 'Mewtwo EX use psydrive']
Evaluation:  25.0 Actions:  ['Add psychic energy to Card(Mewtwo EX with 150 hp, Energies: )', 'Use ability Psy Shadow on Mewtwo EX', 'Mewtwo EX use psydrive']
```

To simulate a simple game with random actions for each turn (snippet of test.py):

```python
from card import Card, Cards
from deck import Deck
from player import Player
from match import Match
from item import Item
from supporter import Supporter
from action import Action

test_deck1 = Deck(energy_types=["psychic"])
test_deck1.add_card(Card.create_card(Cards.RALTS))
test_deck1.add_card(Card.create_card(Cards.KIRLIA))
test_deck1.add_card(Card.create_card(Cards.GARDEVOIR))
test_deck1.add_card(Card.create_card(Cards.MEWTWO_EX))
test_deck1.add_card(Card.create_card(Cards.MEWTWO_EX))

test_deck2 = Deck(energy_types=["psychic"])
test_deck2.add_card(Card.create_card(Cards.RALTS))
test_deck2.add_card(Card.create_card(Cards.KIRLIA))
test_deck2.add_card(Card.create_card(Cards.GARDEVOIR))
test_deck2.add_card(Card.create_card(Cards.MEWTWO_EX))
test_deck2.add_card(Card.create_card(Cards.MEWTWO_EX))


test_player1 = Player("p1", test_deck1)
test_player2 = Player("p2", test_deck2)
test_match = Match(test_player1, test_player2)

test_match.play_one_match()
```

Output snippet:

```
...
Turn 26, p2's turn, p1 2 - p2 2
p2 active card: Card(Kirlia with 20 hp, Energies: psychic: 1)
p2 hand:
         Card(Gardevoir with 110 hp, Energies: )
p2 bench:
         Card(Mewtwo EX with 40 hp, Energies: psychic: 0)
Possible actions:
         Action(Name: Evolve Kirlia to Gardevoir, Type: ActionType.EVOLVE)
         Action(Name: Retreat active card (Card(Kirlia with 20 hp, Energies: psychic: 1)), Type: ActionType.FUNCTION)
         Action(Name: Add psychic energy to Card(Kirlia with 20 hp, Energies: psychic: 1), Type: ActionType.ADD_ENERGY)
         Action(Name: Add psychic energy to Card(Mewtwo EX with 40 hp, Energies: psychic: 0), Type: ActionType.ADD_ENERGY)
Acting: Add psychic energy to Card(Kirlia with 20 hp, Energies: psychic: 1)
Current energies of Kirlia {'psychic': 2}
Possible actions:
         Action(Name: Evolve Kirlia to Gardevoir, Type: ActionType.EVOLVE)
         Action(Name: Retreat active card (Card(Kirlia with 20 hp, Energies: psychic: 2)), Type: ActionType.FUNCTION)
Acting: Evolve Kirlia to Gardevoir
Possible actions:
         Action(Name: Use ability Psy Shadow on Gardevoir, Type: ActionType.ABILITY)
         Action(Name: Retreat active card (Card(Gardevoir with 50 hp, Energies: psychic: 2)), Type: ActionType.FUNCTION)
Acting: Retreat active card (Card(Gardevoir with 50 hp, Energies: psychic: 2))
Gardevoir retreated, Mewtwo EX set as active
Possible actions:
         Action(Name: Use ability Psy Shadow on Mewtwo EX, Type: ActionType.ABILITY)


Turn 27, p1's turn, p1 2 - p2 2
p1 active card: Card(Gardevoir with 110 hp, Energies: psychic: 3)
p1 hand:
p1 bench:
         Card(Mewtwo EX with 100 hp, Energies: psychic: 0)
Possible actions:
         Action(Name: Use ability Psy Shadow on Gardevoir, Type: ActionType.ABILITY)
         Action(Name: Gardevoir use psyshot, Type: ActionType.ATTACK)
         Action(Name: Retreat active card (Card(Gardevoir with 110 hp, Energies: psychic: 3)), Type: ActionType.FUNCTION)
         Action(Name: Add psychic energy to Card(Gardevoir with 110 hp, Energies: psychic: 3), Type: ActionType.ADD_ENERGY)
         Action(Name: Add psychic energy to Card(Mewtwo EX with 100 hp, Energies: psychic: 0), Type: ActionType.ADD_ENERGY)
Acting: Use ability Psy Shadow on Gardevoir
Current energies of Gardevoir {'psychic': 4}
Possible actions:
         Action(Name: Gardevoir use psyshot, Type: ActionType.ATTACK)
         Action(Name: Retreat active card (Card(Gardevoir with 110 hp, Energies: psychic: 4)), Type: ActionType.FUNCTION)
         Action(Name: Add psychic energy to Card(Gardevoir with 110 hp, Energies: psychic: 4), Type: ActionType.ADD_ENERGY)
         Action(Name: Add psychic energy to Card(Mewtwo EX with 100 hp, Energies: psychic: 0), Type: ActionType.ADD_ENERGY)
Acting: Gardevoir use psyshot
Dealing 60 to Mewtwo EX
p2's Mewtwo EX knocked out!

------ GAME OVER -------
p1 won 4-2
after 27 turns
```
