import random
import uuid
from enum import Enum
from action import Action, ActionType
from attack import Attack, EnergyType


class Cards(Enum):
    MEWTWO_EX = "Mewtwo EX"


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
    }
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

    def gather_actions(self):
        for attack in self.attacks:
            if Attack.can_use_attack(self, attack):
                yield Action(
                    f"{self.name} use {attack.__name__}",
                    attack,
                    ActionType.ATTACK,
                    can_continue_turn=False,
                )

    def add_condition(self, condition):
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
            available_energies = list(self.energies.keys())
            
            if not available_energies:
                raise ValueError("Not enough energy to cover the retreat cost.")
            selected_energy = random.choice(available_energies)
            self.energies[selected_energy] -= 1
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
