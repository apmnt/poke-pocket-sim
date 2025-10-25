import json
import random
import uuid
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Union

from ..mechanics.ability import Ability
from ..mechanics.attack import Attack, EnergyType

if TYPE_CHECKING:
    from .player import Player


def _parse_card_data(card_data: List[Dict[str, Dict[str, Any]]]) -> List[Dict[str, Dict[str, Any]]]:
    """Process raw card data from JSON to convert strings to enum values."""
    for entry in card_data:
        pokemon = entry.get("Pokemon", {})
        if not pokemon:
            continue

        # Convert energy type from string to enum
        if "energy_type" in pokemon:
            pokemon["energy_type"] = getattr(EnergyType, pokemon["energy_type"])

        # Convert weakness from string to enum if present
        if "weakness" in pokemon and pokemon["weakness"]:
            pokemon["weakness"] = getattr(EnergyType, pokemon["weakness"])

        # Deep copy attacks list to avoid shared references
        if "attacks" in pokemon:
            pokemon["attacks"] = [attack.copy() for attack in pokemon["attacks"]]

        # Convert ability from string to instance if present
        if "ability" in pokemon and pokemon["ability"]:
            pokemon["ability"] = getattr(Ability, pokemon["ability"])()

        # Normalize retreat_cost: accept either an int or a list (compute length)
        if "retreat_cost" in pokemon:
            rc = pokemon["retreat_cost"]
            if isinstance(rc, list):
                # JSON format contains list of cost entries, use length as int cost
                pokemon["retreat_cost"] = len(rc)
            else:
                pokemon["retreat_cost"] = int(rc)

    return card_data


def _load_cards() -> List[Dict[str, Dict[str, Any]]]:
    """Load and parse the card database from JSON file."""
    pkg_dir = Path(__file__).parent.parent  # Go up to pokepocketsim/
    json_path = pkg_dir / "data" / "database.json"

    try:
        with open(json_path, encoding="utf-8") as f:
            raw_data = json.load(f)
        return _parse_card_data(raw_data)
    except (OSError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Failed to load card database from {json_path}: {e}") from e


# Load card data when module is imported
CARDS_DATA = _load_cards()


def find_card_by_name(name: str) -> Dict[str, Any]:
    """Find a card dict by its 'name' field in CARDS_DATA.

    The incoming JSON format will be a list where each item is an
    object like {"Pokemon": {...}}. This function returns the inner card dict
    for the matching name.
    """
    for entry in CARDS_DATA:
        if not entry:
            continue
        # each entry is expected to have a single top-level key like 'Pokemon'
        inner = next(iter(entry.values()))
        if inner.get("name") == name:
            return inner
    raise ValueError(f"Card {name} not found in CARDS_DATA")


class Card:
    def __init__(
        self,
        id: str,
        name: str,
        hp: int,
        energy_type: EnergyType,
        attacks: List[Dict[str, Any]],  # attack metadata dicts from JSON
        retreat_cost: int,
        ability: Optional[Any] = None,
        weakness: Optional[EnergyType] = None,
        is_ex: bool = False,
        stage: int = 0,
        evolves_from: Optional[Union[str, "Card"]] = None,
    ) -> None:
        self.id: str = id
        self.uuid: uuid.UUID = uuid.uuid4()
        self.name: str = name
        self.max_hp: int = hp
        self.hp: int = hp
        self.energy_type: EnergyType = energy_type
        self.energies: Dict[str, int] = {}
        
        # attacks is expected to be a list of attack metadata dicts
        if attacks is None:
            self.attacks: List[Dict[str, Any]] = []
        else:
            self.attacks = [attack.copy() for attack in attacks]
        self.retreat_cost: int = retreat_cost
        self.modifiers: List[Any] = []
        self.ability: Optional[Any] = ability
        self.conditions: List[Any] = []
        self.weakness: Optional[EnergyType] = weakness
        self.is_ex: bool = is_ex
        self.stage: int = stage
        self.has_used_ability: bool = False
        self.evolves_from: Optional[Union[str, Card]] = evolves_from
        self.can_evolve: bool = False

    @property
    def is_basic(self) -> bool:
        """Computed property: a card is Basic when its stage is 0."""
        return getattr(self, "stage", 0) == 0

    def add_condition(self, condition: Any) -> None:
        if any(isinstance(cond, condition.__class__) for cond in self.conditions):
            # TODO: sometimes the conditions do not get removed off benched pokemon
            return
        self.conditions.append(condition)

    def remove_condition(self, condition_name: str) -> None:
        self.conditions = [
            condition for condition in self.conditions if condition != condition_name
        ]

    def update_conditions(self) -> None:
        self.conditions = [condition for condition in self.conditions if not condition.rid()]

    @staticmethod
    def add_energy(player: "Player", card: "Card", energy: str) -> None:
        if energy in card.energies:
            card.energies[energy] += 1
        else:
            card.energies[energy] = 1
        if player.print_actions:
            print(f"Current energies of {card.name} {card.energies}")

    def remove_energy(self, energy_enum: EnergyType) -> None:
        energy = energy_enum.value
        if energy not in self.energies:
            raise ValueError(f"Energy type {energy_enum.value} not found in energies.")
        if self.energies[energy_enum.value] <= 0:
            raise ValueError(f"Energy count for {energy_enum.value} is already 0 or less.")
        self.energies[energy_enum.value] -= 1

    def remove_retreat_cost_energy(self) -> None:
        total_energy_needed = self.retreat_cost
        while total_energy_needed > 0:
            available_energies = [energy for energy, count in self.energies.items() if count > 0]
            if not available_energies:
                raise ValueError("Not enough energy to cover the retreat cost.")
            selected_energy = random.choice(available_energies)
            self.remove_energy(EnergyType(selected_energy))
            total_energy_needed -= 1

    def get_total_energy(self) -> int:
        return sum(self.energies.values())

    def evolve(self, evolved_card_name: str) -> None:
        """Evolves this card into the given evolved card.

        Args:
            evolved_card_name (str): The name of the card to evolve into.
        """
        try:
            evolved_card_info = find_card_by_name(evolved_card_name)
        except ValueError as e:
            raise ValueError(f"Card {evolved_card_name} does not exist in CARDS_DATA.") from e

        # evolved_card_info['evolves_from'] is expected to be the name (str)
        evolves_from_value = evolved_card_info.get("evolves_from")
        if evolves_from_value is None or evolves_from_value != self.name:
            raise ValueError(f"{evolved_card_name} cannot evolve from {self.name}")

        # apply evolution
        self.name = evolved_card_info["name"]
        self.hp = evolved_card_info["hp"] - (self.max_hp - self.hp)
        self.max_hp = evolved_card_info["hp"]
        self.energy_type = evolved_card_info["energy_type"]
        self.attacks = evolved_card_info.get("attacks", [])

        try:
            self.attacks = [a.copy() for a in evolved_card_info["attacks"]]
        except Exception:
            self.attacks = []

        self.retreat_cost = evolved_card_info["retreat_cost"]
        self.ability = evolved_card_info["ability"]
        self.weakness = evolved_card_info["weakness"]
        self.is_ex = evolved_card_info["is_ex"]
        self.stage = evolved_card_info["stage"]
        self.evolves_from = evolved_card_info["evolves_from"]
        self.can_evolve = False

    def __repr__(self) -> str:
        energies_str = ", ".join(f"{energy}: {amount}" for energy, amount in self.energies.items())
        return f"Card({self.name} with {self.hp} hp, Energies: {energies_str})"

    def serialize(self) -> Dict[str, Any]:
        ability_name = None
        if self.ability:
            ability_name = getattr(self.ability, "name", None)

        weakness_name = None
        if self.weakness:
            weakness_name = self.weakness.name

        evolves_from_name = None
        if self.evolves_from:
            if isinstance(self.evolves_from, str):
                evolves_from_name = self.evolves_from
            else:
                # If evolves_from is a Card object
                other_card = self.evolves_from
                evolves_from_name = getattr(other_card, "name", str(other_card))

        return {
            "id": self.id,  # Card's printed ID (e.g. set number)
            "uuid": str(self.uuid),  # Instance-unique identifier
            "name": self.name,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "type": str(self.energy_type),
            "energies": self.energies,
            "retreat_cost": self.retreat_cost,
            "ability": ability_name,
            "weakness": weakness_name,
            "is_basic": self.is_basic,
            "is_ex": self.is_ex,
            "stage": self.stage,
            "evolves_from": evolves_from_name,
            "can_evolve": self.can_evolve,
            "conditions": [cond.serialize() for cond in self.conditions],
        }

    @staticmethod
    def create_card(card_name: str) -> "Card":
        """
        Factory method to create a card from a name or Cards class constant.

        Args:
            card_name (Union[str, Cards]): The name of the card to create, either as a string
                                        or a Cards class constant.

        Returns:
            Card: A new card instance with properties set according to the name.
        """
        try:
            card_info = find_card_by_name(card_name)
        except ValueError as e:
            raise ValueError(f"Card {card_name} not found in CARDS_DATA.") from e

        return Card(**card_info)
