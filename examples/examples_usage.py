"""
Example: Using the Refactored Architecture

This example demonstrates how to use the new decoupled architecture
to build different types of applications.
"""

# Mock GUI to avoid tkinter dependency
import sys
from unittest.mock import MagicMock

sys.modules["pokepocketsim.gui"] = MagicMock()

import json

from pokepocketsim import Card, Deck, Item, Match, Player
from pokepocketsim.engine import execute_action, get_available_actions
from pokepocketsim.utils import config


def example_1_basic_usage() -> None:
    """Example 1: Basic usage with the new engine."""
    print("=" * 60)
    print("Example 1: Basic Engine Usage")
    print("=" * 60)

    config.gui_enabled = False

    # Create a simple game
    deck = Deck(energy_types=["psychic"])
    deck.add(Card.create_card("Mewtwo EX"))

    player = Player("Player1", deck, is_bot=False)
    opponent = Player("Bot", deck, is_bot=True)
    player.set_opponent(opponent)
    opponent.set_opponent(player)

    # Get available actions
    actions = get_available_actions(player)

    print(f"\nAvailable actions for {player.name}:")
    for i, action in enumerate(actions):
        print(f"  {i}: {action.name}")

    # Execute first action
    if actions:
        print(f"\nExecuting: {actions[0].name}")
        can_continue = execute_action(player, actions[0], None)
        print(f"Can continue turn: {can_continue}")

    print()


def example_2_state_serialization():
    """Example 2: State serialization for web APIs."""
    print("=" * 60)
    print("Example 2: State Serialization")
    print("=" * 60)

    config.gui_enabled = False

    # Create a game
    deck1 = Deck(energy_types=["psychic"])
    deck1.add(Card.create_card("Mewtwo EX"))

    deck2 = Deck(energy_types=["psychic"])
    deck2.add(Card.create_card("Mewtwo EX"))

    player1 = Player("Player1", deck1, is_bot=True)
    player2 = Player("Player2", deck2, is_bot=True)

    match = Match(player1, player2)

    # Convert to state
    match_state = match.to_state()

    print("\nMatch State:")
    print(f"  Turn: {match_state.turn}")
    print(f"  Game Over: {match_state.game_over}")
    print(f"  Player 1: {match_state.starting_player.name}")
    print(f"  Player 2: {match_state.second_player.name}")

    # Serialize to JSON
    state_dict = match_state.to_dict()
    state_json = json.dumps(state_dict, indent=2)

    print("\nJSON representation (first 500 chars):")
    print(state_json[:500] + "...")
    print()


def example_3_custom_ui():
    """Example 3: Building a custom UI using the engine."""
    print("=" * 60)
    print("Example 3: Custom UI Implementation")
    print("=" * 60)

    config.gui_enabled = False

    # Create a simple game
    deck = Deck(energy_types=["psychic"])
    deck.add(Card.create_card("Mewtwo EX"))

    player = Player("Player", deck, is_bot=False)
    opponent = Player("Opponent", deck, is_bot=True)
    player.set_opponent(opponent)
    opponent.set_opponent(player)

    # Custom UI loop (simplified)
    print("\nCustom UI Loop:")
    print("=" * 40)

    turn = 1
    max_turns = 3

    while turn <= max_turns:
        print(f"\nTurn {turn}")
        print("-" * 40)

        # Get available actions
        actions = get_available_actions(player)

        if not actions:
            print("No actions available!")
            break

        # Display actions (custom format)
        print("Actions:")
        for i, action in enumerate(actions):
            print(f"  [{i}] {action.name}")

        # Auto-select first action for demo
        selected = 0
        print(f"\nSelecting: [{selected}] {actions[selected].name}")

        # Execute action
        can_continue = execute_action(player, actions[selected], None)

        if not can_continue:
            turn += 1

    print("\nCustom UI loop completed!")
    print()


def example_4_action_filtering():
    """Example 4: Filtering and analyzing actions."""
    print("=" * 60)
    print("Example 4: Action Filtering")
    print("=" * 60)

    config.gui_enabled = False

    # Create a game with more options
    deck = Deck(energy_types=["psychic"])
    deck.add(Card.create_card("Ralts"))
    deck.add(Card.create_card("Kirlia"))
    deck.add(Card.create_card("Gardevoir"))
    deck.add(Card.create_card("Mewtwo EX"))
    deck.add(Item.Potion)

    player = Player("Player", deck, is_bot=False)

    # Get all actions
    actions = get_available_actions(player)

    print(f"\nTotal actions: {len(actions)}")

    # Filter by action type

    action_types = {}
    for action in actions:
        action_type = action.action_type.name
        if action_type not in action_types:
            action_types[action_type] = []
        action_types[action_type].append(action.name)

    print("\nActions by type:")
    for action_type, action_names in action_types.items():
        print(f"\n  {action_type}:")
        for name in action_names:
            print(f"    - {name}")

    print()


def main():
    """Run all examples."""
    examples = [
        example_1_basic_usage,
        example_2_state_serialization,
        example_3_custom_ui,
        example_4_action_filtering,
    ]

    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"Error in {example.__name__}: {e}")
            import traceback

            traceback.print_exc()

    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
