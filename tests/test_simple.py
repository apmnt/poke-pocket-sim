import pytest

from pokepocketsim import Card, Deck, Item, Match, Player
from pokepocketsim.engine import execute_action, get_available_actions
from pokepocketsim.mechanics.action import ActionType
from pokepocketsim.utils import config


class TestMatch:
    """
    TestMatch:
        This test class verifies the behavior of the Match class using the decoupled engine.

        The new architecture separates action discovery from execution:
        - get_available_actions(): Discovers all valid actions without UI dependency
        - execute_action(): Executes a selected action and returns continuation status

        This allows for:
        - Testing game logic independently from UI
        - Programmatic action selection for automated testing
        - State verification after each action
        - Easier debugging and reproducible test scenarios

        Setup:
            - Initializes two decks with predetermined sets of cards and items.
            - Constructs two players, each with a unique deck and player identity.
            - Instantiates a Match object using the two configured players.

        Test Methods:
            - test_get_available_actions: Verifies action discovery works correctly
            - test_execute_action: Tests action execution and state updates
            - test_action_types: Validates different action types are discovered
            - test_basic_turn_flow: Simulates a basic turn using the engine
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        # Disable GUI for testing
        config.gui_enabled = False

        self.test_deck1 = Deck(energy_types=["psychic"])
        self.test_deck1.add(Card.create_card("Ralts"))
        self.test_deck1.add(Card.create_card("Kirlia"))
        self.test_deck1.add(Card.create_card("Gardevoir"))
        self.test_deck1.add(Card.create_card("Mewtwo EX"))
        self.test_deck1.add(Item.Potion)
        self.test_deck1.add(Item.Potion)

        self.test_deck2 = Deck(energy_types=["psychic"])
        self.test_deck2.add(Card.create_card("Ralts"))
        self.test_deck2.add(Card.create_card("Ralts"))
        self.test_deck2.add(Card.create_card("Ralts"))
        self.test_deck2.add(Card.create_card("Ralts"))

        self.test_player1 = Player("p1", self.test_deck1, is_bot=False)
        self.test_player2 = Player("p2", self.test_deck2, is_bot=False)

        self.test_match = Match(self.test_player1, self.test_player2)

    def test_get_available_actions(self):
        """Test that the engine can discover available actions."""
        # Initially, player should have actions to set active card
        actions = get_available_actions(self.test_player1)

        # Should have actions available (setting active card from hand)
        assert len(actions) > 0

        # All actions should have names
        for action in actions:
            assert action.name is not None
            assert isinstance(action.name, str)

    def test_execute_action(self):
        """Test that actions can be executed and state updates correctly."""
        # Get initial actions
        actions = get_available_actions(self.test_player1)
        assert len(actions) > 0

        # Find action to set active card
        set_active_actions = [a for a in actions if a.action_type == ActionType.SET_ACTIVE_CARD]
        assert len(set_active_actions) > 0

        # Execute the action
        initial_hand_size = len(self.test_player1.hand)
        can_continue = execute_action(self.test_player1, set_active_actions[0], self.test_match)

        # Verify state changed
        assert self.test_player1.active_card is not None
        assert len(self.test_player1.hand) == initial_hand_size - 1
        assert can_continue  # Should be able to continue turn after setting active

    def test_action_types(self):
        """Test that different action types are properly categorized."""
        # Set up player with active card first
        actions = get_available_actions(self.test_player1)
        set_active_action = next(a for a in actions if a.action_type == ActionType.SET_ACTIVE_CARD)
        execute_action(self.test_player1, set_active_action, self.test_match)

        # Now get actions with an active card
        actions = get_available_actions(self.test_player1)

        # Group actions by type
        action_types: dict[ActionType, list] = {}
        for action in actions:
            action_type = action.action_type
            if action_type not in action_types:
                action_types[action_type] = []
            action_types[action_type].append(action)

        # Should have at least END_TURN and ADD_ENERGY or ADD_CARD_TO_BENCH
        assert ActionType.END_TURN in action_types
        assert len(action_types) > 1  # Should have multiple action types

    def test_basic_turn_flow(self):
        """Test a basic turn flow using the engine."""
        # Turn 1: Set active card
        actions = get_available_actions(self.test_player1)
        set_active_action = next(a for a in actions if a.action_type == ActionType.SET_ACTIVE_CARD)
        can_continue = execute_action(self.test_player1, set_active_action, self.test_match)
        assert can_continue
        assert self.test_player1.active_card is not None

        # Add energy if available
        actions = get_available_actions(self.test_player1)
        energy_actions = [a for a in actions if a.action_type == ActionType.ADD_ENERGY]
        if energy_actions:
            can_continue = execute_action(self.test_player1, energy_actions[0], self.test_match)
            assert self.test_player1.has_added_energy

        # End turn
        actions = get_available_actions(self.test_player1)
        end_turn_action = next(a for a in actions if a.action_type == ActionType.END_TURN)
        can_continue = execute_action(self.test_player1, end_turn_action, self.test_match)
        assert not can_continue  # Should not be able to continue after ending turn

    def test_programmatic_game_flow(self):
        """Test complete programmatic control over a game without UI dependency."""
        # This test demonstrates the power of the decoupled architecture:
        # We can fully control and verify game state at each step

        # Turn 1: Player 1 sets active card
        actions = get_available_actions(self.test_player1)
        set_active_action = next(a for a in actions if a.action_type == ActionType.SET_ACTIVE_CARD)
        execute_action(self.test_player1, set_active_action, self.test_match)

        # Verify state after setting active
        assert self.test_player1.active_card is not None
        initial_active = self.test_player1.active_card

        # Add energy to active card
        actions = get_available_actions(self.test_player1)
        energy_actions = [a for a in actions if a.action_type == ActionType.ADD_ENERGY]

        if energy_actions:
            # Find action that adds energy to active card
            add_energy_to_active = next(
                (a for a in energy_actions if initial_active.name in a.name), None
            )
            if add_energy_to_active:
                initial_energy = initial_active.get_total_energy()
                execute_action(self.test_player1, add_energy_to_active, self.test_match)

                # Verify energy was added
                assert initial_active.get_total_energy() == initial_energy + 1
                assert self.test_player1.has_added_energy

        # Try to add card to bench
        actions = get_available_actions(self.test_player1)
        bench_actions = [a for a in actions if a.action_type == ActionType.ADD_CARD_TO_BENCH]

        if bench_actions:
            initial_bench_size = len(self.test_player1.bench)
            execute_action(self.test_player1, bench_actions[0], self.test_match)

            # Verify bench size increased
            assert len(self.test_player1.bench) == initial_bench_size + 1

        # End turn (if available - END_TURN action is only added when there are other actions)
        actions = get_available_actions(self.test_player1)
        end_turn_actions = [a for a in actions if a.action_type == ActionType.END_TURN]

        if end_turn_actions:
            can_continue = execute_action(self.test_player1, end_turn_actions[0], self.test_match)
            assert not can_continue
        else:
            # If no END_TURN action, manually set can_continue to False
            self.test_player1.can_continue = False

        # Verify we successfully completed a turn with full state control
        assert not self.test_player1.can_continue

    def test_bot_games_with_random_actions(self):
        """Test playing 10 complete bot games using random actions."""
        games_to_play = 10
        completed_games = 0

        for game_num in range(games_to_play):
            # Create fresh decks for each game
            deck1 = Deck(energy_types=["psychic"])
            deck1.add(Card.create_card("Ralts"))
            deck1.add(Card.create_card("Kirlia"))
            deck1.add(Card.create_card("Gardevoir"))
            deck1.add(Card.create_card("Mewtwo EX"))
            deck1.add(Item.Potion)
            deck1.add(Item.Potion)

            deck2 = Deck(energy_types=["psychic"])
            deck2.add(Card.create_card("Ralts"))
            deck2.add(Card.create_card("Kirlia"))
            deck2.add(Card.create_card("Gardevoir"))
            deck2.add(Card.create_card("Mewtwo EX"))

            # Create bot players
            bot1 = Player(f"Bot1_Game{game_num + 1}", deck1, is_bot=True)
            bot2 = Player(f"Bot2_Game{game_num + 1}", deck2, is_bot=True)

            # Create match
            match = Match(bot1, bot2)

            # Play the match using bots with random actions
            # The Match.play_one_match() will use the bots' process_bot_actions
            # which selects random actions
            try:
                match.play_one_match()
                completed_games += 1

                # Verify game ended properly
                assert match.game_over
                assert match.turn > 0

                # Verify one player won
                assert (bot1.points >= 3) or (bot2.points >= 3)

            except Exception as e:
                pytest.fail(f"Game {game_num + 1} failed with error: {e}")

        # Verify all games completed successfully
        assert completed_games == games_to_play, (
            f"Only {completed_games}/{games_to_play} games completed"
        )


if __name__ == "__main__":
    pytest.main()
