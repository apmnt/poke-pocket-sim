from typing import List, Optional, Dict, Any
import uuid
from ..state import GameState, PlayerState, CardState
from ..action import Action, ActionType
from .game_rules import GameRules
from .action_processor import ActionProcessor


class GameEngine:
    """Stateless game engine for Pokemon TCG Pocket simulation."""

    def create_game(
        self,
        player1_name: str,
        player1_deck: List[Dict[str, Any]],
        player2_name: str,
        player2_deck: List[Dict[str, Any]],
    ) -> GameState:
        """Create a new game with two players and their decks."""

        # Generate unique IDs
        game_id = str(uuid.uuid4())
        player1_id = str(uuid.uuid4())
        player2_id = str(uuid.uuid4())

        # Convert deck data to CardState objects
        player1_cards = [
            self._create_card_from_dict(card_data) for card_data in player1_deck
        ]
        player2_cards = [
            self._create_card_from_dict(card_data) for card_data in player2_deck
        ]

        # Create initial player states
        player1 = PlayerState(
            id=player1_id,
            name=player1_name,
            hand=[],
            bench=[],
            active_card=None,
            deck=player1_cards,
            discard_pile=[],
            points=0,
            has_used_trainer=False,
            has_added_energy=False,
            current_energy="psychic",  # Starting energy
        )

        player2 = PlayerState(
            id=player2_id,
            name=player2_name,
            hand=[],
            bench=[],
            active_card=None,
            deck=player2_cards,
            discard_pile=[],
            points=0,
            has_used_trainer=False,
            has_added_energy=False,
            current_energy="psychic",  # Starting energy
        )

        # Draw initial hands (5 cards each)
        player1 = self._draw_initial_hand(player1, 5)
        player2 = self._draw_initial_hand(player2, 5)

        # Create game state
        game_state = GameState(
            id=game_id,
            player1=player1,
            player2=player2,
            current_turn=1,
            current_player_id=player1_id,
            game_over=False,
            winner_id=None,
        )

        return game_state

    def get_available_actions(
        self, game_state: GameState, player_id: str
    ) -> List[Action]:
        """Get all available actions for a player in the current game state."""
        if game_state.current_player_id != player_id:
            return []  # Not this player's turn

        if GameRules.is_game_over(game_state):
            return []  # Game is over

        player = game_state.get_player_by_id(player_id)
        if not player:
            return []

        return self._gather_actions(game_state, player)

    def execute_action(self, game_state: GameState, action: Action) -> GameState:
        """Execute an action and return the new game state."""
        if GameRules.is_game_over(game_state):
            raise ValueError("Cannot execute action: game is over")

        new_state = ActionProcessor.process_action(game_state, action)

        # Check if game is over after action
        if GameRules.is_game_over(new_state):
            winner_id = GameRules.get_winner(new_state)
            new_state = new_state.with_game_over(winner_id)

        return new_state

    def is_game_over(self, game_state: GameState) -> bool:
        """Check if the game is over."""
        return GameRules.is_game_over(game_state)

    def get_winner(self, game_state: GameState) -> Optional[str]:
        """Get the winner of the game if it's over."""
        return GameRules.get_winner(game_state)

    def validate_action(self, game_state: GameState, action: Action) -> bool:
        """Validate if an action is legal in the current game state."""
        return GameRules.validate_action(game_state, action)

    def _create_card_from_dict(self, card_data: Dict[str, Any]) -> CardState:
        """Create a CardState from dictionary data."""
        return CardState(
            id=str(uuid.uuid4()),
            name=card_data["name"],
            hp=card_data["hp"],
            max_hp=card_data["hp"],
            card_type=card_data["type"],
            energies={},
            retreat_cost=card_data.get("retreat_cost", 0),
            is_basic=card_data.get("is_basic", True),
            is_ex=card_data.get("is_ex", False),
            evolves_from=card_data.get("evolves_from"),
            can_evolve=False,
            has_used_ability=False,
            conditions=[],
        )

    def _draw_initial_hand(self, player: PlayerState, num_cards: int) -> PlayerState:
        """Draw initial hand for a player."""
        cards_to_draw = min(num_cards, len(player.deck))
        drawn_cards = player.deck[:cards_to_draw]
        remaining_deck = player.deck[cards_to_draw:]

        return PlayerState(
            id=player.id,
            name=player.name,
            hand=drawn_cards,
            bench=player.bench,
            active_card=player.active_card,
            deck=remaining_deck,
            discard_pile=player.discard_pile,
            points=player.points,
            has_used_trainer=player.has_used_trainer,
            has_added_energy=player.has_added_energy,
            current_energy=player.current_energy,
        )

    def _gather_actions(
        self, game_state: GameState, player: PlayerState
    ) -> List[Action]:
        """Gather all possible actions for a player."""
        actions: List[Action] = []

        # If no active card, must set one from hand
        if not player.active_card:
            for card in player.hand:
                if card.is_basic:
                    actions.append(
                        Action(
                            name=f"Set {card.name} as active card",
                            function=lambda: None,  # Placeholder
                            action_type=ActionType.SET_ACTIVE_CARD,
                            can_continue_turn=True,
                        )
                    )
            return actions

        # Attack actions
        if player.active_card:
            # Simplified - assume card can attack if it has energy
            if player.active_card.get_total_energy() > 0:
                actions.append(
                    Action(
                        name=f"{player.active_card.name} attack",
                        function=lambda: None,
                        action_type=ActionType.ATTACK,
                        can_continue_turn=False,
                    )
                )

        # Add energy action
        if not player.has_added_energy and player.current_energy:
            for card in player.get_all_pokemon():
                actions.append(
                    Action(
                        name=f"Add {player.current_energy} energy to {card.name}",
                        function=lambda: None,
                        action_type=ActionType.ADD_ENERGY,
                        can_continue_turn=True,
                    )
                )

        # Add cards to bench
        for card in player.hand:
            if card.is_basic and len(player.bench) < 3:
                actions.append(
                    Action(
                        name=f"Add {card.name} to bench",
                        function=lambda: None,
                        action_type=ActionType.ADD_CARD_TO_BENCH,
                        can_continue_turn=True,
                    )
                )

        # Retreat action
        if player.active_card and len(player.bench) > 0:
            if GameRules.can_retreat_card(player.active_card):
                actions.append(
                    Action(
                        name=f"Retreat {player.active_card.name}",
                        function=lambda: None,
                        action_type=ActionType.RETREAT,
                        can_continue_turn=True,
                    )
                )

        # End turn action
        actions.append(
            Action(
                name="End turn",
                function=lambda: None,
                action_type=ActionType.END_TURN,
                can_continue_turn=False,
            )
        )

        return actions
