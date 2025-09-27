from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from .card_state import CardState


@dataclass(frozen=True)
class PlayerState:
    """Immutable state representation of a player."""

    id: str
    name: str
    hand: List[CardState] = field(default_factory=lambda: [])
    bench: List[CardState] = field(default_factory=lambda: [])
    active_card: Optional[CardState] = None
    deck: List[CardState] = field(default_factory=lambda: [])
    discard_pile: List[CardState] = field(default_factory=lambda: [])
    points: int = 0
    has_used_trainer: bool = False
    has_added_energy: bool = False
    current_energy: Optional[str] = None

    def serialize(self) -> Dict[str, Any]:
        """Serialize player state to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "hand": [card.serialize() for card in self.hand],
            "bench": [card.serialize() for card in self.bench],
            "active_card": self.active_card.serialize() if self.active_card else None,
            "deck": [card.serialize() for card in self.deck],
            "discard_pile": [card.serialize() for card in self.discard_pile],
            "points": self.points,
            "has_used_trainer": self.has_used_trainer,
            "has_added_energy": self.has_added_energy,
            "current_energy": self.current_energy,
        }

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> "PlayerState":
        """Deserialize player state from dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            hand=[
                CardState.deserialize(card_data) for card_data in data.get("hand", [])
            ],
            bench=[
                CardState.deserialize(card_data) for card_data in data.get("bench", [])
            ],
            active_card=(
                CardState.deserialize(data["active_card"])
                if data.get("active_card")
                else None
            ),
            deck=[
                CardState.deserialize(card_data) for card_data in data.get("deck", [])
            ],
            discard_pile=[
                CardState.deserialize(card_data)
                for card_data in data.get("discard_pile", [])
            ],
            points=data.get("points", 0),
            has_used_trainer=data.get("has_used_trainer", False),
            has_added_energy=data.get("has_added_energy", False),
            current_energy=data.get("current_energy"),
        )

    def get_all_pokemon(self) -> List[CardState]:
        """Get all pokemon in play (active + bench)."""
        pokemon = self.bench.copy()
        if self.active_card:
            pokemon.append(self.active_card)
        return pokemon

    def find_card_by_id(
        self, card_id: str, location: str = "all"
    ) -> Optional[CardState]:
        """Find a card by ID in specified location(s)."""
        if location in ("all", "hand"):
            for card in self.hand:
                if card.id == card_id:
                    return card

        if location in ("all", "bench"):
            for card in self.bench:
                if card.id == card_id:
                    return card

        if location in ("all", "active") and self.active_card:
            if self.active_card.id == card_id:
                return self.active_card

        if location in ("all", "deck"):
            for card in self.deck:
                if card.id == card_id:
                    return card

        if location in ("all", "discard"):
            for card in self.discard_pile:
                if card.id == card_id:
                    return card

        return None

    def with_hand(self, new_hand: List[CardState]) -> "PlayerState":
        """Create new state with updated hand."""
        return PlayerState(
            id=self.id,
            name=self.name,
            hand=new_hand,
            bench=self.bench,
            active_card=self.active_card,
            deck=self.deck,
            discard_pile=self.discard_pile,
            points=self.points,
            has_used_trainer=self.has_used_trainer,
            has_added_energy=self.has_added_energy,
            current_energy=self.current_energy,
        )

    def with_bench(self, new_bench: List[CardState]) -> "PlayerState":
        """Create new state with updated bench."""
        return PlayerState(
            id=self.id,
            name=self.name,
            hand=self.hand,
            bench=new_bench,
            active_card=self.active_card,
            deck=self.deck,
            discard_pile=self.discard_pile,
            points=self.points,
            has_used_trainer=self.has_used_trainer,
            has_added_energy=self.has_added_energy,
            current_energy=self.current_energy,
        )

    def with_active_card(self, new_active: Optional[CardState]) -> "PlayerState":
        """Create new state with updated active card."""
        return PlayerState(
            id=self.id,
            name=self.name,
            hand=self.hand,
            bench=self.bench,
            active_card=new_active,
            deck=self.deck,
            discard_pile=self.discard_pile,
            points=self.points,
            has_used_trainer=self.has_used_trainer,
            has_added_energy=self.has_added_energy,
            current_energy=self.current_energy,
        )

    def with_points(self, new_points: int) -> "PlayerState":
        """Create new state with updated points."""
        return PlayerState(
            id=self.id,
            name=self.name,
            hand=self.hand,
            bench=self.bench,
            active_card=self.active_card,
            deck=self.deck,
            discard_pile=self.discard_pile,
            points=new_points,
            has_used_trainer=self.has_used_trainer,
            has_added_energy=self.has_added_energy,
            current_energy=self.current_energy,
        )

    def with_trainer_used(self, used: bool = True) -> "PlayerState":
        """Create new state with trainer usage updated."""
        return PlayerState(
            id=self.id,
            name=self.name,
            hand=self.hand,
            bench=self.bench,
            active_card=self.active_card,
            deck=self.deck,
            discard_pile=self.discard_pile,
            points=self.points,
            has_used_trainer=used,
            has_added_energy=self.has_added_energy,
            current_energy=self.current_energy,
        )

    def with_energy_added(self, added: bool = True) -> "PlayerState":
        """Create new state with energy usage updated."""
        return PlayerState(
            id=self.id,
            name=self.name,
            hand=self.hand,
            bench=self.bench,
            active_card=self.active_card,
            deck=self.deck,
            discard_pile=self.discard_pile,
            points=self.points,
            has_used_trainer=self.has_used_trainer,
            has_added_energy=added,
            current_energy=self.current_energy,
        )

    def with_current_energy(self, energy: Optional[str]) -> "PlayerState":
        """Create new state with updated current energy."""
        return PlayerState(
            id=self.id,
            name=self.name,
            hand=self.hand,
            bench=self.bench,
            active_card=self.active_card,
            deck=self.deck,
            discard_pile=self.discard_pile,
            points=self.points,
            has_used_trainer=self.has_used_trainer,
            has_added_energy=self.has_added_energy,
            current_energy=energy,
        )
