class Item:
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value

    def __repr__(self):
        return f"Item(Name: {self.name}, Description: {self.description}, Value: {self.value})"
