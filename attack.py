class Attack:
    def __init__(self, name, damage, energy_cost):
        self.name = name
        self.damage = damage
        self.energy_cost = energy_cost

    def act(self, player):
        player.opponent.active_card.hp -= self.damage
        if player.opponent.active_card.type is player.active_card.type:
            player.opponent.active_card.hp -= 20

    def able_to_use(self, card):
        for energy_type, required_amount in self.energy_cost.items():
            if card.energies.get(energy_type, 0) < required_amount:
                return False
        return True

    def __repr__(self):
        return f"Attack(Name: {self.name}, Damage: {self.damage}, Energy Cost: {self.energy_cost})"
