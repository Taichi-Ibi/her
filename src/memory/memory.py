from src.message import Messages
from src.utils import write_jsonl_file

class Memory:
    history_path = "logs/history.jsonl"

    def __init__(self) -> None:
        pass

    def save(self, messages: Messages) -> None:
        write_jsonl_file(file_path=self.history_path, data=messages.to_list())

    def remind(self):
        pass

    def reflect(self):
        pass
