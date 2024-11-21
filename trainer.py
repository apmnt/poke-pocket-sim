class Trainer:
    def __init__(self, name, pokemon=None, items=None):
        self.name = name
        self.pokemon = pokemon if pokemon is not None else []
        self.items = items if items is not None else []

    def __repr__(self):
        return (
            f"Trainer(Name: {self.name}, Pokemon: {self.pokemon}, Items: {self.items})"
        )
