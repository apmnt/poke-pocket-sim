import uuid
from enum import Enum
from action import Action, ActionType
from attack import Attack


class CardsEnum(Enum):
    MEWTWO_EX = "Mewtwo EX"


CARDS_DICT = {
    CardsEnum.MEWTWO_EX: {
        "hp": 150,
        "attacks": [Attack.psydrive, Attack.psychic_sphere],
    }
}


class Card:
    def __init__(
        self,
        name,
        hp,
        type=None,
        attacks=None,
        retreat_cost=0,
        ability=None,
        weakness=None,
        is_basic=True,
    ):
        self.id = uuid.uuid4()
        self.name = name
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

    def gather_actions(self):
        for attack in self.attacks:
            if attack.able_to_use(self):
                yield Action(
                    f"{self.name} use {attack.name}",
                    attack,
                    ActionType.ATTACK,
                    can_continue_turn=False,
                )

    def add_energy(self, energy):
        if energy in self.energies:
            self.energies[energy] += 1
        else:
            self.energies[energy] = 1

    def remove_energy(self, energy):
        if energy not in self.energies:
            raise ValueError(f"Energy type {energy} not found in energies.")
        if self.energies[energy] <= 0:
            raise ValueError(f"Energy count for {energy} is already 0 or less.")
        self.energies[energy] -= 1

    def get_total_energy(self):
        return sum(self.energies.values())

    def __repr__(self):
        energies_str = ", ".join(
            f"{energy}: {amount}" for energy, amount in self.energies.items()
        )
        return f"Card({self.name} with {self.hp} hp, Energies: {energies_str})"

    @staticmethod
    def create_card(card: CardsEnum):
        return Card(card)
