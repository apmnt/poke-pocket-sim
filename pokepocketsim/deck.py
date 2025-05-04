import random
import uuid
from typing import List, Optional, Any, Union, Type
from .card import Card


class Deck:
    def __init__(
        self, energy_types: List[str], cards: Optional[List[Any]] = None
    ) -> None:
        self.uid: uuid.UUID = uuid.uuid4()
        self.energy_types: List[str] = energy_types
        self.cards: List[Any] = cards if cards is not None else []

    def _add_card(self, card: Card) -> None:
        """Internal method to add a Card object to the deck."""
        self.cards.append(card)

    def add_card(self, card: Card) -> None:
        """Add a Card object to the deck.

        This method is maintained for backward compatibility.

        Args:
            card: The Card object to add to the deck.
        """
        self.add(card)

    def _add_item(self, item_class: Type) -> None:
        """Internal method to add an item to the deck.

        Args:
            item_class: The item class to add to the deck.
        """
        self.cards.append(item_class)

    def add(self, card_or_item: Any) -> None:
        """Add a card or item to the deck.

        This is the general method to add any type of card to the deck.
        It automatically detects the type and handles it appropriately.

        Args:
            card_or_item: The card or item to add to the deck.
        """
        if isinstance(card_or_item, Card):
            self._add_card(card_or_item)
        else:
            # For Item classes and future card types
            self._add_item(card_or_item)

    def draw_card(self) -> Optional[Any]:
        if self.cards:
            return self.cards.pop(0)
        else:
            return None

    def draw_energy(self) -> str:
        return random.choice(self.energy_types)

    def __repr__(self) -> str:
        return "Deck:\n" + "\n".join(str(card) for card in self.cards)
