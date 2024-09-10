import json
from pathlib import Path

from src.message import Messages


class Memory:
    history_path = Path("logs/history.jsonl")

    def __init__(self) -> None:
        pass

    def save(self, messages: Messages) -> None:
        with self.history_path.open("w") as file:
            for message in messages:
                json.dump(message.as_dict, fp=file, ensure_ascii=False)
                file.write("\n")

    def remind(self):
        pass

    def reflect(self):
        pass
