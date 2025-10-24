"""
State representation for Action entities.
Pure data class for easy serialization and deserialization.
"""

import uuid
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ActionState:
    """Immutable state representation of an Action."""

    id: str  # Unique identifier for this action instance
    name: str
    action_type: str  # ActionType as string
    can_continue_turn: bool
    item_class: Optional[str]  # Class name as string
    # Additional context for execution
    context: Dict[
        str, Any
    ]  # Any additional data needed to execute (e.g., target_card_id, energy_type)

    @classmethod
    def from_action(
        cls, action: Any, action_id: Optional[str] = None, context: Optional[Dict[str, Any]] = None
    ) -> "ActionState":
        """Create ActionState from Action instance."""
        return cls(
            id=action_id or str(uuid.uuid4()),
            name=action.name,
            action_type=(
                action.action_type.name
                if hasattr(action.action_type, "name")
                else str(action.action_type)
            ),
            can_continue_turn=action.can_continue_turn,
            item_class=action.item_class.__name__ if action.item_class else None,
            context=context or {},
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "action_type": self.action_type,
            "can_continue_turn": self.can_continue_turn,
            "item_class": self.item_class,
            "context": self.context,
        }
