import logging

from src.memory import Memory
from src.message import Message, Messages
from src.model import ModelSelector, ModelIdentifier
from src.prompt import Prompt

logging.basicConfig(level=logging.INFO)


class Her:
    def __init__(self) -> None:
        pass

    def invoke(self, model_id: ModelIdentifier, user_prompt: str) -> Message:
        model = ModelSelector(model_id=model_id).model

        messages = Messages(
            messages=[
                Message(role="system", content=Prompt.system_prompt),
                Message(role="user", content=user_prompt),
            ]
        )
        for message in messages:
            logging.info(message.as_dict)

        model_message: Message = model.invoke(messages=messages)
        messages.add(message=model_message)
        logging.info(model_message.as_dict)

        memory = Memory()
        memory.save(messages=messages)

        return model_message
