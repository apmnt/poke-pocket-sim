import random, copy
from typing import (
    List,
    Optional,
    TYPE_CHECKING,
    Dict,
    Any,
    Union,
    Type,
    Callable,
    cast,
    Protocol,
)
import uuid
from .action import Action, ActionType
from .card import Card, Cards
from .item import Item
from .supporter import Supporter
from .attack import Attack
from .attack_common import EnergyType
from .protocols import ICard, IPlayer

if TYPE_CHECKING:
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
        self.deck: "Deck" = deck
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
        self.opponent: Optional["Player"] = None
        self.current_energy: Optional[str] = None
        self.has_used_trainer: bool = False
        self.has_added_energy: bool = False
        self.can_continue: bool = True
        self.id: uuid.UUID = uuid.uuid4()
        self.evaluate_actions: bool = False
        self.print_actions: bool = True

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
                print(
                    f"{self.opponent.name}'s {self.opponent.active_card.name} knocked out!"
                )

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
            print("Possible actions:")
            for i, action in enumerate(actions):
                print(f"\t{i}: {action}")

    def process_best_actions(
        self, match: "Match", best_actions: List[Action]
    ) -> List[Action]:
        if best_actions:
            actions = self.gather_actions()
            best_action = Action.find_action(actions, best_actions[0])
            self.act_and_regather_actions(match, best_action)
            best_actions.pop(0)
            return best_actions
        else:
            self.can_continue = False
            return []

    def process_user_actions(
        self, match: "Match", actions: List[Action]
    ) -> List[Action]:
        if actions:
            selected_index = self.choose_action(actions, print_actions=True)
            actions = self.act_and_regather_actions(match, actions[selected_index])
            return actions
        else:
            self.can_continue = False
            return []

    def process_bot_actions(
        self, match: "Match", actions: List[Action]
    ) -> List[Action]:
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

        # Execute the action and update can_continue status
        self.can_continue = action.act(self)

        # DATA COLLECTION: Collect actions
        if match.data_collector:
            match.data_collector.actions_taken.append(action.serialize())

        # Initialize an empty list of actions
        actions: List[Action] = []

        # Handle SET_ACTIVE_CARD action type
        if action.action_type == ActionType.SET_ACTIVE_CARD:
            # Clear any existing SET_ACTIVE_CARD actions (should be empty already)
            actions = []

            # If past the first two turns, gather new actions
            if match.turn > 2:
                actions = self.gather_actions()
        # Handle other action types
        else:
            # Update energy status if energy was added
            if action.action_type == ActionType.ADD_ENERGY:
                self.has_added_energy = True

            # Update trainer status if a supporter was used
            if action.action_type == ActionType.SUPPORTER:
                self.has_used_trainer = True
                if action.item_class:
                    self.remove_item_from_hand(action.item_class)

            # Remove used items from hand
            if action.action_type == ActionType.ITEM:
                if action.item_class:
                    self.remove_item_from_hand(action.item_class)

            # Gather new actions after processing
            actions = self.gather_actions()

        return actions

    def remove_item_from_hand(self, item_class: Optional[Type[Any]]) -> None:
        if item_class is None:
            return

        try:
            card_to_remove = next(
                card for card in self.hand if isinstance(card, item_class)
            )
            self.hand.remove(card_to_remove)
        except StopIteration:
            # Handle the case where no matching card is found
            if self.print_actions:
                print(f"No {item_class.__name__} card found in hand to remove")

    @staticmethod
    def remove_card_from_hand(player: "Player", card_id: uuid.UUID) -> None:
        card = Player.find_by_id(player.hand, card_id)
        if not card:
            raise ValueError(f"Card not found in hand.")
        player.hand.remove(card)

    def gather_actions(self) -> List[Action]:
        """Gather all possible actions for the player."""
        actions: List[Action] = []
        if self.active_card is not None:
            # Get all potion cards
            potion_cards = [
                card
                for card in self.hand
                if hasattr(card, "card_able_to_use")
                and card.__class__.__name__ == "Potion"
            ]

            # Process potion cards
            for potion_card in potion_cards:
                for pokemon in self.active_card_and_bench:
                    potion = Item.Potion()
                    if potion.card_able_to_use(cast(ICard, pokemon)):
                        actions.append(
                            Action(
                                f"Use potion on ({pokemon})",
                                lambda pokemon=pokemon: potion.use(
                                    cast(ICard, pokemon)
                                ),
                                ActionType.ITEM,
                                item_class=Item.Potion,
                            )
                        )

            # Process supporter cards if trainers haven't been used
            if not self.has_used_trainer:
                # Get all Erika cards
                erika_cards = [
                    card
                    for card in self.hand
                    if hasattr(card, "card_able_to_use")
                    and card.__class__.__name__ == "Erika"
                ]

                # Process Erika cards
                for _ in erika_cards:
                    for pokemon in self.active_card_and_bench:
                        erika = Supporter.Erika()
                        # Using structural typing without needing cast
                        # TODO: Refactor the trainer classes to use the same interface
                        if hasattr(pokemon, "type") and erika.card_able_to_use(pokemon):  # type: ignore
                            actions.append(
                                Action(
                                    f"Use Erika on ({pokemon})",
                                    lambda card=pokemon: erika.use(
                                        card
                                    ),  # Renamed parameter to avoid variable capture issues
                                    ActionType.SUPPORTER,
                                    item_class=Supporter.Erika,
                                )
                            )

                # Get all Giovanni cards
                giovanni_cards = [
                    card
                    for card in self.hand
                    if hasattr(card, "name") and card.__class__.__name__ == "Giovanni"
                ]

                # Process Giovanni cards
                if giovanni_cards:
                    giovanni = Supporter.Giovanni()
                    actions.append(
                        Action(
                            f"Use Giovanni",
                            lambda player=self: giovanni.use(player),
                            ActionType.SUPPORTER,
                            item_class=Supporter.Giovanni,
                        )
                    )

            # EVOLUTIONS
            for card in self.hand:
                if isinstance(card, Card) and card.evolves_from is not None:
                    for card_to_evolve in self.active_card_and_bench:
                        # Check if evolves_from has a value attribute and conditions match
                        try:
                            evolves_from_name = getattr(
                                card.evolves_from, "value", None
                            )
                            if (
                                card_to_evolve
                                and evolves_from_name
                                and evolves_from_name == card_to_evolve.name
                                and card_to_evolve.can_evolve
                            ):
                                actions.append(
                                    Action(
                                        f"Evolve {card_to_evolve.name} to {card.name}",
                                        lambda player=self, card_to_evolve_id=card_to_evolve.id, evolution_card_id=card.id: Player.evolve_and_remove_from_hand(
                                            player,
                                            card_to_evolve_id,
                                            evolution_card_id,
                                        ),
                                        ActionType.EVOLVE,
                                    )
                                )
                        except AttributeError:
                            # Skip cards with invalid evolves_from attribute
                            continue

            # ABILITY
            for card in self.active_card_and_bench:
                if (
                    card.ability
                    and not card.has_used_ability
                    and hasattr(card.ability, "able_to_use")
                    and card.ability.able_to_use(self)
                ):
                    ability_actions = card.ability.gather_actions(self, card)
                    for ability_action in ability_actions:
                        actions.append(ability_action)

            # ATTACKS
            for attack in self.active_card.attacks:
                if Attack.can_use_attack(self.active_card, attack):
                    actions.append(
                        Action(
                            f"{self.active_card.name} use {getattr(attack, '__name__', str(attack))}",
                            attack,
                            ActionType.ATTACK,
                            can_continue_turn=False,
                        )
                    )

            # RETREAT
            if (
                self.active_card.get_total_energy() >= self.active_card.retreat_cost
                and len(self.bench) > 0
            ):
                actions.append(
                    Action(
                        f"Retreat active card ({self.active_card})",
                        lambda player=self: Player.retreat(player),
                        ActionType.FUNCTION,
                    )
                )

            # ADD CARD TO BENCH
            for card in self.hand:
                if isinstance(card, Card) and card.is_basic:
                    actions.append(
                        Action(
                            f"Add {card.name} to bench",
                            lambda player=self, card_id=card.id: Player.add_card_to_bench(
                                player, card_id
                            ),
                            ActionType.ADD_CARD_TO_BENCH,
                        )
                    )

            # ADD ENERGY
            if self.has_added_energy is False and self.current_energy is not None:
                for card in self.active_card_and_bench:
                    actions.append(
                        Action(
                            f"Add {self.current_energy} energy to {card.name}",
                            lambda player=self, card_id=card.id, energy=self.current_energy: self._add_energy_action(
                                card_id, energy
                            ),
                            ActionType.ADD_ENERGY,
                        )
                    )
        # SET AN ACTIVE CARD
        else:
            if not self.active_card:
                for card in self.hand:
                    if isinstance(card, Card) and card.is_basic:
                        actions.append(
                            Action(
                                f"Set {card.name} as active card",
                                lambda player=self, card_id=card.id: Player.set_active_card_from_hand(
                                    player, card_id
                                ),
                                ActionType.SET_ACTIVE_CARD,
                            )
                        )

        # END TURN
        if self.active_card is not None and len(actions) > 0:
            actions.append(
                Action(
                    "End turn",
                    lambda player: setattr(player, "can_continue", False),
                    ActionType.END_TURN,
                    can_continue_turn=False,
                )
            )

        return actions

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
        card_to_evolve = Player.find_by_id(
            player.active_card_and_bench, card_to_evolve_id
        )
        evolution_card = Player.find_by_id(player.hand, evolution_card_id)

        if card_to_evolve and evolution_card:
            # Convert name to enum format and evolve
            enum_name = evolution_card.name.replace(" ", "_").upper()
            try:
                card_enum = Cards[enum_name]
                card_to_evolve.evolve(card_enum)
                Player.remove_card_from_hand(player, evolution_card.id)
            except KeyError:
                raise ValueError(f"Cannot find card enum for {evolution_card.name}")
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
                print(
                    f"{old_active_card.name} retreated, {self.active_card.name} set as active"
                )
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
            raise ValueError(f"Card not found in hand or invalid")

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
            raise ValueError(f"Card not found in hand")
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
            print(f"{self.name} active card: {self.active_card}")
            print(f"{self.name} hand: ")
            for c in self.hand:
                print("\t", c)
            print(f"{self.name} bench: ")
            for c in self.bench:
                print("\t", c)

    @staticmethod
    def find_by_id(objects: List[Any], target_id: uuid.UUID) -> Optional[Any]:
        for obj in objects:
            if hasattr(obj, "id") and obj.id == target_id:
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
        return {
            "name": self.name,
            "hand": [card.serialize() for card in self.hand],
            "bench": [card.serialize() for card in self.bench],
            "active_card": self.active_card.serialize() if self.active_card else None,
            "deck": [card.serialize() for card in self.deck.cards],
            "discard_pile": [card.serialize() for card in self.discard_pile],
            "points": self.points,
            "has_used_trainer": self.has_used_trainer,
        }

    def __repr__(self) -> str:
        return f"Player({self.name}, Hand: {len(self.hand)} cards, Active Card: {self.active_card}, Bench: {len(self.bench)} cards, Points: {self.points})"
