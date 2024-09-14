import logging
import re

from src.memory import Memory
from src.message import Message, Messages
from src.model import ModelSelector, ModelIdentifier
from src.prompt import Prompt

logging.basicConfig(level=logging.INFO)


class Her:
    def __init__(self) -> None:
        self.prompt = Prompt()
        self.memory = Memory()

    @property
    def _new_chat_messages(self) -> Messages:
        print("**Start new conversation**")
        return Messages([self.system_message, self.user_message])

    def _prep_messages(self, user_prompt: str) -> Messages:
        self.memory.load()
        self.history = self.memory.history
        self.user_message = Message(role="user", content=user_prompt)
        self.system_message = Message(role="system", content=self.prompt.system_prompt)

        if not self.history or user_prompt == self.history[-2].content:
            return self._new_chat_messages

        judge_model = ModelSelector(model_id=ModelIdentifier("judge")).model
        msg1ctx = self.history[1:].to_context(title="Message1")
        msg2ctx = Messages([self.user_message]).to_context(title="Message2")
        self.judge_messages = Messages(
            [
                Message(role="system", content=self.prompt.judge_prompt),
                Message(role="user", content=f"{msg1ctx}\n\n{msg2ctx}"),
            ]
        )
        judge_response = judge_model.invoke(messages=self.judge_messages)
        logging.info(judge_response.__dict__)

        if bool(re.search(r"\bTrue\b", judge_response.content)):
            print("**Continue conversation**")
            self.history.append(self.user_message)
            return self.history
        else:
            return self._new_chat_messages

    def invoke(self, model_id: ModelIdentifier, user_prompt: str) -> Message:
        messages = self._prep_messages(user_prompt=user_prompt)
        chat_model = ModelSelector(model_id=model_id).model
        model_response = chat_model.invoke(messages=messages)
        messages.append(model_response)
        for message in messages:
            logging.info(message.__dict__)
        self.memory.save(messages=messages)
        return model_response
