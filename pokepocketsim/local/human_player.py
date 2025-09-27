from typing import Protocol, List
from ..action import Action


class PlayerInterface(Protocol):
    """Interface that all player types must implement."""

    def choose_action(self, available_actions: List[Action]) -> Action:
        """Choose an action from the available actions."""
        ...

    @property
    def name(self) -> str:
        """Get the player's name."""
        ...

    @property
    def is_human(self) -> bool:
        """Check if this is a human player."""
        ...


class HumanPlayer:
    """Human player that accepts input from console."""

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_human(self) -> bool:
        return True

    def choose_action(self, available_actions: List[Action]) -> Action:
        """Let human player choose an action via console input."""
        if not available_actions:
            raise ValueError("No actions available")

        print(f"\n{self.name}, choose your action:")
        for i, action in enumerate(available_actions):
            print(f"{i + 1}: {action.name}")

        while True:
            try:
                choice = input("Enter your choice (number): ").strip()
                index = int(choice) - 1

                if 0 <= index < len(available_actions):
                    return available_actions[index]
                else:
                    print(
                        f"Please enter a number between 1 and {len(available_actions)}"
                    )

            except ValueError:
                print("Please enter a valid number")
            except KeyboardInterrupt:
                print("\nGame interrupted by user")
                raise
            except EOFError:
                print("\nInput ended, exiting...")
                raise
