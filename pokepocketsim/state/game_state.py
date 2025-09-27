from typing import Dict, Any, Optional
from dataclasses import dataclass
from .player_state import PlayerState


@dataclass(frozen=True)
class GameState:
    """Immutable state representation of a complete game."""

    id: str
    player1: PlayerState
    player2: PlayerState
    current_turn: int = 0
    current_player_id: str = ""
    game_over: bool = False
    winner_id: Optional[str] = None

    def serialize(self) -> Dict[str, Any]:
        """Serialize game state to dictionary."""
        return {
            "id": self.id,
            "player1": self.player1.serialize(),
            "player2": self.player2.serialize(),
            "current_turn": self.current_turn,
            "current_player_id": self.current_player_id,
            "game_over": self.game_over,
            "winner_id": self.winner_id,
        }

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> "GameState":
        """Deserialize game state from dictionary."""
        return cls(
            id=data["id"],
            player1=PlayerState.deserialize(data["player1"]),
            player2=PlayerState.deserialize(data["player2"]),
            current_turn=data.get("current_turn", 0),
            current_player_id=data.get("current_player_id", ""),
            game_over=data.get("game_over", False),
            winner_id=data.get("winner_id"),
        )

    def get_current_player(self) -> PlayerState:
        """Get the current player's state."""
        if self.current_player_id == self.player1.id:
            return self.player1
        return self.player2

    def get_opponent(self, player_id: str) -> PlayerState:
        """Get the opponent of the specified player."""
        if player_id == self.player1.id:
            return self.player2
        return self.player1

    def get_player_by_id(self, player_id: str) -> Optional[PlayerState]:
        """Get player by ID."""
        if player_id == self.player1.id:
            return self.player1
        elif player_id == self.player2.id:
            return self.player2
        return None

    def with_player1(self, new_player1: PlayerState) -> "GameState":
        """Create new game state with updated player1."""
        return GameState(
            id=self.id,
            player1=new_player1,
            player2=self.player2,
            current_turn=self.current_turn,
            current_player_id=self.current_player_id,
            game_over=self.game_over,
            winner_id=self.winner_id,
        )

    def with_player2(self, new_player2: PlayerState) -> "GameState":
        """Create new game state with updated player2."""
        return GameState(
            id=self.id,
            player1=self.player1,
            player2=new_player2,
            current_turn=self.current_turn,
            current_player_id=self.current_player_id,
            game_over=self.game_over,
            winner_id=self.winner_id,
        )

    def with_current_turn(self, turn: int) -> "GameState":
        """Create new game state with updated turn."""
        return GameState(
            id=self.id,
            player1=self.player1,
            player2=self.player2,
            current_turn=turn,
            current_player_id=self.current_player_id,
            game_over=self.game_over,
            winner_id=self.winner_id,
        )

    def with_current_player(self, player_id: str) -> "GameState":
        """Create new game state with updated current player."""
        return GameState(
            id=self.id,
            player1=self.player1,
            player2=self.player2,
            current_turn=self.current_turn,
            current_player_id=player_id,
            game_over=self.game_over,
            winner_id=self.winner_id,
        )

    def with_game_over(self, winner_id: Optional[str] = None) -> "GameState":
        """Create new game state marked as game over."""
        return GameState(
            id=self.id,
            player1=self.player1,
            player2=self.player2,
            current_turn=self.current_turn,
            current_player_id=self.current_player_id,
            game_over=True,
            winner_id=winner_id,
        )

    def update_player(
        self, player_id: str, new_player_state: PlayerState
    ) -> "GameState":
        """Create new game state with updated player."""
        if player_id == self.player1.id:
            return self.with_player1(new_player_state)
        elif player_id == self.player2.id:
            return self.with_player2(new_player_state)
        else:
            raise ValueError(f"Unknown player ID: {player_id}")
