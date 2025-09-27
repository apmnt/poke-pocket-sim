import random
from .player import Player
from .attack import Attack
from .action import Action, ActionType
from .data_collector import DataCollector
from typing import List, Optional, Tuple, Dict, Any
import copy


class Match:
    """
    A class to represent a match between two players.

    Attributes:
        starting_player (Player): The player who will start the match.
        second_player (Player): The player who will play second.
        turn (int): The current turn number, starting at 0.
        game_over (bool): A flag indicating whether the game is over.

    Methods:
    -------
    start_turn():
        Advances the match by one turn, alternating between players.
        Checks if the game is over after each turn.
    __repr__():
        Returns a string representation of the match.
    """

    def __init__(
        self,
        starting_player: Player,
        second_player: Player,
        data_collector: Optional[DataCollector] = None,
    ):
        """
        Initializes a match between two players.

        Args:
            starting_player (Player): The player who will start the match.
            second_player (Player): The player who will play second.
        """
        starting_player.set_opponent(second_player)
        second_player.set_opponent(starting_player)
        self.starting_player: Player = starting_player
        self.second_player: Player = second_player

        self.data_collector: Optional[DataCollector] = data_collector

        self.turn: int = 0  # The current turn number
        self.game_over = False

    def start_turn(self):
        """
        Starts a new turn in the match.

        This method increments the turn counter and determines which player goes first.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        self.turn += 1
        if self.turn % 2 == 0:
            active_player = self.second_player
            non_active_player = self.starting_player
        else:
            active_player = self.starting_player
            non_active_player = self.second_player
        print(
            f"\n\nTurn {self.turn}, {active_player.name}'s turn, {self.starting_player.name} {self.starting_player.points} - {self.second_player.name} {self.second_player.points}"
        )

        self.game_over = active_player.start_turn(self)

        # DATA COLLECTOR: Save the state after and collect the properties
        if self.data_collector:
            self.data_collector.match_state_after = self.serialize()
            self.data_collector.add_data_from_properties()

        if self.game_over:
            print()
            print("------ GAME OVER -------")
            print(
                f"{active_player.name} won {active_player.points}-{non_active_player.points}"
            )
            print(f"after {self.turn} turns")

        if self.turn > 100:
            print()
            print("Game terminated at turn 1000 due to infinite loop")
            self.game_over = True

    def play_one_match(self):
        """
        Plays one complete match until the game is over.
        """
        while not self.game_over:
            self.start_turn()

        if self.data_collector:
            self.data_collector.save_to_csv()

    def serialize(self) -> Dict[str, Any]:
        return {
            "turn": self.turn,
            "player1": self.starting_player.serialize(),
            "player2": self.second_player.serialize(),
            # Add other relevant match state data
        }

    def get_best_actions_for_player(self, player: Player) -> List[Action]:
        """
        Determines the best sequence of actions for a given player by simulating all possible turn actions
        and evaluating their outcomes.

        Args:
            player (Player): The player for whom the best actions are being determined.

        Returns:
            List[Action]: The sequence of actions that has the highest evaluation score.
        """
        all_actions = self.simulate_turn_actions(player)
        best_evaluation = float("-inf")
        best_sequence = []

        for evaluation, sequence, _ in all_actions:
            if evaluation > best_evaluation:
                best_evaluation = evaluation
                best_sequence = sequence

        return best_sequence

    def simulate_turn_actions(self, player: Player) -> List[Tuple[int, List[Action]]]:
        """
        Simulates all possible combinations of actions for this turn.

        Args:
            match (Match): The current match.

        Returns:
            List[Tuple[int, List[Action]]]: A list of all possible sequences of actions.
        """
        match_copy = copy.deepcopy(self)
        match_copy.turn += 1

        player_copy = copy.deepcopy(player)
        player_copy.print_actions = False
        player_copy.evaluate_actions = False

        player_copy.setup_turn(self.turn)

        # Update conditions
        if player_copy.active_card:
            player_copy.active_card.update_conditions()
        elif self.turn > 2:
            # If active card is knocked out and there are no cards on the bench
            # Game over
            if len(player_copy.bench) == 0:
                raise Exception("Player lost this turn")
            else:
                player_copy.set_active_card_from_bench(random.choice(player_copy.bench))

        # Draw card
        drawn_card = player_copy.deck.draw_card()
        if drawn_card is not None:
            player_copy.hand.append(drawn_card)

        all_sequences: List[Tuple[int, List[Action]]] = []
        self._simulate_recursive(
            match_copy,
            player_copy,
            current_sequence=[],
            all_sequences=all_sequences,
            depth=0,
        )

        # Print all possible sequences of actions
        unique_sequences = []
        seen_sequences = set()

        for sequence in all_sequences:
            sequence_tuple = tuple(action.name for action in sequence[1])
            if sequence_tuple not in seen_sequences:
                seen_sequences.add(sequence_tuple)
                unique_sequences.append(sequence)

        return unique_sequences

    @staticmethod
    def _simulate_recursive(
        match: "Match",
        player: "Player",
        current_sequence: List[Action],
        all_sequences: List[Tuple[int, List[Action]]],
        depth: int,
    ) -> None:
        """
        Recursively simulates actions and collects all possible sequences.

        Args:
            match (Match): The current match.
            player (Player): The player whose actions are being simulated.
            actions (List[Action]): The list of actions to simulate.
            current_sequence (List[Action]): The current sequence of actions taken.
            all_sequences (List[List[Action]]): The list to store all possible sequences of actions.
        """

        if depth > 10:
            return

        actions = player.gather_actions()

        for action in actions:
            player_copy = copy.deepcopy(player)
            match_copy = copy.deepcopy(match)
            new_actions = player_copy.act_and_regather_actions(match_copy, action)
            new_sequence = current_sequence + [action]
            if new_actions and player_copy.can_continue:
                Match._simulate_recursive(
                    match_copy,
                    player_copy,
                    new_sequence,
                    all_sequences,
                    depth=depth + 1,
                )
            else:
                # If no new actions, add the current sequence to all_sequences
                evaluation = Player.evaluate_player(player_copy)
                all_sequences.append((evaluation, new_sequence, depth))

    def __repr__(self):
        return f"Match(Players: {self.players}, Deck: {self.deck})"
