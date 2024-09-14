from src.message import Message, Messages
from src.utils import load_jsonl_file, write_jsonl_file


class Memory:
    history_path = "logs/history.jsonl"

    def __init__(self) -> None:
        pass

    def load(self) -> Messages:
        self.history = Messages(
            [
                Message(**message)
                for message in load_jsonl_file(file_path=self.history_path)
            ]
        )

    def save(self, messages: Messages) -> None:
        write_jsonl_file(file_path=self.history_path, data=messages.to_list())

    def remind(self):
        pass

    def reflect(self):
        pass
