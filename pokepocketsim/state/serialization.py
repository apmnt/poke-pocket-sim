from typing import Dict, Any, Union
import json
from .game_state import GameState
from .player_state import PlayerState
from .card_state import CardState


class StateSerializer:
    """Utilities for serializing and deserializing game states."""

    @staticmethod
    def serialize_to_json(state: Union[GameState, PlayerState, CardState]) -> str:
        """Serialize any state object to JSON string."""
        return json.dumps(state.serialize(), indent=2)

    @staticmethod
    def deserialize_game_state_from_json(json_str: str) -> GameState:
        """Deserialize GameState from JSON string."""
        data = json.loads(json_str)
        return GameState.deserialize(data)

    @staticmethod
    def deserialize_player_state_from_json(json_str: str) -> PlayerState:
        """Deserialize PlayerState from JSON string."""
        data = json.loads(json_str)
        return PlayerState.deserialize(data)

    @staticmethod
    def deserialize_card_state_from_json(json_str: str) -> CardState:
        """Deserialize CardState from JSON string."""
        data = json.loads(json_str)
        return CardState.deserialize(data)

    @staticmethod
    def serialize_to_dict(
        state: Union[GameState, PlayerState, CardState],
    ) -> Dict[str, Any]:
        """Serialize any state object to dictionary."""
        return state.serialize()

    @staticmethod
    def deserialize_game_state_from_dict(data: Dict[str, Any]) -> GameState:
        """Deserialize GameState from dictionary."""
        return GameState.deserialize(data)

    @staticmethod
    def deserialize_player_state_from_dict(data: Dict[str, Any]) -> PlayerState:
        """Deserialize PlayerState from dictionary."""
        return PlayerState.deserialize(data)

    @staticmethod
    def deserialize_card_state_from_dict(data: Dict[str, Any]) -> CardState:
        """Deserialize CardState from dictionary."""
        return CardState.deserialize(data)
