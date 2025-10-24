"""
State representation for Card entities.
Pure data class for easy serialization and deserialization.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class CardState:
    """Immutable state representation of a Card."""

    id: str
    uuid: str
    name: str
    hp: int
    max_hp: int
    energy_type: str  # EnergyType as string for serialization
    energies: Dict[str, int]
    retreat_cost: int
    is_ex: bool
    stage: int
    is_basic: bool
    evolves_from: Optional[str]
    weakness: Optional[str]  # EnergyType as string
    attacks: List[str]  # Attack names as strings
    ability: Optional[str]  # Ability name as string
    has_used_ability: bool
    can_evolve: bool
    conditions: List[str]  # Condition names as strings
    damage_modifier: int

    @classmethod
    def from_card(cls, card: Any) -> "CardState":
        """Create CardState from Card instance."""
        return cls(
            id=card.id,
            uuid=str(card.uuid),
            name=card.name,
            hp=card.hp,
            max_hp=card.max_hp,
            energy_type=card.energy_type.name
            if hasattr(card.energy_type, "name")
            else str(card.energy_type),
            energies=card.energies.copy(),
            retreat_cost=card.retreat_cost,
            is_ex=card.is_ex,
            stage=card.stage,
            is_basic=card.is_basic,
            evolves_from=card.evolves_from if isinstance(card.evolves_from, str) else None,
            weakness=card.weakness.name
            if card.weakness and hasattr(card.weakness, "name")
            else None,
            attacks=[getattr(a, "__name__", str(a)) for a in card.attacks],
            ability=card.ability.__class__.__name__ if card.ability else None,
            has_used_ability=card.has_used_ability,
            can_evolve=card.can_evolve,
            conditions=[c.__class__.__name__ for c in card.conditions],
            damage_modifier=getattr(card, "damage_modifier", 0),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "uuid": self.uuid,
            "name": self.name,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "energy_type": self.energy_type,
            "energies": self.energies,
            "retreat_cost": self.retreat_cost,
            "is_ex": self.is_ex,
            "stage": self.stage,
            "is_basic": self.is_basic,
            "evolves_from": self.evolves_from,
            "weakness": self.weakness,
            "attacks": self.attacks,
            "ability": self.ability,
            "has_used_ability": self.has_used_ability,
            "can_evolve": self.can_evolve,
            "conditions": self.conditions,
            "damage_modifier": self.damage_modifier,
        }
