class Ability:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

    def __repr__(self):
        return f"Ability(Name: {self.name}, Effect: {self.effect}, Cooldown: {self.cooldown})"