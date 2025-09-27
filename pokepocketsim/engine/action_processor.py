import random
from ..state import GameState, PlayerState
from ..action import Action, ActionType
from .game_rules import GameRules


class ActionProcessor:
    """Processes actions and updates game state."""

    @staticmethod
    def process_action(game_state: GameState, action: Action) -> GameState:
        """Process an action and return new game state."""
        if not GameRules.validate_action(game_state, action):
            raise ValueError(f"Invalid action: {action}")

        current_player = game_state.get_current_player()
        opponent = game_state.get_opponent(current_player.id)

        # Process the action based on type
        if action.action_type == ActionType.ATTACK:
            return ActionProcessor._process_attack(
                game_state, action, current_player, opponent
            )

        elif action.action_type == ActionType.ADD_ENERGY:
            return ActionProcessor._process_add_energy(
                game_state, action, current_player
            )

        elif action.action_type == ActionType.EVOLVE:
            return ActionProcessor._process_evolve(game_state, action, current_player)

        elif action.action_type == ActionType.ADD_CARD_TO_BENCH:
            return ActionProcessor._process_add_to_bench(
                game_state, action, current_player
            )

        elif action.action_type == ActionType.SET_ACTIVE_CARD:
            return ActionProcessor._process_set_active(
                game_state, action, current_player
            )

        elif action.action_type == ActionType.RETREAT:
            return ActionProcessor._process_retreat(game_state, current_player)

        elif action.action_type == ActionType.ITEM:
            return ActionProcessor._process_item(game_state, action, current_player)

        elif action.action_type == ActionType.SUPPORTER:
            return ActionProcessor._process_supporter(
                game_state, action, current_player
            )

        elif action.action_type == ActionType.END_TURN:
            return ActionProcessor._process_end_turn(game_state)

        else:
            raise ValueError(f"Unknown action type: {action.action_type}")

    @staticmethod
    def _process_attack(
        game_state: GameState,
        action: Action,
        attacker_player: PlayerState,
        defender_player: PlayerState,
    ) -> GameState:
        """Process an attack action."""
        if not attacker_player.active_card or not defender_player.active_card:
            return game_state

        # Calculate damage
        damage = GameRules.calculate_damage(
            attacker_player.active_card, defender_player.active_card, action.name
        )

        # Apply damage to defender
        new_defender_hp = defender_player.active_card.hp - damage
        updated_defender_card = defender_player.active_card.with_hp(new_defender_hp)

        # Update defender's active card
        updated_defender_player = defender_player.with_active_card(
            updated_defender_card
        )

        # Check for knockout and award points
        if updated_defender_card.is_knocked_out():
            points_to_award = 2 if updated_defender_card.is_ex else 1
            updated_attacker_player = attacker_player.with_points(
                attacker_player.points + points_to_award
            )

            # Move knocked out card to discard
            updated_defender_discard = defender_player.discard_pile + [
                updated_defender_card
            ]
            updated_defender_player = updated_defender_player.with_active_card(None)
            updated_defender_player = PlayerState(
                id=updated_defender_player.id,
                name=updated_defender_player.name,
                hand=updated_defender_player.hand,
                bench=updated_defender_player.bench,
                active_card=None,
                deck=updated_defender_player.deck,
                discard_pile=updated_defender_discard,
                points=updated_defender_player.points,
                has_used_trainer=updated_defender_player.has_used_trainer,
                has_added_energy=updated_defender_player.has_added_energy,
                current_energy=updated_defender_player.current_energy,
            )
        else:
            updated_attacker_player = attacker_player

        # Update game state
        new_game_state = game_state.update_player(
            attacker_player.id, updated_attacker_player
        )
        new_game_state = new_game_state.update_player(
            defender_player.id, updated_defender_player
        )

        return new_game_state

    @staticmethod
    def _process_add_energy(
        game_state: GameState, action: Action, current_player: PlayerState
    ) -> GameState:
        """Process adding energy to a card."""
        if not current_player.current_energy:
            return game_state

        # Extract card name from action
        # Format: "Add {energy_type} energy to {card_name}"
        parts = action.name.split(" energy to ")
        if len(parts) != 2:
            return game_state

        card_name = parts[1]

        # Find the target card (active card or bench)
        target_card = None
        is_active = False

        if current_player.active_card and current_player.active_card.name == card_name:
            target_card = current_player.active_card
            is_active = True
        else:
            for card in current_player.bench:
                if card.name == card_name:
                    target_card = card
                    break

        if not target_card:
            return game_state

        # Add energy to the card
        updated_card = target_card.with_energy(current_player.current_energy, 1)

        # Update player state
        if is_active:
            updated_player = current_player.with_active_card(
                updated_card
            ).with_energy_added(True)
        else:
            # Update bench
            new_bench = [
                updated_card if card.id == target_card.id else card
                for card in current_player.bench
            ]
            updated_player = current_player.with_bench(new_bench).with_energy_added(
                True
            )

        return game_state.update_player(current_player.id, updated_player)

    @staticmethod
    def _process_evolve(
        game_state: GameState, action: Action, current_player: PlayerState
    ) -> GameState:
        """Process evolving a card."""
        # This would need more complex logic to handle evolution
        # For now, return unchanged state
        return game_state

    @staticmethod
    def _process_add_to_bench(
        game_state: GameState, action: Action, current_player: PlayerState
    ) -> GameState:
        """Process adding a card to bench."""
        # Extract card name from action
        card_name = action.name.replace("Add ", "").replace(" to bench", "")

        # Find the card in hand
        target_card = None
        for card in current_player.hand:
            if card.name == card_name and card.is_basic:
                target_card = card
                break

        if not target_card or len(current_player.bench) >= 3:
            return game_state  # Card not found, not basic, or bench full

        # Remove card from hand and add to bench
        new_hand = [card for card in current_player.hand if card.id != target_card.id]
        new_bench = current_player.bench + [target_card]
        updated_player = current_player.with_hand(new_hand).with_bench(new_bench)

        return game_state.update_player(current_player.id, updated_player)

    @staticmethod
    def _process_set_active(
        game_state: GameState, action: Action, current_player: PlayerState
    ) -> GameState:
        """Process setting an active card."""
        # Extract card name from action (we'll match the first card with that name)
        card_name = action.name.replace("Set ", "").replace(" as active card", "")

        # Find the card in hand
        target_card = None
        for card in current_player.hand:
            if card.name == card_name and card.is_basic:
                target_card = card
                break

        if not target_card:
            return game_state  # Card not found or not basic

        # Remove card from hand and set as active
        new_hand = [card for card in current_player.hand if card.id != target_card.id]
        updated_player = current_player.with_hand(new_hand).with_active_card(
            target_card
        )

        return game_state.update_player(current_player.id, updated_player)

    @staticmethod
    def _process_retreat(
        game_state: GameState, current_player: PlayerState
    ) -> GameState:
        """Process retreating the active card."""
        if not current_player.active_card or len(current_player.bench) == 0:
            return game_state

        # Remove energy for retreat cost
        retreat_cost = current_player.active_card.retreat_cost
        updated_card = current_player.active_card

        # Remove energy (simplified - just reduce total energy)
        total_energy = updated_card.get_total_energy()
        if total_energy >= retreat_cost:
            # Move active to bench and pick new active
            new_bench = current_player.bench + [updated_card]
            new_active = new_bench[0]  # Pick first card as new active
            new_bench = new_bench[1:]

            updated_player = current_player.with_active_card(new_active).with_bench(
                new_bench
            )
            return game_state.update_player(current_player.id, updated_player)

        return game_state

    @staticmethod
    def _process_item(
        game_state: GameState, action: Action, current_player: PlayerState
    ) -> GameState:
        """Process using an item."""
        # Item usage would be handled here
        return game_state

    @staticmethod
    def _process_supporter(
        game_state: GameState, action: Action, current_player: PlayerState
    ) -> GameState:
        """Process using a supporter card."""
        updated_player = current_player.with_trainer_used(True)
        return game_state.update_player(current_player.id, updated_player)

    @staticmethod
    def _process_end_turn(game_state: GameState) -> GameState:
        """Process ending the current turn."""
        next_player_id = GameRules.get_next_player_id(game_state)
        new_turn = game_state.current_turn + 1

        # Reset turn-based flags for next player
        next_player = game_state.get_player_by_id(next_player_id)
        if next_player:
            reset_player = next_player.with_trainer_used(False).with_energy_added(False)

            # Draw a card for next player if they have cards in deck
            if reset_player.deck:
                drawn_card = reset_player.deck[0]
                new_hand = reset_player.hand + [drawn_card]
                new_deck = reset_player.deck[1:]
                reset_player = reset_player.with_hand(new_hand)
                reset_player = PlayerState(
                    id=reset_player.id,
                    name=reset_player.name,
                    hand=new_hand,
                    bench=reset_player.bench,
                    active_card=reset_player.active_card,
                    deck=new_deck,
                    discard_pile=reset_player.discard_pile,
                    points=reset_player.points,
                    has_used_trainer=reset_player.has_used_trainer,
                    has_added_energy=reset_player.has_added_energy,
                    current_energy=reset_player.current_energy,
                )

            # Set new current energy
            energy_types = ["psychic", "fire", "water", "electric", "grass", "fighting"]
            new_energy = random.choice(energy_types)
            reset_player = reset_player.with_current_energy(new_energy)

            updated_game_state = game_state.update_player(next_player_id, reset_player)
            updated_game_state = updated_game_state.with_current_turn(
                new_turn
            ).with_current_player(next_player_id)

            return updated_game_state

        return game_state
