import uuid
from action import Action, ActionType


class Card:
    def __init__(
        self,
        name,
        hp,
        energies={},
        attacks=None,
        retreat_cost=0,
        modifiers=None,
        ability=None,
        conditions=None,
        weakness=None,
        is_basic=True,
    ):
        self.id = uuid.uuid4()
        self.name = name
        self.hp = hp
        self.energies = energies
        self.attacks = attacks
        self.retreat_cost = retreat_cost
        self.modifiers = modifiers
        self.ability = ability
        self.conditions = conditions
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

    def get_total_energy(self):
        return sum(self.energies.values())

    def __repr__(self):
        return f"Card({self.name} with {self.hp} hp, {self.get_total_energy()} energy)"
