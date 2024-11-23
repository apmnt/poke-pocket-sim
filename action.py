from enum import Enum
from attack import Attack


class ActionType(Enum):
    FUNCTION = 1
    ATTACK = 2
    SET_ACTIVE_CARD = 3
    ADD_ENERGY = 4
    ADD_CARD_TO_BENCH = 5


class Action:
    def __init__(self, name, function, action_type, can_continue_turn=True):
        self.name = name
        self.function = function
        self.action_type = action_type
        self.can_continue_turn = can_continue_turn

    def act(self, player):
        print(f"Acting: {self.name}")
        if self.action_type == ActionType.ATTACK:
            self.function(player)
        else:
            self.function()
        return self.can_continue_turn

    def __repr__(self):
        return f"Action(Name: {self.name}, Type: {self.action_type})"
