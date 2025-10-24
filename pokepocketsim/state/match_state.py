"""
State representation for Match entities.
Pure data class for easy serialization and deserialization.
"""

from dataclasses import dataclass
from typing import Any, Dict

from .player_state import PlayerState


@dataclass
class MatchState:
    """Immutable state representation of a Match."""

    turn: int
    game_over: bool
    starting_player: PlayerState
    second_player: PlayerState

    @classmethod
    def from_match(cls, match: Any) -> "MatchState":
        """Create MatchState from Match instance."""
        return cls(
            turn=match.turn,
            game_over=match.game_over,
            starting_player=PlayerState.from_player(match.starting_player),
            second_player=PlayerState.from_player(match.second_player),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "turn": self.turn,
            "game_over": self.game_over,
            "starting_player": self.starting_player.to_dict(),
            "second_player": self.second_player.to_dict(),
        }

    def get_active_player(self) -> PlayerState:
        """Get the currently active player based on turn number."""
        return self.starting_player if self.turn % 2 == 1 else self.second_player

    def get_inactive_player(self) -> PlayerState:
        """Get the currently inactive player based on turn number."""
        return self.second_player if self.turn % 2 == 1 else self.starting_player
