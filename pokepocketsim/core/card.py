import random
import uuid
from enum import Enum
from .action import Action, ActionType
from .attack import Attack, EnergyType
from .ability import Ability
from typing import TYPE_CHECKING, Dict, Any

if TYPE_CHECKING:
    from player import Player


class Cards(Enum):
    MEWTWO_EX = "Mewtwo EX"
    RALTS = "Ralts"
    KIRLIA = "Kirlia"
    GARDEVOIR = "Gardevoir"


CARDS_DICT = {
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
        name,
        hp,
        type,
        attacks,
        retreat_cost,
        ability=None,
        weakness=None,
        is_basic=True,
        is_ex=False,
        evolves_from=None,
    ):
        self.id = uuid.uuid4()
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.type: EnergyType = type
        self.energies = {}
        self.attacks = attacks
        self.retreat_cost = retreat_cost
        self.modifiers = []
        self.ability: Ability = ability
        self.conditions = []
        self.weakness = weakness
        self.is_basic = is_basic
        self.is_ex = is_ex
        self.has_used_ability = False
        self.evolves_from: Card = evolves_from
        self.can_evolve = False

    def add_condition(self, condition):
        if any(isinstance(cond, condition.__class__) for cond in self.conditions):
            # TODO: sometimes the conditions do not get removed off benched pokemon
            return
        self.conditions.append(condition)

    def remove_condition(self, condition_name):
        self.conditions = [
            condition for condition in self.conditions if condition != condition_name
        ]

    def update_conditions(self):
        self.conditions = [
            condition for condition in self.conditions if not condition.rid()
        ]

    @staticmethod
    def add_energy(player: "Player", card: "Card", energy):
        if energy in card.energies:
            card.energies[energy] += 1
        else:
            card.energies[energy] = 1
        if player.print_actions:
            print(f"Current energies of {card.name} {card.energies}")

    def remove_energy(self, energy_enum):
        energy = energy_enum.value
        if energy not in self.energies:
            raise ValueError(f"Energy type {energy_enum.value} not found in energies.")
        if self.energies[energy_enum.value] <= 0:
            raise ValueError(
                f"Energy count for {energy_enum.value} is already 0 or less."
            )
        self.energies[energy_enum.value] -= 1

    def remove_retreat_cost_energy(self):
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

    def get_total_energy(self):
        return sum(self.energies.values())

    def evolve(self, evolved_card_name: str) -> None:
        """
        Evolves this card into the given evolved card.

        Args:
            evolved_card_name (str): The card to evolve into.
        """
        if evolved_card_name not in CARDS_DICT.keys():
            raise ValueError(f"Card {evolved_card_name} does not exist in CARDS_DICT.")

        evolved_card_info = CARDS_DICT[evolved_card_name]

        if evolved_card_info["evolves_from"].value != self.name:
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

    def __repr__(self):
        energies_str = ", ".join(
            f"{energy}: {amount}" for energy, amount in self.energies.items()
        )
        return f"Card({self.name} with {self.hp} hp, Energies: {energies_str})"

    def serialize(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "name": self.name,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "type": self.type.value,
            "energies": self.energies,
            "attacks": [attack.__name__ for attack in self.attacks],
            "retreat_cost": self.retreat_cost,
            "ability": self.ability.name if self.ability else None,
            "conditions": [condition.serialize() for condition in self.conditions],
            "weakness": self.weakness.name if self.weakness else None,
            "is_basic": self.is_basic,
            "is_ex": self.is_ex,
            "has_used_ability": self.has_used_ability,
            "evolves_from": self.evolves_from.name if self.evolves_from else None,
            "can_evolve": self.can_evolve,
        }

    @staticmethod
    def create_card(card_enum: Cards):
        if card_enum not in CARDS_DICT:
            raise ValueError(f"Card {card_enum} does not exist in CARDS_DICT.")

        card_info = CARDS_DICT[card_enum]
        return Card(name=card_enum.value, **card_info)
