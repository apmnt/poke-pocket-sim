# Pokemon TCG Pocket Simulator - Game Engine
#
# This package provides a stateless game engine for Pokemon TCG Pocket simulation
# along with local game interfaces for human and CPU players.

# Main game engine
from .engine import GameEngine

# State management
from .state import GameState, PlayerState, CardState, StateSerializer

# Local game interfaces
from .local import LocalGame, HumanPlayer, CPUPlayer, create_sample_deck

# Core game components (for advanced usage)
from .core import Action, ActionType, Card, Cards, Deck, Attack, EnergyType

# Utilities
from .utils import validate_deck, validate_game_state

__version__ = "2.0.0"

__all__ = [
    # Engine
    "GameEngine",
    # State
    "GameState",
    "PlayerState",
    "CardState",
    "StateSerializer",
    # Local interface
    "LocalGame",
    "HumanPlayer",
    "CPUPlayer",
    "create_sample_deck",
    # Core components
    "Action",
    "ActionType",
    "Card",
    "Cards",
    "Deck",
    "Attack",
    "EnergyType",
    # Utilities
    "validate_deck",
    "validate_game_state",
]


# Quick start function
def create_local_game(
    player1_name: str = "Player 1",
    player2_name: str = "CPU",
    player1_human: bool = True,
    cpu_difficulty: str = "medium",
) -> LocalGame:
    """
    Create a local game with default settings.

    Args:
        player1_name: Name for player 1
        player2_name: Name for player 2
        player1_human: Whether player 1 is human (True) or CPU (False)
        cpu_difficulty: CPU difficulty if player2 is CPU ("easy", "medium", "hard")

    Returns:
        LocalGame instance ready to start
    """
    if player1_human:
        player1 = HumanPlayer(player1_name)
    else:
        player1 = CPUPlayer(player1_name, difficulty=cpu_difficulty)

    player2 = CPUPlayer(player2_name, difficulty=cpu_difficulty)

    return LocalGame(player1, player2)


# Example usage
def run_example_game():
    """Run an example game for demonstration."""
    print("Creating example game...")

    # Create players
    human = HumanPlayer("Human Player")
    cpu = CPUPlayer("CPU Player", difficulty="medium")

    # Create game
    game = LocalGame(human, cpu)

    # Create sample decks
    deck1 = create_sample_deck()
    deck2 = create_sample_deck()

    # Start and play the game
    game.start_game(deck1, deck2)
    winner = game.play_game()

    if winner:
        print(f"Congratulations to {winner}!")
    else:
        print("Game ended without a winner.")


if __name__ == "__main__":
    run_example_game()
