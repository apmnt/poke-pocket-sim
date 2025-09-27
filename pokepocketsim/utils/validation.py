# Validation utilities for the game engine

from typing import List, Dict, Any
from ..state import GameState, PlayerState


def validate_deck(deck_data: List[Dict[str, Any]]) -> bool:
    """Validate a deck configuration."""
    if not deck_data or len(deck_data) < 20:
        return False

    # Check that all cards have required fields
    required_fields = ["name", "hp", "type", "is_basic"]
    for card in deck_data:
        for field in required_fields:
            if field not in card:
                return False

    return True


def validate_game_state(game_state: GameState) -> bool:
    """Validate that a game state is consistent."""
    try:
        # Basic validation checks
        if not game_state.player1 or not game_state.player2:
            return False

        if game_state.current_turn < 0:
            return False

        # Validate each player state
        if not _validate_player_state(game_state.player1):
            return False

        if not _validate_player_state(game_state.player2):
            return False

        return True

    except Exception:
        return False


def _validate_player_state(player: PlayerState) -> bool:
    """Validate a single player state."""
    # Check points are non-negative
    if player.points < 0:
        return False

    # Check card consistency
    all_cards = player.hand + player.bench + player.deck + player.discard_pile
    if player.active_card:
        all_cards.append(player.active_card)

    # Check for duplicate IDs (each card should be unique)
    card_ids = [card.id for card in all_cards]
    if len(card_ids) != len(set(card_ids)):
        return False

    return True
