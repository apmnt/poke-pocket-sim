import random, copy
from typing import List, Optional, TYPE_CHECKING, Dict, Any
import uuid
from action import Action, ActionType
from card import Card, Cards
from item import Item
from supporter import Supporter
from attack import Attack, EnergyType

if TYPE_CHECKING:
    from deck import Deck
    from match import Match

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
        current_energy (Optional[Energy]): The current energy available to the player.
        has_used_trainer (bool): Indicates if the player has used a trainer card this turn.
        has_added_energy (bool): Indicates if the player has added energy this turn.
    """

    def __init__(self, name: str, deck: "Deck"):
        self.name: str = name
        self.deck: "Deck" = deck
        self.discard_pile: List = []
        self.hand: List[Card] = [
            self.deck.draw_card() for _ in range(min(5, len(self.deck.cards)))
        ]
        self.bench: List[Card] = []
        self.active_card: Optional[Card] = None
        self.points: int = 0
        self.opponent: Optional[Player] = None
        self.current_energy: Optional[EnergyType] = None
        self.has_used_trainer: bool = False
        self.has_added_energy: bool = False
        self.can_continue: bool = True
        self.id = uuid.uuid4()
        self.evaluate_actions = False
        self.print_actions = True

    @property
    def active_card_and_bench(self) -> List[Card]:
        return self.bench + [self.active_card]

    def set_opponent(self, opponent: "Player") -> None:
        self.opponent = opponent

    def start_turn(self, match: "Match") -> bool:
        self.reset_for_turn(match.turn)

        # Update conditions
        if self.active_card:
            self.active_card.update_conditions()
        elif match.turn > 2:
            # If active card is knocked out and there are no cards on the bench
            # Game over
            if len(self.bench) == 0:
                return True
            else:
                self.set_active_card_from_bench(random.choice(self.bench))

        # Draw card
        drawn_card = self.deck.draw_card()
        if drawn_card is not None:
            self.hand.append(drawn_card)

        # Draw energy
        self.current_energy = self.deck.draw_energy()

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

        return self.process_action_loop(match=match)

    def process_action_loop(self, match: "Match"):

        # Gather actions
        actions = self.gather_actions()

        # Do random action
        if len(actions) > 0:
            # Print actions
            if self.print_actions:
                print("Possible actions:")
                for action in actions:
                    print("\t", action)
            random_action = actions.pop(random.randint(0, len(actions) - 1))
            self.can_continue = True
        else:
            self.can_continue = False

        # Action loop, act -> gather -> act... until attack or actions run out
        actions = [random_action]
        while self.can_continue is True:
            if actions:
                actions = self.act_and_regather_actions(match, random.choice(actions))
            else:
                self.can_continue = False

        if self.opponent.active_card is not None and self.opponent.active_card.hp <= 0:
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

    def act_and_regather_actions(self, match: "Match", random_action: "Action"):

        self.can_continue = random_action.act(self)

        # DATA COLLECTION: Collect actions
        if match.data_collector:
            match.data_collector.actions_taken.append(random_action.serialize())
        actions = []

        if random_action.action_type == ActionType.SET_ACTIVE_CARD:
            actions = [
                action
                for action in actions
                if action.action_type != ActionType.SET_ACTIVE_CARD
            ]

            if match.turn > 2:
                actions = self.gather_actions()
        else:
            if random_action.action_type == ActionType.ADD_ENERGY:
                self.has_added_energy = True
            if random_action.action_type == ActionType.SUPPORTER:
                self.has_used_trainer = True
                self.remove_item_from_hand(random_action.item_class)
            if random_action.action_type == ActionType.ITEM:
                self.remove_item_from_hand(random_action.item_class)
            actions = self.gather_actions()

        if self.can_continue and len(actions) > 0:
            # Print actions
            if self.print_actions:
                print("Possible actions:")
                for action in actions:
                    print("\t", action)
            random_action = actions.pop(random.randint(0, len(actions) - 1))
        else:
            self.can_continue = False

        return actions

    def remove_item_from_hand(self, item_class: type) -> None:
        try:
            card_to_remove = next(
                card for card in self.hand if isinstance(card, item_class)
            )
            self.hand.remove(card_to_remove)
            self.discard_pile.append(card_to_remove)
        except StopIteration:
            raise ValueError(f"No card of type {item_class} found in hand.")

    @staticmethod
    def remove_card_from_hand(player, card_id: uuid) -> None:
        card = Player.find_by_id(player.hand, card_id)
        if not card:
            raise ValueError(f"Card not found in hand.")
        player.hand.remove(card)

    def gather_actions(self) -> List[Action]:
        actions: List[Action] = []
        if self.active_card is not None:

            # ITEM
            for card in self.hand:
                if isinstance(card, Item.Potion):
                    for pokemon in self.active_card_and_bench:
                        if Item.Potion.card_able_to_use(pokemon):
                            actions.append(
                                Action(
                                    f"Use potion on ({pokemon})",
                                    lambda pokemon=pokemon: Item.Potion.use(pokemon),
                                    ActionType.ITEM,
                                    item_class=Item.Potion,
                                )
                            )

                # Break if trainer has already been used this turn
                if self.has_used_trainer:
                    break

                if isinstance(card, Supporter.Erika):
                    for pokemon in self.active_card_and_bench:
                        if Supporter.Erika.card_able_to_use(pokemon):
                            actions.append(
                                Action(
                                    f"Use Erika on ({pokemon})",
                                    lambda pokemon=pokemon: Supporter.Erika.use(
                                        pokemon
                                    ),
                                    ActionType.ITEM,
                                    item_class=Supporter.Erika,
                                )
                            )

                if isinstance(card, Supporter.Giovanni):
                    actions.append(
                        Action(
                            f"Use Giovanni",
                            lambda player=self: Supporter.Giovanni.use(player),
                            ActionType.ITEM,
                            item_class=Supporter.Giovanni,
                        )
                    )

            # EVOLUTIONS
            for card in self.hand:
                if isinstance(card, Card) and card.evolves_from is not None:
                    for card_to_evolve in self.active_card_and_bench:
                        if (
                            card_to_evolve
                            and card.evolves_from.value == card_to_evolve.name
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

            # ABILITY
            for card in self.active_card_and_bench:
                if (
                    card.ability
                    and not card.has_used_ability
                    and card.ability.able_to_use(self)
                ):
                    ability_action = card.ability.gather_actions(self, card)
                    if ability_action:
                        actions.append(ability_action)

            # ATTACKS
            for attack in self.active_card.attacks:
                if Attack.can_use_attack(self.active_card, attack):
                    actions.append(
                        Action(
                            f"{self.active_card.name} use {attack.__name__}",
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
                        Player.retreat,
                        ActionType.FUNCTION,
                    )
                )

            # ADD CARD TO BENCH
            for card in self.hand:
                if isinstance(card, Card) and card.is_basic:
                    actions.append(
                        Action(
                            f"Add {card.name} to bench",
                            lambda player, card_id=card.id: Player.add_card_to_bench(
                                player, card_id
                            ),
                            ActionType.ADD_CARD_TO_BENCH,
                        )
                    )

            # ADD ENERGY
            if self.has_added_energy is False:
                actions.append(
                    Action(
                        f"Add {self.current_energy} energy to {self.active_card}",
                        lambda card=self.active_card, energy=self.current_energy: Card.add_energy(
                            card, energy
                        ),
                        ActionType.ADD_ENERGY,
                    )
                )
                for card in self.bench:
                    actions.append(
                        Action(
                            f"Add {self.current_energy} energy to {card}",
                            lambda card=card, energy=self.current_energy: Card.add_energy(
                                card, energy
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
                                lambda player, card_id=card.id: Player.set_active_card_from_hand(
                                    player, card_id
                                ),
                                ActionType.SET_ACTIVE_CARD,
                            )
                        )
        return actions

    @staticmethod
    def evolve_and_remove_from_hand(
        player: "Player", card_to_evolve_id: uuid, evolution_card_id: uuid
    ):
        card_to_evolve = Player.find_by_id(
            player.active_card_and_bench, card_to_evolve_id
        )
        evolution_card = Player.find_by_id(player.hand, evolution_card_id)

        if card_to_evolve and evolution_card:
            card_to_evolve.evolve(Cards[evolution_card.name.replace(" ", "_").upper()])
            Player.remove_card_from_hand(player, evolution_card.id)
        else:
            raise ValueError("Card to evolve or evolution card not found.")

    @staticmethod
    def retreat(player) -> None:
        if player.active_card.get_total_energy() < player.active_card.retreat_cost:
            raise Exception(f"Not enough energy to retreat {player.active_card.name}")

        player.active_card.remove_retreat_cost_energy()
        player.move_active_card_to_bench()

    def move_active_card_to_bench(self) -> None:
        if self.active_card is None:
            raise Exception("No active card to move to bench")
        if not self.bench:
            raise Exception("No cards in the bench to switch with")
        old_active_card = self.active_card
        self.bench.append(self.active_card)

        # Ensure the new active card is different from the old one
        self.active_card = random.choice(
            [card for card in self.bench if card != old_active_card]
        )
        self.bench.remove(self.active_card)
        if self.print_actions:
            print(
                f"{old_active_card.name} retreated, {self.active_card.name} set as active"
            )

    @staticmethod
    def set_active_card_from_hand(player: "Player", card_id: uuid) -> None:
        card = Player.find_by_id(player.hand, card_id)
        if card in player.hand:
            if player.print_actions:
                print(f"Setting active card from hand to {card.name}")
            player.active_card = card
            player.hand.remove(card)
        else:
            raise ValueError(f"Card {card.name} not found in hand. Hand: {player.hand}")

    def set_active_card_from_bench(self, card: Card) -> None:
        if self.print_actions:
            print(f"Setting active card from bench to {card.name}")
        self.active_card = card
        self.bench.remove(card)

    @staticmethod
    def add_card_to_bench(player: "Player", card_id: uuid) -> None:
        card = Player.find_by_id(player.hand, card_id)
        if not card:
            raise Exception(f"Card {card.name} not in hand")
        if len(player.bench) < 3:
            player.bench.append(card)
            player.hand.remove(card)

    def reset_for_turn(self, turn: int) -> None:
        self.has_added_energy = False
        self.has_used_trainer = False
        if self.active_card:
            for card in self.active_card_and_bench:
                # Reset the ability property for each card
                card.has_used_ability = False
                if turn > 2:
                    # Set this property to true, so the turn after placing the card they can be evolved
                    card.can_evolve = True

    @staticmethod
    def find_by_id(objects, target_id):
        for obj in objects:
            if obj.id == target_id:
                return obj
        return None

    @staticmethod
    def evaluate_player(player: "Player") -> int:
        points = 0
        points += player.points * 25
        points += Player.get_damage_dealt_to_cards(player.opponent) * 0.1
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
            card: Card
            if not card.is_basic:
                evolved_cards += 1
        return evolved_cards

    def serialize(self: "Player") -> Dict[str, Any]:
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
        return f"Player({self.name}, Hand: {self.hand}, Active Card: {self.active_card}, Bench: {self.bench}, Deck: {self.deck}, Energy Queue: {self.energy_queue}, Points: {self.points}, Has Used Trainer This Turn: {self.has_used_trainer})"
