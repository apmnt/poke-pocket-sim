from typing import TYPE_CHECKING

from ..protocols import ICard

if TYPE_CHECKING:
    pass


class Item:
    """Base class for all item cards."""

    class Potion:
        """Restores 30 HP to a pokemon."""

        def card_able_to_use(self, card: ICard) -> bool:
            """Check if the card can use the potion."""
            return card.hp < card.max_hp

        def use(self, card: ICard) -> None:
            """Use the potion on a card."""
            card.hp = min(card.hp + 20, card.max_hp)
            restored_amount = min(20, card.max_hp - card.hp)
            print(
                f"\t- Potion used on {card.name}. Restored {restored_amount} HP. Current HP: {card.hp}"
            )

        @staticmethod
        def serialize() -> str:
            return "Potion"
