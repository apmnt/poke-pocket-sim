from typing import List
import random
from ..action import Action


class CPUPlayer:
    """CPU player with configurable difficulty."""

    def __init__(self, name: str, difficulty: str = "medium"):
        self._name = name
        self.difficulty = difficulty

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_human(self) -> bool:
        return False

    def choose_action(self, available_actions: List[Action]) -> Action:
        """Choose an action based on difficulty level."""
        if not available_actions:
            raise ValueError("No actions available")

        if self.difficulty == "easy":
            return self._choose_random_action(available_actions)
        elif self.difficulty == "medium":
            return self._choose_smart_action(available_actions)
        elif self.difficulty == "hard":
            return self._choose_optimal_action(available_actions)
        else:
            return self._choose_random_action(available_actions)

    def _choose_random_action(self, actions: List[Action]) -> Action:
        """Choose a random action."""
        return random.choice(actions)

    def _choose_smart_action(self, actions: List[Action]) -> Action:
        """Choose action with basic strategy."""
        # Prioritize attacks over other actions
        attack_actions = [a for a in actions if "attack" in a.name.lower()]
        if attack_actions:
            return random.choice(attack_actions)

        # Avoid ending turn if there are other options
        non_end_actions = [a for a in actions if "end turn" not in a.name.lower()]
        if non_end_actions:
            return random.choice(non_end_actions)

        return random.choice(actions)

    def _choose_optimal_action(self, actions: List[Action]) -> Action:
        """Choose action with advanced strategy (placeholder for now)."""
        # This would implement more sophisticated AI logic
        # For now, use smart action logic
        return self._choose_smart_action(actions)
