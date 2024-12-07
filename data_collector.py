import json
import csv
from typing import List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from action import Action


class DataCollector:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = []
        self.turn = None
        self.active_player = None
        self.match_state_before = None
        self.actions_taken: List = None
        self.match_state_after = None
        self.actions_taken = []

    def add_data(
        self,
        turn: int,
        active_player: str,
        match_state_before: Dict[str, Any],
        actions_taken: List[Dict[str, Any]],
        match_state_after: Dict[str, Any],
    ):
        self.data.append(
            {
                "turn": turn,
                "active_player": active_player,
                "match_state_before": json.dumps(match_state_before),
                "actions_taken": json.dumps(actions_taken),
                "match_state_after": json.dumps(match_state_after),
            }
        )

    def add_data_from_properties(self):
        self.data.append(
            {
                "turn": self.turn,
                "active_player": self.active_player,
                "match_state_before": json.dumps(self.match_state_before),
                "actions_taken": json.dumps(self.actions_taken),
                "match_state_after": json.dumps(self.match_state_after),
            }
        )
        self.turn = None
        self.active_player = None
        self.match_state_before = None
        self.actions_taken = []
        self.match_state_after = None

    def save_to_csv(self):
        with open(self.file_path, mode="w", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "turn",
                    "active_player",
                    "match_state_before",
                    "actions_taken",
                    "match_state_after",
                ],
            )
            writer.writeheader()
            for row in self.data:
                writer.writerow(row)
