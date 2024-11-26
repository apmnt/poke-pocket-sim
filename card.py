import random
import uuid
from enum import Enum
from action import Action, ActionType
from attack import Attack, EnergyType
from ability import Ability


class Cards(Enum):
    MEWTWO_EX = "Mewtwo EX"
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
    },
    Cards.GARDEVOIR: {
        "hp": 110,
        "type": EnergyType.PSYCHIC,
        "attacks": [Attack.psyshot],
        "retreat_cost": 2,
        "ability": Ability.PsyShadow(),
        "weakness": EnergyType.DARKNESS,
        "is_basic": True,
        "is_ex": False,
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
    ):
        self.id = uuid.uuid4()
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.type = type
        self.energies = {}
        self.attacks = attacks
        self.retreat_cost = retreat_cost
        self.modifiers = []
        self.ability = ability
        self.conditions = []
        self.weakness = weakness
        self.is_basic = is_basic
        self.is_ex = is_ex
        self.has_used_ability = False

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

    def add_energy(self, energy):
        if energy in self.energies:
            self.energies[energy] += 1
        else:
            self.energies[energy] = 1

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

    def __repr__(self):
        energies_str = ", ".join(
            f"{energy}: {amount}" for energy, amount in self.energies.items()
        )
        return f"Card({self.name} with {self.hp} hp, Energies: {energies_str})"

    @staticmethod
    def create_card(card_enum: Cards):
        if card_enum not in CARDS_DICT:
            raise ValueError(f"Card {card_enum} does not exist in CARDS_DICT.")

        card_info = CARDS_DICT[card_enum]
        return Card(name=card_enum.value, **card_info)
