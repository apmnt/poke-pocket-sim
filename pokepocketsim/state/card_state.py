from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from ..attack import EnergyType


@dataclass(frozen=True)
class CardState:
    """Immutable state representation of a card."""

    id: str
    name: str
    hp: int
    max_hp: int
    card_type: Union[str, EnergyType]
    energies: Dict[str, int] = field(default_factory=lambda: {})
    retreat_cost: int = 0
    is_basic: bool = True
    is_ex: bool = False
    evolves_from: Optional[str] = None
    can_evolve: bool = False
    has_used_ability: bool = False
    conditions: List[str] = field(default_factory=lambda: [])

    def serialize(self) -> Dict[str, Any]:
        """Serialize card state to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "type": str(self.card_type),
            "energies": self.energies.copy(),
            "retreat_cost": self.retreat_cost,
            "is_basic": self.is_basic,
            "is_ex": self.is_ex,
            "evolves_from": self.evolves_from,
            "can_evolve": self.can_evolve,
            "has_used_ability": self.has_used_ability,
            "conditions": self.conditions.copy(),
        }

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> "CardState":
        """Deserialize card state from dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            hp=data["hp"],
            max_hp=data["max_hp"],
            card_type=data["type"],
            energies=data.get("energies", {}),
            retreat_cost=data.get("retreat_cost", 0),
            is_basic=data.get("is_basic", True),
            is_ex=data.get("is_ex", False),
            evolves_from=data.get("evolves_from"),
            can_evolve=data.get("can_evolve", False),
            has_used_ability=data.get("has_used_ability", False),
            conditions=data.get("conditions", []),
        )

    def get_total_energy(self) -> int:
        """Get total energy attached to this card."""
        return sum(self.energies.values())

    def with_hp(self, new_hp: int) -> "CardState":
        """Create new state with updated HP."""
        return CardState(
            id=self.id,
            name=self.name,
            hp=max(0, min(new_hp, self.max_hp)),
            max_hp=self.max_hp,
            card_type=self.card_type,
            energies=self.energies,
            retreat_cost=self.retreat_cost,
            is_basic=self.is_basic,
            is_ex=self.is_ex,
            evolves_from=self.evolves_from,
            can_evolve=self.can_evolve,
            has_used_ability=self.has_used_ability,
            conditions=self.conditions,
        )

    def with_energy(self, energy_type: str, amount: int) -> "CardState":
        """Create new state with updated energy."""
        new_energies = self.energies.copy()
        new_energies[energy_type] = new_energies.get(energy_type, 0) + amount
        if new_energies[energy_type] <= 0:
            new_energies.pop(energy_type, None)

        return CardState(
            id=self.id,
            name=self.name,
            hp=self.hp,
            max_hp=self.max_hp,
            card_type=self.card_type,
            energies=new_energies,
            retreat_cost=self.retreat_cost,
            is_basic=self.is_basic,
            is_ex=self.is_ex,
            evolves_from=self.evolves_from,
            can_evolve=self.can_evolve,
            has_used_ability=self.has_used_ability,
            conditions=self.conditions,
        )

    def with_ability_used(self, used: bool = True) -> "CardState":
        """Create new state with ability usage updated."""
        return CardState(
            id=self.id,
            name=self.name,
            hp=self.hp,
            max_hp=self.max_hp,
            card_type=self.card_type,
            energies=self.energies,
            retreat_cost=self.retreat_cost,
            is_basic=self.is_basic,
            is_ex=self.is_ex,
            evolves_from=self.evolves_from,
            can_evolve=self.can_evolve,
            has_used_ability=used,
            conditions=self.conditions,
        )

    def with_evolution_status(self, can_evolve: bool) -> "CardState":
        """Create new state with evolution status updated."""
        return CardState(
            id=self.id,
            name=self.name,
            hp=self.hp,
            max_hp=self.max_hp,
            card_type=self.card_type,
            energies=self.energies,
            retreat_cost=self.retreat_cost,
            is_basic=self.is_basic,
            is_ex=self.is_ex,
            evolves_from=self.evolves_from,
            can_evolve=can_evolve,
            has_used_ability=self.has_used_ability,
            conditions=self.conditions,
        )

    def is_knocked_out(self) -> bool:
        """Check if card is knocked out."""
        return self.hp <= 0
