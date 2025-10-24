import random
import uuid
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Optional,
    Type,
    cast,
)

from ..mechanics.action import Action, ActionType
from ..utils import color_print as cprint
from ..utils import config
from .card import Card

if TYPE_CHECKING:
    from ..state.player_state import PlayerState
    from .deck import Deck
    from .match import Match

"""
Evaluation of the positions:

Evolving a pokemon = 5
Dealing damage = damage * 0.1
Knocking a pokemon out = 25 if normal, 50 if ex


"""


class Player:
    """
    Represents a player in the game.

    Attributes:
        name (str): The name of the player.
        deck (Deck): The deck of cards the player has.
        hand (List[Card]): The cards currently in the player's hand.
        bench (List[Card]): The cards currently on the player's bench.
        active_card (Optional[Card]): The card currently active for the player.
        points (int): The points the player has scored.
        opponent (Optional[Player]): The opponent player.
        current_energy (Optional[str]): The current energy available to the player.
        has_used_trainer (bool): Indicates if the player has used a trainer card this turn.
        has_added_energy (bool): Indicates if the player has added energy this turn.
    """

    def __init__(self, name: str, deck: "Deck", is_bot: bool = True) -> None:
        self.name: str = name
        self.deck: Deck = deck
        self.is_bot: bool = is_bot
        self.discard_pile: List[Card] = []
        self.hand: List[Any] = [
            card
            for _ in range(min(5, len(self.deck.cards)))
            if (card := self.deck.draw_card()) is not None
        ]
        self.bench: List[Card] = []
        self.active_card: Optional[Card] = None
        self.points: int = 0
        self.opponent: Optional[Player] = None
        self.current_energy: Optional[str] = None
        self.has_used_trainer: bool = False
        self.has_added_energy: bool = False
        self.can_continue: bool = True
        self.id: uuid.UUID = uuid.uuid4()
        self.evaluate_actions: bool = False
        self.print_actions: bool = True

        self.cname = (
            cprint.get(self.name, cprint.RED)
            if self.name == "p1"
            else cprint.get(self.name, cprint.CYAN)
        )

    @property
    def active_card_and_bench(self) -> List[Card]:
        return self.bench + ([self.active_card] if self.active_card is not None else [])

    def set_opponent(self, opponent: "Player") -> None:
        self.opponent = opponent

    def start_turn(self, match: "Match") -> bool:
        self.setup_turn(match)
        return self.process_action_loop(match)

    def choose_action(self, actions: List[Action], print_actions: bool = True) -> int:
        # Print actions
        if print_actions:
            self.print_possible_actions(actions)

        while True:
            try:
                selected_index = int(
                    input("Select an action by entering the corresponding number: ")
                )
                if 0 <= selected_index < len(actions):
                    return selected_index
                else:
                    print(f"Please enter a number between 0 and {len(actions) - 1}.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def process_action_loop(self, match: "Match") -> bool:
        # Gather actions
        actions: List[Action] = self.gather_actions()

        self.can_continue = True

        # Action loop, act -> gather -> act... until attack or actions run out
        while self.can_continue is True:
            if self.evaluate_actions:
                actions = self.process_best_actions(match, actions)
            elif not self.is_bot:
                actions = self.process_user_actions(match, actions)
            else:
                actions = self.process_bot_actions(match, actions)

        return self.handle_knockout_points()

    def handle_knockout_points(self) -> bool:
        if (
            self.opponent is not None
            and self.opponent.active_card is not None
            and self.opponent.active_card.hp <= 0
        ):
            if self.print_actions:
                print(f"{self.opponent.name}'s {self.opponent.active_card.name} knocked out!")

            if self.opponent.active_card.is_ex:
                self.points += 2
            else:
                self.points += 1

            self.opponent.active_card = None

            if self.points >= 3:
                return True
            else:
                return False
        return False

    def print_possible_actions(self, actions: List[Action]) -> None:
        if self.print_actions:
            print(cprint.get("Possible actions:", cprint.YELLOW))
            for i, action in enumerate(actions):
                if not config.debug:
                    action_str = action.name
                else:
                    action_str = str(action)
                print(f"\t{i}: {action_str}")

    def process_best_actions(self, match: "Match", best_actions: List[Action]) -> List[Action]:
        if best_actions:
            actions = self.gather_actions()
            best_action = Action.find_action(actions, best_actions[0])
            self.act_and_regather_actions(match, best_action)
            best_actions.pop(0)
            return best_actions
        else:
            self.can_continue = False
            return []

    def process_user_actions(self, match: "Match", actions: List[Action]) -> List[Action]:
        if actions:
            selected_index = self.choose_action(actions, print_actions=True)
            actions = self.act_and_regather_actions(match, actions[selected_index])
            return actions
        else:
            self.can_continue = False
            return []

    def process_bot_actions(self, match: "Match", actions: List[Action]) -> List[Action]:
        if actions:
            action_index = random.randint(0, len(actions) - 1)
            selected_action = actions.pop(action_index)
            actions = self.act_and_regather_actions(match, selected_action)
            return actions
        else:
            self.can_continue = False
            return []

    def process_rl_actions(
        self, match: "Match", actions: List[Action], action_to_take: int
    ) -> List[Action]:
        if actions:
            if 0 <= action_to_take < len(actions):
                selected_action = actions.pop(action_to_take)
                actions = self.act_and_regather_actions(match, selected_action)
                return actions
            else:
                self.can_continue = False
                return []
        else:
            self.can_continue = False
            return []

    def act_and_regather_actions(self, match: "Match", action: Action) -> List[Action]:
        """
        Process the given action and gather new actions.

        Args:
            match: The current match
            action: The action to process

        Returns:
            A list of new actions
        """
        from ..engine import execute_action, get_available_actions

        # Execute the action using the engine and update can_continue status
        self.can_continue = execute_action(self, action, match)

        # Initialize an empty list of actions
        actions: List[Action] = []

        # Handle SET_ACTIVE_CARD action type
        if action.action_type == ActionType.SET_ACTIVE_CARD:
            # Clear any existing SET_ACTIVE_CARD actions (should be empty already)
            actions = []

            # If past the first two turns, gather new actions
            if match.turn > 2:
                actions = get_available_actions(self)
        # Handle other action types
        else:
            # Gather new actions after processing
            actions = get_available_actions(self)

        return actions

    def remove_item_from_hand(self, item_class: Optional[Type[Any]]) -> None:
        if item_class is None:
            return

        try:
            card_to_remove = next(card for card in self.hand if isinstance(card, item_class))
            self.hand.remove(card_to_remove)
        except StopIteration:
            # Handle the case where no matching card is found
            if self.print_actions:
                print(f"No {item_class.__name__} card found in hand to remove")

    @staticmethod
    def remove_card_from_hand(player: "Player", card_id: uuid.UUID) -> None:
        card = Player.find_by_id(player.hand, card_id)
        if not card:
            raise ValueError("Card not found in hand.")
        player.hand.remove(card)

    def gather_actions(self) -> List[Action]:
        """
        Gather all possible actions for the player.

        This method now delegates to the engine module for action discovery.
        Maintained for backwards compatibility.
        """
        from ..engine import get_available_actions

        return get_available_actions(self)

    def _add_energy_action(self, card_id: uuid.UUID, energy: str) -> None:
        """Helper method to handle adding energy to a card"""
        card = Player.find_by_id(self.active_card_and_bench, card_id)
        if card:
            Card.add_energy(self, card, energy)
            self.has_added_energy = True
        return None

    @staticmethod
    def evolve_and_remove_from_hand(
        player: "Player", card_to_evolve_id: uuid.UUID, evolution_card_id: uuid.UUID
    ) -> None:
        card_to_evolve = Player.find_by_id(player.active_card_and_bench, card_to_evolve_id)
        evolution_card = Player.find_by_id(player.hand, evolution_card_id)

        if card_to_evolve and evolution_card:
            # Evolve using the evolution card's name (string-based card registry)
            try:
                card_to_evolve.evolve(evolution_card.name)
                Player.remove_card_from_hand(player, evolution_card.uuid)
            except Exception as e:
                raise ValueError(
                    f"Failed to evolve {card_to_evolve.name} to {evolution_card.name}: {e}"
                ) from e
        else:
            raise ValueError("Card to evolve or evolution card not found.")

    @staticmethod
    def retreat(player: "Player") -> None:
        if player.active_card is None:
            raise ValueError("No active card to retreat")

        if player.active_card.get_total_energy() < player.active_card.retreat_cost:
            raise ValueError(f"Not enough energy to retreat {player.active_card.name}")

        player.active_card.remove_retreat_cost_energy()
        player.move_active_card_to_bench()

    def move_active_card_to_bench(self) -> None:
        if self.active_card is None:
            raise ValueError("No active card to move to bench")
        if not self.bench:
            raise ValueError("No cards in the bench to switch with")

        old_active_card = self.active_card
        self.bench.append(self.active_card)

        # Ensure the new active card is different from the old one
        eligible_cards = [card for card in self.bench if card != old_active_card]
        if eligible_cards:
            self.active_card = random.choice(eligible_cards)
            self.bench.remove(self.active_card)
            if self.print_actions:
                print(f"{old_active_card.name} retreated, {self.active_card.name} set as active")
        else:
            raise ValueError("No eligible cards in bench to set as active")

    @staticmethod
    def set_active_card_from_hand(player: "Player", card_id: uuid.UUID) -> None:
        card = Player.find_by_id(player.hand, card_id)
        if card and card in player.hand:
            if player.print_actions:
                print(f"Setting active card from hand to {card.name}")
            player.active_card = card
            player.hand.remove(card)
        else:
            raise ValueError("Card not found in hand or invalid")

    def set_active_card_from_bench(self, card: Card) -> None:
        if card not in self.bench:
            raise ValueError(f"Card {card.name} not in bench")

        if self.print_actions:
            print(f"Setting active card from bench to {card.name}")
        self.active_card = card
        self.bench.remove(card)

    @staticmethod
    def add_card_to_bench(player: "Player", card_id: uuid.UUID) -> None:
        card = Player.find_by_id(player.hand, card_id)
        if not card:
            raise ValueError("Card not found in hand")
        if len(player.bench) < 3:
            player.bench.append(card)
            player.hand.remove(card)
        else:
            raise ValueError("Bench is full, cannot add more cards")

    def setup_turn(self, match: "Match") -> None:
        self.has_added_energy = False
        self.has_used_trainer = False

        # For all cards in play, reset ability usage and enable evolution
        if self.active_card:
            for card in self.active_card_and_bench:
                # Reset the ability property for each card
                card.has_used_ability = False
                if match.turn > 2:
                    # Set this property to true, so the turn after placing the card they can be evolved
                    card.can_evolve = True

        # Update conditions
        if self.active_card:
            self.active_card.update_conditions()
        elif match.turn > 2:
            # If active card is knocked out and there are no cards on the bench
            # Game over
            if len(self.bench) == 0:
                return
            else:
                self.set_active_card_from_bench(random.choice(self.bench))

        # Draw card
        drawn_card = self.deck.draw_card()
        if drawn_card is not None:
            self.hand.append(drawn_card)

        # Draw energy
        energy_type = self.deck.draw_energy()
        if energy_type is not None:
            self.current_energy = energy_type

        # DATA COLLECTION: turn number, player name, state before turn
        if match.data_collector:
            match.data_collector.turn = match.turn
            match.data_collector.active_player = self.name
            match.data_collector.match_state_before = match.serialize()

        # Prints
        if self.print_actions:
            active_card_str = str(self.active_card) if self.active_card else "None"
            print(f"{self.cname} active card: " + cprint.get(active_card_str, cprint.GREEN))
            print(f"{self.cname} hand: ")
            for c in self.hand:
                print("\t", c)
            print(f"{self.cname} bench: ")
            for c in self.bench:
                print("\t", c)

    @staticmethod
    def find_by_id(objects: List[Any], target_id: uuid.UUID) -> Optional[Any]:
        for obj in objects:
            if hasattr(obj, "uuid") and obj.uuid == target_id:
                return obj
        return None

    @staticmethod
    def evaluate_player(player: "Player") -> int:
        points = 0
        points += player.points * 25

        # Calculate damage dealt to opponent if opponent exists
        if player.opponent:
            points += int(Player.get_damage_dealt_to_cards(player.opponent) * 0.1)

        points += Player.get_number_of_evolved_cards(player) * 5
        return points

    @staticmethod
    def get_damage_dealt_to_cards(player: "Player") -> int:
        damage_dealt = 0
        if player.active_card is None:
            return 0

        for card in player.active_card_and_bench:
            damage_dealt += card.max_hp - card.hp
        return damage_dealt

    @staticmethod
    def get_number_of_evolved_cards(player: "Player") -> int:
        evolved_cards = 0
        for card in player.active_card_and_bench:
            if not card.is_basic:
                evolved_cards += 1
        return evolved_cards

    def serialize(self) -> Dict[str, Any]:
        """Serialize player state to dictionary."""

        # Helper to serialize items in hand that may be Card instances or Item classes
        def serialize_hand_item(item: Any) -> Dict[str, Any]:
            if hasattr(item, "serialize") and callable(item.serialize):
                return cast(Dict[str, Any], item.serialize())
            elif hasattr(item, "__name__"):
                # It's a class (like Item.Potion), not an instance
                return {"type": "item_class", "name": item.__name__}
            else:
                return {"type": "unknown", "name": str(item)}

        return {
            "name": self.name,
            "hand": [serialize_hand_item(card) for card in self.hand],
            "bench": [card.serialize() for card in self.bench],
            "active_card": self.active_card.serialize() if self.active_card else None,
            "deck": [card.serialize() for card in self.deck.cards],
            "discard_pile": [card.serialize() for card in self.discard_pile],
            "points": self.points,
            "has_used_trainer": self.has_used_trainer,
        }

    def to_state(self) -> "PlayerState":
        """
        Convert Player to PlayerState for serialization.

        Returns:
            PlayerState object representing current player state
        """
        from ..state import PlayerState

        return PlayerState.from_player(self)

    def __repr__(self) -> str:
        return f"Player({self.name}, Hand: {len(self.hand)} cards, Active Card: {self.active_card}, Bench: {len(self.bench)} cards, Points: {self.points})"
