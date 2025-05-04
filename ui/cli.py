#!/usr/bin/env python3
...
# New UI CLI program for playing a single-player game in the terminal using the engine API
import random
from pokepocketsim import Deck, Card, Cards, Player, Match, Item


def build_deck():
    deck = Deck(energy_types=["psychic"])
    deck.add(Card.create_card(Cards.RALTS))
    deck.add(Card.create_card(Cards.KIRLIA))
    deck.add(Card.create_card(Cards.GARDEVOIR))
    deck.add(Card.create_card(Cards.MEWTWO_EX))
    deck.add(Item.Potion)
    deck.add(Item.Potion)
    return deck


def main():
    # Create players and match
    deck1 = build_deck()
    deck2 = build_deck()
    human = Player("You", deck1, is_bot=False)
    bot = Player("Bot", deck2, is_bot=True)
    human.set_opponent(bot)
    bot.set_opponent(human)
    match = Match(human, bot)
    game_over = False

    # Game loop
    while not game_over:
        match.turn += 1
        # Determine active player
        if match.turn % 2 == 1:
            active, other = human, bot
        else:
            active, other = bot, human
        print(f"\nTurn {match.turn}: {active.name}'s turn")

        # Setup turn
        active.setup_turn(match)

        # Action loop
        actions = active.gather_actions()
        while active.can_continue and actions:
            if active.is_bot:
                action = random.choice(actions)
                print(f"{active.name} plays: {action}")
            else:
                print("Available actions:")
                for idx, act in enumerate(actions):
                    print(f"  {idx}: {act}")
                choice = input("Select action: ")
                try:
                    idx = int(choice)
                    action = actions[idx]
                except (ValueError, IndexError):
                    print("Invalid choice, try again.")
                    continue
            actions = active.act_and_regather_actions(match, action)

        # Handle knockout and check end
        game_over = active.handle_knockout_points()

    # Game over summary
    winner = human if human.points > bot.points else bot
    print(f"\nGame over! Winner: {winner.name} ({winner.points}-{other.points})")


if __name__ == "__main__":
    main()
