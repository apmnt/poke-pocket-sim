"""
State representation for Player entities.
Pure data class for easy serialization and deserialization.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .card_state import CardState


@dataclass
class PlayerState:
    """Immutable state representation of a Player."""

    id: str  # Player UUID as string
    name: str
    is_bot: bool
    hand: List[CardState]
    bench: List[CardState]
    active_card: Optional[CardState]
    deck_cards: List[CardState]
    discard_pile: List[CardState]
    points: int
    current_energy: Optional[str]
    has_used_trainer: bool
    has_added_energy: bool
    can_continue: bool

    @classmethod
    def from_player(cls, player: Any) -> "PlayerState":
        """Create PlayerState from Player instance."""
        return cls(
            id=str(player.id),
            name=player.name,
            is_bot=player.is_bot,
            hand=[CardState.from_card(c) for c in player.hand if hasattr(c, "uuid")],
            bench=[CardState.from_card(c) for c in player.bench],
            active_card=CardState.from_card(player.active_card) if player.active_card else None,
            deck_cards=[CardState.from_card(c) for c in player.deck.cards],
            discard_pile=[CardState.from_card(c) for c in player.discard_pile],
            points=player.points,
            current_energy=player.current_energy,
            has_used_trainer=player.has_used_trainer,
            has_added_energy=player.has_added_energy,
            can_continue=player.can_continue,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "is_bot": self.is_bot,
            "hand": [c.to_dict() for c in self.hand],
            "bench": [c.to_dict() for c in self.bench],
            "active_card": self.active_card.to_dict() if self.active_card else None,
            "deck_cards": [c.to_dict() for c in self.deck_cards],
            "discard_pile": [c.to_dict() for c in self.discard_pile],
            "points": self.points,
            "current_energy": self.current_energy,
            "has_used_trainer": self.has_used_trainer,
            "has_added_energy": self.has_added_energy,
            "can_continue": self.can_continue,
        }
