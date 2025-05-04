import random
import uuid
from enum import Enum
from .action import Action, ActionType
from .attack import Attack, EnergyType
from .ability import Ability
from typing import TYPE_CHECKING, Dict, Any, List, Optional, Union, Callable, Type, cast
from .item import Item

if TYPE_CHECKING:
    from .player import Player


class Cards(Enum):
    MEWTWO_EX = "Mewtwo EX"
    RALTS = "Ralts"
    KIRLIA = "Kirlia"
    GARDEVOIR = "Gardevoir"


CARDS_DICT: Dict[Cards, Dict[str, Any]] = {
    Cards.MEWTWO_EX: {
        "hp": 150,
        "type": EnergyType.PSYCHIC,
        "attacks": [Attack.psydrive, Attack.psychic_sphere],
        "retreat_cost": 2,
        "ability": None,
        "weakness": EnergyType.FIGHTING,
        "is_basic": True,
        "is_ex": True,
        "evolves_from": None,
    },
    Cards.RALTS: {
        "hp": 60,
        "type": EnergyType.PSYCHIC,
        "attacks": [Attack.ram],
        "retreat_cost": 1,
        "ability": None,
        "weakness": EnergyType.DARKNESS,
        "is_basic": True,
        "is_ex": False,
        "evolves_from": None,
    },
    Cards.KIRLIA: {
        "hp": 80,
        "type": EnergyType.PSYCHIC,
        "attacks": [Attack.smack],
        "retreat_cost": 1,
        "ability": None,
        "weakness": EnergyType.DARKNESS,
        "is_basic": False,
        "is_ex": False,
        "evolves_from": Cards.RALTS,
    },
    Cards.GARDEVOIR: {
        "hp": 110,
        "type": EnergyType.PSYCHIC,
        "attacks": [Attack.psyshot],
        "retreat_cost": 2,
        "ability": Ability.PsyShadow(),
        "weakness": EnergyType.DARKNESS,
        "is_basic": False,
        "is_ex": False,
        "evolves_from": Cards.KIRLIA,
    },
}


class Card:
    def __init__(
        self,
        name: str,
        hp: int,
        type: EnergyType,
        attacks: List[Callable],
        retreat_cost: int,
        ability: Optional[Any] = None,
        weakness: Optional[EnergyType] = None,
        is_basic: bool = True,
        is_ex: bool = False,
        evolves_from: Optional[Union[Cards, "Card"]] = None,
    ) -> None:
        self.id: uuid.UUID = uuid.uuid4()
        self.name: str = name
        self.max_hp: int = hp
        self.hp: int = hp
        self.type: EnergyType = type
        self.energies: Dict[str, int] = {}
        self.attacks: List[Callable] = attacks
        self.retreat_cost: int = retreat_cost
        self.modifiers: List[Any] = []
        self.ability: Optional[Any] = ability
        self.conditions: List[Any] = []
        self.weakness: Optional[EnergyType] = weakness
        self.is_basic: bool = is_basic
        self.is_ex: bool = is_ex
        self.has_used_ability: bool = False
        self.evolves_from: Optional[Union[Cards, "Card"]] = evolves_from
        self.can_evolve: bool = False

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
        self.conditions = [
            condition for condition in self.conditions if not condition.rid()
        ]

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
            raise ValueError(
                f"Energy count for {energy_enum.value} is already 0 or less."
            )
        self.energies[energy_enum.value] -= 1

    def remove_retreat_cost_energy(self) -> None:
        total_energy_needed = self.retreat_cost
        while total_energy_needed > 0:
            available_energies = [
                energy for energy, count in self.energies.items() if count > 0
            ]
            if not available_energies:
                raise ValueError("Not enough energy to cover the retreat cost.")
            selected_energy = random.choice(available_energies)
            self.remove_energy(EnergyType(selected_energy))
            total_energy_needed -= 1

    def get_total_energy(self) -> int:
        return sum(self.energies.values())

    def evolve(self, evolved_card_name: Cards) -> None:
        """
        Evolves this card into the given evolved card.

        Args:
            evolved_card_name (Cards): The card to evolve into.
        """
        if evolved_card_name not in CARDS_DICT:
            raise ValueError(f"Card {evolved_card_name} does not exist in CARDS_DICT.")

        evolved_card_info = CARDS_DICT[evolved_card_name]

        if (
            evolved_card_info["evolves_from"] is None
            or evolved_card_info["evolves_from"].value != self.name
        ):
            raise ValueError(
                f"{evolved_card_name.value} cannot evolve from {self.name}"
            )

        self.name = evolved_card_name.value
        self.hp = evolved_card_info["hp"] - (self.max_hp - self.hp)
        self.max_hp = evolved_card_info["hp"]
        self.type = evolved_card_info["type"]
        self.attacks = evolved_card_info["attacks"]
        self.retreat_cost = evolved_card_info["retreat_cost"]
        self.ability = evolved_card_info["ability"]
        self.weakness = evolved_card_info["weakness"]
        self.is_basic = evolved_card_info["is_basic"]
        self.is_ex = evolved_card_info["is_ex"]
        self.evolves_from = evolved_card_info["evolves_from"]
        self.can_evolve = False

    def __repr__(self) -> str:
        energies_str = ", ".join(
            f"{energy}: {amount}" for energy, amount in self.energies.items()
        )
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
            if isinstance(self.evolves_from, Cards):
                evolves_from_name = self.evolves_from.value
            else:
                # If evolves_from is a Card object
                other_card = self.evolves_from
                evolves_from_name = other_card.name

        return {
            "name": self.name,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "type": str(self.type),
            "energies": self.energies,
            "retreat_cost": self.retreat_cost,
            "ability": ability_name,
            "weakness": weakness_name,
            "is_basic": self.is_basic,
            "is_ex": self.is_ex,
            "evolves_from": evolves_from_name,
            "can_evolve": self.can_evolve,
            "conditions": [cond.serialize() for cond in self.conditions],
        }

    @staticmethod
    def create_card(card_enum: Cards) -> "Card":
        """
        Factory method to create a card from an enum.

        Args:
            card_enum (Cards): The enum value representing the card.

        Returns:
            Card: A new card instance with properties set according to the enum.
        """
        if card_enum not in CARDS_DICT:
            raise ValueError(f"Card {card_enum} not found in CARDS_DICT.")

        card_info = CARDS_DICT[card_enum]
        return Card(name=card_enum.value, **card_info)
