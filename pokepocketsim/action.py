from enum import Enum
from .attack import Attack
from typing import TYPE_CHECKING, List, Optional, Any, Dict, Callable, Type, Union

if TYPE_CHECKING:
    from .player import Player


class ActionType(Enum):
    FUNCTION = 1
    ATTACK = 2
    SET_ACTIVE_CARD = 3
    ADD_ENERGY = 4
    ADD_CARD_TO_BENCH = 5
    ITEM = 6
    SUPPORTER = 7
    ABILITY = 8
    EVOLVE = 9
    RETREAT = 10
    END_TURN = 11


class Action:
    def __init__(
        self,
        name: str,
        function: Callable[..., Any],
        action_type: ActionType,
        can_continue_turn: bool = True,
        item_class: Optional[Type[Any]] = None,
    ) -> None:
        self.name: str = name
        self.function: Callable[..., Any] = function
        self.action_type: ActionType = action_type
        self.can_continue_turn: bool = can_continue_turn
        self.item_class: Optional[Type[Any]] = item_class

    def act(self, player: "Player") -> bool:
        if player.print_actions:
            print(f"Acting: {self.name}")
        if self.action_type == ActionType.ITEM:
            for card in player.hand:
                if isinstance(card, type(self.item_class)):
                    player.hand.remove(card)
                    break
            self.function()
        elif self.action_type == ActionType.ADD_ENERGY:
            self.function()
        else:
            self.function(player)
        return self.can_continue_turn

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "action_type": self.action_type.name,
            "can_continue_turn": self.can_continue_turn,
            "item_class": self.item_class.__name__ if self.item_class else None,
        }

    def serialize(self) -> Dict[str, Any]:
        return self.to_dict()

    def __repr__(self) -> str:
        return f"Action(Name: {self.name}, Type: {self.action_type})"

    @staticmethod
    def find_action(action_list: List["Action"], action_to_find: "Action") -> "Action":
        for action in action_list:
            if all(
                [
                    action.name == action_to_find.name,
                    action.action_type == action_to_find.action_type,
                    (
                        action.item_class == action_to_find.item_class
                        if action_to_find.item_class
                        else True
                    ),
                ]
            ):
                return action
        raise Exception(
            f"No action found, tried to find \n{action_to_find} from \n{action_list}"
        )
