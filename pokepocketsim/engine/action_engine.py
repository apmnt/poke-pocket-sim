"""
Game engine for Pokemon Pocket Simulator.
Decouples game logic from UI by separating action discovery from execution.
"""

from typing import TYPE_CHECKING, List, Optional, cast

from ..core.card import Card
from ..mechanics.action import Action, ActionType
from ..mechanics.attack import Attack
from ..mechanics.item import Item
from ..mechanics.supporter import Supporter

if TYPE_CHECKING:
    from ..core.match import Match
    from ..core.player import Player


def get_available_actions(player: "Player") -> List[Action]:
    """
    Discover and return all available actions for the given player.
    This method does NOT execute any actions, only discovers them.

    Args:
        player: The player to get actions for

    Returns:
        List of Action objects representing all possible actions
    """
    actions: List[Action] = []

    if player.active_card is not None:
        # ITEM ACTIONS: Potion cards
        potion_cards = [
            card
            for card in player.hand
            if hasattr(card, "card_able_to_use") and card.__class__.__name__ == "Potion"
        ]

        for _ in potion_cards:
            from ..protocols import ICard

            for pokemon in player.active_card_and_bench:
                potion = Item.Potion()
                if potion.card_able_to_use(cast(ICard, pokemon)):
                    current_potion = Item.Potion()  # Create instance for lambda
                    actions.append(
                        Action(
                            f"Use potion on ({pokemon})",
                            lambda pokemon=pokemon, p=current_potion: p.use(cast(ICard, pokemon)),
                            ActionType.ITEM,
                            item_class=Item.Potion,
                        )
                    )

        # SUPPORTER ACTIONS (if not used this turn)
        if not player.has_used_trainer:
            # Erika cards
            erika_cards = [
                card
                for card in player.hand
                if hasattr(card, "card_able_to_use") and card.__class__.__name__ == "Erika"
            ]

            for _ in erika_cards:
                for pokemon in player.active_card_and_bench:
                    erika = Supporter.Erika()
                    if erika.card_able_to_use(pokemon):
                        current_erika = Supporter.Erika()  # Create instance for lambda
                        actions.append(
                            Action(
                                f"Use Erika on ({pokemon})",
                                lambda card=pokemon, e=current_erika: e.use(card),
                                ActionType.SUPPORTER,
                                item_class=Supporter.Erika,
                            )
                        )

            # Giovanni cards
            giovanni_cards = [
                card
                for card in player.hand
                if hasattr(card, "name") and card.__class__.__name__ == "Giovanni"
            ]

            if giovanni_cards:
                giovanni = Supporter.Giovanni()
                actions.append(
                    Action(
                        "Use Giovanni",
                        lambda player=player: giovanni.use(player),
                        ActionType.SUPPORTER,
                        item_class=Supporter.Giovanni,
                    )
                )

        # EVOLUTION ACTIONS
        for card in player.hand:
            if isinstance(card, Card) and card.evolves_from is not None:
                for card_to_evolve in player.active_card_and_bench:
                    evolves_from_name = (
                        card.evolves_from if isinstance(card.evolves_from, str) else None
                    )

                    if (
                        card_to_evolve
                        and evolves_from_name
                        and evolves_from_name == card_to_evolve.name
                        and card_to_evolve.can_evolve
                    ):
                        from ..core.player import Player as PlayerClass

                        actions.append(
                            Action(
                                f"Evolve {card_to_evolve.name} to {card.name}",
                                lambda player=player, card_to_evolve_id=card_to_evolve.uuid, evolution_card_id=card.uuid: PlayerClass.evolve_and_remove_from_hand(
                                    player,
                                    card_to_evolve_id,
                                    evolution_card_id,
                                ),
                                ActionType.EVOLVE,
                            )
                        )

        # ABILITY ACTIONS
        for card in player.active_card_and_bench:
            if (
                card.ability
                and not card.has_used_ability
                and hasattr(card.ability, "able_to_use")
                and card.ability.able_to_use(player)
            ):
                ability_actions = card.ability.gather_actions(player, card)
                for ability_action in ability_actions:
                    actions.append(ability_action)

        # ATTACK ACTIONS
        for attack in player.active_card.attacks:
            if Attack.can_use_attack(player.active_card, attack):
                actions.append(
                    Action(
                        f"{player.active_card.name} use {getattr(attack, '__name__', str(attack))}",
                        attack,
                        ActionType.ATTACK,
                        can_continue_turn=False,
                    )
                )

        # RETREAT ACTIONS
        if (
            player.active_card.get_total_energy() >= player.active_card.retreat_cost
            and len(player.bench) > 0
        ):
            from ..core.player import Player as PlayerClass

            actions.append(
                Action(
                    f"Retreat active card ({player.active_card})",
                    lambda player=player: PlayerClass.retreat(player),
                    ActionType.FUNCTION,
                )
            )

        # ADD CARD TO BENCH
        for card in player.hand:
            if isinstance(card, Card) and card.is_basic:
                from ..core.player import Player as PlayerClass

                actions.append(
                    Action(
                        f"Add {card.name} to bench",
                        lambda player=player, card_id=card.uuid: PlayerClass.add_card_to_bench(
                            player, card_id
                        ),
                        ActionType.ADD_CARD_TO_BENCH,
                    )
                )

        # ADD ENERGY
        if player.has_added_energy is False and player.current_energy is not None:
            for card in player.active_card_and_bench:
                actions.append(
                    Action(
                        f"Add {player.current_energy} energy to {card.name}",
                        lambda player=player, card_id=card.uuid, energy=player.current_energy: player._add_energy_action(
                            card_id, energy
                        ),
                        ActionType.ADD_ENERGY,
                    )
                )

    # SET AN ACTIVE CARD (when no active card exists)
    else:
        if not player.active_card:
            from ..core.player import Player as PlayerClass

            for card in player.hand:
                if isinstance(card, Card) and card.is_basic:
                    actions.append(
                        Action(
                            f"Set {card.name} as active card",
                            lambda player=player, card_id=card.uuid: PlayerClass.set_active_card_from_hand(
                                player, card_id
                            ),
                            ActionType.SET_ACTIVE_CARD,
                        )
                    )

    # END TURN ACTION
    if player.active_card is not None and len(actions) > 0:
        actions.append(
            Action(
                "End turn",
                lambda player=player: setattr(player, "can_continue", False),
                ActionType.END_TURN,
                can_continue_turn=False,
            )
        )

    return actions


def execute_action(player: "Player", action: Action, match: Optional["Match"] = None) -> bool:
    """
    Execute the given action for the player.

    Args:
        player: The player performing the action
        action: The action to execute
        match: Optional match context for data collection and GUI updates

    Returns:
        bool: True if the player can continue their turn, False otherwise
    """
    # Execute the action and get continuation status
    can_continue = action.act(player)

    # DATA COLLECTION: Collect actions
    if match and match.data_collector:
        match.data_collector.actions_taken.append(action.serialize())

    # Update GUI after each action
    if match:
        from ..utils import config

        if config.gui_enabled and hasattr(match, "gui"):
            try:
                match.gui.update_gui(match.starting_player, match.second_player)
            except Exception:
                # GUI failures should not interrupt game logic
                pass

    # Update player state based on action type
    if action.action_type == ActionType.ADD_ENERGY:
        player.has_added_energy = True

    if action.action_type == ActionType.SUPPORTER:
        player.has_used_trainer = True
        if action.item_class:
            player.remove_item_from_hand(action.item_class)

    if action.action_type == ActionType.ITEM:
        if action.item_class:
            player.remove_item_from_hand(action.item_class)

    return can_continue
