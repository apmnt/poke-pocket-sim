from enum import Enum
from attack import Attack


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


class Action:
    def __init__(
        self, name, function, action_type, can_continue_turn=True, item_class=None
    ):
        self.name = name
        self.function = function
        self.action_type = action_type
        self.can_continue_turn = can_continue_turn
        self.item_class = item_class

    def act(self, player):
        print(f"Acting: {self.name}")
        if self.action_type == ActionType.ATTACK:
            self.function(player)
        elif self.action_type == ActionType.ITEM:
            for card in player.hand:
                if isinstance(card, type(self.item_class)):
                    player.hand.remove(card)
                    break
            self.function()
        elif self.action_type == ActionType.ADD_CARD_TO_BENCH:
            self.function(player)        
        elif self.action_type == ActionType.FUNCTION:
            self.function(player)
        else:
            self.function()
        return self.can_continue_turn

    def __repr__(self):
        return f"Action(Name: {self.name}, Type: {self.action_type})"
