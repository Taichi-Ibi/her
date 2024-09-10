import logging

from src.memory import Memory
from src.message import Message, Messages
from src.model import ModelSelector, ModelIdentifier
from src.prompt import Prompt
from src.utils import load_jsonl_file

logging.basicConfig(level=logging.INFO)


class Her:
    def __init__(self) -> None:
        self.history_path = "logs/history.jsonl"
        self.messages = Messages(messages=[])

    def remember(self):
        _history = load_jsonl_file(file_path=self.history_path)
        self.history = Messages(messages=[Message(**message) for message in _history])

    def invoke(self, model_id: ModelIdentifier, user_prompt: str) -> Message:
        model = ModelSelector(model_id=model_id).model

        if len(self.history):
            self.messages.add_multiple(messages=Messages(messages=self.history))
            self.messages.add(message=Message(role="user", content=user_prompt))
        else:
            self.messages.add_multiple(
                messages=Messages(
                    messages=[
                        Message(role="system", content=Prompt.system_prompt),
                        Message(role="user", content=user_prompt),
                    ]
                )
            )
        for message in self.messages:
            logging.info(message.as_dict)

        model_message: Message = model.invoke(messages=self.messages)
        self.messages.add(message=model_message)
        logging.info(model_message.as_dict)

        memory = Memory()
        memory.save(messages=self.messages)

        return model_message
