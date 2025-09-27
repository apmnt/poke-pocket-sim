class Item:
    class Potion:
        def __init__(self):
            self.name = "Potion"

        def card_able_to_use(card):
            return card.hp != card.max_hp

        def serialize():
            return "Potion"

        def use(card):
            card.hp = min(card.hp + 20, card.max_hp)
            restored_amount = min(20, card.max_hp - card.hp)
            print(
                f"\t- Potion used on {card.name}. Restored {restored_amount} HP. Current HP: {card.hp}"
            )
