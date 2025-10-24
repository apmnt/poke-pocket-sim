"""
Game engine module for Pokemon Pocket Simulator.
Provides decoupled game logic for UI-independent operation.
"""

from .action_engine import execute_action, get_available_actions

__all__ = [
    "get_available_actions",
    "execute_action",
]
