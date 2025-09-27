from typing import Optional
from ..state import GameState, PlayerState, CardState
from ..action import Action, ActionType


class GameRules:
    """Pure functions for game rule validation and checking."""

    @staticmethod
    def is_game_over(game_state: GameState) -> bool:
        """Check if the game is over."""
        # Don't check for no pokemon in play during early setup turns
        if game_state.current_turn <= 2:
            return (
                game_state.game_over
                or game_state.player1.points >= 3
                or game_state.player2.points >= 3
            )

        return (
            game_state.game_over
            or game_state.player1.points >= 3
            or game_state.player2.points >= 3
            or GameRules._player_has_no_pokemon_in_play(game_state.player1)
            or GameRules._player_has_no_pokemon_in_play(game_state.player2)
            or game_state.current_turn > 100  # Prevent infinite games
        )

    @staticmethod
    def get_winner(game_state: GameState) -> Optional[str]:
        """Determine the winner of the game."""
        if not GameRules.is_game_over(game_state):
            return None

        if game_state.winner_id:
            return game_state.winner_id

        # Check points
        if game_state.player1.points >= 3:
            return game_state.player1.id
        if game_state.player2.points >= 3:
            return game_state.player2.id

        # Check if opponent has no pokemon
        if GameRules._player_has_no_pokemon_in_play(game_state.player1):
            return game_state.player2.id
        if GameRules._player_has_no_pokemon_in_play(game_state.player2):
            return game_state.player1.id

        # Timeout - determine by points
        if game_state.current_turn > 100:
            if game_state.player1.points > game_state.player2.points:
                return game_state.player1.id
            elif game_state.player2.points > game_state.player1.points:
                return game_state.player2.id
            else:
                return None  # Draw

        return None

    @staticmethod
    def _player_has_no_pokemon_in_play(player: PlayerState) -> bool:
        """Check if player has no pokemon in play."""
        return player.active_card is None and len(player.bench) == 0

    @staticmethod
    def can_use_attack(card_state: CardState, attack_name: str) -> bool:
        """Check if a card can use a specific attack."""
        # TODO: Finish this
        return card_state.get_total_energy() > 0  # Simplified check

    @staticmethod
    def can_evolve_card(card_state: CardState, evolution_name: str) -> bool:
        """Check if a card can evolve to the specified evolution."""
        return (
            card_state.can_evolve
            and not card_state.is_knocked_out()
            and card_state.evolves_from is not None  # TODO: logic will need refinement
        )

    @staticmethod
    def can_retreat_card(card_state: CardState) -> bool:
        """Check if a card can retreat."""
        return card_state.get_total_energy() >= card_state.retreat_cost

    @staticmethod
    def validate_action(game_state: GameState, action: Action) -> bool:
        """Validate if an action is legal in the current game state."""
        current_player = game_state.get_current_player()

        if action.action_type == ActionType.ATTACK:
            if not current_player.active_card:
                return False
            return GameRules.can_use_attack(current_player.active_card, action.name)

        elif action.action_type == ActionType.ADD_ENERGY:
            return (
                not current_player.has_added_energy
                and current_player.current_energy is not None
            )

        elif action.action_type == ActionType.SUPPORTER:
            return not current_player.has_used_trainer

        elif action.action_type == ActionType.RETREAT:
            if not current_player.active_card:
                return False
            return (
                GameRules.can_retreat_card(current_player.active_card)
                and len(current_player.bench) > 0
            )

        # TODO: more validation rules as needed
        return True

    @staticmethod
    def get_next_player_id(game_state: GameState) -> str:
        """Get the ID of the next player to play."""
        if game_state.current_player_id == game_state.player1.id:
            return game_state.player2.id
        return game_state.player1.id

    @staticmethod
    def calculate_damage(
        attacker: CardState, defender: CardState, attack_name: str
    ) -> int:
        """Calculate damage from an attack (simplified)."""
        # TODO: check attack definitions, weaknesses, resistances, etc.
        base_damage = 20  # Default damage

        # TODO: weakness/resistance logic here
        # TODO: condition modifiers here

        return base_damage
