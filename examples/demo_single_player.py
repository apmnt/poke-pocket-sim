"""
Demo file for Pokemon Pocket Simulator.

This demo can run in two modes:
1. CLI mode - Traditional command-line interface (default for human player)
2. Bot mode - Both players are bots (no UI needed)

Usage:
    python demo_single_player.py           # Run with CLI (human vs bot)
    python demo_single_player.py --bot     # Run with both bots
"""

import argparse

from pokepocketsim import Card, Deck, Item, Match, Player
from pokepocketsim.utils import config


def create_decks():
    """Create test decks for the demo."""
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

    return test_deck1, test_deck2


def run_cli_mode():
    """Run the game with traditional CLI."""
    print("Starting Pokemon Pocket Simulator...")

    # Disable GUI for CLI mode
    config.gui_enabled = False

    test_deck1, test_deck2 = create_decks()

    # Create players
    test_player1 = Player("p1", test_deck1, is_bot=False)
    test_player2 = Player("p2", test_deck2, is_bot=True)

    # Create a match object and pass the players as parameters
    test_match = Match(test_player1, test_player2)

    # Start the match
    test_match.play_one_match()


def run_bot_mode():
    """Run the game with both players as bots."""
    print("Starting Pokemon Pocket Simulator with bots...")

    # Disable GUI for bot mode
    config.gui_enabled = False

    test_deck1, test_deck2 = create_decks()

    # Create players (both bots)
    test_player1 = Player("Bot 1", test_deck1, is_bot=True)
    test_player2 = Player("Bot 2", test_deck2, is_bot=True)

    # Create a match object and pass the players as parameters
    test_match = Match(test_player1, test_player2)

    # Start the match
    test_match.play_one_match()


def main():
    """Main entry point for the demo."""
    parser = argparse.ArgumentParser(
        description="Pokemon Pocket Simulator Demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--bot", action="store_true", help="Run with both players as bots")

    args = parser.parse_args()

    # Determine which mode to run
    if args.bot:
        run_bot_mode()
    else:
        # Default to CLI mode
        run_cli_mode()


if __name__ == "__main__":
    main()
