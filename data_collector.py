import json
import csv
from typing import List, Dict, Any

class DataCollector:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = []

    def collect_data(self, turn: int,
                    active_player: str,
                    match_state_before: Dict[str, Any], 
                    actions_taken: List[Dict[str, Any]],
                      match_state_after: Dict[str, Any]):
        self.data.append({
            "turn": turn,
            "active_player": active_player,
            "match_state_before": json.dumps(match_state_before),
            "actions_taken": json.dumps(actions_taken),
            "match_state_after": json.dumps(match_state_after)
        })

    def save_to_csv(self):
        with open(self.file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["turn", "active_player", "match_state_before", "actions_taken", "match_state_after"])
            writer.writeheader()
            for row in self.data:
                writer.writerow(row)